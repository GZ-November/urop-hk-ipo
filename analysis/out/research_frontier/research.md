# 2026 研究前沿：探索性实证

设计见 docs/RESEARCH_DESIGN_2026.md；不作因果或预注册声明。

## 零售申请资金与配售资金的收益

共同有效样本 N=113，上市月份 G=9；2,000 次按上市月重抽样，seed=20260930。少月份区间仅作描述，不能消除市场冲击或信息类型选择。

| Measure | Estimate | Cluster-bootstrap lower | Cluster-bootstrap upper |
|---|---|---|---|
| mean_ir | 53.153% | 28.904% | 77.053% |
| allocation_weighted_ir | 1.165% | -2.239% | 8.574% |
| application_return | 0.020% | -0.051% | 0.098% |

表中收益以百分比显示，CSV保留小数。申请 HK$10,000 的平均毛收益为 HK$1.97。这是发行人层面平均配售率下的等额申请情景，不能当作一手中奖概率或实际账户收益。融资情景详见 retail_cost_scenarios.csv；费率、借款比例及2天占款是情景参数，未从真实借贷记录估计。未补入股票交易、申购交易费或机会成本；不能称完整净投资回报。
## 基石份额：关联、少聚类推断与遗漏变量

| Specification | n | g | b | hc3_se | hc3_p | restricted_wild_p | rv_to_zero_equal_strength |
|---|---|---|---|---|---|---|---|
| Ex-ante controls | 106 | 9 | -0.309 | 0.410 | 0.451 | 0.191 | 0.096 |
| + final demand (endogenous) | 106 | 9 | -0.455 | 0.365 | 0.213 | 0.082 | 0.144 |

两个规格共用同一发行人样本。焦点变化0.10对应 log(1+IR) 变化0.10×b，exp(0.10×b)-1是价格比(1+IR)的比例变化，不是 IR 百分点。wild 检验沿用已验证的 restricted bootstrap-t，枚举 G 个上市月的全部 Rademacher 符号组合；HC3 的两个焦点检验独立作为 Holm family，聚类 p 不混用于星号。

RV/partial-R² 是点估计对未观测混杂的代数诊断，使用普通 OLS 的残差尺度，不是聚类显著性或因果置信区间。最终需求和基石份额均内生；加入需求可能条件化于通道或碰撞点。任意一个显著结果都不能修复识别。

事件与六日历月窗口覆盖见 event_readiness.csv；机制共同支持见 mechanism_support.csv。缺证据和未成熟分别保留，不填估计。
