# Member 3 Slides 中文精简布局规划

适用场景：小组 presentation 总时长为 **10 分钟讲解 + 5 分钟 Q&A**。Member 3 建议控制在 **3 分钟左右**，所以正式 slides 建议做 **4 页**。原来的第 5 页可以作为备用页或 Q&A 页，不一定正式讲。

核心原则：

- 每页只讲一个重点。
- 不放完整大表，只放最关键数字。
- 重点围绕：实验设置、方法选择、主结果、稳健性与管理意义。
- 方法名统一写成 `Balanced Geo + NN + 2-opt`。

## 推荐正式 4 页结构

| 页码 | 标题 | 核心作用 | 建议讲解时间 |
|---|---|---|---:|
| Slide 12 | Computational Experiment Setup | 说明实验对象和基本假设 | 25 秒 |
| Slide 13 | Routing Methods and Final Choice | 说明比较方法和为什么选最终方法 | 45 秒 |
| Slide 14 | Main Result: Jaipur Scenario | 展示主实验改善结果 | 70 秒 |
| Slide 15 | Robustness and Managerial Takeaway | 展示三城市结果和业务意义 | 50 秒 |

合计约 3 分钟。

## Slide 12: Computational Experiment Setup

推荐标题：

`Computational Experiment Setup`

推荐布局：

| 区域 | 内容 |
|---|---|
| 左侧 60% | 放 `outputs/figures/jaipur_customer_locations.png` |
| 右侧 40% | 放 4 条 setup bullets |

右侧文字：

- 3 city scenarios: Jaipur, Mumbai, Hyderabad
- 50 orders per city scenario
- 5 riders, 10 orders per rider
- Common depot and Haversine distance

讲稿重点：

Member 3 把清洗后的订单数据转成 routing experiment。每个城市 50 单、5 个 rider、每人容量 10 单，并假设从 common depot 出发和返回。

## Slide 13: Routing Methods and Final Choice

推荐标题：

`Routing Methods and Final Choice`

推荐布局：

| 区域 | 内容 |
|---|---|
| 上方 | 5 个方法的极简对比表 |
| 下方 | 一句话解释 final choice |

表格建议：

| Method | Role | Capacity |
|---|---|---|
| Original Order | Baseline | Yes |
| Random Assignment | Random baseline | Yes |
| Geographic Clustering | Spatial grouping | Not guaranteed |
| Geographic + NN | Spatial grouping + sequencing | Not guaranteed |
| Balanced Geo + NN + 2-opt | Final optimized method | Yes |

下方 key message：

`The final method is selected because it reduces distance while keeping exactly 10 orders per rider.`

讲稿重点：

K-means 方法有时距离更短，但可能把太多订单分给一个 rider，不符合容量约束。最终方法更适合作为 prescriptive solution，因为它同时考虑路线效率和 rider capacity。

## Slide 14: Main Result: Jaipur Scenario

推荐标题：

`Main Result: Jaipur Scenario`

推荐布局：

| 区域 | 内容 |
|---|---|
| 左侧 40% | 两个大数字 KPI |
| 右侧 60% | 放 optimized route 图，空间够再加 baseline route |
| 底部 | Original vs Final 的 2 行小表 |

KPI：

- `47.661%` distance reduction
- `472.537 km -> 247.324 km`

小表格：

| Method | Distance | Time |
|---|---:|---:|
| Original Order | 472.537 km | 1692.977 min |
| Balanced Geo + NN + 2-opt | 247.324 km | 871.263 min |

推荐图片：

- 首选：`outputs/figures/jaipur_optimized_route.png`
- 如果模板空间允许，再加：`outputs/figures/jaipur_baseline_route.png`

讲稿重点：

这是 Member 3 最重要的一页。优化后 Jaipur 总距离从 472.537 km 降到 247.324 km，减少 47.661%。这说明方法不是单纯描述数据，而是真的改变了订单分配和路线顺序。

## Slide 15: Robustness and Managerial Takeaway

推荐标题：

`Robustness Across Cities`

推荐布局：

| 区域 | 内容 |
|---|---|
| 左侧 60% | 放 `outputs/figures/distance_comparison.png` |
| 右侧 40% | 三城市 improvement 小表 + takeaway |

右侧表格：

| City | Improvement |
|---|---:|
| Jaipur | 47.661% |
| Mumbai | 61.802% |
| Hyderabad | 56.240% |

Takeaway：

`Grouping nearby customers and improving route sequences can reduce unnecessary travel while preserving rider capacity.`

讲稿重点：

同一套方法在三个城市都明显减少距离，说明结果不是只对 Jaipur 有效。管理意义是平台可以通过更合理的订单分组和配送顺序减少无效行驶，同时保持 workload fairness。

## 备用页：Capacity and Workload Balance

这页不建议放进正式 10 分钟主线，除非 Member 3 有 4 分钟以上。可以作为 Q&A 备用页。

推荐标题：

`Capacity Feasibility`

推荐内容：

| Rider | Orders | Distance |
|---:|---:|---:|
| 1 | 10 | 55.407 km |
| 2 | 10 | 44.946 km |
| 3 | 10 | 46.080 km |
| 4 | 10 | 45.100 km |
| 5 | 10 | 55.790 km |

配图：

- `outputs/figures/workload_comparison.png`

使用场景：

如果老师问为什么不用 `Geographic + Nearest Neighbor`，可以用这页解释：它可能距离更短，但不保证每个 rider 的订单数量满足容量限制；最终方法保证每人 10 单。

## 图片使用清单

| 图片 | 推荐页 | 用途 |
|---|---|---|
| `outputs/figures/jaipur_customer_locations.png` | Slide 12 | 实验点位和 depot |
| `outputs/figures/jaipur_optimized_route.png` | Slide 14 | 主结果路线图 |
| `outputs/figures/jaipur_baseline_route.png` | Slide 14 可选 | baseline 对比 |
| `outputs/figures/distance_comparison.png` | Slide 15 | 三城市稳健性 |
| `outputs/figures/workload_comparison.png` | 备用页 | capacity / workload Q&A |

## 3 分钟讲稿节奏

| 时间 | 内容 |
|---:|---|
| 0:00-0:25 | 介绍实验设置 |
| 0:25-1:10 | 介绍比较方法和最终选择 |
| 1:10-2:20 | 讲 Jaipur 主结果 |
| 2:20-3:00 | 讲 robustness 和 managerial takeaway |

## 最后检查

- 正式主线控制在 4 页。
- 不要把备用页内容塞进主线。
- Jaipur improvement 写成 `47.661%`。
- 三城市 improvement 分别是 `47.661%`、`61.802%`、`56.240%`。
- 每页文字不超过 4 个 bullet 或 1 个小表格。
