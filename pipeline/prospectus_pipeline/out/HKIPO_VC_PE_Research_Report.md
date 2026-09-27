# 香港主板 2026 Q1 IPO Pre-IPO VC/PE 学术研究细分维度全景报告

> **计量数据源**：`HKIPO-MB2026Q1.xlsx` (Sheet: `NLR`, 列 53~63)
> **样本范围**：2026 年第一季度香港联交所主板新上市企业全集 (N = 38)
> **理论支撑**：Lowry, Michaely, & Volkova (2017) Intermediary Governance; Gompers (1996) Grandstanding; Megginson & Weiss (1991) Certification.

---

## 一、核心实证统计量总览 (Executive Summary)

| 维度指标 | 变量字段 | 覆盖家数 | 样本占比 (%) | 经典文献与实证用途 |
| :--- | :--- | :---: | :---: | :--- |
| **Pre-IPO 机构总覆盖** | `col_BA` | 28 / 38 | 73.7% | 传统基础哑变量（Base VC/PE Dummy） |
| **早期风险投资 (VC)** | `col_vc_backed` | 23 / 38 | 60.5% | 检验早期创业孵化与高成长筛选机制 |
| **私募股权基金 (PE)** | `col_pe_backed` | 11 / 38 | 28.9% | 检验成熟期/并购重组基金的资本赋能与交叉融资 |
| **产业资本/企业创投 (CVC)** | `col_cvc_backed` | 16 / 38 | 42.1% | 检验战略协同、生态绑定与上下游订单支持效应 |
| **国资/产业引导基金 (Gov)** | `col_gov_backed` | 12 / 38 | 31.6% | 检验地方政府招商、硬科技政策支持与制度背书 |
| **顶级机构认证 (Top-tier)** | `col_top_tier_vc` | 22 / 38 | 57.9% | 检验 Megginson & Weiss (1991) 声誉认证假说 |
| **董事会席位派驻 (Board Seat)** | `col_vc_board_seat` | 19 / 38 | 50.0% | 检验 Sørensen (2007) 积极监控与公司治理赋能 |
| **上市前机构平均持股比例** | `col_vc_pe_stake` | 均值 33.8% | - | 衡量投资人股权集中度与信息不对称折价 |
| **平均持有投资年限 (久期)** | `col_holding_duration` | 均值 7.30 年 | - | 检验 Gompers (1996) 基金急迫退出与立名造势假说 |

---

## 二、38 家公司 10 大细分维度完整对账清单

| 股票代码 | 公司名称 (中文) | VC/PE | VC | PE | CVC | 国资 | 顶级 | 董事席位 | 最早轮次 | 持有年限 | 机构持股(%) | 核心机构投资者清单 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `6082.HK` | 上海壁仞科技股份有限公司 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | Series Pre-A | 6.04 | 68.5% | Qiming Venture Partners; Country Garden VC; Sky9 Capital; Songhe Capital; Zhuhai Gree; Walden International; Shanghai SOE Reform Fund |
| `2513.HK` | 北京智谱华章科技股份有限公司 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | Series Angel | 4.58 | 65.2% | Qiming Venture Partners; HongShan; Legend Capital; Meituan; Alibaba; Tencent; Xiaomi; Prosperity7; Beijing AI Fund |
| `9903.HK` | 上海天数智芯半导体股份有限公司 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | Series A | 9.42 | 58.4% | Princeville Global; HongShan; Shanghai Lianhe Investment; Cathay Capital; Greater Bay Area Fund |
| `2675.HK` | 深圳市精锋医疗科技股份有限公司 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | Series Angel | 8.16 | 54.8% | LYFE Capital; Legend Star; Boyu Capital; Sequoia China; OrbiMed; Temasek |
| `0100.HK` | NA | 1 | 1 | 0 | 1 | 0 | 1 | 1 | Series Angel | 4.08 | 45.3% | Alisoft China (Alibaba); miHoYo; IDG Capital; Tencent; Future Capital |
| `6938.HK` | 苏州瑞博生物技术股份有限公司 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | Series A | 10.12 | 48.2% | Panlin Capital; Legend Capital; CITIC Securities Investment; CS Capital; Guoshun Fund |
| `3636.HK` | 云南金浔资源股份有限公司 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | Pre-IPO | 3.02 | 8.2% | Chuanghe Xincai (CITIC Goldstone) |
| `0501.HK` | 豪威集成电路（集团）股份有限公司 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | None | 0.00 | 0.0% | NA |
| `3986.HK` | 兆易创新科技集团股份有限公司 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | Series A | 12.50 | 11.9% | Tus Zhonghai Venture Capital; Insight Power; InfoGrid |
| `1641.HK` | 红星冷链(湖南)股份有限公司 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | None | 0.00 | 0.0% | NA |
| `9611.HK` | 上海龙旗科技股份有限公司 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | Series A | 10.20 | 9.1% | Suzhou Industrial Park Shunwei Technology Venture Investment (Shunwei Capital) |
| `1768.HK` | 湖南鸣鸣很忙商业连锁股份有限公司 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | Series A | 4.67 | 26.5% | HongShan; Gaocheng Capital; Black Ant Capital |
| `9980.HK` | 东鹏饮料（集团）股份有限公司 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | None | 0.00 | 0.0% | NA |
| `2768.HK` | 青岛国恩科技股份有限公司 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | None | 0.00 | 0.0% | NA |
| `2677.HK` | 卓正医疗控股有限公司 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | Series A | 11.75 | 52.1% | Matrix Partners; Waterwood DHC; Tiantu Capital; Tencent |
| `2714.HK` | 牧原食品股份有限公司 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | Pre-IPO | 6.42 | 3.5% | Henan Hongbao Group; Beixin Ruifeng Fund |
| `3200.HK` | 深圳市大族数控科技股份有限公司 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | None | 0.00 | 0.0% | NA |
| `6809.HK` | 澜起科技股份有限公司 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | Strategic Round | 9.50 | 10.0% | Intel Capital |
| `0600.HK` | 爱芯元智半导体股份有限公司 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | Series Angel | 6.25 | 56.7% | Qiming Venture Partners; Meituan; Tencent; GGV Capital; Walden International; Boyuan Capital |
| `2720.HK` | 乐欣户外国际有限公司 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | None | 0.00 | 0.0% | NA |
| `0470.HK` | 无锡先导智能装备股份有限公司 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | None | 0.00 | 0.0% | NA |
| `2706.HK` | 北京海致科技集团股份有限公司 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | Series A-1 | 11.42 | 42.3% | Legend Capital; IDG Capital; Baidu; CICC Alpha |
| `9981.HK` | 深圳市沃尔核材股份有限公司 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | Pre-IPO | 3.25 | 2.4% | Xuanyuan Private Fund |
| `2649.HK` | 苏州优乐赛共享服务股份有限公司 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | Series Pre-A | 5.33 | 18.5% | Suzhou Industrial Park Fund; Green Pine Capital; Hengxu Capital |
| `2715.HK` | 南京埃斯顿自动化股份有限公司 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | None | 0.00 | 0.0% | NA |
| `2692.HK` | 深圳市兆威机电股份有限公司 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | None | 0.00 | 0.0% | NA |
| `3268.HK` | 美格智能技术股份有限公司 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | Pre-IPO | 4.50 | 5.2% | Fenghuangshan Investment |
| `1989.HK` | 广州广合科技股份有限公司 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | Pre-IPO | 4.00 | 4.1% | Shenzhen Talent Innovation Venture Fund No. 2 |
| `2701.HK` | 国民技术股份有限公司 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | None | 0.00 | 0.0% | NA |
| `3355.HK` | 深圳市飞速创新技术股份有限公司 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | Series Pre-A | 7.42 | 22.6% | Fortune Venture Capital (达晨财智); Harvest Capital; Shenzhen Chiyu |
| `2632.HK` | 江苏泽景汽车电子股份有限公司 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | Series A | 8.64 | 38.4% | Shunwei Capital; Cathay Capital; SAIC Capital; Baidu Ventures |
| `2729.HK` | 浙江凯乐士科技集团股份有限公司 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | Series A | 7.50 | 32.1% | ByteDance; Legend Star; Infore Capital |
| `1021.HK` | 广东华沿机器人股份有限公司 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | Series A | 6.33 | 60.6% | Foxconn (Industrial Fulian); Guangdong Semiconductor Fund; Yuecai Venture Capital |
| `2526.HK` | 杭州德适生物科技股份有限公司 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | Series A | 7.42 | 44.5% | Lilly Asia Ventures; CDH Investments; Hangzhou High-Tech Venture Fund |
| `2726.HK` | 瀚天天成电子科技（厦门）股份有限公司 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | Series A | 6.50 | 36.8% | Huawei Hubble; BYD; SAIC; Guangdong Semiconductor Fund |
| `6636.HK` | 山东极视角科技股份有限公司 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | Series Angel | 9.33 | 41.2% | Qualcomm Ventures; China Resources Capital; Shandong Development Fund |
| `0664.HK` | 杭州铜师傅文创（集团）股份有限公司 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | Series A | 8.50 | 29.4% | Shunwei Capital; Xiaomi; Tiantu Capital |
| `3625.HK` | 上海傅里叶半导体股份有限公司 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | Pre-Series A | 7.50 | 51.3% | Tencent; Didi; NIO Capital; NavInfo; Hefei High-Tech Fund |