> [!WARNING]
> **已废弃归档文档**：现行 schema 已统一为 **60 个字段**。请参阅 schema/fields.json 与 CODE_REVIEW_2026-09-13.md。

> [!WARNING]
> **已废弃归档文档**：现行 schema 已统一为 **60 个字段**。请参阅  与 。

# 交接：浅蓝 42 字段（招股书）

工作目录：
`/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News`

目标工作簿：`HKIPO-MB2026Q1.xlsx`（sheet `NLR`，38 家，行 2–39）

## 现在做到哪

| 块 | 列 | 状态 |
|---|---|---|
| 浅绿 | A:K | ✅ 38/38 已写回 |
| 深蓝配发 | CK, CM–DC（含 CX） | ✅ 38/38 已写回 |
| 深蓝行情/规则 | DD–DO（除 CJ/CL/DP） | ✅ 38/38 已写回 |
| **浅蓝招股书 42 字段** | L–AY + CJ + DP | **JSON 16/38，工作簿 0/38（还没 write）** |

已抽 JSON（闸门 errors=0，可写）：
`0100, 0501, 1641, 1768, 2513, 2526, 2649, 2675, 2720, 2729, 3200, 3625, 3636, 6082, 6938, 9903`

**还剩 22 家**（`out/extracted/HKIPO-MB{code}.json` 不存在）：
```
2677 9980 3986 9611 2768 2714 6809 0600
9981 2706 2715 0470 1989 3268 2701 3355
2632 2692 1021 2726 0664 6636
```

packet / 写盘路径在 `prospectus_pipeline/out/packets.json`。
抽取提示词模板：`prospectus_pipeline/prompts/agy_extract.md`。

## 你要做的（按这个顺序）

### 1. 用 agy + Gemini 3.8 Flash High 抽剩下 22 家

每家一条：

```bash
cd "/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News"
agy --print-timeout 45m \
    --dangerously-skip-permissions \
    --add-dir "$(pwd)" \
    --model gemini-3.8-flash-high \
    --log-file "prospectus_pipeline/out/agy_logs/{CODE4}.agy.log" \
    -p="$(cat prospectus_pipeline/out/agy_logs/{CODE4}.prompt.md)"
```

`{CODE4}` = 四位数字（如 `2677`）。prompt 用模板把 `{{CODE}} {{NAME}} {{PACKET}} {{OUT}}` 替换掉。

要求：
- 输出 JSON 必须写到 `prospectus_pipeline/out/extracted/HKIPO-MB{CODE4}.json`
- 然后 `python3 prospectus_pipeline/run.py validate --only {CODE}.HK` 直到不是 ERROR（WARNING_MISSING 可以）
- **不要并行 8 个**：上次 8 并发只连 API、不写文件。建议 **1–2 个并发**
- token / quota 用尽：日志里出现 `quota` / `RESOURCE_EXHAUSTED` / `rate limit` → **睡 5 小时再跑**，不要换模型

也可直接跑：
```bash
python3 prospectus_pipeline/run_agy_remaining.py
```

### 2. 全量校验

```bash
python3 prospectus_pipeline/run.py validate
```

`gate_pass=True` 才写回。WARNING_MISSING 可以（无基石的 CJ=NA 等）。ERROR 必须回原文修。

闸门已认 **全文 jsonl 页**（不只 packet 切片）。佣金等可以引 packet 里没有的页，但 quote 必须是该页连续原文。

### 3. 写回工作簿

```bash
python3 prospectus_pipeline/run.py write --fill-missing
```

只改浅蓝 42 列的 **value**，不改 font/fill/number_format。写前自动备份。

## 字段契约（42）

`schema/fields.json`：L–S 股本，T–U 价格，V–AN 三年财务，AO–AQ 承销/绿鞋，AR–AS 业务/上市途径，AT–AY 附加财务，**CJ 基石名单**，**DP 中文名**。

硬规则：金额基本单位；百分比小数；确认的零填 0；AV=经营现金流净额；AY=资本化开发**当期新增**；AO=AP 若按全球发售披露；AQ 不默认 15%；无基石 CJ=`NA`。

## 不要动

- 浅绿 A:K、深蓝已填列（CK, CM–DC, DD–DO, DF/DG）
- 老师模板格式 / 冻结窗格 D2
- 不要为配平改招股书数字
