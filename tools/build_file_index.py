#!/usr/bin/env python3
"""Build the offline, searchable local file index from canonical paths and the workspace catalog."""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    'excel': 'Excel 数据',
    'csv': 'CSV 数据',
    'reports': '报告与计划',
    'results': '分析结果',
    'definitions': '字段与来源',
    'references': '模板与官方表',
    'history': '历史与恢复',
}
LABELS = {
    '2026_AH_Price_References': '2026 A+H 价格参考',
    '2026_Margin_Financing': '2026 孖展融资数据',
    'All_Years_Master_Panel': '跨年合并数据 · Master',
    'Research_Terminology': '研究术语与样本定义',
    'Variable_Registry': '202 个变量的字段定义',
    'Current_Research_Plan': '当前研究计划',
    'Repairs_and_Remaining_Limits': '数据修复与剩余限制',
    'Research_Design': '研究设计',
    'Research_Start': '研究起点与输入说明',
    'Data_Gaps_and_Collection_Priorities': '数据缺口与采集优先级',
    'Current_Empirical_Research_Report': '当前实证研究报告',
    'Retail_Research_Implementation': '散户研究复现说明',
    'Retail_Mentor_Brief': '导师讨论短稿',
    'Retail_Evidence_Assessment': '散户来源复核与排除说明',
    '2026_Comprehensive_Report': '2026 综合研究报告',
    'Exported_PDF_Reports': '本地 PDF 报告目录',
    'HK_Stock_Market_and_IPO_Overview_Draft': '香港股市与 IPO 概览草稿',
    'HK_IPO_Institutions_Source_Notes': '香港 IPO 制度来源笔记',
    'HK_Stock_Market_Source_Notes': '香港股市来源笔记',
    'US_IPO_Comparison_Source_Notes': '美国 IPO 比较来源笔记',
    '00_basic_statistics': '基础统计与变量覆盖',
    '01_descriptive_statistics': '首日收益描述统计',
    '02_underpricing_regressions': 'IPO 抑价回归',
    '03_retail_returns_and_cornerstones': '散户收益与基石投资者',
    '04_ah_price_anchors': 'A+H 定价',
    '05_margin_financing': '孖展融资分析',
    '06_aftermarket_returns': '上市后收益',
    '07_lockups_stabilization_and_extensions': '禁售期、稳价与扩展分析',
    '08_prediction_and_robustness': '预测与稳健性',
    '09_monthly_analysis': '月度分析',
    '10_q2_analysis': 'Q2 分析',
    '11_return_decomposition': '收益分解',
    '12_subscription_demand': '认购需求与热度',
    '13_retail_allocation_profit': '散户配售与盈利',
    '14_retail_profit_distributions': '散户盈利分布',
    '15_retail_evidence_brief': '散户来源复核配套表格',
    '16_comprehensive_report_tables': '综合报告配套统计表',
    'Audit_and_Exclusion_Reports': '审计与排除记录',
    'Extraction_and_Validation': '披露提取与验证记录',
    'Official_Listing_Sources': 'HKEX 官方上市来源目录',
    'Source_Evidence_and_Market_Data': '原始披露与市场数据',
    'Data_Gap_Collection': '数据缺口采集与修复证据',
    'Legacy_Excel_and_Markdown.tar': '旧 Excel 与 Markdown 归档包',
    'Archive_and_Recovery': '旧版本原路径与恢复说明',
    'All_Years_AH_Price_References': '跨年 A+H 价格参考',
    'Reviews_2026_09_30': '2026-09-30 历史检查',
}


def build() -> int:
    entries = []
    seen = set()

    def add(path: str, label: str, group: str, status: str, note: str = '') -> None:
        source = ROOT / path
        if not source.exists():
            raise ValueError(f'Missing index source: {path}')
        if path in seen:
            return
        seen.add(path)
        entries.append((path, label, group, status, note, source.is_dir()))

    catalog = json.loads((ROOT / 'config/research_workspace.json').read_text())
    for item in catalog['entries']:
        name = Path(item['name'])
        stem = name.stem
        section = name.parts[0]
        label = LABELS.get(stem, stem.replace('_', ' '))
        group, status, note = {
            '01_workbooks': ('excel', '正式工作簿', '2025 Q1–Q2 与 2026 Q1–Q3 正式数据并列保留；原文件位于 pipeline/cohorts/。'),
            '02_research_inputs': ('csv', '研究输入', 'CSV 可用于统计分析，也可用 Excel 打开。'),
            '03_data_dictionary': ('definitions', '字段说明', '查看变量含义、类型、单位与来源。'),
            '04_reports_and_plans': ('reports', '报告 / 计划', ''),
            '05_analysis_results': ('results', '生成结果目录', '进入目录查看统计表、图和结果说明。'),
            '06_sources_and_audits': ('definitions', '来源 / 证据', ''),
            '07_historical_data': ('history', '历史材料', '2025 正式季度数据与旧报告；当前研究按实际上市日期选择 2026。'),
        }[section]
        if stem.endswith('_IPO_Data'):
            label = stem[:7].replace('_', ' ') + ' IPO 数据'
        elif stem.endswith('_Clean_Data'):
            label = stem[:7].replace('_', ' ') + ' 清洗数据'
        elif stem.endswith('_Codebook'):
            label = stem[:7].replace('_', ' ') + ' 变量说明'
        if stem == 'All_Years_Master_Panel':
            note = '包含已存储的 2025 与 2026 数据；2025 仅有 Q1–Q2，并非全年覆盖。'
        if 'Draft' in stem or 'Source_Notes' in stem:
            status = '草稿 / 来源笔记'
        add(item['source'], label, group, status, note)

    for source in sorted((ROOT / 'pipeline/templates').glob('*.xlsx')):
        add(str(source.relative_to(ROOT)), source.name, 'references', '空白模板', '用于建立新工作簿；不是已经采集好的 IPO 数据。')
    for source in sorted((ROOT / 'pipeline/sources').glob('*.xlsx')):
        add(str(source.relative_to(ROOT)), source.stem.replace('_Eng', '') + ' 官方新上市表', 'references', 'HKEX 来源表', '官方新上市原表；普通 IPO 研究范围还需筛选。')
    for source in sorted((ROOT / 'docs/reports/exported_pdfs').glob('*.pdf')):
        add(str(source.relative_to(ROOT)), '2026 综合研究报告 PDF', 'reports', 'PDF 导出稿', '保留原文件名与内容；静态稿的数值应结合当前结果说明阅读。')
    add('docs/maintenance/README.md', '整理记录与恢复说明', 'history', '维护记录')
    add('docs/literature', 'IPO 研究文献', 'references', '文献目录')
    add('dashboard/index.html', 'HK IPO Observatory 数据浏览器', 'results', '交互式数据浏览', '使用已生成的数据快照；不会自动刷新行情。')

    cards = []
    for path, label, group, status, note, is_dir in entries:
        extension = '目录' if is_dir else Path(path).suffix.lstrip('.').upper()
        kind = 'Excel 工作表' if extension in {'XLSX', 'XLS', 'XLSM'} else extension
        search = ' '.join((path, label, GROUPS[group], status, note, extension, kind))
        url = quote(path, safe='/') + ('/' if is_dir else '')
        cards.append(f'<a class="card" href="{url}" data-group="{group}" data-search="{html.escape(search, quote=True)}"><div class="meta"><span>{html.escape(status)}</span><b>{extension}</b></div><h2>{html.escape(label)}</h2><p>{html.escape(note or GROUPS[group])}</p><code>{html.escape(path)}</code><span class="open">打开{extension if is_dir else "文件"} ↗</span></a>')
    filters = '<button class="active" data-filter="all" aria-pressed="true">全部</button>' + ''.join(f'<button data-filter="{key}" aria-pressed="false">{value}</button>' for key, value in GROUPS.items())
    page = '''<!doctype html>
<html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HK IPO · 本地文件导航</title>
<style>
:root{color-scheme:light;--ink:#192d30;--muted:#657678;--accent:#166f66;--line:#dce4df;--paper:#f4f6f1}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1240px;margin:auto;padding:50px 28px}header{display:flex;gap:40px;justify-content:space-between;align-items:center}.eyebrow{font-size:12px;letter-spacing:2px;color:var(--accent);font-weight:700}h1{font-size:clamp(30px,5vw,44px);line-height:1.3;margin:14px 0}header p{max-width:700px;line-height:1.8;color:var(--muted);margin:0}.finder{background:#e5eee5;border-radius:16px;padding:20px;min-width:235px;font-size:14px;line-height:1.8}.finder strong{display:block}.finder code{font-size:15px;color:var(--accent)}.quick{display:flex;flex-wrap:wrap;gap:10px;margin:28px 0}.quick a{color:var(--accent);border:1px solid #b5cfbf;border-radius:9px;padding:10px 15px;background:white;text-decoration:none;font-size:14px}.controls{position:sticky;top:0;z-index:2;background:var(--paper);padding:14px 0 12px}label{display:block;font-size:14px;font-weight:600;margin-bottom:9px}input{width:100%;padding:15px 18px;border:1px solid #b7c9c0;border-radius:12px;background:white;font:inherit;outline-color:var(--accent)}.filters{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}button{background:transparent;color:var(--muted);border:1px solid var(--line);border-radius:20px;padding:8px 13px;font:inherit;font-size:13px;cursor:pointer}button.active{background:var(--ink);color:white;border-color:var(--ink)}.status{font-size:13px;color:var(--muted);margin:15px 0}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.card{display:flex;flex-direction:column;min-height:215px;padding:20px;background:white;border:1px solid var(--line);border-radius:13px;text-decoration:none;color:inherit;transition:border-color .15s,box-shadow .15s}.card:hover{border-color:var(--accent);box-shadow:0 4px 15px #173b3010}.card:focus-visible{outline:3px solid var(--accent);outline-offset:2px}.meta{display:flex;justify-content:space-between;font-size:11px;color:var(--accent);gap:8px}.meta b{background:#f0f4ef;padding:3px 7px;border-radius:4px;white-space:nowrap}h2{font-size:18px;font-weight:650;line-height:1.4;margin:17px 0 10px}.card p{font-size:13px;line-height:1.6;color:var(--muted);margin:0 0 12px}.card code{font-size:11px;line-height:1.6;overflow-wrap:anywhere;color:#74827f;margin-bottom:15px}.open{font-size:12px;color:var(--accent);margin-top:auto}[hidden]{display:none!important}.empty{padding:40px;border:1px dashed var(--line);border-radius:12px;color:var(--muted)}footer{margin-top:35px;padding-top:20px;border-top:1px solid var(--line);font-size:12px;line-height:1.8;color:var(--muted)}footer a{color:var(--accent)}@media(max-width:850px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}header{display:block}.finder{margin-top:20px}}@media(max-width:550px){main{padding:28px 16px}.grid{grid-template-columns:1fr}.controls{position:static}}
</style></head><body><main>
<header><div><div class="eyebrow">HK IPO / LOCAL RESEARCH FILES</div><h1>你要找的资料，从这里打开。</h1><p>按用途浏览，或搜索年份、季度、文件名和研究主题。Excel、CSV、报告、模板及历史备份都有明确标记。</p></div><div class="finder"><strong>在 Finder 中浏览文件</strong>回到项目根目录，双击<br><code>00_Research_Files</code><br>进入七个分类文件夹。</div></header>
<nav class="quick" aria-label="常用文件"><a href="pipeline/cohorts/HKIPO-MB2025Q1.xlsx">2025 Q1 Excel</a><a href="pipeline/cohorts/HKIPO-MB2025Q2.xlsx">2025 Q2 Excel</a><a href="pipeline/cohorts/HKIPO-MB2026Q1.xlsx">2026 Q1 Excel</a><a href="pipeline/cohorts/HKIPO-MB2026Q2.xlsx">2026 Q2 Excel</a><a href="pipeline/cohorts/HKIPO-MB2026Q3.xlsx">2026 Q3 Excel</a><a href="pipeline/exports/HKIPO-MB-MASTER_clean.csv">合并 CSV</a><a href="docs/reports/HK_IPO_2026_COMPREHENSIVE_REPORT.md">综合报告</a></nav>
<div class="controls"><label for="search">查找文件</label><input id="search" type="search" placeholder="例如：2026 Q2、Excel、孖展、基石、导师、PDF、模板" autocomplete="off"><div class="filters">FILTERS</div></div><p id="count" class="status" aria-live="polite"></p><div class="grid">CARDS</div><p id="empty" class="empty" hidden>没有找到匹配的文件。可以减少关键词，或切换到“全部”。</p>
<footer>快捷链接指向项目内的原文件；数据更新后从同一路径打开。跨年 Master 包含已存储的 2025 与 2026 数据，历史覆盖不等于全年覆盖。浏览器对 Excel 的打开方式取决于系统设置，也可以从 Finder 快捷目录用 Excel 打开。<br><a href="research_workspace/README.md">分类目录说明</a> · <a href="docs/maintenance/FILE_ORGANIZATION_2026-10-04.md">本次整理与恢复说明</a> · 导航内容更新：<code>python3 tools/build_file_index.py</code></footer>
</main><script>
const cards=[...document.querySelectorAll('.card')],buttons=[...document.querySelectorAll('[data-filter]')],search=document.querySelector('#search');let active='all';
function update(){const terms=search.value.trim().toLocaleLowerCase().split(/\\s+/).filter(Boolean);let count=0;for(const card of cards){const matches=(active==='all'||card.dataset.group===active)&&terms.every(term=>card.dataset.search.toLocaleLowerCase().includes(term));card.hidden=!matches;if(matches)count++;}document.querySelector('#count').textContent=`显示 ${count} / ${cards.length} 个文件与目录`;document.querySelector('#empty').hidden=count!==0;}
search.addEventListener('input',update);for(const button of buttons)button.addEventListener('click',()=>{active=button.dataset.filter;for(const other of buttons){const selected=other===button;other.classList.toggle('active',selected);other.setAttribute('aria-pressed',String(selected));}update();});update();
</script></body></html>'''
    page = page.replace('FILTERS', filters).replace('CARDS', '\n'.join(cards))
    (ROOT / '00_START_HERE.html').write_text(page, encoding='utf-8')
    return len(entries)


if __name__ == '__main__':
    print(f'Local file index: {build()} entries generated.')
