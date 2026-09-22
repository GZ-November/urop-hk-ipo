"""配发结果公告：下载、抽全文、生成抽取包。

与招股书流水线的区别：
  - 公告只有 14–50 页（6k–26k token），**整篇一次给代理，不切片、不需检索工具**；
  - 字段是**最终值**（配发后），不是招股书的初始值/估计值；
  - 公告刊发日从港交所元数据 DATE_TIME 取（确定性），不靠正文解析。
"""
from __future__ import annotations

import datetime as dt

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from storage import create_http_session, file_sha256, merge_index

import requests

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")


def _safe_name(code: str) -> str:
    return "HKIPO-MB" + "".join(ch for ch in str(code) if ch.isdigit())


# ---------------------------------------------------------------- download
def download_one(cfg: dict, rec: dict, session: requests.Session | None = None, log=print) -> dict:
    dest: Path = cfg["paths"]["allot_pdf"] / f"{_safe_name(rec['code'])}.pdf"
    url = cfg["hkex"]["base_url"] + rec["file"]
    if dest.exists() and dest.stat().st_size > 20_000:
        return {
            **rec,
            "pdf": str(dest),
            "bytes": dest.stat().st_size,
            "sha256": file_sha256(dest),
            "download": "cached",
            "pdf_url": url,
        }
    sess = session or create_http_session()
    try:
        r = sess.get(url, timeout=180, headers={"User-Agent": UA}, stream=True)
        r.raise_for_status()
        tmp = dest.with_suffix(".part")
        with open(tmp, "wb") as fh:
            for chunk in r.iter_content(1 << 16):
                fh.write(chunk)
        tmp.rename(dest)
        return {
            **rec,
            "pdf": str(dest),
            "bytes": dest.stat().st_size,
            "sha256": file_sha256(dest),
            "download": "ok",
            "pdf_url": url,
            "retrieved_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "http_status": r.status_code,
            "etag": r.headers.get("ETag"),
            "last_modified": r.headers.get("Last-Modified"),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            **rec,
            "pdf": None,
            "bytes": 0,
            "sha256": None,
            "download": f"error: {type(exc).__name__}: {exc}",
            "pdf_url": url,
        }


def download_all(cfg: dict, index: list[dict], workers: int = 5, log=print) -> list[dict]:
    out: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(download_one, cfg, rec): rec for rec in index}
        for i, fut in enumerate(as_completed(futs), 1):
            res = fut.result()
            out.append(res)
            log(f"[{i}/{len(index)}] {res['code']:9s} {res['bytes']/1e6:5.2f}MB  {res['download']}")
    dest = cfg["paths"]["allot_out"] / "downloaded.json"
    merge_index(dest, out)
    ok = sum(1 for x in out if x["pdf"])
    log(f"\n下载完成：{ok}/{len(index)} -> {dest}")
    return out


# ---------------------------------------------------------------- text
def extract_text(cfg: dict, code: str, log=print) -> Path:
    import fitz  # PyMuPDF
    pdf = cfg["paths"]["allot_pdf"] / f"{_safe_name(code)}.pdf"
    dest: Path = cfg["paths"]["allot_text"] / f"{_safe_name(code)}.jsonl"
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    doc = fitz.open(pdf)
    with open(dest, "w", encoding="utf-8") as fh:
        for i, page in enumerate(doc, 1):
            fh.write(json.dumps({"page": i, "text": page.get_text()}, ensure_ascii=False) + "\n")
    n = doc.page_count
    doc.close()
    log(f"   文本抽取 {code}: {n} 页")
    return dest


def _pages(cfg: dict, code: str) -> list[dict]:
    f = cfg["paths"]["allot_text"] / f"{_safe_name(code)}.jsonl"
    return [json.loads(line) for line in f.open(encoding="utf-8")]


# ---------------------------------------------------------------- packet
HEADER = """# 配发结果公告抽取任务：{code} {name}

- 公告：{title}
- 刊发时间（港交所元数据）：**{datetime}**  ← `col_CR` 直接填这个值
- 公告 PDF：{pdf_url}
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{{"code":"{code}","fields":{{"col_CK":{{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}}}}
```

- `fields` 必须包含下面**每一个** key，不能少、不能多、不能重复。
- 每个字段 entry 只能有 `value` / `page` / `quote` / `confidence` 四个键。
- `page` 是**本包中的整数页码**；缺失写 `null`。`quote` 是原文短摘录（≤200 字符）；缺失写 `""`。
- 数值字段缺失写字符串 `"NaN"`；文本/日期缺失写 `"NA"`。
- 非缺失字段必须有真实页码与原文摘录，否则校验不通过。

## 手册口径

1. 金额用**基本单位**（HK$125.6 million → 125600000）；百分比用**小数**（68.86% → 0.6886）。
2. 认购倍数填**倍数**（2,347.53 times → 2347.53）。
3. 确认零填数字 `0`（例如超额配售权未行使 → `col_CV` = 0）。
4. 「最终」与「初始」必须分清：`col_CS` 是**行使发售规模调整权之后**的全球发售股数，且**不含**超额配售。
5. `col_CK` 的分母是 **base offer（不含超额配售）**；公告基石表里若已给「假设超额配售权未行使」的
   百分比列，可直接采用该列合计。
6. `col_CX` 是发行人的**净募资额**（扣除开支），**不含**售股股东所得。
7. 不确定就填 `NaN`/`NA` 并在 quote 说明，**不要猜**。

## 基石与发售机制要点（已按港交所 2025-08-04 改革公告核实）

- **基石禁售期仍为 6 个月**：港交所在该次改革的「Proposals not adopted」中明确
  *retain the existing six-month cornerstone lock-up requirement*，
  即**分阶段/3 个月解禁的方案未被采纳**。不要假设 3 个月解禁。
- **超额配售（绿鞋）与发售规模调整是两个不同的东西**：
  绿鞋是 Over-allotment Option；发售规模调整是 Offer Size Adjustment Option。
  `col_CS` 的 base offer **包含已行使的规模调整、排除绿鞋**。
- **承诺投资金额 ≠ 最终获配**：基石最终股数只认公告基石表的逐行配发数。
- 绿鞋是否实际行使要看行使公告；**不能**从本公告里「假设未行使」的口径反推。
- 本公告可能是双语对照重复排版（英文段之后是中文段），同一数字出现两次属正常。
- 每项证据必须给出**本包内**的页码与原文摘录。

### 发售机制（用于理解公告中的分配，不用来填 §DN/DO）

- **Mechanism A**：按公开发售超额认购倍数**分档回拨**到公开认购部分——
  初始 5%；≥15x 且 <50x → 15%；≥50x 且 <100x → 25%；≥100x → 35%（上限 35%）。
- **Mechanism B**：公开发售初始分配**至少 10%、最多 60%**，**无回拨机制**。
- 另：首次公开发售中至少 **40%** 须分配予建簿配售部分。

---

## 字段清单

"""


def build_packet(cfg: dict, rec: dict, fields: list[dict], text: str) -> Path:
    dest: Path = cfg["paths"]["allot_packets"] / f"{_safe_name(rec['code'])}.md"
    parts = [HEADER.format(code=rec["code"], name=rec.get("name", ""),
                           title=rec.get("title", ""), datetime=rec.get("datetime", ""),
                           pdf_url=rec.get("pdf_url", ""))]
    for group, cols in _groups(fields).items():
        parts.append(f"\n### {group}\n")
        for f in cols:
            parts.append(f"- `{f['key']}` = {f['header']}"
                         f"（type={f['kind']} unit={f['unit']} missing={f['missing']}）")
            parts.append(f"  - 提示：{f['hint']}")
    parts.append("\n---\n\n## 公告全文\n")
    parts.append(text)
    dest.write_text("\n".join(parts), encoding="utf-8")
    return dest


GROUP_TITLES = {
    "cornerstone_final": "基石最终获配",
    "demand": "认购需求",
    "pricing": "定价与公告日",
    "final_shares": "最终发售与回拨",
    "proceeds": "净募资",
    "shareholding": "上市时持股与自由流通",
}


def _groups(fields: list[dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for f in fields:
        out.setdefault(GROUP_TITLES.get(f.get("group", ""), f.get("group", "字段")), []).append(f)
    return out


def prepare_all(cfg: dict, index: list[dict], log=print) -> list[dict]:
    fields = json.loads((cfg["_root"] / "schema" / "allot_fields.json").read_text())["fields"]
    cap = int(cfg["extract"].get("allot_max_chars", 400000))
    out = []
    for i, rec in enumerate(index, 1):
        if not rec.get("pdf"):
            log(f"[{i}/{len(index)}] {rec['code']:9s} 无 PDF，跳过")
            continue
        extract_text(cfg, rec["code"])
        pages = _pages(cfg, rec["code"])
        text = "".join(f"\n<<<PAGE {p['page']}>>>\n{p['text']}" for p in pages)
        truncated = len(text) > cap
        text = text[:cap]
        pkt = build_packet(cfg, rec, fields, text)
        out.append({"code": rec["code"], "name": rec.get("name", ""),
                    "packet_path": str(pkt),
                    "out_path": str(cfg["paths"]["allot_out"] / "extracted" / f"{_safe_name(rec['code'])}.json"),
                    "pages": len(pages), "chars": len(text), "packet_kb": round(pkt.stat().st_size / 1024, 1),
                    "truncated": truncated})
        log(f"[{i}/{len(index)}] {rec['code']:9s} {len(pages):3d} 页 {len(text)/1000:6.1f}k 字符 "
            f"包 {pkt.stat().st_size/1024:5.0f}KB" + ("  ⚠️截断" if truncated else ""))
    merge_index(cfg["paths"]["allot_out"] / "packets.json", out)
    log(f"\n抽取包生成完成：{len(out)} 个")
    return out
