#!/usr/bin/env python3
"""生成「扩展 18 列」的小抽取包。

为什么要单独打包：42 列已完成且已入表，重抽一次要 ¥0.5/家。
扩展包只含 18 个新字段的定义 + bundle 预计算候选原文（≈12KB vs 主包 426KB），
抽完成本约 ¥0.15/家，再与已有 JSON 合并。

输出 data/packets_ext/HKIPO-MB<code>.md 与 out_ext/packets_ext.json
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PIPE = ROOT
OUT_DIR = PIPE / "data" / "packets_ext"
EXT_KEYS = ["col_BA", "col_BB", "col_BC", "col_BD", "col_BE", "col_BF", "col_BG",
            "col_BI", "col_BP", "col_BR", "col_BT", "col_CC", "col_CD", "col_CE",
            "col_CF", "col_CG", "col_CH", "col_CI"]

FIXED = """## 输出契约（机器校验，违反即失败）
顶层**只能**有 `code` 和 `fields`：
```json
{"code":"<CODE>","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  <CODE> 33,314,416
python3 prospectus_pipeline/tools_search.py search <CODE> "正则" --context 3 --max 5
```
"""


def build(code: str, name: str, packet_path: Path, out_path: Path) -> dict:
    digits = "".join(c for c in code if c.isdigit())
    schema = json.loads((PIPE / "schema" / "fields.json").read_text(encoding="utf-8"))
    by_key = {f["key"]: f for f in schema["fields"]}

    rows = ["| key | 列 | 表头 | 类型 | 缺失 | 提示 |", "|---|---|---|---|---|---|"]
    for k in EXT_KEYS:
        f = by_key[k]
        hint = (f.get("hint") or "").replace("|", "/")
        rows.append(f"| {k} | {f['col']} | {f['header']} | {f['kind']} | "
                    f"{f['missing']} | {hint} |")

    # 已有的确定性结论，避免代理推翻
    fixed = []
    jf = PIPE / "out" / "extracted" / f"HKIPO-MB{digits}.json"
    if jf.exists():
        old = json.loads(jf.read_text(encoding="utf-8"))["fields"]
        def g(k):
            return old.get(k, {}).get("value")
        fixed.append(f"- 股本结构（**已确认，不要改**）：L={g('col_L')} M={g('col_M')} "
                     f"N={g('col_N')} O={g('col_O')} P={g('col_P')} Q={g('col_Q')} "
                     f"R={g('col_R')} S={g('col_S')}")
        fixed.append(f"- 财务期间（**已确认**）：year-1 期末 = {g('col_AT')}；"
                     f"币种 = {g('col_V')}；year-1 净利 = {g('col_AN')}")
    hc = PIPE / "out" / "hsic_codes.json"
    if hc.exists():
        d = json.loads(hc.read_text(encoding="utf-8")).get(code)
        if d:
            fixed.append(f"- 行业分类（港交所官方）：{d['code']} {d['sub_sector']}")
    ca = PIPE / "out" / "allot" / "cornerstone_absence.json"
    if ca.exists():
        d = json.loads(ca.read_text(encoding="utf-8")).get(code)
        if d:
            fixed.append(f"- 基石投资者：{'确认无' if d['verdict']=='none' else '有'}")

    try:
        bundle = subprocess.run(
            [sys.executable, str(PIPE / "tools_search.py"), "bundle", code,
             "--fields", ",".join(EXT_KEYS), "--per-field", "3", "--context", "3",
             "--max-chars", "30000"],
            capture_output=True, text=True, timeout=300).stdout
    except Exception as exc:  # noqa: BLE001
        bundle = f"（bundle 失败：{exc}）"

    md = f"""# {code} 扩展 18 列抽取包

公司：{code} {name}

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `{out_path}`。
主包（42 列）已完成并已入表，这里只补扩展列。

## 字段清单
{chr(10).join(rows)}

## 已确认的结论（直接用，不要推翻）
{chr(10).join(fixed) if fixed else '（无）'}

## 手册规则
- 金额换算成**基本货币单位**（披露币种见上面的 col_V，表格若标 RMB'000 或 US$'000 必须乘以 1,000）；百分比填**小数**。
- `col_CF`（毛利）与 `col_CG`（资本开支）：**强制与 col_AT 期间强绑定**！当 col_AT 为中期截止日（如 30/06/25 或 30/09/25）时，必须严格取该中期报告期（如 6M 或 9M 对应列）的披露原值，**绝对严禁错采 2024 全年列数值**！二者均不年化。
- `col_BE` 只算**有息负债**（借款/债券/租赁负债），取 INDEBTEDNESS 表格的 Total 总计（含流动与非流动有息负债），必须折算为基本货币单位，不含应付账款。
- `col_BG` = 用于偿债的金额 ÷ 计划净募资额；没有该用途填 `0`。
- `col_BF` 按招股书原文的产品阶段表述，**不要**按行业推测。
- `col_BA` 只要上市前有专业投资机构（VC/PE/产业基金）入股即 `1`，否则 `0`。
- `col_CD`/`col_CC` 取 EXPECTED TIMETABLE 的认购起止日。
- `col_BP`（注册成立日期）：**严禁从 Definitions（释义）章节取值**。必须取自 Statutory and General Information（附录五「1. Incorporation」）、History and Development 或会计师报告附注 1。若释义章节与法定/正文存在冲突，一律以法定/审计数据为准。
- `col_CI` 是**总上市费用**（含承销佣金与其他开支），用 HK$ 基本单位。
- 不确定就填 NaN/NA 并在 quote 说明，**不要猜**。

{FIXED.replace('<CODE>', code)}

## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）
{bundle}

## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only {code}`
有 ERROR 必须回原文修正。
"""
    packet_path.parent.mkdir(parents=True, exist_ok=True)
    packet_path.write_text(md, encoding="utf-8")
    return {"code": code, "name": name, "packet_path": str(packet_path),
            "out_path": str(out_path)}


def main() -> int:
    packets = json.loads((PIPE / "out" / "packets.json").read_text(encoding="utf-8"))
    out_dir = PIPE / "out_ext" / "extracted"
    out_dir.mkdir(parents=True, exist_ok=True)
    recs = [build(x["code"], x.get("name", ""),
                  OUT_DIR / f"HKIPO-MB{''.join(c for c in x['code'] if c.isdigit())}.md",
                  out_dir / f"HKIPO-MB{''.join(c for c in x['code'] if c.isdigit())}.json")
            for x in packets]
    (PIPE / "out_ext" / "packets_ext.json").write_text(
        json.dumps(recs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    sizes = [Path(r["packet_path"]).stat().st_size for r in recs]
    print(f"生成 {len(recs)} 个扩展包，"
          f"平均 {sum(sizes)//len(sizes)//1024}KB（主包平均 380KB）")
    print("-> prospetus_pipeline/out_ext/packets_ext.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
