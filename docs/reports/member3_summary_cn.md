# Member 3 中文简短报告

## 1. Member 3 负责什么

Member 3 主要负责项目中的计算实验部分，也就是把 Member 1 清洗好的订单数据和 Member 2 确认的优化模型思路，转成可以运行的 Python 实验。重点任务包括：构建路线距离、设置配送员分配规则、比较不同 routing 方法、生成结果表格和路线图，并检验方法在不同城市上的稳健性。

## 2. 使用的数据和基本假设

实验使用三个城市场景：

| 场景 | 城市 | 订单数 | 配送员数 | 每人容量 |
|---|---|---:|---:|---:|
| 主实验 | Jaipur | 50 | 5 | 10 |
| 稳健性测试 1 | Mumbai | 50 | 5 | 10 |
| 稳健性测试 2 | Hyderabad | 50 | 5 | 10 |

每个场景都假设有一个共同 depot，这个 depot 用该城市订单中的平均餐厅位置表示。每个配送员从 depot 出发，完成分配到的订单后再回到 depot。距离使用 Haversine distance 近似计算，也就是根据经纬度估算直线地理距离。

## 3. 比较了哪些方法

Member 3 比较了五种方法：

| 方法 | 含义 | 是否满足每人 10 单容量 |
|---|---|---|
| Original Order | 按原始订单时间顺序分配和配送 | 是 |
| Random Assignment | 随机分配订单 | 是 |
| Geographic Clustering | 用 K-means 按地理位置聚类 | 不保证 |
| Geographic + Nearest Neighbor | K-means 分配后，用最近邻安排路线顺序 | 不保证 |
| Balanced Geo + NN + 2-opt | 平衡地理分配 + 最近邻路线 + 2-opt 改进 | 是 |

最终选择的是 `Balanced Geo + NN + 2-opt`。原因是它不一定永远得到最短距离，但它能保证 5 个配送员每人刚好 10 单，更符合项目里的 capacitated vehicle routing problem 设定。

## 4. 最终方法怎么做

最终方法先根据客户相对 depot 的角度和距离进行排序，把地理上相近的客户尽量放在一起，同时平均分成 5 组，每组 10 单。然后每个配送员内部先用 nearest neighbor 方法生成一条初始路线，再用 2-opt 方法减少路线中的低效交叉，从而进一步缩短总距离。

简单理解：先把订单公平地、按地理位置分给配送员，再优化每个配送员自己的送餐顺序。

## 5. 主要结果

在主实验 Jaipur 中，原始方法总距离是 472.537 km，最终优化方法总距离是 247.324 km，距离减少 47.661%。估计总配送时间也从 1692.977 分钟下降到 871.263 分钟。

| 城市 | 原始距离 km | 优化后距离 km | 改善比例 |
|---|---:|---:|---:|
| Jaipur | 472.537 | 247.324 | 47.661% |
| Mumbai | 768.190 | 293.432 | 61.802% |
| Hyderabad | 571.753 | 250.198 | 56.240% |

这说明该方法不只在 Jaipur 有效，在 Mumbai 和 Hyderabad 的稳健性测试中也能明显减少配送距离。

## 6. 生成了哪些产物

Member 3 已经生成了以下主要文件：

- 代码工具函数：`src/member3_utils.py`
- 一键运行脚本：`scripts/member3_run_experiment.py`
- Notebook 版本：`notebooks/member3_computational_experiment.ipynb`
- 英文报告：`docs/reports/member3_report.md`
- 结果表格：`outputs/tables/member3_results_summary.csv`
- 路线与对比图片：`outputs/figures/`
- 展示提纲：`docs/slides/member3_slide_outline.md`

其中 `scripts/member3_run_experiment.py` 是最重要的复现入口。运行后会重新生成结果表格和图片。

## 7. 可以怎么向老师解释

Member 3 的工作是把理论模型落地成可运行的 prescriptive analytics 实验。它不是只描述现有订单，而是主动改变订单分配和配送顺序，比较优化前后的路线距离、配送时间和工作量平衡。最终方法在保持每个配送员 10 单的约束下，大幅减少了总配送距离，因此可以作为项目中的实际推荐方案。

需要注意的是，当前路线距离是基于经纬度的直线距离，不是真实道路距离；depot 也是用平均餐厅位置近似得到。因此结果适合作为规划层面的优化证据，而不是实时地图导航方案。
