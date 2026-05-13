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

The final method is used as the implemented optimized heuristic because it respects the 10-order rider capacity. The pure K-means methods are useful baselines and may produce lower raw distance, but they can assign too many orders to one rider and therefore may violate the final capacity requirement.

The balanced geographic assignment method sorts customers around the common depot by angular position and distance, then divides them into equal-sized rider groups. This keeps nearby customers together while enforcing the 10-order capacity for each rider. After assignment, nearest neighbor creates an initial route for each rider, and 2-opt improves the route by removing inefficient edge crossings.

| Method | Assignment Optimized? | Route Sequencing Optimized? | Capacity Feasible? |
|---|---|---|---|
| Original Order | No | No | Yes |
| Random Assignment | No | No | Yes |
| Geographic Clustering | Partly | No | No / not guaranteed |
| Geographic + Nearest Neighbor | Partly | Yes | No / not guaranteed |
| Balanced Geo + NN + 2-opt | Yes | Yes | Yes |

## 4. Main Jaipur Results

| Method | Total Distance (km) | Avg Distance/Rider (km) | Workload Imbalance (km) | Estimated Time (min) | Improvement vs Original |
|---|---:|---:|---:|---:|---:|
| Original Order | 472.537 | 94.507 | 59.339 | 1692.977 | 0.000% |
| Random Assignment | 514.278 | 102.856 | 26.207 | 1849.544 | -8.833% |
| Geographic Clustering | 319.475 | 63.895 | 37.397 | 1093.101 | 32.392% |
| Geographic + Nearest Neighbor | 224.868 | 44.974 | 9.016 | 810.889 | 52.413% |
| Balanced Geo + NN + 2-opt | 247.324 | 49.465 | 10.844 | 871.263 | 47.661% |

For the main Jaipur scenario, the balanced optimized heuristic reduces total distance from 472.537 km to 247.324 km, which is a 47.661% improvement over the original-order baseline. Estimated total travel time also decreases from 1692.977 minutes to 871.263 minutes.

The capacity columns in the result table confirm why the balanced optimized method is selected as the final computational solution. In Jaipur, the unconstrained K-means methods assign between 3 and 20 orders per rider, while the balanced method assigns exactly 10 orders to each rider. Therefore, the final method is slightly longer than unconstrained K-means plus nearest neighbor, but it is more realistic for a 5-rider, 10-order-capacity operating setting.

The per-rider optimized route summary for Jaipur is:

| Rider | Number of Orders | Route Distance (km) | Estimated Time (min) |
|---:|---:|---:|---:|
| 1 | 10 | 55.407 | 192.343 |
| 2 | 10 | 44.946 | 146.470 |
| 3 | 10 | 46.080 | 178.596 |
| 4 | 10 | 45.100 | 147.529 |
| 5 | 10 | 55.790 | 206.326 |

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
- `scripts/member3_run_experiment.py`

The generated tables are:

- `outputs/tables/member3_validation_summary.csv`
- `outputs/tables/member3_results_summary.csv`
- `outputs/tables/member3_jaipur_optimized_rider_summary.csv`
- `outputs/tables/member3_jaipur_optimized_routes.csv`
- `outputs/tables/member3_random_seed_sensitivity.csv`
- `outputs/tables/member3_random_seed_sensitivity_summary.csv`

The generated figures are:

- `outputs/figures/jaipur_customer_locations.png`
- `outputs/figures/jaipur_baseline_route.png`
- `outputs/figures/jaipur_optimized_route.png`
- `outputs/figures/distance_comparison.png`
- `outputs/figures/workload_comparison.png`

## 7. Interpretation for Final Report

The experiment shows that simple non-optimized delivery rules can create unnecessary travel distance. Geographic clustering improves performance because nearby customers are grouped together, but unconstrained clustering may overload individual riders. The balanced optimized heuristic addresses this issue by enforcing equal route size while still using spatial structure and local route improvement. This makes it a practical prescriptive analytics solution that is consistent with the formal CVRP model while remaining computationally feasible for the project scope.

Member 2 formalizes the problem as a simplified capacitated vehicle routing problem. The computational experiment implements this logic through a balanced geographic assignment and route improvement heuristic. This practical approach respects the main CVRP assumptions: each order is served once, each rider receives 10 orders, routes start from and return to the common depot, and route distance is reduced through sequencing improvement.

Estimated travel time is calculated after route construction using average rider speed and multipliers for traffic density and weather condition. Therefore, traffic and weather are included in performance evaluation, while the optimization objective remains total Haversine distance.

From a managerial perspective, the results suggest that a platform can reduce unnecessary travel by grouping nearby customers and improving rider route sequences. The balanced optimized method is especially useful because it reduces total distance while maintaining equal order counts across riders, which supports both operational efficiency and workload fairness.

A random-seed sensitivity check was also run for the random assignment baseline using 10 seeds. This check is used only to verify that the optimized heuristic is not being compared with an unusually weak single random draw; the final decision still relies on the deterministic balanced optimized method.

## 8. Limitations

The route plots use straight-line geographic distances rather than actual road network distances. The model also uses a common depot instead of modeling separate restaurant pickup locations. Therefore, the results should be interpreted as a planning-level estimate of routing improvement, not an exact real-time dispatch plan.

## 9. Reproducibility Note

The experiment can be reproduced by running `python3 scripts/member3_run_experiment.py` from the project root after installing the required Python packages. The script loads the processed datasets, validates the scenarios, runs all baseline and optimized methods, exports result tables, and saves route and comparison figures.
