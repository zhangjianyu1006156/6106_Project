from pathlib import Path
import os

import pandas as pd

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "4")

from src.member3_utils import (
    load_scenarios,
    plot_customer_scatter,
    plot_metric_bar,
    plot_routes,
    run_scenario_workflow,
    validate_scenario,
)


OUTPUT_DIR = Path("outputs")
TABLE_DIR = OUTPUT_DIR / "tables"
FIGURE_DIR = OUTPUT_DIR / "figures"


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    scenarios = load_scenarios()
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

    jaipur = scenarios["Jaipur"]
    jaipur_routes = scenario_outputs["Jaipur"].routes
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
        jaipur_routes["Balanced Geo + NN + 2-opt"],
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
    print(f"Saved tables to {TABLE_DIR.resolve()}")
    print(f"Saved figures to {FIGURE_DIR.resolve()}")


if __name__ == "__main__":
    main()
