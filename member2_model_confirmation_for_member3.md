# Member 2 Model Confirmation for Member 3

The final model settings are confirmed as follows.

| Question | Confirmed Setting |
|---|---|
| Common depot? | Yes. Use one common depot defined as the average restaurant location in each scenario. |
| Return to depot? | Yes. Each rider starts from and returns to the depot. |
| Main objective? | Minimize total Haversine travel distance. |
| Rider capacity? | Maximum 10 orders per rider. Since there are 50 orders and 5 riders, each rider receives exactly 10 orders in the final balanced solution. |
| Traffic/weather? | Include as estimated travel-time multipliers for reporting and interpretation, not as the base optimization objective. |
| Final model type? | Present a simplified capacitated VRP formulation in the report. Use the balanced geographic assignment + nearest neighbor + 2-opt heuristic as the computational implementation. |
| Robustness scenarios? | Apply the same method independently to Jaipur, Mumbai, and Hyderabad. |

Recommended final wording:

```text
Member 2 confirms that the project will use a simplified capacitated vehicle routing problem as the formal optimization model. The base objective is total distance minimization. Each scenario has 50 orders, 5 riders, and rider capacity 10. A common depot is defined as the average restaurant location, and each rider returns to the depot after completing deliveries. Traffic and weather are included in estimated travel-time evaluation. For implementation, Member 3's balanced geographic assignment plus nearest-neighbor and 2-opt method is accepted as the practical optimized solution.
```

