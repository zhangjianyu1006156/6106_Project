# Member 3 Slide Outline: Computational Experiment and Results

## Slide 1: Computational Setup

- Scenarios: Jaipur main test, Mumbai robustness test, Hyderabad robustness test
- Data size: 50 orders per city scenario
- Resources: 5 riders, 10-order capacity per rider
- Depot assumption: common depot from average restaurant location
- Routing measure: Haversine distance between depot and customer delivery nodes
- Evaluation metrics: total distance, estimated travel time, rider workload imbalance

Suggested visual:

- `outputs/figures/jaipur_customer_locations.png`

## Slide 2: Methods Compared

| Method | Role in Experiment | Capacity Feasible? |
|---|---|---|
| Original Order | Time-order baseline | Yes |
| Random Assignment | Randomized baseline | Yes |
| Geographic Clustering | Spatial assignment baseline | Not guaranteed |
| Geographic + Nearest Neighbor | Spatial assignment plus route sequencing | Not guaranteed |
| Balanced Geo + NN + 2-opt | Final optimized heuristic | Yes |

Key message:

Balanced Geo + NN + 2-opt is the final implemented method because it reduces distance while keeping exactly 10 orders per rider.

## Slide 3: Main Jaipur Results

| Method | Total Distance (km) | Estimated Time (min) | Improvement |
|---|---:|---:|---:|
| Original Order | 472.537 | 1692.977 | 0.000% |
| Balanced Geo + NN + 2-opt | 247.324 | 871.263 | 47.661% |

Key message:

The optimized heuristic reduces total travel distance by 47.661% in the main Jaipur scenario while maintaining feasible rider capacity.

Suggested visuals:

- `outputs/figures/jaipur_baseline_route.png`
- `outputs/figures/jaipur_optimized_route.png`

## Slide 4: Robustness and Managerial Takeaway

| Scenario | Original Distance (km) | Optimized Distance (km) | Improvement |
|---|---:|---:|---:|
| Jaipur | 472.537 | 247.324 | 47.661% |
| Mumbai | 768.190 | 293.432 | 61.802% |
| Hyderabad | 571.753 | 250.198 | 56.240% |

Key message:

The same prescriptive routing logic works across three city layouts. Grouping nearby customers and improving route sequences can reduce unnecessary travel while preserving workload fairness.

Suggested visuals:

- `outputs/figures/distance_comparison.png`
- `outputs/figures/workload_comparison.png`
