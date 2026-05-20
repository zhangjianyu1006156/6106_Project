# Member 2 Slide Outline: Optimization Model

## Slide 1: Optimization Problem

- Problem type: simplified capacitated vehicle routing problem
- Scenario: 50 food delivery orders in one city evening peak period
- Resources: 5 riders, maximum 10 orders per rider
- Decisions:
  - assign each order to one rider
  - decide each rider's delivery sequence
- Goal: reduce total delivery travel distance

## Slide 2: Key Assumptions

- One scenario contains one city and one operating period
- Common depot is the average restaurant location
- Each rider starts from and returns to the depot
- Each order is delivered exactly once
- Rider capacity is 10 orders
- Haversine distance approximates travel distance
- Traffic and weather are used for estimated travel-time evaluation

## Slide 3: Decision Variables

| Variable | Meaning |
|---|---|
| `x_ijk` | 1 if rider `k` travels from node `i` to node `j` |
| `y_ik` | 1 if order `i` is assigned to rider `k` |
| `u_ik` | route position variable used to eliminate subtours |

## Slide 4: Objective and Constraints

- Objective:
  - minimize total distance across all riders
- Main constraints:
  - every order assigned exactly once
  - each rider serves at most 10 orders
  - assigned customer nodes must be entered and left
  - every rider departs from and returns to the depot
  - no self-loops
  - subtour elimination using MTZ constraints

## Slide 5: Link to Implementation

- Formal model: simplified CVRP
- Practical implementation:
  - balanced geographic assignment
  - nearest-neighbor route construction
  - 2-opt route improvement
- Reason:
  - keeps exactly 10 orders per rider
  - is computationally feasible
  - preserves the assignment and routing logic of the CVRP

## Slide 6: Main Result Connection

These results are from Member 3's computational experiment and are shown here only to connect the model with implementation outcomes.

| Jaipur Method | Total Distance (km) | Improvement |
|---|---:|---:|
| Original Order | 472.537 | 0.000% |
| Balanced Geo + NN + 2-opt | 247.324 | 47.661% |

Key message:

The model shows why optimized assignment and route sequencing should reduce delivery distance, while Member 3's computational experiment reports the actual numerical improvement.

