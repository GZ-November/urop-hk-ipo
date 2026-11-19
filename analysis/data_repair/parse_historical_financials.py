#!/usr/bin/env python3
"""Strict year-1 parser for the Accountants' Report.

Year-1 is the rightmost period column of the audited statements. A statement is
accepted only if it passes an accounting identity; anything else is left for
document-level extraction.
"""
from __future__ import annotations
import re
import fitz

NUM = re.compile(r"^\(?-?\$?\d[\d,]*(?:\.\d+)?\)?$")
DASH = {"-", "–", "—", "−", "N/A", "Nil", "nil"}
L = r"(?:profit|loss|\(loss\)|\(profit\)|earnings|surplus|deficit)(?:\s*/?\s*\(?(?:profit|loss)\)?)?"
ROW = {
    "revenue": r"^(?:total\s+)?(?:net\s+)?(?:operating\s+)?(?:revenues?|turnover|sales)\b(?!.*(?:cost|tax))",
    "cos": r"^cost\s+of\s+(?:sales|revenues?|services?|goods\s+sold|turnover)\b",
    "gp": r"^gross\s+(?:profit|loss|\(loss\))",
    "pbt": rf"^(?:net\s+)?(?:operating\s+)?{L}\s+(?:before|from ordinary activities before)\s+(?:income\s+|enterprise\s+)?tax",
    "tax": r"^(?:(?:income|enterprise income|profits?)\s+)?tax(?:ation)?\b|^income tax",
    "np": rf"^(?:net\s+)?{L}(?:\s+and\s+(?:total\s+)?(?:other\s+)?comprehensive\s+(?:income|expenses?|loss)(?:\s*/?\s*\(?\w+\)?)?)?\s+(?:for\s+the\s+(?:year|period|financial)|after\s+(?:income\s+)?tax|attributable\s+to)",
    "ta": r"^total\s+assets\b(?!\s+less)",
    "tl": r"^total\s+liabilities\b",
    "te": r"^(?:total\s+(?:shareholders['’]?\s+)?(?:equity|deficit|capital deficiency)|net\s+(?:assets|liabilities|\(liabilities\)|assets\s*/\s*\(liabilities\)))\b",
    "nca": r"^total\s+non[- ]current\s+assets\b",
    "ca": r"^total\s+current\s+assets\b",
    "cl": r"^total\s+current\s+liabilities\b",
    "ncl": r"^total\s+non[- ]current\s+liabilities\b",
    "tacl": r"^total\s+assets\s+less\s+current\s+liabilities\b",
}
ROW = {k: re.compile(v, re.I) for k, v in ROW.items()}
IS_T = re.compile(r"(statements?\s+of\s+(?:consolidated\s+|combined\s+)?(?:profit\s+or\s+loss|comprehensive\s+(?:income|loss)|income|operations)|income\s+statements?|profit\s+and\s+loss\s+accounts?|results)", re.I)
_PFX = r"^(?:\(?[a-z0-9ivx]{1,4}[.)]\s+)?(?:the\s+group.{0,3}\s+)?(?:audited\s+)?"
PRIMARY_IS = re.compile(_PFX + r"(?:(?:consolidated|combined)\s+(?:\w+\s+){0,2}?(?:income\s+statements?|statements?\s+of\s+(?:profit\s+or\s+loss|comprehensive\s+(?:income|loss)|income|operations)|profit\s+and\s+loss\s+accounts?|results\b)|statements?\s+of\s+(?:consolidated|combined)\s+(?:profit\s+or\s+loss|comprehensive\s+(?:income|loss)|income|operations))", re.I)
PRIMARY_BS = re.compile(_PFX + r"(?:(?:consolidated|combined)\s+(?:\w+\s+){0,2}?(?:balance\s+sheets?|statements?\s+of\s+(?:financial\s+position|assets\s+and\s+liabilities))|statements?\s+of\s+(?:consolidated|combined)\s+(?:financial\s+position|assets\s+and\s+liabilities))", re.I)
OTHER_ENTITY = re.compile(r"\btarget\b|\bacquired\b|\bpredecessor\b|pre-?acquisition|accountants?.{0,2}\s+report\s+(?:of|on)\s+(?!the\s+(?:group|company))", re.I)
BS_T = re.compile(r"(statements?\s+of\s+(?:consolidated\s+|combined\s+)?financial\s+position|balance\s+sheets?|statements?\s+of\s+assets\s+and\s+liabilities|net\s+assets)", re.I)


def tonum(tok):
    if tok in DASH:
        return 0.0
    neg = tok.startswith("(") or tok.startswith("-")
    v = float(re.sub(r"[^\d.]", "", tok))
    return -v if neg else v


def lines(page):
    words = sorted(page.get_text("words"), key=lambda w: (round(w[1] / 3), w[0]))
    out, cur, y = [], [], None
    for w in words:
        if y is None or abs(w[1] - y) <= 3.5:
            cur.append(w); y = w[1] if y is None else y
        else:
            out.append(sorted(cur, key=lambda a: a[0])); cur, y = [w], w[1]
    if cur:
        out.append(sorted(cur, key=lambda a: a[0]))
    return out


def rows(page):
    ls = lines(page)
    numeric_edges = []
    parsed = []
    for lw in ls:
        toks = []
        for w in lw:
            t = w[4].strip()
            if NUM.match(t) or t in DASH:
                toks.append((t, w[2]))
        # number tokens at the end of the line only
        n = len(lw)
        while n and (NUM.match(lw[n - 1][4].strip()) or lw[n - 1][4].strip() in DASH or lw[n - 1][4].strip() in {"$", ")", "("}):
            n -= 1
        label = " ".join(w[4] for w in lw[:n]).strip()
        vals = [(w[4].strip(), w[2]) for w in lw[n:] if NUM.match(w[4].strip()) or w[4].strip() in DASH]
        parsed.append((label, vals))
        numeric_edges += [x for t, x in vals if t not in DASH and len(re.sub(r"\D", "", t)) >= 3]
    if not numeric_edges:
        return [], None
    right = max(numeric_edges)
    edges = [x for x in numeric_edges if x > right - 25]
    if len(edges) < 2:
        right = sorted(numeric_edges)[-2] if len(numeric_edges) > 1 else right
    out, pending = [], []
    for label, vals in parsed:
        if vals:
            out.append((label, vals))
            # a row label may wrap over several lines; offer each possible start
            for j in range(len(pending)):
                out.append(("\x00" + " ".join(pending[j:] + ([label] if label else [])), vals))
            pending = []
        elif label and len(label) < 90:
            pending = (pending + [label])[-5:]
        else:
            pending = []
    return out, right


CCY = {"renminbi": "RMB", "rmb": "RMB", "hong kong dollar": "HK$", "hk$": "HK$", "hk dollar": "HK$", "us dollar": "US$",
       "united states dollar": "US$", "u.s. dollar": "US$", "us$": "US$", "singapore dollar": "S$", "s$": "S$"}


def unit_ccy(text):
    t = text
    m = re.search(r"(RMB|HK\$|HKD|US\$|USD|S\$|SGD|NT\$|MOP|A\$|AUD|C\$|CAD|JPY|EUR|GBP|MYR|\u00a3|\u20ac)\s*[^\w\s]{0,2}\s*(000|thousands?|millions?|mn\b|m\b|billions?)", t, re.I)
    if m:
        u = m.group(2).lower()
        code = {"HKD": "HK$", "USD": "US$", "SGD": "S$", "AUD": "A$", "CAD": "C$"}.get(m.group(1).upper(), m.group(1).upper())
        return code, 1e3 if u.startswith(("000", "thousand")) else 1e9 if u.startswith("billion") else 1e6
    m = re.search(r"(thousands?|millions?)\s+of\s+(renminbi|rmb|hong\s+kong\s+dollars?|hk\$|u\.?s\.?\s+dollars?|united\s+states\s+dollars?|singapore\s+dollars?)", t, re.I)
    if m:
        name = re.sub(r"\s+", " ", m.group(2).lower()).rstrip("s")
        return CCY.get(name, CCY.get(name.replace(".", ""))), 1e3 if m.group(1).lower().startswith("thousand") else 1e6
    m = re.search(r"(?<![\w$])(RMB|HK\$|US\$|S\$|A\$|NT\$|MOP)\s+\1(?:\s|$)", t)
    if m:
        return m.group(1), 1.0
    m = re.search(r"\b(RMB|HK\$|US\$|S\$|NT\$|MOP)", t)
    if m and re.search(r"(?:^|\s)[^\w\s]?000(?:\s|$)", t):
        return m.group(1), 1e3
    return (m.group(1) if m else None), None


def clean_label(label):
    t = label.replace("\ufb01", "fi").replace("\ufb02", "fl")
    t = re.sub(r"\bpro\s*fi\s*t", "profit", t, flags=re.I)
    t = re.sub(r"\.{2,}", " ", t)
    return re.sub(r"\s+", " ", t).strip(" .:")


def pick(rs, right):
    got = {}
    for label, vals in rs:
        wrapped = label.startswith("\x00")
        lab = clean_label(label.lstrip("\x00"))
        for k, rx in ROW.items():
            if k in got or not rx.search(lab):
                continue
            if wrapped and k in {"revenue", "cos", "gp"}:
                continue
            if k == "np" and re.search(r"per share|continuing|discontinued", lab, re.I):
                continue
            t, x = vals[-1]
            if right and abs(x - right) > 28:
                continue
            v = tonum(t)
            if k in {"pbt", "np"} and v > 0 and re.match(r"^(?:net\s+)?(?:loss|deficit)\b", lab, re.I):
                v = -v
            if k == "te" and v > 0 and re.search(r"deficit|deficiency|net liabilities", lab, re.I) and "assets" not in lab.lower():
                v = -v
            got[k] = v
            got[k + "_label"] = lab
    return got


def close(a, b, unit_tol):
    return abs(a - b) <= max(unit_tol, 0.002 * max(abs(a), abs(b)))


def company_layout(text):
    head = text[:1500]
    return bool(re.search(r"\bthe\s+group\b.{0,200}\bthe\s+company\b", head, re.I | re.S))


SECTION = [("nca", r"^non[- ]?current\s+assets:?$"), ("ca", r"^current\s+assets:?$"),
           ("cl", r"^current\s+liabilities:?$"), ("ncl", r"^non[- ]?current\s+liabilities:?$")]
SECTION_END = re.compile(r"^(net\s+current|net\s+non[- ]current|total\b|net\s+assets|net\s+liabilities|capital\s+and\s+reserves|equity\b|share\s+capital|shareholders)", re.I)


def raw_rows(page):
    """Rows in page order, headings included, with the right edge of the figure columns."""
    parsed, edges = [], []
    for lw in lines(page):
        n = len(lw)
        while n and (NUM.match(lw[n - 1][4].strip()) or lw[n - 1][4].strip() in DASH or lw[n - 1][4].strip() in {"$", ")", "("}):
            n -= 1
        label = " ".join(w[4] for w in lw[:n]).strip(" .:")
        vals = [(w[4].strip(), w[2]) for w in lw[n:] if NUM.match(w[4].strip()) or w[4].strip() in DASH]
        parsed.append((label, vals))
        edges += [x for t, x in vals if t not in DASH and len(re.sub(r"\D", "", t)) >= 3]
    return parsed, (max(edges) if edges else None)


def section_totals(pages):
    """Sum the balance-sheet sections; a printed subtotal replaces the sum."""
    out, cur, items = {}, None, []

    def close_section(printed=None):
        nonlocal cur, items
        if cur and (items or printed is not None):
            out.setdefault(cur, printed if printed is not None else sum(items))
        cur, items = None, []

    for parsed, right in pages:
        for label, vals in parsed:
            name = next((k for k, rx in SECTION if re.match(rx, label, re.I)), None)
            if name and not vals:
                close_section(); cur = name; continue
            if cur is None:
                continue
            v = None
            if vals and right is not None and abs(vals[-1][1] - right) <= 28:
                v = tonum(vals[-1][0])
            if not label and vals:
                close_section(v); continue
            if SECTION_END.match(label):
                close_section(v if re.match(r"total", label, re.I) else None); continue
            if vals:
                items.append(v or 0.0)
    close_section()
    return out


def balance_from(g, unit_tol=3):
    ta = g.get("ta")
    if ta is None and "nca" in g and "ca" in g:
        ta = g["nca"] + g["ca"]
    if ta is None and "tacl" in g and "cl" in g:
        ta = g["tacl"] + g["cl"]
    te = g.get("te")
    tl = g.get("tl")
    if tl is None and "cl" in g and "ncl" in g:
        tl = g["cl"] + g["ncl"]
    if tl is None and "cl" in g and "tacl" in g and te is not None and close(g["tacl"], te, unit_tol):
        tl = g["cl"]
    if None in (ta, tl, te) or ta <= 0:
        return None
    return (ta, tl, te) if close(ta, tl + te, unit_tol) else None


AR_RX = re.compile(r"accountant(?:s['\u2019]?|['\u2019]s)?\s+report", re.I)


def in_accountants_report(page):
    """True when the running header of the page names the Accountants' Report."""
    for lw in lines(page)[:6]:
        text = " ".join(w[4] for w in lw).strip()
        if len(text) <= 70 and AR_RX.search(text) and re.fullmatch(r"(?:appendix\s+[ivx\d]+[a-z]?\s*[-\u2013\u2014:]?\s*)?(?:the\s+)?(?:[a-z'\u2019&.,]+\s+){0,3}?accountant(?:s['\u2019]?|['\u2019]s)?\s+report(?:\s+[-\u2013\u2014(]?.*)?", text, re.I):
            return True
    return False


def rightmost_matches(page, value):
    """True when `value` is the rightmost figure of some row on the page."""
    rs, _ = rows(page)
    return any(abs(abs(tonum(v[-1][0])) - abs(float(value))) < 1e-6 for _, v in rs if v)


def latest_period_on_left(page):
    """True when the rightmost year column of the statement is not the latest year."""
    for lw in lines(page)[:30]:
        ys = [int(m) for w in lw for m in re.findall(r"^\(?((?:19|20)\d\d)\)?,?$", w[4])]
        if len(ys) >= 2 and ys[-1] < max(ys):
            return True
    return False


def primary_title(page, rx):
    """True when the page opens a group statement, not a note, segment table or another entity's accounts."""
    ls = [" ".join(w[4] for w in lw).strip() for lw in lines(page)[:22]]
    top = " ".join(ls)
    if OTHER_ENTITY.search(top) or re.search(r"notes?\s+to\s+the", top, re.I):
        return False
    return any(len(l) <= 90 and rx.search(l) for l in ls)


def parse_doc(paths, whole_document=False):
    res = {"income": None, "balance": None, "flags": []}
    balances, incomes = [], []
    income_void = False
    for path in paths:
        doc = fitz.open(path)
        pending = None
        acc, last, acc_unit, acc_ccy, acc_page = {}, -9, None, None, None
        acc_pages = []
        acc_primary = False
        for i in range(doc.page_count):
            p = doc[i]
            text = p.get_text()
            if whole_document and not in_accountants_report(p):
                continue
            head = text[:600]
            company_only = re.search(r"of\s+(?:the\s+)?company\b", head, re.I) and not re.search(r"group|consolidated|combined", head, re.I)
            is_bs = bool(BS_T.search(text))
            cont = bool(acc) and i == last + 1
            if company_only or not (IS_T.search(text) or is_bs or cont):
                pending = None
                continue
            rs, right = rows(p)
            if not rs:
                continue
            g = pick(rs, right)
            if g.get("revenue") in (0, 100, 100.0):
                pending = None
                continue
            ccy, unit = unit_ccy(text)
            if "revenue" in g or "pbt" in g or pending:
                merged = {**(pending or {}), **{k: v for k, v in g.items() if k not in (pending or {})}}
                pb, tx, np_ = merged.get("pbt"), merged.get("tax"), merged.get("np")
                u = unit or (pending or {}).get("_unit")
                c = ccy or (pending or {}).get("_ccy")
                disc = any(re.search(r"discontinued", clean_label(l), re.I) and v and tonum(v[-1][0]) != 0 and (right is None or abs(v[-1][1] - right) <= 28) for l, v in rs)
                if disc:
                    res["flags"].append(f"discontinued_operations:p{i+1}")
                    pending = None
                elif None not in (pb, tx, np_) and u and "revenue" in merged:
                    gross_ok = True
                    if merged.get("cos") is not None and merged.get("gp") is not None:
                        # Other cost lines may sit between the first cost row and gross profit,
                        # so revenue less that row may exceed gross profit but never fall short of it.
                        gross_ok = merged["revenue"] - abs(merged["cos"]) >= merged["gp"] - 3
                    if merged.get("gp") is not None:
                        gross_ok = gross_ok and abs(merged["gp"]) <= abs(merged["revenue"]) * 1.002
                    if not gross_ok:
                        res["flags"].append(f"revenue_gross_profit_mismatch:p{i+1}")
                        if merged.get("_primary") or primary_title(p, PRIMARY_IS):
                            income_void = True
                    elif close(pb - abs(tx), np_, 3) or close(pb + abs(tx), np_, 3):
                        if merged.get("_primary") or primary_title(p, PRIMARY_IS):
                            incomes.append({**merged, "ccy": c, "unit": u, "file": str(path), "page": merged.get("_page") or i + 1, "check": "pbt_tax_np", "primary": True})
                    pending = None
                elif "revenue" in merged and "pbt" in merged:
                    pending = {**merged, "_unit": u, "_ccy": c, "_page": merged.get("_page") or i + 1, "_primary": merged.get("_primary") or primary_title(p, PRIMARY_IS)}
                else:
                    pending = None
            else:
                pending = None
            if is_bs or cont:
                if not cont:
                    acc, acc_unit, acc_ccy, acc_page = {}, None, None, i + 1
                    acc_primary = primary_title(p, PRIMARY_BS)
                acc = {**acc, **{k: v for k, v in g.items() if k not in acc}}
                acc_pages = (acc_pages if cont else []) + [raw_rows(p)]
                for k, v in section_totals(acc_pages).items():
                    acc.setdefault(k, v)
                acc.setdefault("ncl", 0.0) if {"cl", "te"} <= set(acc) and "ca" in acc and "nca" in acc else None
                acc_unit = acc_unit or unit
                acc_ccy = acc_ccy or ccy
                last = i
                b = balance_from(acc)
                if b and acc_unit:
                    parent_only = any(re.match(r"(?:interests?|investments?)\s+in\s+(?:a\s+)?subsidiar", clean_label(l), re.I) for pg in acc_pages for pr in [pg[0]] for l, _ in pr)
                    if parent_only:
                        res["flags"].append(f"parent_only_balance:p{i+1}")
                        acc, last = {}, -9
                    elif company_layout(text):
                        res["flags"].append(f"group_company_columns:p{i+1}")
                    elif acc_primary:
                        balances.append({"ta": b[0], "tl": b[1], "te": b[2], "ccy": acc_ccy, "unit": acc_unit, "file": str(path), "page": acc_page, "check": "a_l_e"})
                    acc, last = {}, -9
        doc.close()
    if incomes and not income_void:
        res["income"] = max(incomes, key=lambda x: (x["primary"], abs(x["revenue"] * x["unit"])))
    if balances:
        res["balance"] = max(balances, key=lambda x: x["ta"] * x["unit"])
    return res


def values(res):
    o = {}
    inc, bal = res.get("income"), res.get("balance")
    if inc:
        for k in ("revenue", "pbt", "np", "tax"):
            if inc.get(k) is not None:
                o[k] = inc[k] * inc["unit"]
        o.update(ccy=inc["ccy"], income_page=inc["page"], income_file=inc["file"])
    if bal:
        for k in ("ta", "tl", "te"):
            o[k] = bal[k] * bal["unit"]
        o.update(bal_ccy=bal["ccy"], balance_page=bal["page"], balance_file=bal["file"])
    return o
