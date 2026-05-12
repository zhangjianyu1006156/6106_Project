# Member 3 Follow-up Tasks: Computational Experiment Finalization

## 1. Current Status

Member 3 has already completed the main computational framework. This is not a fresh-start task anymore. The current project already includes:

| Item | Status | Evidence |
|---|---|---|
| Data loading for three scenarios | Completed | `load_scenarios()` in `src/member3_utils.py` |
| Scenario validation | Completed | `outputs/tables/member3_validation_summary.csv` |
| Haversine distance matrix | Completed | `build_distance_matrix()` |
| Common depot assumption | Completed | `create_depot()` |
| Original order baseline | Completed | `original_order_baseline()` |
| Random assignment baseline | Completed | `random_assignment_baseline()` |
| Geographic clustering baseline | Completed | `geographic_clustering_baseline()` |
| Nearest-neighbor route sequencing | Completed | `nearest_neighbor_route()` |
| 2-opt route improvement | Completed | `two_opt_route()` |
| Balanced optimized heuristic | Completed | `Balanced Geo + NN + 2-opt` in workflow |
| Robustness tests | Completed | Jaipur, Mumbai, Hyderabad results |
| Result table export | Completed | `outputs/tables/member3_results_summary.csv` |
| Route and metric figures | Completed | `outputs/figures/*.png` |
| Draft computational report | Completed | `member3_report.md` |

Member 2 has now confirmed the final model direction:

- formal model: simplified capacitated vehicle routing problem;
- main objective: total Haversine distance;
- depot: average restaurant location;
- rider capacity: 10 orders;
- return to depot: yes;
- traffic and weather: used for estimated travel-time evaluation;
- implemented optimized method: balanced geographic assignment + nearest neighbor + 2-opt.

This means Member 3's existing implementation is aligned with the final model. The remaining work is mainly finalization, verification, explanation, and presentation polish.

## 2. Must-do Tasks Before Final Submission

### Task 1: Re-run the Experiment Once and Confirm Outputs

Run:

```bash
python member3_run_experiment.py
```

Expected outputs:

| Output | Required Check |
|---|---|
| `outputs/tables/member3_validation_summary.csv` | 3 rows: Jaipur, Mumbai, Hyderabad |
| `outputs/tables/member3_results_summary.csv` | 15 rows: 3 scenarios x 5 methods |
| `outputs/figures/jaipur_customer_locations.png` | customer scatter and depot visible |
| `outputs/figures/jaipur_baseline_route.png` | baseline route visible |
| `outputs/figures/jaipur_optimized_route.png` | optimized route visible |
| `outputs/figures/distance_comparison.png` | all scenarios and methods shown |
| `outputs/figures/workload_comparison.png` | workload imbalance comparison shown |

After rerunning, confirm that the main result is still:

| Scenario | Original Distance | Optimized Distance | Improvement |
|---|---:|---:|---:|
| Jaipur | 472.537 km | 247.324 km | 47.661% |
| Mumbai | 768.190 km | 293.432 km | 61.802% |
| Hyderabad | 571.753 km | 250.198 km | 56.240% |

If the numbers change, update `member3_report.md`, `member2_report.md`, and all slides using the new values.

### Task 2: Update Member 3 Report to Match Member 2's Final Model

In `member3_report.md`, update Section 7 because it still says:

```text
If Member 2 later provides a full VRP or MIP formulation...
```

This is now outdated. Replace it with a final alignment statement:

```text
Member 2 formalizes the problem as a simplified capacitated vehicle routing problem. The computational experiment implements this logic through a balanced geographic assignment and route improvement heuristic. This practical approach respects the main CVRP assumptions: each order is served once, each rider receives 10 orders, routes start from and return to the common depot, and route distance is minimized through sequencing improvement.
```

Also make sure the report clearly states:

- the optimized method is the final implemented method, not a placeholder;
- K-means methods are useful baselines but may violate rider capacity;
- Balanced Geo + NN + 2-opt is preferred because it respects capacity exactly.

### Task 3: Add a Short Explanation of the Balanced Geographic Method

The report currently names the method, but the final report should explain it in plain language. Add a short paragraph:

```text
The balanced geographic assignment method sorts customers around the depot by angular position and distance, then divides them into equal-sized rider groups. This keeps nearby customers together while enforcing the 10-order capacity for each rider. After assignment, nearest neighbor creates an initial route for each rider, and 2-opt improves the route by removing inefficient edge crossings.
```

This matters because teachers may ask how the method differs from ordinary K-means.

### Task 4: Verify Capacity Feasibility in the Results Table

Use `outputs/tables/member3_results_summary.csv` and confirm:

| Method | Expected Capacity Behavior |
|---|---|
| Original Order | 10 orders per rider |
| Random Assignment | 10 orders per rider |
| Geographic Clustering | may be unbalanced |
| Geographic + Nearest Neighbor | may be unbalanced |
| Balanced Geo + NN + 2-opt | exactly 10 orders per rider |

The current results already show this through:

- `max_orders_per_rider`;
- `min_orders_per_rider`.

In the final report, mention this explicitly. The balanced optimized method may not always have the shortest distance compared with unconstrained K-means + NN, but it is more realistic because it respects rider capacity.

### Task 5: Check the Notebook Matches the Script

The project includes:

- `member3_computational_experiment.ipynb`;
- `member3_run_experiment.py`;
- `src/member3_utils.py`.

The notebook should not contain outdated logic that contradicts the script. Check that the notebook:

1. uses the same three datasets;
2. uses the same common depot assumption;
3. includes the same five methods;
4. reports the same final optimized method;
5. exports or displays the same result values.

If the notebook is not needed for submission, say in the final report or README that the script is the reproducible one-click runner.

### Task 6: Prepare Final Presentation Material

Member 3 should prepare 3-4 slides:

| Slide | Content |
|---|---|
| Computational Setup | datasets, 50 orders, 5 riders, common depot, Haversine distance |
| Methods Compared | Original Order, Random Assignment, Geographic Clustering, Geographic + NN, Balanced Geo + NN + 2-opt |
| Main Jaipur Results | result table and optimized route figure |
| Robustness Test | distance reduction across Jaipur, Mumbai, Hyderabad |

Use these figures:

- `outputs/figures/jaipur_baseline_route.png`;
- `outputs/figures/jaipur_optimized_route.png`;
- `outputs/figures/distance_comparison.png`;
- `outputs/figures/workload_comparison.png`.

The slides should emphasize that the final method is not just descriptive analysis. It is a prescriptive solution that changes assignment and routing decisions.

## 3. Should-do Tasks for a Stronger Final Report

### Task 7: Add a Short Reproducibility Note

Add a small section to `member3_report.md`:

```text
The experiment can be reproduced by running `python member3_run_experiment.py` from the project root. The script loads the processed datasets, validates the scenarios, runs all baseline and optimized methods, exports result tables, and saves route and comparison figures.
```

This makes the computational part look more professional.

### Task 8: Explain Traffic and Weather Time Evaluation

Member 3 calculates estimated travel time using traffic and weather multipliers. The final report should make clear that:

- distance is the optimization objective;
- estimated time is an evaluation metric;
- traffic/weather multipliers adjust leg time based on destination order conditions.

Suggested wording:

```text
Estimated travel time is calculated after route construction using average rider speed and multipliers for traffic density and weather condition. Therefore, traffic and weather are included in performance evaluation, while the optimization objective remains total distance.
```

This matches Member 2's model decision.

### Task 9: Add One Limitation Paragraph

The final computational section should honestly state limitations:

```text
The route plots use straight-line geographic distances rather than actual road network distances. The model also uses a common depot instead of modeling separate restaurant pickup locations. Therefore, the results should be interpreted as a planning-level estimate of routing improvement, not an exact real-time dispatch plan.
```

This is important because the distance reductions are large, and the simplifications should be transparent.

### Task 10: Add One Managerial Interpretation Paragraph

After the results, add a practical takeaway:

```text
The results suggest that a platform can reduce unnecessary travel by grouping nearby customers and improving rider route sequences. The balanced optimized method is especially useful because it reduces total distance while maintaining equal order counts across riders, which supports both operational efficiency and workload fairness.
```

This helps connect the coding results back to the business problem.

## 4. Optional Improvement Tasks

These are useful only if there is time. Do not do them before the must-do tasks.

### Optional 1: Add Per-rider Route Summary Table

Create a table for Jaipur optimized routes:

| Rider | Number of Orders | Route Distance |
|---|---:|---:|
| Rider 1 | 10 | xx |
| Rider 2 | 10 | xx |
| Rider 3 | 10 | xx |
| Rider 4 | 10 | xx |
| Rider 5 | 10 | xx |

This can support the workload balance argument.

### Optional 2: Save Routes as CSV

Export the final optimized route sequence:

```text
outputs/tables/member3_jaipur_optimized_routes.csv
```

Suggested columns:

- `scenario`;
- `rider`;
- `route_position`;
- `scenario_order_id`.

This makes the optimized decision more concrete.

### Optional 3: Add Sensitivity Test for Random Seed

Random assignment uses a fixed seed. If time allows, run random assignment under several seeds and report the average. This is not required for the main result because the optimized method is deterministic under the current workflow.

### Optional 4: Add a Small Table Explaining Method Feasibility

Add this table to the report:

| Method | Assignment Optimized? | Route Sequencing Optimized? | Capacity Feasible? |
|---|---|---|---|
| Original Order | No | No | Yes |
| Random Assignment | No | No | Yes |
| Geographic Clustering | Partly | No | No / not guaranteed |
| Geographic + Nearest Neighbor | Partly | Yes | No / not guaranteed |
| Balanced Geo + NN + 2-opt | Yes | Yes | Yes |

This helps explain why the final optimized method is selected even when another method has lower raw distance.

## 5. Final Acceptance Checklist

Before Member 3 says the work is finished, all of the following should be true:

- `python member3_run_experiment.py` runs successfully from the project root.
- `member3_results_summary.csv` has 15 rows.
- `member3_validation_summary.csv` has 3 rows.
- Jaipur optimized distance is reported as 247.324 km unless rerun results change.
- The final optimized method is named consistently as `Balanced Geo + NN + 2-opt`.
- The report explains why unconstrained K-means methods are not the final chosen method.
- The report states that distance is the optimization objective and estimated time is an evaluation metric.
- The report states the common depot and return-to-depot assumptions.
- The report includes at least one baseline route figure and one optimized route figure.
- The robustness section includes Jaipur, Mumbai, and Hyderabad.
- Any slide numbers match the latest result table.

## 6. Recommended Work Order

Do the remaining work in this order:

1. Re-run `member3_run_experiment.py`.
2. Confirm the output tables and figures.
3. Update `member3_report.md` Section 7 to remove outdated wording.
4. Add explanation of the balanced geographic method.
5. Add reproducibility, limitation, and managerial interpretation paragraphs.
6. Check the notebook for consistency with the script.
7. Prepare 3-4 presentation slides.
8. Only then consider optional route export or sensitivity testing.

The main goal now is not to add a completely new model. The goal is to make the existing computational experiment defensible, reproducible, and fully aligned with Member 2's final mathematical formulation.

