# Flash 低成本采集计划（约 ¥1 / 家）

目标：从下载招股书到写进 Excel，**空闲时段 DeepSeek Flash 约 ¥1/家**。  
不走 GUI 从头代劳，不走 Gemini/agy，不走 Pro。

权威单价：https://api-docs.deepseek.com/zh-cn/quick_start/pricing  
空闲 = 北京时间除「周一至周五 9:00–12:00、14:00–18:00」以外。

---

## 0. 为什么能压到 ¥1

| 步骤 | 谁跑 | 钱 |
|---|---|---|
| find / download / prepare / allot 准备 | `python3 prospectus_pipeline/run.py …` | ¥0 |
| 招股书抽取 + 复核 | DSH workflow，`deepseek-flash` | ≈ ¥0.73 |
| 配发抽取 + 复核 | 同上（Q1 已完成，以后新公司才跑） | ≈ ¥0.22 |
| validate / write | Python | ¥0 |

贵的路径（¥3–4）：在对话里让模型自己下 PDF、读全文、debug、重抽；或用 Gemini 上百轮；或选 Pro / 高峰。

---

## 1. 硬规则（每次触发前勾）

1. **模型只许 `deepseek-flash`**，不要 Pro，不要 Gemini，不要 `agy --model gemini-3.8-flash-high`。
2. **只在空闲时段跑抽取**：晚上、周末，或工作日 12:00–14:00、18:00 以后。
3. **下载和切片禁止进模型**。先跑 Python；聊天里不要 `read` 招股书 PDF / jsonl 全文（一家全文约 42 万 token）。
4. **并发 1–2 家**。不要 8 路；失败重跑会把一家打到 ¥2+。
5. **已有 JSON 且 `validate` 无 ERROR 的，禁止重抽。**
6. **packet 是唯一模型输入**（约 11 万 token）+ `tools_search.py` 片段。不要把全文贴进对话。
7. 写回前必须 `gate_pass=True`。WARNING_MISSING 可以，ERROR 回原文修，不要为配平改数。

---

## 2. 稳定触发：一条公司从零到 Excel

工作目录：

```bash
cd "/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News"
```

### A. 免费准备（Python，可白天跑）

```bash
# 新公司 / 新季度：定位 + 下载 + 切片
python3 prospectus_pipeline/run.py all --only 6809.HK

# 配发公告准备（Q1 已 38/38，新公司才需要）
python3 prospectus_pipeline/run.py allot --only 6809.HK
```

检查这三件存在再进抽取：

- `prospectus_pipeline/data/pdf/HKIPO-MB6809.pdf`
- `prospectus_pipeline/data/packets/HKIPO-MB6809.md`
- `prospectus_pipeline/data/allot/packets/HKIPO-MB6809.md`（若本家要配发字段）

### B. 花钱抽取（Flash，空闲时段，1 家或 2 家）

在 **本 GUI / DSH workflow** 里跑，不要新开闲聊：

1. 打开 `prospectus_pipeline/workflows/prospectus_extract.js`
2. `args.packets` 只放目标公司（从 `out/packets.json` 抄 `code/name/packet_path/out_path`）
3. `verify: true`（复核已含在 ¥1 预算里；不要再开第三轮人工闲聊核对）
4. 配发同理：`workflows/allot_extract.js`（Q1 已齐，跳过）

对模型的口头指令只许类似：

> 用 `deepseek-flash` 跑 `prospectus_extract.js`，只处理 6809.HK。不要读 PDF/jsonl 全文。抽完跑 validate。已有 JSON 的不要重抽。

### C. 写回 Excel（Python）

```bash
python3 prospectus_pipeline/run.py validate --only 6809.HK
python3 prospectus_pipeline/run.py write --fill-missing --only 6809.HK
```

配发字段：

```bash
python3 prospectus_pipeline/run.py validate --target allot --only 6809.HK
python3 prospectus_pipeline/run.py write --target allot --only 6809.HK
```

---

## 3. 当前 Q1 收尾（先做这个）

工作簿 `HKIPO-MB2026Q1.xlsx`，38 家：

| 状态 | 家数 | 公司 |
|---|---|---|
| 招股书已写回 | 23 | 其余 |
| JSON 有、表还没写 | **1** | **2706.HK** |
| PDF/packet 有、还没抽 | **14** | 见下 |
| 配发 JSON | 38/38 | 已齐 |

还没抽的 14 家（packet 已在，**不要重新 download**）：

```
6809.HK  0600.HK  0470.HK  2715.HK  2692.HK  3268.HK  1989.HK
2701.HK  3355.HK  2632.HK  1021.HK  2726.HK  6636.HK  0664.HK
```

### 今晚（空闲）建议批次

**批次 0 — 0 token：** 把 2706 写进表。

```bash
python3 prospectus_pipeline/run.py validate --only 2706.HK
python3 prospectus_pipeline/run.py write --fill-missing --only 2706.HK
```

**批次 1 — 2 家试跑，核对账单：** `6809.HK` `0600.HK`  
抽完看控制台用量，确认一家是否落在 **¥0.5–1.5**。偏差超过 2 倍就停，先查是不是读了全文或选了 Pro。

**批次 2–7：** 其余 12 家，每批 2 家，仍在空闲时段。

预算：14 × ¥0.73 ≈ **¥10**（只要招股书；配发已完成）。加上 2706 写回 = ¥0。全 Q1 招股书收尾大约一张午餐。

---

## 4. 以后每个新季度（从零）

样本进表（浅绿 A–K）之后，对每家或整批：

```text
白天   run.py all          → PDF + packet          ¥0
白天   run.py allot        → 配发 packet           ¥0
晚上   Flash 抽招股书+复核  → out/extracted/*.json  ≈¥0.73
晚上   Flash 抽配发+复核    → out/allot/extracted   ≈¥0.22
随时   validate + write    → Excel                 ¥0
```

整季 30–40 家：空闲大约 **¥30–40**；高峰会翻倍。不要用本聊天窗口当爬虫。

浅绿 A–K 继续用 `NLR20xx_Eng.xlsx` 合并 (a)/(b) 行，不走模型。  
深蓝行情（DD–DO）继续用现有 `tools_market.py` / HKMA CSV，不走模型。

---

## 5. 成本失控时怎么查

一家超过 **¥2**，按这个顺序查：

1. 模型是不是 Flash？（Pro 空闲就是 ¥4）
2. 是不是高峰？（Flash 高峰 ≈ ¥2）
3. 对话里有没有 `read` PDF 或 `*.jsonl`？
4. 同一家是不是抽了第二次？
5. 检索是不是上百轮？（上次 Gemini 一家 75–180 次 stream）

正常 Flash 一家：招股书大约十几到三十轮工具，不是上百轮。

---

## 6. 本周完成定义

- [ ] 2706.HK 写回
- [ ] 14 家 JSON 齐，`validate` 无 ERROR
- [ ] `write --fill-missing` 后 L 列 38/38 有值
- [ ] 抽 2 家后记下实际扣费，用来校正「¥1」是否仍成立
- [ ] 不再用 `run_agy_remaining.py` / Gemini 抽新公司

不做（本阶段）：AZ–CI 扩列、CL 基石解禁日。那些不在 ¥1 的 42 字段预算里，另开任务。
