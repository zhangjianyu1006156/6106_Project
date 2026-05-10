# Member 3 Report: Computational Experiment, Baselines, Optimization, and Robustness Testing

## 1. Computational Setup

This section implements the computational experiment for the food delivery order assignment and routing problem. The experiment uses the three processed datasets prepared by Member 1:

| Scenario | City | File | Orders | Riders | Capacity |
|---|---|---|---:|---:|---:|
| Main | Jaipur | `data/processed/main_optimization_jaipur.csv` | 50 | 5 | 10 |
| Robustness 1 | Mumbai | `data/processed/robustness_mumbai.csv` | 50 | 5 | 10 |
| Robustness 2 | Hyderabad | `data/processed/robustness_hyderabad.csv` | 50 | 5 | 10 |

A common depot is defined as the average restaurant location in each city scenario. Customer nodes are represented by delivery latitude and longitude. Haversine distance is used to approximate the travel distance between nodes. Each rider starts from the common depot and returns to the depot after completing assigned deliveries.

The main objective in this computational experiment is to reduce total travel distance while keeping rider workload feasible. Estimated travel time is also reported using traffic and weather multipliers.

## 2. Data Validation

The validation confirms that each scenario contains 50 orders from one city, selected from one evening peak date, with no missing values in the key routing columns.

| Scenario | Rows | City Code | Date | Order Hour Range | Missing Key Values |
|---|---:|---|---|---|---:|
| Jaipur | 50 | JAP | 02-04-2022 | 17.0-23.0 | 0 |
| Mumbai | 50 | MUM | 02-03-2022 | 17.0-23.0 | 0 |
| Hyderabad | 50 | HYD | 18-03-2022 | 17.0-23.0 | 0 |

## 3. Methods Compared

Five methods are compared:

1. **Original Order**: orders are sorted by order time and assigned to riders by round-robin.
2. **Random Assignment**: orders are randomly shuffled and assigned by round-robin.
3. **Geographic Clustering**: K-means groups customers spatially, but the within-cluster sequence is not optimized.
4. **Geographic + Nearest Neighbor**: K-means assignment followed by nearest-neighbor route sequencing.
5. **Balanced Geo + NN + 2-opt**: customers are assigned using a balanced geographic sweep so that each rider receives 10 orders, then each route is sequenced by nearest neighbor and improved by 2-opt.

The final method is used as the current optimized heuristic because it respects the 10-order rider capacity. The pure K-means methods may produce lower distance, but they can assign too many orders to one rider.

## 4. Main Jaipur Results

| Method | Total Distance (km) | Avg Distance/Rider (km) | Workload Imbalance (km) | Estimated Time (min) | Improvement vs Original |
|---|---:|---:|---:|---:|---:|
| Original Order | 472.537 | 94.507 | 59.339 | 1692.977 | 0.000% |
| Random Assignment | 514.278 | 102.856 | 26.207 | 1849.544 | -8.833% |
| Geographic Clustering | 319.475 | 63.895 | 37.397 | 1093.101 | 32.392% |
| Geographic + Nearest Neighbor | 224.868 | 44.974 | 9.016 | 810.889 | 52.413% |
| Balanced Geo + NN + 2-opt | 247.324 | 49.465 | 10.844 | 871.263 | 47.661% |

For the main Jaipur scenario, the balanced optimized heuristic reduces total distance from 472.537 km to 247.324 km, which is a 47.661% improvement over the original-order baseline. Estimated total travel time also decreases from 1692.977 minutes to 871.263 minutes.

## 5. Robustness Results

| Scenario | Original Distance (km) | Optimized Distance (km) | Improvement vs Original |
|---|---:|---:|---:|
| Jaipur | 472.537 | 247.324 | 47.661% |
| Mumbai | 768.190 | 293.432 | 61.802% |
| Hyderabad | 571.753 | 250.198 | 56.240% |

The optimized heuristic remains effective across all three city scenarios. The improvement is largest in Mumbai, where the original routing pattern produces the longest total distance. Hyderabad and Jaipur also show large reductions, suggesting that geographic assignment and route sequencing are transferable across different urban layouts.

## 6. Deliverables Generated

The computational code is implemented in:

- `src/member3_utils.py`
- `member3_run_experiment.py`

The generated tables are:

- `outputs/tables/member3_validation_summary.csv`
- `outputs/tables/member3_results_summary.csv`

The generated figures are:

- `outputs/figures/jaipur_customer_locations.png`
- `outputs/figures/jaipur_baseline_route.png`
- `outputs/figures/jaipur_optimized_route.png`
- `outputs/figures/distance_comparison.png`
- `outputs/figures/workload_comparison.png`

## 7. Interpretation for Final Report

The experiment shows that simple non-optimized delivery rules can create unnecessary travel distance. Geographic clustering improves performance because nearby customers are grouped together, but unconstrained clustering may overload individual riders. The balanced optimized heuristic addresses this issue by enforcing equal route size while still using spatial structure and local route improvement. This makes it a practical prescriptive analytics solution before implementing a full mathematical programming model.

If Member 2 later provides a full VRP or MIP formulation, the current workflow can be used as the benchmark framework. The optimized model can replace the current heuristic while keeping the same validation, metrics, visualizations, and robustness tests.
