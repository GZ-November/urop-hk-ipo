#!/usr/bin/env python3
"""Harness 无关的抽取/复核 prompt 生成器（缓存友好）。

设计：
  extract 与 review 两个 prompt 共享**字节一致**的前缀
  （角色 + 公司信息 + 内联抽取包 + 手册硬规则），阶段任务（抽取/复核）
  只出现在尾部——支持 prompt caching 的 harness 在复核遍命中前缀缓存，
  不支持的 harness 也能直接把 prompt 全文贴进对话使用。

  escalate 变体面向验证驱动的定向重抽（auto_fill next-escalation 的产物）：
  只内联相关主题分片，并携带 only_fields 清单。

用法（经 auto_fill CLI）：
  python3 src/auto_fill.py prompt --phase extract --only 6656.HK
  python3 src/auto_fill.py prompt --phase review  --only 6656.HK
  python3 src/auto_fill.py prompt --phase escalate --only 6656.HK

产物写入 out/prompts/HKIPO-MB####.{phase}.prompt.md（本地工件）。
"""
from __future__ import annotations


# ---------------------------------------------------------------------------- #
# 手册硬规则（与 workflows/prospectus_extract.js 的口径保持一致；改动需同步）
# ---------------------------------------------------------------------------- #

MANUAL_RULES = """## 手册硬规则（必须遵守）
1. 金额一律换算成**基本货币单位**（HK$125.6 million -> 125600000）；百分比填小数；确认的零填数字 0。
2. **合并报表唯一原则（严防母公司单体报表混淆）**：所有资产、权益、负债、销售、利润、现金流、有息债务等财务指标（V–AN、AU–AY、BE 等）**必须且只能**取自**合并财务报表（CONSOLIDATED Financial Statements / Group）**；**绝对严禁**采纳母公司单体报表（`STATEMENT OF FINANCIAL POSITION OF THE COMPANY` / `COMPANY BALANCE SHEETS`）。year-1/2/3 必须是**同一套历史期间**；year-1 销售/利润若不是全年（如 9 个月），按手册年化并在 quote 注明原始期间；附加流量 AU/AW/AX 一律**不年化**；AV（年末现金）和 BE（有息负债）是期末余额，AY 是比例。
3. AU 经营现金流 = net cash from operating activities，**不是**经营利润；AV 现金及等价物**不自动包含**受限现金。
4. AX 只填**当期新增**的资本化开发成本，不是期末余额；表中明确写 `–`/nil 时填数字 0。
5. AL/AM/AN 是净利润（profit for the year）；AI/AJ/AK 是税前利润。
6. 承销佣金：招股书按全球发售披露时 AO/AP 填同一比例；只按香港公开发售披露时 AP=0；给金额时用金额÷对应基数；
   **不能**把总上市费用当佣金。AQ 绿鞋只能按招股书披露，**不能默认 15%**。
7. col_CJ 基石名单必须来自真正的 Cornerstone Investors / Cornerstone Placing 名单表，
   **不要**用目录、豁免段、风险因素里的普通提及；无基石填 `"NA"`；用分号分隔全称。
8. col_AS 上市途径按招股书披露的 basis of listing / 适用章节填（如 Chapter 18C），**不能**按行业推断；col_DP 中文名填简体。
9. **Pre-IPO VC/PE 十个字段（所有 cohort 均适用）**：先检索 `HISTORY AND DEVELOPMENT — Pre-IPO Investments`，再用 `SUBSTANTIAL SHAREHOLDERS`、股本表和董事章节核对。名单、轮次、持股比例、协议日期必须按该公司自己的招股书取值；严禁从其他公司 JSON、旧 cohort 数据或投资机构常识补值。
   - `col_pre_ipo_investors` 仅列招股书披露的上市前投资者，分号分隔；同一投资者只记一次。
   - VC、PE、CVC、国资可同时为 1；按投资者/基金性质分类并在各自 quote 中给出该公司披露依据。普通产业股东不自动算 CVC，国资身份不自动等于 VC/PE。
   - 只有招股书明确披露上市前投资，或可从上市前股东表确认，才填 1。没有找到证据不等于 0；只有披露明确确认无此类投资时填 0，否则填 NaN/NA。
   - `col_vc_pe_stake` 取上市前所有机构投资者持股合计，统一使用紧邻上市前的股权口径，避免把上市后新股或基石配售重复计入；无明确合计时逐项核对并说明计算，不得猜。
   - 董事席位只在能把董事/观察员与上市前机构投资者明确关联时填 1；最早轮次与持有年限按最早投资协议日期计算至该公司的招股书日期。缺日期则持有年限填 NaN。
   - 十个字段分别引用支持本字段的页码和连续原文；不得把一条通用 Pre-IPO 引文复制到所有字段。审慎分类或关键日期不确定时留缺失并说明原因。
10. 不确定就填 NaN/NA 并在 quote 里写明原因，**绝对不要猜**；**不要**为了配平等式修改原文数字。"""

EXTRACT_TASK = """## 任务：抽取
1. 通读上方内联抽取包（字段契约、单位、期间、手册规则、种子切片都在里面）。
2. 对命中不够确定的字段，按包内页码回原文核实（或使用检索工具，若你的环境支持）。
3. 写 JSON（契约见包内「唯一输出契约」节），写到指定 out 路径。
4. 运行一次 `validate --only <code>`，有 ERROR 再修；通过后记录 state（extracted）。

## 严禁（做了纯属浪费，且会写错）
- **禁止**读其它公司的 `out/extracted/*.json` —— 每家的值都不同，抄了就是错
- **禁止**读 `prospectus_pipeline/src/*.py`、README、HANDOFF 等任何文档源码
- **禁止** `ls` / `find` / `pwd` / `wc` / `cat` 探路 —— 所需内容已内联在上方
- **禁止**调用 skill 工具
- **禁止**直接读 PDF 或 `data/text/*.jsonl` 全文（包内已含所需切片）
- **每轮尽量一次并行发多个工具调用**，减少来回轮数（轮数直接决定成本）

## 允许的检索工具（仅 agent 环境且包内信息不足时使用）
```bash
python3 run.py search sharecap <code>    # 权威股本汇总表（L/M/N/O/P/Q/R/S）
python3 run.py search periods  <code>    # 财务期间判定（19 个财务字段）
python3 run.py search bundle   <code>    # 全部字段候选页
python3 run.py search pages    <code> 4,90,172
python3 run.py search search   <code> "正则" --context 3 --max 8
```
**预算**：三个必跑命令之后，最多再调 **15 次**工具。"""

REVIEW_TASK = """## 任务：独立复核
0. **先跑一次** `validate --only <code>`：验证器已确定性判定的恒等式
   （M=R+S、M=Q+P、L=N+Q、L=O+M、三年资产=权益+负债、U<=T）**通过项不必再检索复核**，
   只需抽查其中 1 项确认命令输出可信；把检索预算集中在命令覆盖不到的语义项
   （合并报表来源、名单真实性、VC/PE 十字段引文、分类判断、期间口径）和验证器报出的失败项上。
1. 读取待复核 JSON（指定 out 路径），**不要相信**抽取结果，回到上方原文独立核对。
2. 高风险字段核对清单（至少这些，可再抽查其他）：
   - **合并报表唯一性**：财务字段（W–AN、AU–AY、BE 等）引用的页码是否来自合并报表
   - 三年资产 = 权益 + 负债（W/Z/AC、X/AA/AD、Y/AB/AE）
   - AX 资本化开发成本当期新增（区分"当期新增"与"期末余额"，`–` 应为 0）
   - AY 前五大客户占比的期间是否与 year-1 一致
   - AO/AP/AQ 佣金的基数口径与绿鞋是否按披露
   - **VC/PE 十字段**：名单、轮次、机构持股比例、分类 flags、董事席位及持有年限是否各自有字段特定引文支持；没有证据是否被错误地填成 0
   - CJ 基石名单是否为真实协议名单（不是目录/豁免段）
   - AR/AS/DP 是否为招股书披露内容、中文名是否简体
3. 输出复核结论：verdict（pass/fail）+ 逐项差异（field / in_file / should_be / page / reason）。

## 检索工具（仅 agent 环境使用；原文已内联于上方前缀）
```bash
python3 run.py search search <code> "<正则>" --context 3 --max 8
python3 run.py search pages <code> <页码或范围>
```"""

ESCALATE_TASK = """## 任务：定向重抽（验证驱动升级）
1. 上方内联的是**相关主题分片**（不是完整包），下方 only_fields 列出本次必须补齐/修正的字段。
2. 只处理 only_fields 列出的字段；其余字段以现有 JSON 为准，不要改动。
3. 找不到证据的字段按契约填 NaN/NA，并在 quote 里说明已检索过。
4. 写 JSON 到指定 out 路径（完整契约结构），运行 `validate --only <code>` 确认后记录 state。"""

PACKET_BEGIN = "\n\n<<< 抽取包开始（权威字段契约与种子切片） >>>\n\n"
PACKET_END = "\n\n<<< 抽取包结束 >>>\n\n"


def _shared_prefix(code: str, name: str, packet_text: str) -> str:
    """extract / review / escalate 共享的字节一致前缀。"""
    return (
        f"你是 HK IPO 数据库的数据员，负责公司 {code} {name} 的字段质量。\n"
        f"\n## 公司\n- 公司：{code} {name}\n"
        f"{PACKET_BEGIN}{packet_text}{PACKET_END}\n"
        f"{MANUAL_RULES}\n"
    )


def build_prompt(
    phase: str,
    code: str,
    name: str,
    packet_text: str,
    *,
    out_path: str = "",
    only_fields: list[str] | None = None,
) -> str:
    """生成指定阶段的完整 prompt；三阶段共享同一前缀。"""
    if phase not in ("extract", "review", "escalate"):
        raise ValueError(f"未知 phase：{phase}")
    prefix = _shared_prefix(code, name, packet_text)
    header = f"## 输出位置\n- out：`{out_path}`\n\n" if out_path else ""
    if phase == "extract":
        task = EXTRACT_TASK
    elif phase == "review":
        task = REVIEW_TASK
    else:
        fields = "\n".join(f"- {f}" for f in (only_fields or [])) or "-（见 validation）"
        task = f"{ESCALATE_TASK}\n\n## only_fields（本次范围）\n{fields}\n"
    return f"{prefix}{header}{task}\n"


def shared_prefix(extract_prompt: str, review_prompt: str) -> str:
    """诊断用：两阶段 prompt 的共享前缀字符串（缓存命中区）。"""
    import os

    return os.path.commonprefix([extract_prompt, review_prompt])
