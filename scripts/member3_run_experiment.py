"""Member 3 computational experiment runner.

ChatLog Link: https://chatgpt.com/share/69fac10c-8ebc-839c-a19d-c83718097045
"""

from pathlib import Path
import os
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

OUTPUT_DIR = PROJECT_ROOT / "outputs"
TABLE_DIR = OUTPUT_DIR / "tables"
FIGURE_DIR = OUTPUT_DIR / "figures"
MPL_CONFIG_DIR = OUTPUT_DIR / ".matplotlib"

MPL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CONFIG_DIR))
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "4")

import pandas as pd

from src.member3_utils import (
    build_rider_summary_table,
    build_random_seed_sensitivity_table,
    build_route_sequence_table,
    load_scenarios,
    plot_customer_scatter,
    plot_metric_bar,
    plot_routes,
    run_scenario_workflow,
    summarize_random_seed_sensitivity,
    validate_scenario,
)

RANDOM_SENSITIVITY_SEEDS = range(6101, 6111)


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    scenarios = load_scenarios(PROJECT_ROOT / "data" / "processed")
    validation = pd.DataFrame(
        [validate_scenario(df, name) for name, df in scenarios.items()]
    )
    validation.to_csv(TABLE_DIR / "member3_validation_summary.csv", index=False)

    scenario_outputs = {
        name: run_scenario_workflow(df, name)
        for name, df in scenarios.items()
    }
    all_results = pd.concat(
        [scenario_result.results for scenario_result in scenario_outputs.values()],
        ignore_index=True,
    )

    rounded = all_results.copy()
    numeric_cols = rounded.select_dtypes(include="number").columns
    rounded[numeric_cols] = rounded[numeric_cols].round(3)
    rounded.to_csv(TABLE_DIR / "member3_results_summary.csv", index=False)

    random_sensitivity = build_random_seed_sensitivity_table(
        scenarios,
        scenario_outputs,
        RANDOM_SENSITIVITY_SEEDS,
    )
    random_sensitivity_summary = summarize_random_seed_sensitivity(random_sensitivity)
    rounded_random_sensitivity = random_sensitivity.copy()
    random_numeric_cols = rounded_random_sensitivity.select_dtypes(
        include="number"
    ).columns
    rounded_random_sensitivity[random_numeric_cols] = rounded_random_sensitivity[
        random_numeric_cols
    ].round(3)
    rounded_random_sensitivity.to_csv(
        TABLE_DIR / "member3_random_seed_sensitivity.csv",
        index=False,
    )
    rounded_random_sensitivity_summary = random_sensitivity_summary.copy()
    summary_numeric_cols = rounded_random_sensitivity_summary.select_dtypes(
        include="number"
    ).columns
    rounded_random_sensitivity_summary[summary_numeric_cols] = (
        rounded_random_sensitivity_summary[summary_numeric_cols].round(3)
    )
    rounded_random_sensitivity_summary.to_csv(
        TABLE_DIR / "member3_random_seed_sensitivity_summary.csv",
        index=False,
    )

    jaipur = scenarios["Jaipur"]
    jaipur_output = scenario_outputs["Jaipur"]
    jaipur_routes = scenario_outputs["Jaipur"].routes
    optimized_method = "Balanced Geo + NN + 2-opt"
    jaipur_optimized_routes = jaipur_routes[optimized_method]

    rider_summary = build_rider_summary_table(
        jaipur_optimized_routes,
        jaipur_output.distance_matrix,
        jaipur,
        "Jaipur",
        optimized_method,
    )
    route_sequence = build_route_sequence_table(
        jaipur_optimized_routes,
        jaipur,
        "Jaipur",
        optimized_method,
    )
    rounded_rider_summary = rider_summary.copy()
    rider_numeric_cols = rounded_rider_summary.select_dtypes(include="number").columns
    rounded_rider_summary[rider_numeric_cols] = rounded_rider_summary[
        rider_numeric_cols
    ].round(3)
    rounded_rider_summary.to_csv(
        TABLE_DIR / "member3_jaipur_optimized_rider_summary.csv",
        index=False,
    )
    route_sequence.to_csv(
        TABLE_DIR / "member3_jaipur_optimized_routes.csv",
        index=False,
    )

    plot_customer_scatter(
        jaipur,
        "Jaipur Customer Locations and Common Depot",
        FIGURE_DIR / "jaipur_customer_locations.png",
    )
    plot_routes(
        jaipur,
        jaipur_routes["Original Order"],
        "Jaipur Original Order Baseline Routes",
        FIGURE_DIR / "jaipur_baseline_route.png",
    )
    plot_routes(
        jaipur,
        jaipur_optimized_routes,
        "Jaipur Optimized Heuristic Routes",
        FIGURE_DIR / "jaipur_optimized_route.png",
    )
    plot_metric_bar(
        all_results,
        "total_distance_km",
        "Total Distance by Scenario and Method",
        FIGURE_DIR / "distance_comparison.png",
    )
    plot_metric_bar(
        all_results,
        "workload_imbalance_km",
        "Workload Imbalance by Scenario and Method",
        FIGURE_DIR / "workload_comparison.png",
    )

    print("Validation summary")
    print(validation.to_string(index=False))
    print()
    print("Result summary")
    print(rounded.to_string(index=False))
    print()
    print("Jaipur optimized rider summary")
    print(rounded_rider_summary.to_string(index=False))
    print()
    print("Random seed sensitivity summary")
    print(rounded_random_sensitivity_summary.to_string(index=False))
    print()
    print(f"Saved tables to {TABLE_DIR.resolve()}")
    print(f"Saved figures to {FIGURE_DIR.resolve()}")


if __name__ == "__main__":
    main()
