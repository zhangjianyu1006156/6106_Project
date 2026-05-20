"""Member 3 routing experiment utilities.

ChatLog Link: https://chatgpt.com/share/69fac10c-8ebc-839c-a19d-c83718097045
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


NUM_RIDERS = 5
RIDER_CAPACITY = 10
RANDOM_SEED = 6106
RETURN_TO_DEPOT = True
AVERAGE_SPEED_KMPH = 25

TRAFFIC_MULTIPLIER = {
    "Low": 1.00,
    "Medium": 1.20,
    "High": 1.50,
    "Jam": 1.80,
}

WEATHER_MULTIPLIER = {
    "Sunny": 1.00,
    "Cloudy": 1.05,
    "Windy": 1.10,
    "Fog": 1.20,
    "Sandstorms": 1.25,
    "Stormy": 1.35,
}


RouteMap = Dict[int, List[int]]


@dataclass(frozen=True)
class ScenarioResult:
    results: pd.DataFrame
    distance_matrix: pd.DataFrame
    routes: Dict[str, RouteMap]


def load_scenarios(data_dir: str | Path = "data/processed") -> Dict[str, pd.DataFrame]:
    data_path = Path(data_dir)
    return {
        "Jaipur": pd.read_csv(data_path / "main_optimization_jaipur.csv"),
        "Mumbai": pd.read_csv(data_path / "robustness_mumbai.csv"),
        "Hyderabad": pd.read_csv(data_path / "robustness_hyderabad.csv"),
    }


def validate_scenario(df: pd.DataFrame, scenario_name: str) -> dict:
    key_cols = [
        "scenario_order_id",
        "Restaurant_latitude",
        "Restaurant_longitude",
        "Delivery_location_latitude",
        "Delivery_location_longitude",
        "Time_Orderd",
        "Weather_conditions",
        "Road_traffic_density",
        "time_taken_min",
    ]
    return {
        "scenario": scenario_name,
        "rows": len(df),
        "city_codes": ", ".join(sorted(df["city_code"].dropna().astype(str).unique())),
        "dates": ", ".join(sorted(df["Order_Date"].dropna().astype(str).unique())),
        "min_order_hour": df["order_hour"].min(),
        "max_order_hour": df["order_hour"].max(),
        "missing_key_values": int(df[key_cols].isna().sum().sum()),
    }


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    )
    return float(radius_km * 2 * np.arcsin(np.sqrt(a)))


def create_depot(df: pd.DataFrame) -> dict:
    return {
        "node_id": 0,
        "lat": float(df["Restaurant_latitude"].mean()),
        "lon": float(df["Restaurant_longitude"].mean()),
    }


def create_customer_nodes(df: pd.DataFrame) -> pd.DataFrame:
    nodes = df[
        [
            "scenario_order_id",
            "Delivery_location_latitude",
            "Delivery_location_longitude",
            "Time_Orderd",
            "Weather_conditions",
            "Road_traffic_density",
            "time_taken_min",
        ]
    ].copy()
    nodes = nodes.rename(
        columns={
            "scenario_order_id": "node_id",
            "Delivery_location_latitude": "lat",
            "Delivery_location_longitude": "lon",
        }
    )
    return nodes.sort_values("node_id").reset_index(drop=True)


def build_node_table(df: pd.DataFrame) -> pd.DataFrame:
    depot = create_depot(df)
    depot_df = pd.DataFrame(
        [
            {
                "node_id": 0,
                "lat": depot["lat"],
                "lon": depot["lon"],
                "Time_Orderd": None,
                "Weather_conditions": None,
                "Road_traffic_density": None,
                "time_taken_min": None,
            }
        ]
    )
    return pd.concat([depot_df, create_customer_nodes(df)], ignore_index=True)


def build_distance_matrix(all_nodes: pd.DataFrame) -> pd.DataFrame:
    node_ids = all_nodes["node_id"].astype(int).tolist()
    coords = all_nodes.set_index("node_id")[["lat", "lon"]].to_dict("index")
    dist = pd.DataFrame(index=node_ids, columns=node_ids, dtype=float)
    for i in node_ids:
        for j in node_ids:
            dist.loc[i, j] = haversine_km(
                coords[i]["lat"], coords[i]["lon"], coords[j]["lat"], coords[j]["lon"]
            )
    return dist


def original_order_baseline(df: pd.DataFrame, num_riders: int = NUM_RIDERS) -> RouteMap:
    df_sorted = df.sort_values(["Time_Orderd", "scenario_order_id"]).reset_index(drop=True)
    return _round_robin_routes(df_sorted["scenario_order_id"].astype(int), num_riders)


def random_assignment_baseline(
    df: pd.DataFrame,
    num_riders: int = NUM_RIDERS,
    seed: int = RANDOM_SEED,
) -> RouteMap:
    df_shuffled = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    return _round_robin_routes(df_shuffled["scenario_order_id"].astype(int), num_riders)


def geographic_clustering_baseline(
    df: pd.DataFrame,
    num_riders: int = NUM_RIDERS,
    seed: int = RANDOM_SEED,
) -> RouteMap:
    coords = df[["Delivery_location_latitude", "Delivery_location_longitude"]].values
    labels = KMeans(n_clusters=num_riders, random_state=seed, n_init=10).fit_predict(coords)
    temp = df.copy()
    temp["cluster"] = labels
    temp = temp.sort_values(["cluster", "Time_Orderd", "scenario_order_id"])
    return {
        rider: temp[temp["cluster"] == rider]["scenario_order_id"].astype(int).tolist()
        for rider in range(num_riders)
    }


def balanced_geographic_baseline(
    df: pd.DataFrame,
    num_riders: int = NUM_RIDERS,
    capacity: int = RIDER_CAPACITY,
) -> RouteMap:
    if num_riders <= 0 or capacity <= 0:
        raise ValueError("num_riders and capacity must be positive.")
    if len(df) > num_riders * capacity:
        raise ValueError(
            f"{len(df)} orders exceed total rider capacity "
            f"of {num_riders * capacity}."
        )

    depot = create_depot(df)
    temp = df.copy()
    temp["angle"] = np.arctan2(
        temp["Delivery_location_latitude"] - depot["lat"],
        temp["Delivery_location_longitude"] - depot["lon"],
    )
    temp["radius"] = temp.apply(
        lambda row: haversine_km(
            depot["lat"],
            depot["lon"],
            row["Delivery_location_latitude"],
            row["Delivery_location_longitude"],
        ),
        axis=1,
    )
    temp = temp.sort_values(["angle", "radius", "scenario_order_id"]).reset_index(drop=True)
    routes = {rider: [] for rider in range(num_riders)}
    for idx, row in temp.iterrows():
        rider = min(idx // capacity, num_riders - 1)
        routes[rider].append(int(row["scenario_order_id"]))
    return routes


def nearest_neighbor_route(nodes: Iterable[int], distance_matrix: pd.DataFrame) -> List[int]:
    unvisited = set(int(node) for node in nodes)
    route = []
    current = 0
    while unvisited:
        next_node = min(unvisited, key=lambda node: distance_matrix.loc[current, node])
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node
    return route


def improve_routes_nearest_neighbor(routes: RouteMap, distance_matrix: pd.DataFrame) -> RouteMap:
    return {
        rider: nearest_neighbor_route(route, distance_matrix)
        for rider, route in routes.items()
    }


def improve_routes_two_opt(routes: RouteMap, distance_matrix: pd.DataFrame) -> RouteMap:
    return {
        rider: two_opt_route(route, distance_matrix)
        for rider, route in routes.items()
    }


def two_opt_route(route: List[int], distance_matrix: pd.DataFrame) -> List[int]:
    if len(route) < 4:
        return list(route)

    best = list(route)
    best_distance = calculate_route_distance(best, distance_matrix)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best)):
                if j - i == 1:
                    continue
                candidate = best[:i] + best[i:j][::-1] + best[j:]
                candidate_distance = calculate_route_distance(candidate, distance_matrix)
                if candidate_distance + 1e-9 < best_distance:
                    best = candidate
                    best_distance = candidate_distance
                    improved = True
    return best


def calculate_route_distance(
    route: List[int],
    distance_matrix: pd.DataFrame,
    return_to_depot: bool = RETURN_TO_DEPOT,
) -> float:
    if not route:
        return 0.0
    total = 0.0
    current = 0
    for node in route:
        total += float(distance_matrix.loc[current, node])
        current = node
    if return_to_depot:
        total += float(distance_matrix.loc[current, 0])
    return total


def estimate_leg_time_min(
    distance_km: float,
    traffic: str = "Medium",
    weather: str = "Sunny",
) -> float:
    traffic_factor = TRAFFIC_MULTIPLIER.get(str(traffic), 1.20)
    weather_factor = WEATHER_MULTIPLIER.get(str(weather), 1.10)
    return distance_km / AVERAGE_SPEED_KMPH * 60 * traffic_factor * weather_factor


def evaluate_routes(
    routes: RouteMap,
    distance_matrix: pd.DataFrame,
    df: pd.DataFrame | None = None,
    return_to_depot: bool = RETURN_TO_DEPOT,
) -> Tuple[dict, Dict[int, float]]:
    rider_distances = {
        rider: calculate_route_distance(route, distance_matrix, return_to_depot)
        for rider, route in routes.items()
    }
    distances = list(rider_distances.values())
    metrics = {
        "total_distance_km": sum(distances),
        "avg_distance_per_rider_km": float(np.mean(distances)),
        "max_distance_per_rider_km": float(np.max(distances)),
        "min_distance_per_rider_km": float(np.min(distances)),
        "workload_imbalance_km": float(np.max(distances) - np.min(distances)),
        "max_orders_per_rider": max(len(route) for route in routes.values()),
        "min_orders_per_rider": min(len(route) for route in routes.values()),
    }
    if df is not None:
        metrics["estimated_total_time_min"] = estimate_routes_time(routes, distance_matrix, df)
    return metrics, rider_distances


def estimate_routes_time(routes: RouteMap, distance_matrix: pd.DataFrame, df: pd.DataFrame) -> float:
    return sum(
        calculate_route_time(route, distance_matrix, df)
        for route in routes.values()
    )


def calculate_route_time(
    route: List[int],
    distance_matrix: pd.DataFrame,
    df: pd.DataFrame,
) -> float:
    conditions = df.set_index("scenario_order_id")[
        ["Road_traffic_density", "Weather_conditions"]
    ].to_dict("index")
    total_time = 0.0
    current = 0
    for node in route:
        distance = float(distance_matrix.loc[current, node])
        row = conditions[node]
        total_time += estimate_leg_time_min(
            distance,
            row["Road_traffic_density"],
            row["Weather_conditions"],
        )
        current = node
    if RETURN_TO_DEPOT and route:
        total_time += estimate_leg_time_min(float(distance_matrix.loc[current, 0]))
    return total_time


def build_rider_summary_table(
    routes: RouteMap,
    distance_matrix: pd.DataFrame,
    df: pd.DataFrame,
    scenario_name: str,
    method_name: str,
) -> pd.DataFrame:
    rows = []
    for rider, route in sorted(routes.items()):
        rows.append(
            {
                "scenario": scenario_name,
                "method": method_name,
                "rider": rider + 1,
                "num_orders": len(route),
                "route_distance_km": calculate_route_distance(route, distance_matrix),
                "estimated_time_min": calculate_route_time(route, distance_matrix, df),
            }
        )
    return pd.DataFrame(rows)


def build_route_sequence_table(
    routes: RouteMap,
    df: pd.DataFrame,
    scenario_name: str,
    method_name: str,
) -> pd.DataFrame:
    node_lookup = df.set_index("scenario_order_id")[
        [
            "Delivery_location_latitude",
            "Delivery_location_longitude",
            "Time_Orderd",
            "Road_traffic_density",
            "Weather_conditions",
        ]
    ].to_dict("index")
    rows = []
    for rider, route in sorted(routes.items()):
        for route_position, node in enumerate(route, start=1):
            row = node_lookup[node]
            rows.append(
                {
                    "scenario": scenario_name,
                    "method": method_name,
                    "rider": rider + 1,
                    "route_position": route_position,
                    "scenario_order_id": node,
                    "delivery_latitude": row["Delivery_location_latitude"],
                    "delivery_longitude": row["Delivery_location_longitude"],
                    "order_time": row["Time_Orderd"],
                    "traffic_density": row["Road_traffic_density"],
                    "weather_condition": row["Weather_conditions"],
                }
            )
    return pd.DataFrame(rows)


def build_random_seed_sensitivity_table(
    scenarios: Dict[str, pd.DataFrame],
    scenario_outputs: Dict[str, ScenarioResult],
    seeds: Iterable[int],
    num_riders: int = NUM_RIDERS,
) -> pd.DataFrame:
    rows = []
    for scenario_name, df in scenarios.items():
        scenario_result = scenario_outputs[scenario_name]
        baseline_distance = float(
            scenario_result.results.loc[
                scenario_result.results["method"] == "Original Order",
                "total_distance_km",
            ].iloc[0]
        )
        for seed in seeds:
            routes = random_assignment_baseline(df, num_riders, seed)
            metrics, _ = evaluate_routes(routes, scenario_result.distance_matrix, df)
            rows.append(
                {
                    "scenario": scenario_name,
                    "seed": seed,
                    "total_distance_km": metrics["total_distance_km"],
                    "estimated_total_time_min": metrics["estimated_total_time_min"],
                    "improvement_vs_original_pct": (
                        (baseline_distance - metrics["total_distance_km"])
                        / baseline_distance
                        * 100
                    ),
                }
            )
    return pd.DataFrame(rows)


def summarize_random_seed_sensitivity(sensitivity: pd.DataFrame) -> pd.DataFrame:
    return sensitivity.groupby("scenario", as_index=False).agg(
        mean_total_distance_km=("total_distance_km", "mean"),
        std_total_distance_km=("total_distance_km", "std"),
        min_total_distance_km=("total_distance_km", "min"),
        max_total_distance_km=("total_distance_km", "max"),
        mean_estimated_total_time_min=("estimated_total_time_min", "mean"),
        mean_improvement_vs_original_pct=("improvement_vs_original_pct", "mean"),
    )


def run_scenario_workflow(
    df: pd.DataFrame,
    scenario_name: str,
    num_riders: int = NUM_RIDERS,
    capacity: int = RIDER_CAPACITY,
    seed: int = RANDOM_SEED,
) -> ScenarioResult:
    all_nodes = build_node_table(df)
    distance_matrix = build_distance_matrix(all_nodes)

    original = original_order_baseline(df, num_riders)
    random_routes = random_assignment_baseline(df, num_riders, seed)
    geographic = geographic_clustering_baseline(df, num_riders, seed)
    balanced_geo = balanced_geographic_baseline(df, num_riders, capacity)
    geographic_nn = improve_routes_nearest_neighbor(geographic, distance_matrix)
    optimized = improve_routes_two_opt(
        improve_routes_nearest_neighbor(balanced_geo, distance_matrix),
        distance_matrix,
    )

    method_routes = {
        "Original Order": original,
        "Random Assignment": random_routes,
        "Geographic Clustering": geographic,
        "Geographic + Nearest Neighbor": geographic_nn,
        "Balanced Geo + NN + 2-opt": optimized,
    }

    rows = []
    for method_name, routes in method_routes.items():
        metrics, _ = evaluate_routes(routes, distance_matrix, df)
        row = {"scenario": scenario_name, "method": method_name}
        row.update(metrics)
        rows.append(row)

    results = pd.DataFrame(rows)
    baseline_value = float(
        results.loc[results["method"] == "Original Order", "total_distance_km"].iloc[0]
    )
    results["improvement_vs_original_pct"] = (
        (baseline_value - results["total_distance_km"]) / baseline_value * 100
    )
    return ScenarioResult(results=results, distance_matrix=distance_matrix, routes=method_routes)


def plot_customer_scatter(
    df: pd.DataFrame,
    title: str,
    output_path: str | Path | None = None,
) -> None:
    depot = create_depot(df)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(
        df["Delivery_location_longitude"],
        df["Delivery_location_latitude"],
        label="Customers",
        alpha=0.72,
        s=38,
    )
    ax.scatter(depot["lon"], depot["lat"], marker="*", s=260, label="Depot")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.25)
    _save_or_show(fig, output_path)


def plot_routes(
    df: pd.DataFrame,
    routes: RouteMap,
    title: str,
    output_path: str | Path | None = None,
) -> None:
    depot = create_depot(df)
    node_lookup = {
        int(row["scenario_order_id"]): (
            row["Delivery_location_latitude"],
            row["Delivery_location_longitude"],
        )
        for _, row in df.iterrows()
    }
    colors = plt.cm.tab10.colors
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(
        df["Delivery_location_longitude"],
        df["Delivery_location_latitude"],
        alpha=0.55,
        color="#565656",
        label="Customers",
        s=34,
    )
    ax.scatter(depot["lon"], depot["lat"], marker="*", s=280, color="#111111", label="Depot")

    for rider, route in routes.items():
        if not route:
            continue
        lats = [depot["lat"]]
        lons = [depot["lon"]]
        for node in route:
            lat, lon = node_lookup[node]
            lats.append(lat)
            lons.append(lon)
        lats.append(depot["lat"])
        lons.append(depot["lon"])
        ax.plot(
            lons,
            lats,
            marker="o",
            linewidth=1.4,
            markersize=3.5,
            color=colors[rider % len(colors)],
            label=f"Rider {rider + 1}",
        )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(title)
    ax.legend(ncol=2, fontsize=8)
    ax.grid(True, alpha=0.25)
    _save_or_show(fig, output_path)


def plot_metric_bar(
    results_df: pd.DataFrame,
    metric: str,
    title: str,
    output_path: str | Path | None = None,
) -> None:
    pivot = results_df.pivot(index="scenario", columns="method", values=metric)
    fig, ax = plt.subplots(figsize=(11, 6))
    pivot.plot(kind="bar", ax=ax)
    ax.set_ylabel(metric)
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=0)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(fontsize=8)
    _save_or_show(fig, output_path)


def _round_robin_routes(order_ids: Iterable[int], num_riders: int) -> RouteMap:
    routes = {rider: [] for rider in range(num_riders)}
    for idx, order_id in enumerate(order_ids):
        routes[idx % num_riders].append(int(order_id))
    return routes


def _save_or_show(fig: plt.Figure, output_path: str | Path | None) -> None:
    fig.tight_layout()
    if output_path is None:
        plt.show()
    else:
        fig.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
