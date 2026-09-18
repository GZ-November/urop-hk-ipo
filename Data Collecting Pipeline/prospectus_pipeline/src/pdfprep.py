"""招股书 PDF 下载、文本抽取、章节切片、AI 抽取包生成。"""
from __future__ import annotations

import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from contracts import is_company_level_statement
from storage import merge_index

import requests

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

# 每个字段组在招股书里对应的章节标题与向后取的页数窗口。
# 顺序 = 优先级：字符预算用完时，靠后的锚点先被舍弃，所以高价值表放在前面。
GROUP_WINDOWS: dict[str, list[tuple[str, int]]] = {
    "share_structure": [("SHARE CAPITAL", 8), ("GLOBAL OFFERING STATISTICS", 6),
                        ("STATISTICS OF THE GLOBAL OFFERING", 6),
                        ("INFORMATION ON THE GLOBAL OFFERING", 6), ("IMPORTANT", 4)],
    "price": [("__cover__", 3), ("IMPORTANT", 5), ("OFFER PRICE", 4),
              ("MAXIMUM OFFER PRICE", 4), ("MINIMUM OFFER PRICE", 4)],
    # V–AN：三年资产/权益/负债/销售/税前利润/净利润。先取 MD&A 与摘要表，再取正式报表。
    "financials": [("SUMMARY OF HISTORICAL FINANCIAL INFORMATION", 6),
                   ("SUMMARY OF CONSOLIDATED STATEMENTS OF FINANCIAL POSITION", 5),
                   ("SUMMARY OF CONSOLIDATED STATEMENTS OF PROFIT", 5),
                   ("SELECTED CONSOLIDATED FINANCIAL DATA", 5),
                   ("DISCUSSION OF SELECTED ITEMS FROM THE CONSOLIDATED BALANCE", 6),
                   ("DISCUSSION OF SELECTED BALANCE SHEET ITEMS", 6),
                   ("SELECTED BALANCE SHEET ITEMS", 5),
                   ("CONSOLIDATED STATEMENTS OF FINANCIAL POSITION", 6),
                   ("CONSOLIDATED BALANCE SHEETS", 5),
                   ("CONSOLIDATED STATEMENTS OF PROFIT OR LOSS", 5),
                   ("CONSOLIDATED STATEMENTS OF COMPREHENSIVE LOSS", 5),
                   ("CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME", 5),
                   ("HISTORICAL FINANCIAL INFORMATION OF THE GROUP", 6),
                   ("INDEBTEDNESS", 4)],
    "underwriting": [("UNDERWRITING ARRANGEMENTS AND EXPENSES", 15),
                     ("UNDERWRITING COMMISSION", 6), ("UNDERWRITING", 10)],
    "business": [("BUSINESS", 10), ("SUMMARY", 8), ("HISTORY AND DEVELOPMENT", 8),
                 ("BASIS OF LISTING", 5)],
    # 基石投资者单列一组（写入紫色额外信息栏 BS），需要完整协议与名单表。
    "cornerstone": [("CORNERSTONE INVESTORS", 30), ("CORNERSTONE PLACING", 25),
                    ("CORNERSTONE INVESTMENT AGREEMENT", 15)],
    # 附加财务 AU–AY。AX 是资本化开发成本当期新增；AY 是前五大客户集中度。
    "extra_financial": [("CONSOLIDATED STATEMENTS OF CASH FLOWS", 5),
                        ("CONSOLIDATED CASH FLOW STATEMENTS", 5),
                        ("CASH FLOW ANALYSIS", 4),
                        ("R&D EXPENDITURE AND TOTAL OPERATING EXPENDITURE", 4),
                        ("RESEARCH AND DEVELOPMENT COSTS", 4),
                        ("RESEARCH AND DEVELOPMENT EXPENSES", 4),
                        ("INTANGIBLE ASSETS", 5), ("OTHER INTANGIBLE ASSETS", 4),
                        ("CAPITALIZED DEVELOPMENT", 4),
                        ("CUSTOMERS AND SUPPLIERS", 6), ("OUR CUSTOMERS AND SUPPLIERS", 6),
                        ("OUR CUSTOMERS", 6), ("MAJOR CUSTOMERS", 6),
                        ("INFORMATION ABOUT MAJOR CUSTOMERS", 6)],
    "chinese_name": [("__cover__", 3)],
    "ownership": [("HISTORY AND DEVELOPMENT", 15), ("HISTORY DEVELOPMENT", 15),
                  ("HISTORY REORGANISATION", 15), ("HISTORY REORGANIZATION", 15),
                  ("HISTORY AND CORPORATE STRUCTURE", 15),
                  ("PRE-IPO INVESTMENTS", 15),
                  ("SUBSTANTIAL SHAREHOLDERS", 10), ("RELATIONSHIP WITH OUR CONTROLLING", 8),
                  ("STATUTORY AND GENERAL INFORMATION", 12)],
    "offering": [("EXPECTED TIMETABLE", 8), ("HOW TO APPLY FOR HONG KONG OFFER SHARES", 5)],
}
GROUP_KEYWORDS = {g: [k for k, _ in v] for g, v in GROUP_WINDOWS.items()}


def _safe_name(code: str) -> str:
    return "HKIPO-MB" + "".join(ch for ch in code if ch.isdigit())


# ---------------------------------------------------------------- download
def download_one(cfg: dict, rec: dict, log=print) -> dict:
    pdf_dir: Path = cfg["paths"]["pdf"]
    dest = pdf_dir / f"{_safe_name(rec['code'])}.pdf"
    if dest.exists() and dest.stat().st_size > 50_000:
        return {**rec, "pdf": str(dest), "bytes": dest.stat().st_size, "download": "cached"}
    try:
        r = requests.get(rec["pdf_url"], timeout=180, headers={"User-Agent": UA}, stream=True)
        r.raise_for_status()
        tmp = dest.with_suffix(".part")
        with open(tmp, "wb") as fh:
            for chunk in r.iter_content(1 << 16):
                fh.write(chunk)
        tmp.rename(dest)
        return {**rec, "pdf": str(dest), "bytes": dest.stat().st_size, "download": "ok"}
    except Exception as exc:  # noqa: BLE001
        return {**rec, "pdf": None, "bytes": 0, "download": f"error: {type(exc).__name__}: {exc}"}


def download_all(cfg: dict, found: list[dict], workers: int = 5, log=print) -> list[dict]:
    todo = [f for f in found if f.get("status") == "ok" and f.get("pdf_url")]
    out: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(download_one, cfg, rec): rec for rec in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            res = fut.result()
            out.append(res)
            mb = res["bytes"] / 1e6
            log(f"[{i}/{len(todo)}] {res['code']:9s} {mb:6.1f}MB  {res['download']}")
    merge_index(cfg["paths"]["out"] / "downloaded.json", out)
    ok = sum(1 for x in out if x["pdf"])
    log(f"\n下载完成：{ok}/{len(todo)}")
    return out


# ---------------------------------------------------------------- text
def extract_text(cfg: dict, code: str, log=print) -> Path:
    """PDF -> 页级文本 jsonl（带页码），已存在则跳过。"""
    import fitz  # PyMuPDF
    pdf = cfg["paths"]["pdf"] / f"{_safe_name(code)}.pdf"
    dest = cfg["paths"]["text"] / f"{_safe_name(code)}.jsonl"
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    doc = fitz.open(pdf)
    with open(dest, "w") as fh:
        for i, page in enumerate(doc, 1):
            fh.write(json.dumps({"page": i, "text": page.get_text()}, ensure_ascii=False) + "\n")
    n = doc.page_count
    doc.close()
    log(f"   文本抽取 {code}: {n} 页")
    return dest


def _pages(cfg: dict, code: str) -> list[dict]:
    f = cfg["paths"]["text"] / f"{_safe_name(code)}.jsonl"
    return [json.loads(line) for line in f.open()]


def _normalise_heading(text: str) -> str:
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"[,;:.·•]+", " ", text)
    return " ".join(text.upper().split()).strip(" -:")


DOT_LEADER = re.compile(r"(?:\.\s*){3,}|…{2,}")
PAGE_ONLY = re.compile(r"^[\s\-–—\d|]+$")


def _is_toc(text: str) -> bool:
    """目录页：大量“点线 + 页码”行。注意 PDF 里点线是空格分隔的 '. . . .'。"""
    head = text[:2000]
    leaders = len(DOT_LEADER.findall(head))
    if leaders >= 3:
        return True
    return "CONTENTS" in head.upper() and leaders >= 1


def _page_leading_keys(text: str, depth: int = 8) -> list[str]:
    """取页首若干行（跳过页码行/点线行），用于判断该页归属于哪个章节。"""
    out: list[str] = []
    for line in text.splitlines():
        raw = line.strip()
        if not raw or PAGE_ONLY.match(raw) or DOT_LEADER.search(raw):
            continue
        s = _normalise_heading(raw)
        if s:
            out.append(s)
        if len(out) >= depth:
            break
    return out


def _page_trailing_keys(text: str, depth: int = 4) -> list[str]:
    """页尾若干行：招股书页眉（章节名）在 PyMuPDF 抽取里落在页面末尾。"""
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    out: list[str] = []
    for raw in reversed(lines):
        if PAGE_ONLY.match(raw) or DOT_LEADER.search(raw):
            continue
        out.append(_normalise_heading(raw))
        if len(out) >= depth:
            break
    return out


def _matches_anchor(line: str, want: str) -> bool:
    if not line:
        return False
    if line == want or line.startswith("THE " + want):
        return True
    # “BUSINESS – CONTINUED”“CONSOLIDATED STATEMENTS OF FINANCIAL POSITION (CONTINUED)”
    # “INTANGIBLE ASSETS (OTHER THAN GOODWILL)”等续页/限定后缀
    return line.startswith(want + " ") and len(line) <= len(want) + 32


def _hits_anchor(keys: list[str], want: str) -> bool:
    if any(_matches_anchor(k, want) for k in keys):
        return True
    # 标题被 PDF 折成两行的情况
    return any(_matches_anchor(f"{a} {b}", want) for a, b in zip(keys, keys[1:]))


def _heading_runs(pages: list[dict], key: str) -> list[list[int]]:
    """章节 = 命中该锚点的**连续**页面区间（首页标题 + 续页页眉共同界定）。"""
    want = _normalise_heading(key)
    owned: list[int] = []
    for p in pages:
        text = p["text"]
        if _is_toc(text):
            continue
        if _hits_anchor(_page_leading_keys(text), want) or \
                _hits_anchor(_page_trailing_keys(text), want):
            owned.append(p["page"])
    runs: list[list[int]] = []
    for page in sorted(set(owned)):
        if runs and page - runs[-1][-1] <= 2:
            runs[-1].append(page)
        else:
            runs.append([page])
    return runs


def _first_mention(pages: list[dict], key: str) -> int | None:
    """谨慎兜底：只在没有锚点命中时取正文首次提及页。"""
    needle = " ".join(key.upper().split())
    for p in pages:
        if not _is_toc(p["text"]) and needle in _normalise_heading(p["text"]):
            return p["page"]
    return None


def locate_sections(cfg: dict, code: str) -> dict[str, list[int]]:
    """按锚点优先级取页：每个锚点取至多 MAX_RUNS_PER_ANCHOR 段连续章节，
    自章节起点向后延伸 span 页。页码保持优先级顺序，便于在字符预算内先保高价值表。"""
    pages = _pages(cfg, code)
    n_pages = max((p.get("page", 0) for p in pages), default=len(pages))
    page_text_by_no = {p["page"]: p["text"] for p in pages}
    cover = int(cfg["extract"]["cover_pages"])
    max_runs = int(cfg["extract"].get("max_runs_per_anchor", 2))
    result: dict[str, list[int]] = {}
    for group, anchors in GROUP_WINDOWS.items():
        ordered: list[int] = []
        seen: set[int] = set()
        for key, span in anchors:
            if key == "__cover__":
                candidates = list(range(1, min(cover, n_pages) + 1))
            else:
                runs = _heading_runs(pages, key)
                if runs:
                    chosen = sorted(runs, key=len, reverse=True)[:max_runs]
                    chosen.sort(key=lambda r: r[0])
                    candidates = []
                    for run in chosen:
                        for pg in range(run[0], min(run[0] + span, n_pages + 1)):
                            # financials 组延伸遇母公司单体报表时立即截断，防止混入
                            if group == "financials" and is_company_level_statement(page_text_by_no.get(pg, "")):
                                break
                            candidates.append(pg)
                else:
                    fallback = _first_mention(pages, key)
                    candidates = []
                    if fallback is not None:
                        for pg in range(fallback, min(fallback + span, n_pages + 1)):
                            if group == "financials" and is_company_level_statement(page_text_by_no.get(pg, "")):
                                break
                            candidates.append(pg)
            for pg in candidates:
                if group == "financials" and is_company_level_statement(page_text_by_no.get(pg, "")):
                    continue
                if pg not in seen:
                    seen.add(pg)
                    ordered.append(pg)
        result[group] = ordered
    return result


def build_slices(cfg: dict, code: str, loc: dict[str, list[int]]) -> dict[str, str]:
    """按组分页拼接文本；各组独立预算，避免后面的基石/附加财务被全局上限吃掉。"""
    pages = {p["page"]: p["text"] for p in _pages(cfg, code)}
    default_cap = int(cfg["extract"].get("max_chars_per_group", 60000))
    group_caps = {k: int(v) for k, v in cfg["extract"].get("group_caps", {}).items()}
    total_cap = int(cfg["extract"].get("max_chars_total", 900000))
    out: dict[str, str] = {}
    total = 0
    for group, pgs in loc.items():
        cap = group_caps.get(group, default_cap)
        buf, used = [], 0
        for pg in pgs:
            block = f"\n<<<PAGE {pg}>>>\n{pages.get(pg, '')}"
            if used + len(block) > cap or total + len(block) > total_cap:
                buf.append(f"\n<<<PAGE {pg} 起已省略：超出 {group} 字符上限；请人工复核覆盖范围>>>")
                break
            buf.append(block)
            used += len(block)
            total += len(block)
        out[group] = "".join(buf)
    return out


# ---------------------------------------------------------------- packet
PACKET_HEADER = """# 招股书抽取任务包：{code} {name}

- 来源：{pdf_url}
- 港交所文件：{doc_type} / {doc_title}（{doc_datetime}）
- 招股书日期：{prospectus_date} ｜ 上市日期：{listing_date}
- 本包只包含招股书来源字段；字段名、类型、缺失值和期间契约见字段清单。

## 唯一输出契约（必须严格遵守）

只输出一个 JSON 对象，且**顶层必须是**：
`{{"code":"{code}","fields":{{"col_X":{{"value":...,"page":...,"quote":"...","confidence":"high|medium|low"}}}}}}`。
不要输出 Markdown 围栏、解释文字、notes 顶层键或额外字段。每个字段 key 必须出现且只能出现一次。
`page` 必须是本包中的正整数页码；缺失时为 `null`。`quote` 必须是本包原文的短摘录（最多 200 字符）；缺失时为空字符串。

## 手册硬规则

1. 只依据本包原文，不使用常识、外部网页或估算；不确定就使用字段契约指定的 `NaN`/`NA`。
2. 金额换算为基本货币单位；百分比填小数；确认零填数字 0。
3. **合并报表（Group/Consolidated）唯一原则**：所有财务数据（资产负债表 V–AE/BE、利润表 AF–AN、现金流 AU/AV、研发 AX 等）**必须且只能**取自**合并财务报表（CONSOLIDATED Financial Statements）**；**绝对严禁**引用母公司单体报表（如 STATEMENT OF FINANCIAL POSITION OF THE COMPANY / COMPANY BALANCE SHEETS）。year-1/2/3 必须对应同一套历史期间；year-1 销售/利润若为非全年，按手册年化。AU/AW/AX 为期间流量，AV/BE 为期末余额；这些扩展字段不年化。
4. 经营现金流是 net cash from operating activities；现金及等价物不自动包含受限现金。
5. `AX` 只填资本化开发成本的**当期新增**，不是无形资产期末余额；`AY` 是 year-1 前五大客户收入占比。表格明确为 `–`/nil 时填数字 0。
6. 承销佣金：按全球发售披露时 AO/AP 同率；只按香港公开发售披露时 AP=0；不能把总上市费用当佣金。绿鞋 AQ 只能按招股书披露，不能默认 15%。
7. `CJ` 基石名单必须来自真正的 Cornerstone Investors/Cornerstone Placing 协议和名单表；不要使用目录、豁免段或普通提及。
8. listing route 必须按招股书披露的 basis of listing/适用章节填写，不能按行业猜测；中文名填简体中文。
9. `BA` 只表示上市前是否有 VC/PE 支持；基石投资者身份本身不能证明 BA。`BC`/`BD` 分别是控制人上市时经济权益/投票权，不是基石最终获配。
10. 每一项都要保留准确页码、原文短摘录和置信度；不得为了配平而修改原文数字。

---
"""
GROUP_TITLES = {
    "share_structure": "股份结构（L–S）",
    "price": "价格区间（T–U）",
    "financials": "上市前三年财务（V–AN）",
    "underwriting": "承销佣金与超额配售（AO–AQ）",
    "business": "主营业务与上市途径（AR–AS）",
    "cornerstone": "基石投资者名单（CJ）",
    "extra_financial": "附加财务（AT–AY）",
    "chinese_name": "公司中文名（DP）",
    "ownership": "上市前投资与控制权（BA–BD/BP/BR）",
    "offering": "发售时间表（CC–CD）",
}


def build_packet(cfg: dict, rec: dict, fields: list[dict], slices: dict[str, str]) -> Path:
    dest = cfg["paths"]["packets"] / f"{_safe_name(rec['code'])}.md"
    parts = [PACKET_HEADER.format(**rec)]
    for group, title in GROUP_TITLES.items():
        fs = [f for f in fields if f["group"] == group]
        parts.append(f"\n## {title}\n")
        for f in fs:
            details = f"type={f.get('kind')} unit={f.get('unit')} missing={f.get('missing')}"
            if f.get("period"):
                details += f" period={f['period']} annualize={f.get('annualize')}"
            parts.append(f"- `{f['key']}` = {f['header']} ({details})")
        parts.append(f"\n### 原文切片：{title}\n")
        cap = int(cfg["extract"].get("group_caps", {}).get(
            group, cfg["extract"].get("max_chars_per_group", 60000)))
        parts.append(slices.get(group, "(无匹配章节)")[:cap])
        parts.append("\n")
    dest.write_text("\n".join(parts), encoding="utf-8")
    return dest


def prepare_all(cfg: dict, found: list[dict], log=print) -> list[dict]:
    fields = json.loads((cfg["_root"] / "schema" / "fields.json").read_text())["fields"]
    out = []
    for i, rec in enumerate(found, 1):
        if not rec.get("pdf"):
            continue
        extract_text(cfg, rec["code"])
        loc = locate_sections(cfg, rec["code"])
        slices = build_slices(cfg, rec["code"], loc)
        # 保存可审计的分组切片，packet 只是汇总视图。
        section_meta = {}
        for group, text in slices.items():
            section_file = cfg["paths"]["sections"] / f"{_safe_name(rec['code'])}-{group}.txt"
            section_file.write_text(text, encoding="utf-8")
            section_meta[group] = {
                "pages": loc.get(group, []), "chars": len(text),
                "truncated": "超出" in text or "省略" in text,
                "empty": not bool(text.strip()),
                "path": str(section_file),
            }
        pkt = build_packet(cfg, rec, fields, slices)
        size = pkt.stat().st_size
        out.append({"code": rec["code"], "name": rec["name"],
                    "packet_path": str(pkt),
                    "out_path": str(cfg["paths"]["out"] / "extracted" / f"{_safe_name(rec['code'])}.json"),
                    "packet_kb": round(size / 1024, 1),
                    "pages_by_group": {g: len(v) for g, v in loc.items()},
                    "section_quality": section_meta})
        warnings = [g for g, m in section_meta.items() if m["empty"] or m["truncated"]]
        log(f"[{i}/{len(found)}] {rec['code']:9s} 包 {size/1024:6.0f}KB  "
            f"切片页数 " + " ".join(f"{g[:4]}={len(v)}" for g, v in loc.items())
            + (f"  警告={','.join(warnings)}" if warnings else ""))
    merge_index(cfg["paths"]["out"] / "packets.json", out)
    log(f"\n抽取包生成完成：{len(out)} 个 -> {cfg['paths']['packets']}")
    return out
