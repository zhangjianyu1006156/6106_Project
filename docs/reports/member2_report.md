# Member 2 Report: Mathematical Model and Optimization Formulation

## 1. Purpose of the Optimization Model

This project studies a prescriptive analytics problem for food delivery operations. Given a set of delivery orders in one city during the evening peak period, the platform must decide which rider should serve each order and in what sequence each rider should visit the assigned customer locations.

The decision problem has two connected components:

1. order assignment: assign every order to one rider;
2. route sequencing: determine each rider's delivery route.

To represent this problem clearly, we formulate it as a simplified capacitated vehicle routing problem (CVRP). Each customer delivery location is treated as a customer node. A common depot is defined as the average restaurant location in the selected scenario, and each rider starts from and returns to this depot. This simplifies the real food delivery setting into a standard routing model while retaining the project's core operational decision: how to assign and sequence orders to reduce total travel distance.

The main objective is to minimize total Haversine travel distance. Traffic and weather are included as travel-time multipliers for performance evaluation, but they are not used as the primary objective in the base optimization model. This keeps the model interpretable and aligned with the computational experiment completed by Member 3.

## 2. Scenario and Data Inputs

The formulation is designed for the processed datasets prepared by Member 1.

| Scenario | City | File | Orders | Riders | Capacity |
|---|---|---|---:|---:|---:|
| Main | Jaipur | `data/processed/main_optimization_jaipur.csv` | 50 | 5 | 10 |
| Robustness 1 | Mumbai | `data/processed/robustness_mumbai.csv` | 50 | 5 | 10 |
| Robustness 2 | Hyderabad | `data/processed/robustness_hyderabad.csv` | 50 | 5 | 10 |

The key input fields are restaurant coordinates, delivery coordinates, order time, traffic density, weather condition, and actual delivery time. Restaurant coordinates are used to define the common depot, while delivery coordinates define customer nodes. Actual delivery time is used only as reference information and is not treated as a decision variable.

## 3. Modeling Assumptions

The model uses the following assumptions:

1. Each scenario contains orders from one real city and one evening peak operating period.
2. Each order must be served exactly once.
3. There are 5 available riders in each scenario.
4. Each rider can serve at most 10 orders.
5. Since each scenario has 50 orders and 5 riders, the capacity setting implies that each rider serves exactly 10 orders in the final balanced solution.
6. A common depot is used, defined by the average restaurant latitude and longitude in the scenario.
7. Each rider starts from and returns to the depot.
8. Customer nodes are represented by delivery locations.
9. Travel distance is approximated using Haversine distance.
10. The base formulation does not include hard time windows.
11. Traffic and weather affect estimated travel time, but distance remains the main optimization objective.
12. The model is a planning-level simplification rather than a full real-time dispatch system with separate restaurant pickups.

The common depot assumption is the most important simplification. In reality, different orders may originate from different restaurants. For this project, the average restaurant location is used to create a single dispatch reference point, making the problem suitable for a standard CVRP formulation and a consistent computational comparison.

## 4. Sets and Indices

| Symbol | Meaning |
|---|---|
| `N` | Set of customer orders, indexed by `i` and `j` |
| `K` | Set of riders, indexed by `k` |
| `V` | Set of all nodes, including the depot and customers |
| `0` | Common depot node |

For the main 50-order scenario:

```text
N = {1, 2, ..., 50}
K = {1, 2, 3, 4, 5}
V = {0} union N
```

## 5. Parameters

| Parameter | Meaning |
|---|---|
| `d_ij` | Haversine distance from node `i` to node `j`, in kilometers |
| `t_ij` | Estimated travel time from node `i` to node `j`, in minutes |
| `Q` | Rider capacity, set to 10 orders |
| `a_i` | Demand of order `i`; in this project, `a_i = 1` |
| `s` | Average rider speed in kilometers per hour |
| `phi_i` | Traffic multiplier associated with order `i` |
| `psi_i` | Weather multiplier associated with order `i` |

The distance matrix is calculated from latitude and longitude coordinates using the Haversine formula. Estimated travel time can be calculated as:

```text
t_ij = (d_ij / s) * 60 * phi_j * psi_j
```

where `phi_j` and `psi_j` represent the traffic and weather conditions for the destination order `j`. The factor 60 converts hours to minutes.

## 6. Decision Variables

The formal CVRP model uses the following decision variables:

| Variable | Type | Meaning |
|---|---|---|
| `x_ijk` | Binary | 1 if rider `k` travels directly from node `i` to node `j`; 0 otherwise |
| `y_ik` | Binary | 1 if customer order `i` is assigned to rider `k`; 0 otherwise |
| `u_ik` | Continuous or integer | Route position variable for customer `i` on rider `k` route |

The domains are:

```text
x_ijk in {0, 1}, for all i, j in V, i != j, k in K
y_ik in {0, 1}, for all i in N, k in K
u_ik >= 0, for all i in N, k in K
```

The variable `u_ik` is used only for subtour elimination and route ordering.

## 7. Objective Function

The base model minimizes total travel distance across all riders:

```text
minimize Z = sum_{k in K} sum_{i in V} sum_{j in V, j != i} d_ij x_ijk
```

This is the selected objective for the final project because distance is directly observable from the routing geometry, stable across scenarios, and consistent with Member 3's computational evaluation.

A time-based extension can be written by replacing `d_ij` with `t_ij`:

```text
minimize Z_time = sum_{k in K} sum_{i in V} sum_{j in V, j != i} t_ij x_ijk
```

In the final analysis, distance minimization is used as the optimization objective, while estimated travel time is reported as a secondary performance measure.

## 8. Constraints

### 8.1 Order Assignment

Each customer order must be assigned to exactly one rider:

```text
sum_{k in K} y_ik = 1, for all i in N
```

### 8.2 Rider Capacity

Each rider can serve at most `Q` orders:

```text
sum_{i in N} a_i y_ik <= Q, for all k in K
```

Because `a_i = 1`, `Q = 10`, `|N| = 50`, and `|K| = 5`, the final feasible solution assigns exactly 10 orders to each rider.

### 8.3 Flow Out of Assigned Customers

If customer `i` is assigned to rider `k`, rider `k` must leave customer node `i` exactly once:

```text
sum_{j in V, j != i} x_ijk = y_ik, for all i in N, k in K
```

### 8.4 Flow Into Assigned Customers

If customer `i` is assigned to rider `k`, rider `k` must enter customer node `i` exactly once:

```text
sum_{j in V, j != i} x_jik = y_ik, for all i in N, k in K
```

Together, Constraints 8.3 and 8.4 link the assignment decision with the routing decision.

### 8.5 Depot Departure

Each rider starts from the depot:

```text
sum_{j in N} x_0jk = 1, for all k in K
```

### 8.6 Depot Return

Each rider returns to the depot:

```text
sum_{i in N} x_i0k = 1, for all k in K
```

### 8.7 No Self-Loops

A rider cannot travel from a node to itself:

```text
x_iik = 0, for all i in V, k in K
```

Equivalently, self-loop variables can be excluded from the model.

### 8.8 Route Position Bounds

The route position variable is active only when customer `i` is assigned to rider `k`:

```text
y_ik <= u_ik <= Q y_ik, for all i in N, k in K
```

If `y_ik = 0`, then `u_ik = 0`. If `y_ik = 1`, then `u_ik` is between 1 and `Q`.

### 8.9 Subtour Elimination

MTZ subtour elimination constraints prevent disconnected cycles among customer nodes:

```text
u_ik - u_jk + Q x_ijk <= Q - 1 + Q(2 - y_ik - y_jk),
for all i, j in N, i != j, k in K
```

When both customers `i` and `j` are assigned to rider `k`, this becomes the standard MTZ constraint. If either customer is not assigned to rider `k`, the additional term relaxes the constraint. These constraints ensure that the selected arcs for each rider form one connected route that starts at the depot, visits assigned customers, and returns to the depot.

## 9. Practical Computational Approach

The CVRP formulation provides the formal mathematical model. However, solving a 50-customer, 5-rider mixed-integer routing problem can be computationally expensive for a course project, especially when robustness testing is repeated across multiple cities.

For implementation, the project therefore uses a two-stage heuristic that follows the same assignment-and-routing logic:

1. Balanced geographic assignment: assign nearby customers to riders while keeping exactly 10 orders per rider.
2. Route sequencing: for each rider, build an initial route using nearest neighbor and improve it using 2-opt.

This implemented method preserves the key constraints of the formal model:

- every order is served exactly once;
- every rider receives 10 orders;
- routes start from and return to the depot;
- customers are assigned using geographic structure;
- route sequence is improved after assignment.

Thus, the full CVRP is used as the theoretical optimization model, while the balanced geographic assignment plus nearest-neighbor and 2-opt heuristic is used as the practical solution method.

## 10. Connection to Computational Results

Member 3's computational experiment evaluates the proposed assignment and routing logic against several baselines. For the main Jaipur scenario, the optimized heuristic substantially reduces total distance and estimated travel time:

| Method | Total Distance (km) | Estimated Time (min) | Improvement vs Original |
|---|---:|---:|---:|
| Original Order | 472.537 | 1692.977 | 0.000% |
| Balanced Geo + NN + 2-opt | 247.324 | 871.263 | 47.661% |

The same approach is tested on Mumbai and Hyderabad as robustness scenarios:

| Scenario | Original Distance (km) | Optimized Distance (km) | Improvement |
|---|---:|---:|---:|
| Jaipur | 472.537 | 247.324 | 47.661% |
| Mumbai | 768.190 | 293.432 | 61.802% |
| Hyderabad | 571.753 | 250.198 | 56.240% |

These results show that the model-based assignment and routing approach is effective across different city layouts. Even under simplified assumptions, it reduces unnecessary travel distance while maintaining balanced rider workload.

## 11. Final Model Decision

The final project should present the following model decision:

1. Use a simplified CVRP as the formal mathematical formulation.
2. Use total Haversine distance as the main objective.
3. Use a common depot based on average restaurant location.
4. Require every rider to start from and return to the depot.
5. Set rider capacity to `Q = 10`.
6. Use traffic and weather multipliers for estimated travel-time evaluation.
7. Use balanced geographic assignment plus nearest-neighbor and 2-opt as the implemented optimization method.

This combination gives the project a rigorous optimization foundation while keeping the computational solution feasible, explainable, and consistent with the available data.
