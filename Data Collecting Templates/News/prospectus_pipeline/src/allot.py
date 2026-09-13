"""Prepare separately identified allotment evidence; never write unreviewed figures."""
import hashlib
import json
import re
from urllib.parse import urljoin, urlparse

import fitz
import requests

RULES = '''# 基石核对规则（2026-09-10 核实）
- BS（旧 BV）：保留招股书名单，按最终配发公告校准实际参与者；逐项记录差异。
- BC：最终基石股数 / 不含超额配售的 base offer 股数。逐行求和核对 Total；承诺金额不得代替最终获配。公告百分比只用于舍入交叉检查。须区分 Offer Size Adjustment（扩大发售）与 Over-allotment（绿鞋）；最终 base offer 包含已行使的前者、排除后者。
- BH：读取招股书协议的禁售起点、期间、例外和各投资者安排，再结合上市日推算最早解禁日。优先核对公告的 Last day subject to lock-up；该日为最后禁售日，最早解禁日取次日。月份按日历月，不能按 180 天。没有条款证据则 NA。
- 2025-08-04 改革保留六个月基石禁售要求，未采纳分阶段解禁；不得提示模型假设三个月解禁。
  官方来源：https://www.hkex.com.hk/News/Regulatory-Announcements/2025/2508012news?sc_lang=en
- BI：基石身份不构成 pre-IPO VC/PE 证据；1/0 均需支持，无证据填 NaN。
- 每项证据须含 source（prospectus/allotment）、URL、PDF 页码和原文；两个文件的页码不可混用。
- 绿鞋实际行使状态需另查行使公告；不得从配发公告中的“假设未行使”推断。
- 本阶段仅准备证据，不能作为通过 validate/write 的抽取结果。核对后的数值另行审核。
'''


def prepare_allot(cfg, companies):
    index = json.loads((cfg['paths']['out'] / 'allotment_index.json').read_text())
    base = cfg['paths']['data'] / 'allotment'
    base.mkdir(parents=True, exist_ok=True)
    results = []
    for company in companies:
        code = company['code']
        folder = base / re.sub(r'[^0-9A-Za-z.-]', '_', code)
        folder.mkdir(exist_ok=True)
        result = {'code': code, 'status': 'error'}
        try:
            matches = [r for r in index if r['code'] == code]
            if len(matches) != 1:
                raise ValueError(f'Expected exactly one index entry, found {len(matches)}')
            rec = matches[0]
            url = urljoin(cfg['hkex']['base_url'], rec['file'])
            if urlparse(url).hostname not in {'www1.hkexnews.hk', 'www.hkexnews.hk'}:
                raise ValueError('Unexpected announcement host')
            pdf = folder / 'allotment.pdf'
            if not pdf.exists():
                response = requests.get(url, timeout=60)
                response.raise_for_status()
                if not response.content.startswith(b'%PDF-'):
                    raise ValueError('Response is not PDF')
                with fitz.open(stream=response.content, filetype='pdf') as doc:
                    if not doc.page_count:
                        raise ValueError('Empty PDF')
                temp = pdf.with_suffix('.part')
                temp.write_bytes(response.content)
                temp.replace(pdf)
            with fitz.open(pdf) as doc:
                pages = [{'source': 'allotment', 'url': url, 'page': i + 1,
                          'text': p.get_text()} for i, p in enumerate(doc)]
            if not any(p['text'].strip() for p in pages):
                raise ValueError('No text layer; OCR/manual review required')
            (folder / 'pages.jsonl').write_text(''.join(json.dumps(p, ensure_ascii=False) + '\n' for p in pages))
            # Full document avoids losing multi-page investor table continuations.
            packet = RULES + '\n公司：' + json.dumps(company, default=str, ensure_ascii=False)
            packet += '\n公告日期：' + rec['datetime'] + '\n来源：' + url + '\n'
            packet += ''.join(f"\n<<<ALLOTMENT PAGE {p['page']}>>>\n{p['text']}" for p in pages)
            (folder / 'packet.md').write_text(packet)
            result.update(status='prepared', url=url, pages=len(pages),
                          sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(), packet=str(folder / 'packet.md'))
        except Exception as exc:
            result['error'] = f'{type(exc).__name__}: {exc}'
        (folder / 'manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
        results.append(result)
        print(code, result['status'], result.get('error', ''))
    # Per-company manifests preserve prior results on filtered runs.
    if any(r['status'] == 'error' for r in results):
        raise RuntimeError('Allotment preparation failed; see per-company manifest.json')
    return results
