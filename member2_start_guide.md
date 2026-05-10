# Member 2 Start Guide: Mathematical Model and Optimization Formulation

Project: **Food Delivery Order Assignment and Route Optimization under Traffic and Weather Conditions**  
Role: **Member 2 — mathematical formulation, optimization model design, assumptions, and model explanation**

---

## 1. Your Role in the Project

Member 2 is responsible for converting the business problem and cleaned data into a clear prescriptive analytics optimization model.

Your main tasks are:

1. Define the formal optimization problem.
2. Specify decision variables.
3. Define the objective function.
4. Write the constraints.
5. Explain model assumptions.
6. Decide whether the final model is a full VRP/MIP or a simplified assignment-routing model.
7. Coordinate with Member 3 so the model can be implemented in Python.
8. Prepare the mathematical model section for the final report and presentation.

Member 1 has already prepared the datasets. Member 3 has started computational experiments, baselines, heuristic optimization, visualizations, and robustness tests.

---

## 2. Project Problem Statement

The project studies a food delivery assignment and routing problem:

> Given a set of food delivery orders in one city during the evening peak period, how should the platform assign orders to a limited number of riders and determine each rider's delivery route to reduce total travel distance, estimated delivery time, and rider workload imbalance?

The decision problem has two parts:

1. **Assignment decision**: which rider serves each order.
2. **Routing decision**: in what sequence each rider visits assigned customer locations.

The model should be designed around a simplified vehicle routing problem.

---

## 3. Input Data for the Model

Use the processed datasets from Member 1:

| Scenario | File | City | Orders | Suggested Riders | Suggested Capacity |
|---|---|---|---:|---:|---:|
| Main | `data/processed/main_optimization_jaipur.csv` | Jaipur | 50 | 5 | 10 orders/rider |
| Robustness 1 | `data/processed/robustness_mumbai.csv` | Mumbai | 50 | 5 | 10 orders/rider |
| Robustness 2 | `data/processed/robustness_hyderabad.csv` | Hyderabad | 50 | 5 | 10 orders/rider |

Important columns:

| Column | Meaning |
|---|---|
| `scenario_order_id` | Local order ID from 1 to 50 |
| `Restaurant_latitude`, `Restaurant_longitude` | Restaurant coordinates |
| `Delivery_location_latitude`, `Delivery_location_longitude` | Customer coordinates |
| `Time_Orderd` | Order time |
| `Weather_conditions` | Weather condition |
| `Road_traffic_density` | Traffic condition |
| `time_taken_min` | Actual delivery time, for reference only |

Member 3 currently uses a **common depot assumption**, where the depot is the average restaurant location in each scenario.

---

## 4. Recommended Modeling Assumptions

To keep the model feasible and explainable, use these assumptions:

1. All orders in one scenario belong to the same city and same operating period.
2. Each order must be served exactly once.
3. Each rider starts from a common depot.
4. Each rider returns to the depot after completing deliveries.
5. Each rider can serve at most 10 orders.
6. Travel distance is approximated by Haversine distance.
7. Traffic and weather can be included through travel-time multipliers.
8. The model does not include strict time windows.
9. The model is a simplified VRP, not a full real-world food delivery dispatch system.

Recommended default parameters:

```text
Number of riders: K = 5
Number of customer orders: N = 50
Rider capacity: Q = 10
Depot node: 0
Customer nodes: 1, 2, ..., 50
```

---

## 5. Sets and Indices

Use the following notation:

| Symbol | Meaning |
|---|---|
| `N` | Set of customer orders, indexed by `i, j` |
| `V` | Set of all nodes, including depot and customers, `V = {0} ∪ N` |
| `K` | Set of riders, indexed by `k` |
| `0` | Common depot node |

Example:

```text
N = {1, 2, ..., 50}
K = {1, 2, ..., 5}
V = {0, 1, 2, ..., 50}
```

---

## 6. Parameters

| Parameter | Meaning |
|---|---|
| `d_ij` | Distance from node `i` to node `j` |
| `t_ij` | Estimated travel time from node `i` to node `j` |
| `Q` | Maximum number of orders per rider |
| `M` | Large constant for subtour elimination |
| `a_i` | Demand of order `i`, usually `a_i = 1` |
| `traffic_i` | Traffic condition of order `i` |
| `weather_i` | Weather condition of order `i` |

Distance can be calculated using Haversine distance.

Estimated travel time can be defined as:

```text
t_ij = d_ij / speed × traffic_multiplier × weather_multiplier
```

For the first version, the objective can focus on distance. Traffic and weather can be included as secondary analysis if the full time-based model is too complex.

---

## 7. Decision Variables

Recommended full VRP decision variables:

| Variable | Type | Meaning |
|---|---|---|
| `x_ijk` | Binary | 1 if rider `k` travels directly from node `i` to node `j`, 0 otherwise |
| `y_ik` | Binary | 1 if order `i` is assigned to rider `k`, 0 otherwise |
| `u_ik` | Continuous / Integer | Position or load variable for subtour elimination |

Where:

```text
x_ijk ∈ {0, 1}, for i, j ∈ V, i ≠ j, k ∈ K
y_ik ∈ {0, 1}, for i ∈ N, k ∈ K
```

---

## 8. Objective Function

### Option A: Minimize Total Distance

This is the recommended main objective because it is simple, stable, and already matches Member 3's experiment.

```text
Minimize ∑_{k∈K} ∑_{i∈V} ∑_{j∈V, j≠i} d_ij x_ijk
```

### Option B: Minimize Estimated Travel Time

If including traffic and weather directly:

```text
Minimize ∑_{k∈K} ∑_{i∈V} ∑_{j∈V, j≠i} t_ij x_ijk
```

### Option C: Weighted Objective

If the group wants to include both distance and workload balance:

```text
Minimize α × total_distance + β × workload_imbalance
```

For the final report, Option A is safest. Option B can be discussed as an extension or tested by Member 3.

---

## 9. Core Constraints

### Constraint 1: Each Order Is Served Exactly Once

Each customer order must be assigned to one rider.

```text
∑_{k∈K} y_ik = 1, for all i ∈ N
```

### Constraint 2: Rider Capacity

Each rider can serve at most `Q` orders.

```text
∑_{i∈N} y_ik ≤ Q, for all k ∈ K
```

For this project:

```text
Q = 10
```

Since there are 50 orders and 5 riders, this means each rider will effectively serve 10 orders if all riders are used.

### Constraint 3: Link Assignment and Routing

If order `i` is assigned to rider `k`, rider `k` must enter and leave node `i`.

```text
∑_{j∈V, j≠i} x_ijk = y_ik, for all i ∈ N, k ∈ K
```

```text
∑_{j∈V, j≠i} x_jik = y_ik, for all i ∈ N, k ∈ K
```

### Constraint 4: Start from Depot

Each rider starts from the depot.

```text
∑_{j∈N} x_0jk = 1, for all k ∈ K
```

### Constraint 5: Return to Depot

Each rider returns to the depot.

```text
∑_{i∈N} x_i0k = 1, for all k ∈ K
```

### Constraint 6: No Self-Loops

A rider cannot travel from a node to itself.

```text
x_iik = 0, for all i ∈ V, k ∈ K
```

### Constraint 7: Subtour Elimination

Use MTZ subtour elimination constraints.

```text
u_ik - u_jk + Q x_ijk ≤ Q - 1,
for all i, j ∈ N, i ≠ j, k ∈ K
```

Bounds:

```text
1 ≤ u_ik ≤ Q, for all i ∈ N, k ∈ K
```

This prevents a rider's route from splitting into disconnected cycles.

---

## 10. Alternative Simpler Model

If the full VRP MIP is too hard to implement or solve, use a two-stage model:

### Stage 1: Assignment

Assign orders to riders while balancing capacity and geographic compactness.

Possible objective:

```text
Minimize ∑ distance from order i to assigned rider cluster/depot
```

Subject to:

```text
Each order assigned once
Each rider gets at most 10 orders
```

### Stage 2: Route Sequencing

For each rider, solve a small TSP over 10 assigned orders.

This matches Member 3's current heuristic:

```text
Balanced geographic assignment + nearest neighbor + 2-opt
```

This is easier to explain and more reliable computationally than a full 50-order VRP.

---

## 11. What Member 3 Has Already Implemented

Member 3 has already created:

| File | Purpose |
|---|---|
| `src/member3_utils.py` | Distance matrix, baselines, heuristic optimization, route plotting |
| `member3_run_experiment.py` | One-click experiment runner |
| `member3_computational_experiment.ipynb` | Notebook version of experiment workflow |
| `member3_report.md` | Draft computational report |
| `outputs/tables/member3_results_summary.csv` | Results table |
| `outputs/figures/*.png` | Route and comparison figures |

Current optimized method:

```text
Balanced Geo + Nearest Neighbor + 2-opt
```

Reason:

- It keeps each rider at exactly 10 orders.
- It reduces total distance substantially.
- It is easier to implement and explain than a full VRP.
- It can serve as a benchmark or backup if the full MIP is too slow.

---

## 12. Results Member 2 Can Refer To

Current main Jaipur result:

| Method | Total Distance (km) | Improvement vs Original |
|---|---:|---:|
| Original Order | 472.537 | 0.000% |
| Balanced Geo + NN + 2-opt | 247.324 | 47.661% |

Robustness results:

| Scenario | Original Distance (km) | Optimized Distance (km) | Improvement |
|---|---:|---:|---:|
| Jaipur | 472.537 | 247.324 | 47.661% |
| Mumbai | 768.190 | 293.432 | 61.802% |
| Hyderabad | 571.753 | 250.198 | 56.240% |

Member 2 can use these results to motivate why assignment and routing optimization matters.

---

## 13. Questions Member 2 Should Confirm

Please confirm these settings so Member 3 can align the final code:

1. Should the final model assume one common depot using average restaurant location?
2. Should riders return to the depot after completing deliveries?
3. Is the primary objective total distance or estimated delivery time?
4. Is rider capacity exactly 10 orders or at most 10 orders?
5. Should traffic and weather be included directly in the objective, or discussed as estimated-time analysis?
6. Should the final project present a full VRP MIP, or a two-stage assignment and routing heuristic?
7. If using full MIP, should we solve only Jaipur or also Mumbai and Hyderabad?

Recommended answer for project feasibility:

```text
Use a simplified capacitated VRP formulation in the report.
Use total distance as the main objective.
Use common depot and return-to-depot assumptions.
Use capacity Q = 10.
Use traffic/weather for estimated time comparison and discussion.
Use Member 3's balanced geographic + NN + 2-opt method as the computational optimized solution.
```

---

## 14. Suggested Report Text for Member 2

You can adapt this in the final report:

```text
The delivery assignment and routing problem is formulated as a simplified capacitated vehicle routing problem. Each order is represented as a customer node, and a common depot is defined using the average restaurant location in the selected city scenario. The decision variables determine whether a rider travels directly between two nodes and whether an order is assigned to a rider. The objective is to minimize the total travel distance across all riders, subject to assignment, capacity, route continuity, depot departure and return, and subtour elimination constraints.

This formulation captures the core prescriptive decision faced by a food delivery platform: assigning each order to exactly one rider and sequencing the rider's route efficiently. Traffic and weather conditions are incorporated in the computational analysis through travel-time multipliers, while distance remains the primary optimization objective for model simplicity and interpretability.
```

---

## 15. Suggested Slide Content

### Slide: Optimization Model

- Simplified capacitated vehicle routing problem
- 50 customer orders, 5 riders
- Common depot based on average restaurant location
- Each order served exactly once
- Capacity: maximum 10 orders per rider
- Objective: minimize total delivery distance

### Slide: Decision Variables and Constraints

- `x_ijk`: whether rider `k` travels from node `i` to node `j`
- `y_ik`: whether order `i` is assigned to rider `k`
- Assignment constraint
- Rider capacity constraint
- Depot start and return constraints
- Flow conservation
- Subtour elimination

### Slide: Link to Computational Experiment

- Member 3 implements baselines and optimized heuristic
- Baselines: original order, random assignment, geographic clustering
- Optimized method: balanced geographic assignment + nearest neighbor + 2-opt
- Results show large distance reduction across Jaipur, Mumbai, and Hyderabad

---

## 16. First Tasks for Member 2

Priority order:

1. Write the formal problem definition.
2. Define sets, parameters, and decision variables.
3. Choose the main objective function.
4. Write all constraints clearly.
5. Decide whether to present full VRP MIP or two-stage heuristic model.
6. Send confirmed assumptions to Member 3.
7. Prepare the mathematical model section for the final report.

