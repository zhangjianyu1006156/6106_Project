# Member 3 Start Guide: Computational Experiment, Baselines, Optimization, and Visualization

Project: **Food Delivery Order Assignment and Route Optimization under Traffic and Weather Conditions**  
Role: **Member 3 — Python code, computational findings, route visualization, and robustness testing**

---

## 1. Your Role in the Project

You are responsible for turning the cleaned datasets prepared by Member 1 and the mathematical model designed by Member 2 into a runnable computational experiment.

Your main tasks are:

1. Load the processed datasets.
2. Build distance and travel-time calculation functions.
3. Create baseline solutions.
4. Compute baseline metrics.
5. Implement or connect the optimization model after Member 2 confirms the final formulation.
6. Visualize baseline and optimized routes.
7. Repeat the same workflow on robustness datasets.
8. Prepare result tables and figures for the report and presentation.

Do **not** wait for Member 2 to start. You can immediately work on the code framework, baselines, distance matrix, metrics, and visualization templates.

---

## 2. Input Files from Member 1

Use the following files as your starting point.

| File | Purpose | Use by Member 3 |
|---|---|---|
| `main_optimization_jaipur.csv` | Main optimization scenario | Core experiment |
| `robustness_mumbai.csv` | Robustness scenario 1 | Transferability test |
| `robustness_hyderabad.csv` | Robustness scenario 2 | Transferability test |
| `cleaned_zomato_full.csv` | Cleaned full dataset | Optional checking only |
| `member1_data_summary.csv` | Summary of generated datasets | Scenario verification |
| `member1_data_cleaning.py` | Cleaning script | Reference only |
| `member1_report.md` | Business problem and data report | Reference for assumptions and report writing |

Recommended local folder structure:

```text
project_folder/
├── data/
│   └── processed/
│       ├── main_optimization_jaipur.csv
│       ├── robustness_mumbai.csv
│       ├── robustness_hyderabad.csv
│       ├── cleaned_zomato_full.csv
│       └── member1_data_summary.csv
├── notebooks/
│   └── member3_computational_experiment.ipynb
├── outputs/
│   ├── figures/
│   └── tables/
└── src/
    └── member3_utils.py  # optional
```

If you want to keep everything simple, you can place the CSV files and notebook in the same folder first.

---

## 3. Scenario Settings Already Prepared

Member 1 prepared three scenario datasets. Each scenario has 50 orders from one city and one evening peak period.

| Scenario | File | City Code | City | Sample Size | Suggested Riders | Suggested Capacity |
|---|---|---:|---|---:|---:|---:|
| Main | `main_optimization_jaipur.csv` | `JAP` | Jaipur | 50 orders | 5 | 8–10 orders/rider |
| Robustness 1 | `robustness_mumbai.csv` | `MUM` | Mumbai | 50 orders | 5 | 8–10 orders/rider |
| Robustness 2 | `robustness_hyderabad.csv` | `HYD` | Hyderabad | 50 orders | 5 | 8–10 orders/rider |

Recommended default parameters:

```python
NUM_RIDERS = 5
RIDER_CAPACITY = 10
RANDOM_SEED = 6106
RETURN_TO_DEPOT = True
```

---

## 4. Key Columns in the Processed Dataset

Each scenario file has 23 columns.

Important columns for your work:

| Column | Meaning | Usage |
|---|---|---|
| `scenario_order_id` | Local order index from 1 to 50 | Node ID for optimization |
| `ID` | Original Zomato order ID | Reference only |
| `Delivery_person_ID` | Original rider ID | Reference / city code extraction already done |
| `Restaurant_latitude` | Restaurant latitude | Depot or pickup point calculation |
| `Restaurant_longitude` | Restaurant longitude | Depot or pickup point calculation |
| `Delivery_location_latitude` | Customer latitude | Customer node location |
| `Delivery_location_longitude` | Customer longitude | Customer node location |
| `Order_Date` | Order date | Scenario confirmation |
| `Time_Orderd` | Order time | Baseline ordering / time interpretation |
| `Time_Order_picked` | Pickup time | Optional interpretation |
| `Weather_conditions` | Weather | Travel-time multiplier |
| `Road_traffic_density` | Traffic | Travel-time multiplier |
| `Type_of_vehicle` | Vehicle type | Optional speed assumption |
| `multiple_deliveries` | Existing multiple-delivery indicator | Optional interpretation |
| `time_taken_min` | Actual delivery time | Reference / validation only |
| `city_code` | Extracted real city code | Scenario filtering |
| `order_hour` | Hour of order | Peak-hour confirmation |

---

## 5. Recommended Notebook Structure

Create a Jupyter Notebook named:

```text
member3_computational_experiment.ipynb
```

Use this structure:

```text
1. Import libraries
2. Load processed datasets
3. Define helper functions
   3.1 Haversine distance
   3.2 Distance matrix construction
   3.3 Route distance calculation
   3.4 Traffic/weather multiplier
   3.5 Metrics calculation
4. Main scenario: Jaipur
   4.1 Load data
   4.2 Create depot
   4.3 Create customer nodes
   4.4 Compute distance matrix
5. Baseline methods
   5.1 Original order baseline
   5.2 Random assignment baseline
   5.3 Geographic clustering baseline
6. Optimization method
   6.1 Placeholder before Member 2 confirms model
   6.2 Implement final MIP / TSP / VRP later
7. Result comparison
8. Route visualization
9. Robustness tests
   9.1 Mumbai
   9.2 Hyderabad
10. Export result tables and figures
```

---

## 6. Immediate Tasks You Can Start Now

### Task 1: Load the Processed Data

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

NUM_RIDERS = 5
RIDER_CAPACITY = 10
RANDOM_SEED = 6106

main_file = "main_optimization_jaipur.csv"
mumbai_file = "robustness_mumbai.csv"
hyderabad_file = "robustness_hyderabad.csv"

jaipur = pd.read_csv(main_file)
mumbai = pd.read_csv(mumbai_file)
hyderabad = pd.read_csv(hyderabad_file)

print("Jaipur:", jaipur.shape)
print("Mumbai:", mumbai.shape)
print("Hyderabad:", hyderabad.shape)

print(jaipur.head())
print(jaipur.columns.tolist())
```

If you use the recommended folder structure, change paths to:

```python
main_file = "data/processed/main_optimization_jaipur.csv"
mumbai_file = "data/processed/robustness_mumbai.csv"
hyderabad_file = "data/processed/robustness_hyderabad.csv"
```

---

### Task 2: Validate the Scenario Dataset

```python
def validate_scenario(df, scenario_name):
    print(f"\n=== {scenario_name} ===")
    print("Rows:", len(df))
    print("City codes:", df["city_code"].unique())
    print("Dates:", df["Order_Date"].unique())
    print("Order hour range:", df["order_hour"].min(), "to", df["order_hour"].max())
    print("Missing values in key columns:")
    key_cols = [
        "scenario_order_id",
        "Restaurant_latitude", "Restaurant_longitude",
        "Delivery_location_latitude", "Delivery_location_longitude",
        "Time_Orderd", "Weather_conditions", "Road_traffic_density",
        "time_taken_min"
    ]
    print(df[key_cols].isna().sum())

validate_scenario(jaipur, "Jaipur Main Scenario")
validate_scenario(mumbai, "Mumbai Robustness Scenario")
validate_scenario(hyderabad, "Hyderabad Robustness Scenario")
```

Expected result:

- 50 rows per scenario.
- One city code per scenario.
- One selected date per scenario.
- Order hours within evening peak.
- No missing values in key columns.

---

### Task 3: Define Haversine Distance

Use Haversine distance to approximate geographic distance between two latitude/longitude points.

```python
def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate Haversine distance between two points in kilometers."""
    R = 6371.0
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c
```

---

### Task 4: Create a Common Depot

Recommended assumption for now:

> Use the average restaurant coordinates in each scenario as the common dispatch depot.

This makes the model simpler and aligns with a simplified VRP setting.

```python
def create_depot(df):
    return {
        "node_id": 0,
        "lat": df["Restaurant_latitude"].mean(),
        "lon": df["Restaurant_longitude"].mean(),
    }

jaipur_depot = create_depot(jaipur)
print(jaipur_depot)
```

Limitation to mention later:

> In reality, food delivery orders may start from different restaurants. The common depot assumption simplifies the problem into a standard vehicle routing setting.

---

### Task 5: Create Customer Nodes

```python
def create_customer_nodes(df):
    nodes = df[[
        "scenario_order_id",
        "Delivery_location_latitude",
        "Delivery_location_longitude",
        "Time_Orderd",
        "Weather_conditions",
        "Road_traffic_density",
        "time_taken_min"
    ]].copy()

    nodes = nodes.rename(columns={
        "scenario_order_id": "node_id",
        "Delivery_location_latitude": "lat",
        "Delivery_location_longitude": "lon"
    })

    nodes = nodes.sort_values("node_id").reset_index(drop=True)
    return nodes

jaipur_nodes = create_customer_nodes(jaipur)
print(jaipur_nodes.head())
```

---

### Task 6: Build Distance Matrix

Node 0 is the depot. Nodes 1–50 are customer nodes.

```python
def build_node_table(df):
    depot = create_depot(df)
    customers = create_customer_nodes(df)

    depot_df = pd.DataFrame([{
        "node_id": 0,
        "lat": depot["lat"],
        "lon": depot["lon"],
        "Time_Orderd": None,
        "Weather_conditions": None,
        "Road_traffic_density": None,
        "time_taken_min": None,
    }])

    all_nodes = pd.concat([depot_df, customers], ignore_index=True)
    return all_nodes


def build_distance_matrix(all_nodes):
    node_ids = all_nodes["node_id"].tolist()
    n = len(node_ids)
    dist = pd.DataFrame(index=node_ids, columns=node_ids, dtype=float)

    for i in node_ids:
        lat1 = all_nodes.loc[all_nodes["node_id"] == i, "lat"].iloc[0]
        lon1 = all_nodes.loc[all_nodes["node_id"] == i, "lon"].iloc[0]
        for j in node_ids:
            lat2 = all_nodes.loc[all_nodes["node_id"] == j, "lat"].iloc[0]
            lon2 = all_nodes.loc[all_nodes["node_id"] == j, "lon"].iloc[0]
            dist.loc[i, j] = haversine_km(lat1, lon1, lat2, lon2)

    return dist

jaipur_all_nodes = build_node_table(jaipur)
jaipur_dist = build_distance_matrix(jaipur_all_nodes)

print(jaipur_dist.shape)
print(jaipur_dist.iloc[:5, :5])
```

---

## 7. Baseline Methods You Can Implement Now

You can implement baselines before Member 2 finishes the mathematical formulation.

### Baseline 1: Original Order Baseline

Logic:

1. Sort orders by `Time_Orderd` and `scenario_order_id`.
2. Assign orders to riders by round-robin.
3. Each rider delivers orders in the assigned sequence.

```python
def original_order_baseline(df, num_riders=5):
    df_sorted = df.sort_values(["Time_Orderd", "scenario_order_id"]).reset_index(drop=True)
    routes = {r: [] for r in range(num_riders)}

    for idx, row in df_sorted.iterrows():
        rider = idx % num_riders
        routes[rider].append(int(row["scenario_order_id"]))

    return routes
```

---

### Baseline 2: Random Assignment Baseline

Logic:

1. Shuffle orders with a fixed random seed.
2. Assign orders to riders by round-robin.
3. Delivery sequence follows the shuffled order.

```python
def random_assignment_baseline(df, num_riders=5, seed=6106):
    df_shuffled = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    routes = {r: [] for r in range(num_riders)}

    for idx, row in df_shuffled.iterrows():
        rider = idx % num_riders
        routes[rider].append(int(row["scenario_order_id"]))

    return routes
```

---

### Baseline 3: Geographic Clustering Baseline

Logic:

1. Use K-means to group customer locations into 5 clusters.
2. Assign each cluster to one rider.
3. Do not optimize delivery sequence inside the cluster yet.

```python
from sklearn.cluster import KMeans

def geographic_clustering_baseline(df, num_riders=5, seed=6106):
    coords = df[["Delivery_location_latitude", "Delivery_location_longitude"]].values
    kmeans = KMeans(n_clusters=num_riders, random_state=seed, n_init=10)
    labels = kmeans.fit_predict(coords)

    temp = df.copy()
    temp["cluster"] = labels
    temp = temp.sort_values(["cluster", "Time_Orderd", "scenario_order_id"])

    routes = {r: [] for r in range(num_riders)}
    for cluster_id in range(num_riders):
        orders = temp[temp["cluster"] == cluster_id]["scenario_order_id"].astype(int).tolist()
        routes[cluster_id] = orders

    return routes
```

---

## 8. Route Distance and Metrics

### Route Distance Calculation

Assumption:

- Rider starts from depot node 0.
- Rider visits assigned customer nodes in order.
- Rider returns to depot if `return_to_depot=True`.

```python
def calculate_route_distance(route, distance_matrix, return_to_depot=True):
    if len(route) == 0:
        return 0.0

    total = 0.0
    current = 0  # depot

    for node in route:
        total += distance_matrix.loc[current, node]
        current = node

    if return_to_depot:
        total += distance_matrix.loc[current, 0]

    return total
```

---

### Metrics Calculation

```python
def evaluate_routes(routes, distance_matrix, return_to_depot=True):
    rider_distances = {}

    for rider, route in routes.items():
        rider_distances[rider] = calculate_route_distance(
            route,
            distance_matrix,
            return_to_depot=return_to_depot
        )

    distances = list(rider_distances.values())

    metrics = {
        "total_distance_km": sum(distances),
        "avg_distance_per_rider_km": np.mean(distances),
        "max_distance_per_rider_km": np.max(distances),
        "min_distance_per_rider_km": np.min(distances),
        "workload_imbalance_km": np.max(distances) - np.min(distances),
    }

    return metrics, rider_distances
```

---

### Run Baseline Evaluation

```python
original_routes = original_order_baseline(jaipur, NUM_RIDERS)
random_routes = random_assignment_baseline(jaipur, NUM_RIDERS, RANDOM_SEED)
geo_routes = geographic_clustering_baseline(jaipur, NUM_RIDERS, RANDOM_SEED)

baseline_results = []
for method_name, routes in [
    ("Original Order", original_routes),
    ("Random Assignment", random_routes),
    ("Geographic Clustering", geo_routes),
]:
    metrics, rider_distances = evaluate_routes(routes, jaipur_dist)
    row = {"scenario": "Jaipur", "method": method_name}
    row.update(metrics)
    baseline_results.append(row)

baseline_df = pd.DataFrame(baseline_results)
print(baseline_df)
```

---

## 9. Optional: Traffic and Weather Travel-Time Multipliers

This can be added now, but only finalize it after Member 2 confirms whether time is included in the objective.

Example multiplier design:

```python
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

AVERAGE_SPEED_KMPH = 25

def estimate_travel_time_min(distance_km, traffic="Medium", weather="Sunny"):
    traffic_factor = TRAFFIC_MULTIPLIER.get(traffic, 1.20)
    weather_factor = WEATHER_MULTIPLIER.get(weather, 1.10)
    base_time_min = distance_km / AVERAGE_SPEED_KMPH * 60
    return base_time_min * traffic_factor * weather_factor
```

Simpler option:

- Use distance as the main optimization objective.
- Use traffic/weather only in discussion and estimated time comparison.

---

## 10. Visualization You Can Build Now

### Customer Scatter Plot

```python
def plot_customer_scatter(df, title="Customer Locations"):
    depot = create_depot(df)

    plt.figure(figsize=(8, 6))
    plt.scatter(
        df["Delivery_location_longitude"],
        df["Delivery_location_latitude"],
        label="Customers",
        alpha=0.7
    )
    plt.scatter(
        depot["lon"],
        depot["lat"],
        marker="*",
        s=200,
        label="Depot"
    )
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

plot_customer_scatter(jaipur, "Jaipur Customer Locations and Depot")
```

---

### Route Plot

```python
def plot_routes(df, routes, title="Delivery Routes"):
    depot = create_depot(df)
    node_lookup = {
        int(row["scenario_order_id"]): (
            row["Delivery_location_latitude"],
            row["Delivery_location_longitude"]
        )
        for _, row in df.iterrows()
    }

    plt.figure(figsize=(9, 7))

    # customer points
    plt.scatter(
        df["Delivery_location_longitude"],
        df["Delivery_location_latitude"],
        alpha=0.6,
        label="Customers"
    )

    # depot point
    plt.scatter(
        depot["lon"],
        depot["lat"],
        marker="*",
        s=250,
        label="Depot"
    )

    # route lines
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

        plt.plot(lons, lats, marker="o", linewidth=1, label=f"Rider {rider + 1}")

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

plot_routes(jaipur, original_routes, "Jaipur Original Order Baseline Routes")
plot_routes(jaipur, geo_routes, "Jaipur Geographic Baseline Routes")
```

Note: Do not worry if the plot is not a real road map. A latitude/longitude route plot is acceptable for showing relative spatial patterns.

---

## 11. Optimization Part: Placeholder Before Member 2 Confirms

Wait for Member 2 to confirm the final mathematical formulation before finalizing optimization code.

However, you can prepare the function placeholder now:

```python
def solve_optimization_model(df, distance_matrix, num_riders=5, capacity=10):
    """
    Placeholder for final optimization model.

    To be finalized after Member 2 confirms:
    - common depot or multiple restaurant pickup points
    - objective function
    - capacity constraints
    - return-to-depot assumption
    - whether traffic/weather multipliers are included
    - exact MIP/TSP/VRP formulation
    """
    raise NotImplementedError("Waiting for final model formulation from Member 2.")
```

Possible final approaches:

1. **Simplified VRP MIP** using binary arc variables.
2. **K-means + TSP**: assign geographically first, then solve route sequence within each cluster.
3. **Assignment + route heuristic**: assign orders to riders by workload balance, then optimize each route by nearest neighbor / 2-opt.

Recommended for reliability:

> Use K-means or balanced assignment first, then solve small TSP per rider. This is easier to implement and explain than a full 50-order VRP.

---

## 12. Optional Heuristic You Can Implement Before Member 2: Nearest Neighbor Route Improvement

This can be used as an optimized heuristic if the full MIP is too slow.

```python
def nearest_neighbor_route(nodes, distance_matrix):
    """Return a route visiting all nodes using nearest neighbor from depot."""
    unvisited = set(nodes)
    route = []
    current = 0

    while unvisited:
        next_node = min(unvisited, key=lambda node: distance_matrix.loc[current, node])
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node

    return route


def improve_routes_nearest_neighbor(routes, distance_matrix):
    improved = {}
    for rider, route in routes.items():
        improved[rider] = nearest_neighbor_route(route, distance_matrix)
    return improved

geo_nn_routes = improve_routes_nearest_neighbor(geo_routes, jaipur_dist)

metrics, rider_distances = evaluate_routes(geo_nn_routes, jaipur_dist)
print(metrics)
plot_routes(jaipur, geo_nn_routes, "Jaipur Geographic + Nearest Neighbor Optimized Routes")
```

This gives you an early optimized result even before the final MIP is ready.

---

## 13. Result Table Template

Your final report should include a table like this:

| Scenario | Method | Total Distance (km) | Avg Distance/Rider (km) | Max Rider Distance (km) | Workload Imbalance (km) | Improvement vs Baseline |
|---|---|---:|---:|---:|---:|---:|
| Jaipur | Original Order | xx | xx | xx | xx | - |
| Jaipur | Random Assignment | xx | xx | xx | xx | - |
| Jaipur | Geographic Baseline | xx | xx | xx | xx | - |
| Jaipur | Optimized | xx | xx | xx | xx | xx% |

Improvement formula:

```python
def improvement_pct(baseline_value, optimized_value):
    return (baseline_value - optimized_value) / baseline_value * 100
```

---

## 14. Robustness Test Workflow

Once Jaipur works, wrap the entire workflow into a function and apply it to Mumbai and Hyderabad.

```python
def run_scenario_workflow(df, scenario_name, num_riders=5, seed=6106):
    all_nodes = build_node_table(df)
    dist = build_distance_matrix(all_nodes)

    original = original_order_baseline(df, num_riders)
    random_routes = random_assignment_baseline(df, num_riders, seed)
    geo = geographic_clustering_baseline(df, num_riders, seed)
    geo_nn = improve_routes_nearest_neighbor(geo, dist)

    results = []
    for method_name, routes in [
        ("Original Order", original),
        ("Random Assignment", random_routes),
        ("Geographic Clustering", geo),
        ("Geographic + Nearest Neighbor", geo_nn),
    ]:
        metrics, _ = evaluate_routes(routes, dist)
        row = {"scenario": scenario_name, "method": method_name}
        row.update(metrics)
        results.append(row)

    return pd.DataFrame(results), {
        "distance_matrix": dist,
        "routes": {
            "original": original,
            "random": random_routes,
            "geo": geo,
            "geo_nn": geo_nn,
        }
    }

jaipur_results, jaipur_objects = run_scenario_workflow(jaipur, "Jaipur")
mumbai_results, mumbai_objects = run_scenario_workflow(mumbai, "Mumbai")
hyderabad_results, hyderabad_objects = run_scenario_workflow(hyderabad, "Hyderabad")

all_results = pd.concat([jaipur_results, mumbai_results, hyderabad_results], ignore_index=True)
print(all_results)
```

Export results:

```python
all_results.to_csv("member3_results_summary.csv", index=False)
```

---

## 15. Figures to Produce

Recommended figures:

1. Jaipur customer locations and depot.
2. Jaipur original order baseline route.
3. Jaipur optimized route.
4. Bar chart: total distance by method for Jaipur.
5. Bar chart: total distance by method across Jaipur, Mumbai, Hyderabad.
6. Optional: workload imbalance comparison.

Example bar chart:

```python
def plot_metric_bar(results_df, metric, title):
    pivot = results_df.pivot(index="scenario", columns="method", values=metric)
    pivot.plot(kind="bar", figsize=(10, 6))
    plt.ylabel(metric)
    plt.title(title)
    plt.xticks(rotation=0)
    plt.grid(axis="y")
    plt.show()

plot_metric_bar(all_results, "total_distance_km", "Total Distance by Scenario and Method")
plot_metric_bar(all_results, "workload_imbalance_km", "Workload Imbalance by Scenario and Method")
```

---

## 16. Files You Should Export

At the end of your work, export:

| File | Purpose |
|---|---|
| `member3_computational_experiment.ipynb` | Main notebook |
| `member3_results_summary.csv` | Metrics table for all scenarios |
| `jaipur_baseline_route.png` | Baseline route figure |
| `jaipur_optimized_route.png` | Optimized route figure |
| `distance_comparison.png` | Metric comparison figure |
| `workload_comparison.png` | Workload balance comparison figure |

Recommended code for saving figures:

```python
plt.savefig("outputs/figures/figure_name.png", dpi=300, bbox_inches="tight")
```

---

## 17. Questions to Confirm with Member 2

Send this to Member 2:

```text
I have started the computational experiment part using Member 1's cleaned datasets.
Before I finalize the optimization code, could you help confirm these model settings?

1. Do we assume one common depot for all riders, using the average restaurant location?
2. Should riders return to the depot after completing deliveries?
3. Is the main objective total distance, estimated delivery time, or a weighted combination?
4. Do we set each rider capacity as exactly 10 orders or at most 10 orders?
5. Should traffic and weather be included as travel-time multipliers, or only discussed in interpretation?
6. Should the final optimized method be full VRP MIP, K-means + TSP, or geographic assignment + route sequencing heuristic?
```

---

## 18. Suggested Report Text for Your Section

You can later adapt this for the report.

```text
The computational experiment was conducted on the Jaipur evening peak dataset, which contains 50 orders and 5 assumed available riders. A common depot was defined as the average restaurant location in the selected scenario. Haversine distance was used to approximate the travel distance between the depot and customer locations, as well as between customer locations.

We first constructed several baseline solutions, including original order assignment, random assignment, and simple geographic clustering. These baselines represent non-optimized or rule-based operational decisions. The optimized approach was then compared against these baselines using total delivery distance, average rider distance, maximum rider distance, and workload imbalance.

The same workflow was repeated on Mumbai and Hyderabad robustness datasets to test whether the proposed method remains effective under different spatial structures.
```

---

## 19. Suggested Slide Content for Your Presentation Part

### Slide: Computational Experiment Setup

- Main scenario: Jaipur evening peak
- 50 orders, 5 riders
- Depot: average restaurant location
- Distance: Haversine distance
- Baselines: original order, random assignment, geographic clustering
- Optimized method: final model / route optimization

### Slide: Results Comparison

Show one table:

| Method | Total Distance | Avg Distance/Rider | Workload Imbalance | Improvement |
|---|---:|---:|---:|---:|
| Original Order | xx | xx | xx | - |
| Random Assignment | xx | xx | xx | - |
| Geographic Baseline | xx | xx | xx | - |
| Optimized | xx | xx | xx | xx% |

### Slide: Route Visualization

Show two maps/plots:

1. Baseline route.
2. Optimized route.

### Slide: Robustness Test

Show distance reduction across:

- Jaipur
- Mumbai
- Hyderabad

---

## 20. What You Should Complete First

Priority order:

1. Create the notebook.
2. Load the three processed datasets.
3. Validate the datasets.
4. Implement Haversine distance.
5. Build distance matrices.
6. Implement original order baseline.
7. Implement random assignment baseline.
8. Implement geographic clustering baseline.
9. Evaluate baseline metrics.
10. Create Jaipur route visualization.
11. Wrap workflow into a reusable function.
12. Run Mumbai and Hyderabad robustness workflow.
13. Wait for Member 2 to finalize model.
14. Add final optimization model or heuristic.
15. Export result tables and figures.

---

## 21. Key Reminder

Do not make your part look like pure descriptive analytics. Your section should emphasize:

> Given a set of orders and riders, we compare non-optimized delivery rules with an optimized assignment and routing method to reduce operational distance and improve delivery efficiency.

This keeps the project aligned with prescriptive analytics.
