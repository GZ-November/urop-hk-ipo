# 一句话采集港股 IPO · Quickstart

只要告诉 agent 一个时间段，它就会完成整套采集：拆成季度、安装环境、采集主板和 GEM、
逐家抽取招股书和配发结果、独立复核、写入 Excel、审计并打包成 ZIP。

[English version below](#english)

## 你需要什么

- 一个**能运行终端命令、能联网、支持子代理（subagent）**的 agent：推荐 Claude Code，Codex CLI 也可以。
  网页聊天版 agent 不能执行这个流程。独立复核需要子代理；没有子代理时，数据会停在“待复核”，不会写进工作簿。
- Git 和 Python 3.9+。macOS 自带的 `python3` 即可，项目用的 Python 3.12 会自动安装。
- Windows 请使用 WSL。

## 第 1 步：安装（只做一次）

```bash
git clone https://github.com/GZ-November/urop-hk-ipo.git
cd urop-hk-ipo
python3 tools/bootstrap.py
```

这一步装好锁定版本的依赖，并把采集 skill（`hk-ipo-collect`）装进这个目录：
在这里打开 Claude Code 或 Codex 就能直接用。想在**任何目录**都能用：

```bash
python3 tools/bootstrap.py --skills both
```

也可以跳过安装：把仓库链接和时间段一起发给 agent，它会自己 clone、安装。

## 第 2 步：告诉 agent 时间段

在仓库目录里打开 agent（`claude` 或 `codex`），说一句话就行：

> 收集 2025 年第四季度的港股 IPO

Claude Code 里也可以直接输入 `/hk-ipo-collect 2025Q4`。

| 你可以这样说 | agent 理解为 |
|---|---|
| 收集 2025 年第四季度的港股 IPO | 2025-10-01 至 2025-12-31，主板 + GEM |
| 收集 2025 年下半年的主板 IPO | 2025-07-01 至 2025-12-31，只要主板 |
| 采集 2024 年全年的新股 | 2024 全年，拆成 4 个季度 |
| 收集 2024 年 7 月到 2025 年 6 月的港股 IPO | 跨年区间，按季度依次采集 |
| 继续上次的港股 IPO 采集 | 从上次停下的地方接着做 |

想写得更具体（指定板块、观察截止日、是否重采已有数据），用
[采集请求模板](COLLECTION_REQUEST_TEMPLATE.md)。

## 第 3 步：等结果

agent 会先给你看计划，然后一直做到交付：

1. **计划**：`python3 run.py plan 2025Q4` 把时间段拆成“板块 × 季度”的任务，标出仓库里已有的数据（直接复用）。
2. **安装检查**：依赖、网络、测试。
3. **采集**：从港交所官方新上市报告确定发行人，下载招股书和配发结果公告。
4. **抽取 + 独立复核**：每家公司一个抽取子代理，再由另一个子代理对照原文逐项复核。每个数值都带页码和原文引用。
5. **写入和审计**：只有通过复核的数据才写进 Excel，然后审计和交叉检查。
6. **交付**：`deliverables/` 下的一个 ZIP，加一份报告：各季度公司数、上市日期、缺失字段、待复核项和数据源限制。

**时间预期**：近年一个季度约 15–45 家主板公司，抽取和复核最耗时，可能要几个小时。
中途断了也没关系，下次说“继续上次的港股 IPO 采集”就会从进度记录接着做。

**ZIP 里有什么**：每个季度的 Excel、clean CSV、字段字典（codebook）、证据和审计报告、
`START_HERE.html`（先打开它）、`quality_summary.json`。

## 常见问题

| 现象 | 说明 |
|---|---|
| 命令退出码是 3 | 正常：表示在等待抽取或独立复核，agent 会处理完后继续 |
| 报告里写“待复核” | 没有可用的独立复核者，这部分数据没有写入工作簿 |
| 当前季度采集失败（覆盖缺口） | 港交所报告还没覆盖到这些日期；这是缺口，不代表这期间没有 IPO。之后再跑一次 |
| 已有的 2026 年数据 | 计划里标为 `stored`，直接复用并审计，不会重新采集 |
| 只想看计划、不采集 | `python3 run.py plan 2025Q4` |
| 字段是空的 | 招股书没有披露或无法核实；空值不会被填成 0 |

完整操作手册（英文）：[AGENT_INSTRUCTIONS](AGENT_INSTRUCTIONS.md)；GEM 说明：[GEM_PIPELINE](GEM_PIPELINE.md)。

---

## English

Tell an agent one time period; it plans quarters, installs, collects Main Board and
GEM IPOs, extracts each prospectus and allotment notice, obtains an independent
review, writes reviewed values to Excel, audits, and delivers a ZIP.

**Requirements.** An agent with terminal, Internet and subagent support (Claude Code
recommended, or Codex CLI); Git; Python 3.9+. Use WSL on Windows. Without subagents,
data stay "review pending" and are not written to workbooks.

**1. Install once.**

```bash
git clone https://github.com/GZ-November/urop-hk-ipo.git
cd urop-hk-ipo
python3 tools/bootstrap.py              # add --skills both to use the skill from any directory
```

**2. Say the period.** Open `claude` or `codex` in the checkout and write
"Collect Hong Kong IPOs listed in 2025 Q4" (or `/hk-ipo-collect 2025Q4` in Claude Code).
Accepted forms include `2025`, `2025H2`, `2025Q4`, `2025-11`, `2024Q3..2025Q2` and
explicit dates. Optional details go in the [request template](COLLECTION_REQUEST_TEMPLATE.md).

**3. Collect the delivery.** The agent reports the ZIP path in `deliverables/`, issuer
counts and listing dates per quarter, missing fields, pending reviews and source gaps.
Say "continue the HK IPO collection" to resume an interrupted run.
