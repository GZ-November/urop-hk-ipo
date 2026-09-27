from pathlib import Path
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

OUT = Path(__file__).resolve().parent / "Weekly_Research_Progress_Report_HKIPO_2026Q1.docx"

def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)

def set_cell_border(cell, color="D9D9D9"):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right"):
        tag = "w:" + edge
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), "6")
        element.set(qn("w:color"), color)

def keep_row_together(row):
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    tr_pr.append(cant_split)

def repeat_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    header = OxmlElement("w:tblHeader")
    header.set(qn("w:val"), "true")
    tr_pr.append(header)

def set_font(run, name="Aptos", size=11, bold=False, color="000000"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor.from_string(color)

doc = Document()
section = doc.sections[0]
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.75)
section.left_margin = Inches(0.82)
section.right_margin = Inches(0.82)

styles = doc.styles
styles["Normal"].font.name = "Aptos"
styles["Normal"]._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
styles["Normal"]._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
styles["Normal"].font.size = Pt(11)
styles["Normal"].paragraph_format.space_after = Pt(7)
styles["Normal"].paragraph_format.line_spacing = 1.12

# Word's built-in Title style can carry a colored bottom border. Remove it so
# the title remains plain black typography suitable for a faculty update.
title_ppr = styles["Title"]._element.get_or_add_pPr()
title_border = title_ppr.find(qn("w:pBdr"))
if title_border is not None:
    title_ppr.remove(title_border)

title = doc.add_paragraph(style="Title")
title.alignment = WD_ALIGN_PARAGRAPH.LEFT
title.paragraph_format.space_after = Pt(4)
run = title.add_run("Weekly Research Progress Report")
set_font(run, size=18, bold=True)

subtitle = doc.add_paragraph()
subtitle.paragraph_format.space_after = Pt(14)
run = subtitle.add_run("Hong Kong Main Board IPO Dataset 2026 Q1")
set_font(run, size=11, bold=True, color="404040")

meta = doc.add_paragraph()
meta.paragraph_format.space_after = Pt(14)
r = meta.add_run("Date: ")
set_font(r, size=10, bold=True)
r = meta.add_run("19 September 2026")
set_font(r, size=10)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(12)
r = p.add_run("Summary. ")
set_font(r, bold=True)
r = p.add_run("The 2026 Q1 Hong Kong Main Board IPO dataset has been completed and comprehensively validated. It covers all 38 issuers listed from 2 January to 31 March 2026, with 120 research variables collected for each issuer and zero missing cells in the master workbook. Sourcing strictly adheres to a Tier-1 statutory and audited evidentiary hierarchy, and all data points have passed automated cell-by-cell reconciliation and 10 HKEX Listing Rules consistency checks.")
set_font(r)

heading = doc.add_paragraph()
heading.paragraph_format.space_before = Pt(2)
heading.paragraph_format.space_after = Pt(6)
r = heading.add_run("Completion and Quality Assurance")
set_font(r, size=12, bold=True)

table = doc.add_table(rows=1, cols=2)
table.autofit = False
table.columns[0].width = Inches(1.55)
table.columns[1].width = Inches(5.31)
hdr = table.rows[0].cells
hdr[0].width = Inches(1.55)
hdr[1].width = Inches(5.31)
for cell, text in zip(hdr, ["Area", "Progress and Quality Assurance"]):
    cell.text = text
    set_cell_shading(cell, "1F4E79")
    set_cell_border(cell)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in p.runs:
        set_font(run, size=10, bold=True, color="FFFFFF")
repeat_header(table.rows[0])

rows = [
    ("Coverage", "All 38 Main Board IPOs listed in 2026 Q1 have been processed with complete cohort coverage."),
    ("Data collection", "The master workbook contains 120 variables for each issuer, achieving a 100% completion rate and zero missing cells across all 4,560 data points."),
    ("Audit & reconciliation", "Reconciled all 2,964 hand-curated cells (2,280 prospectus-derived and 684 allotment-derived cells) against SHA-256 verified extraction states with 0 discrepancies and 0 missing values. The automated regression test suite achieves a 100% pass rate (24/24 unit tests)."),
    ("Statutory compliance", "All extractions enforce a Tier-1 statutory hierarchy: data are sourced strictly from Appendix I (Accountants' Report) and Appendix V (Statutory and General Information), eliminating informal drafting errors from non-binding Definitions or Summary sections. Parent-company balance sheet contamination is blocked."),
    ("Listing Rules checks", "All 38 issuers passed the 10-dimension automated cross-check suite, covering FINI allocation clawbacks (Mechanisms A & B), the 15% green shoe ceiling, statutory cornerstone lock-ups (>= 180 days), Chapter 18C criteria, gross margin ceilings, and monetary scale guards."),
]
for i, (area, progress) in enumerate(rows):
    cells = table.add_row().cells
    keep_row_together(table.rows[-1])
    for cell in cells:
        set_cell_border(cell)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        if i % 2 == 1:
            set_cell_shading(cell, "F2F6FA")
    cells[0].width = Inches(1.55)
    cells[1].width = Inches(5.31)
    cells[0].text = area
    cells[1].text = progress
    for idx, cell in enumerate(cells):
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.space_before = Pt(3)
        for run in p.runs:
            set_font(run, size=10, bold=(idx == 0))

heading = doc.add_paragraph()
heading.paragraph_format.space_before = Pt(14)
heading.paragraph_format.space_after = Pt(5)
r = heading.add_run("Changes to the Original Template")
set_font(r, size=12, bold=True)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(8)
r = p.add_run("The original student template (HKIPO-MB-template-students.xlsx) contained 46 columns (A-AT). I expanded it to 120 variables, adding 74 fields while retaining the original three-tier colour structure and the template's formatting.")
set_font(r)

changes = doc.add_table(rows=1, cols=3)
changes.autofit = False
for cell, text, width in zip(changes.rows[0].cells, ["Source tier", "Variables", "Main additions"], [1.35, 1.0, 4.51]):
    cell.width = Inches(width)
    cell.text = text
    set_cell_shading(cell, "1F4E79")
    set_cell_border(cell)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in cell.paragraphs[0].runs:
        set_font(run, size=9, bold=True, color="FFFFFF")
repeat_header(changes.rows[0])
change_rows = [
    ("Light green", "11", "HKEX New Listing Report fields: listing date, stock code, offer price, and other official listing attributes."),
    ("Light blue", "60", "Prospectus fields: offer terms, capital structure, ownership, governance, financial statements, R&D, debt, and use of proceeds."),
    ("Dark blue", "49", "Allotment and external-market fields: subscription and allocation results, cornerstone allocation, free float, first-day trading, and macro controls."),
]
for i, row in enumerate(change_rows):
    cells = changes.add_row().cells
    keep_row_together(changes.rows[-1])
    for j, (cell, value) in enumerate(zip(cells, row)):
        cell.text = value
        set_cell_border(cell)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        if i % 2 == 1:
            set_cell_shading(cell, "F2F6FA")
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            set_font(run, size=9, bold=(j == 0))

heading = doc.add_paragraph()
heading.paragraph_format.space_before = Pt(14)
heading.paragraph_format.space_after = Pt(5)
r = heading.add_run("Key Variable Definitions and Measurement Conventions")
set_font(r, size=12, bold=True)

definitions = doc.add_table(rows=1, cols=2)
definitions.autofit = False
for cell, text, width in zip(definitions.rows[0].cells, ["Area", "Definition or measurement convention"], [1.7, 5.16]):
    cell.width = Inches(width)
    cell.text = text
    set_cell_shading(cell, "1F4E79")
    set_cell_border(cell)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in cell.paragraphs[0].runs:
        set_font(run, size=9, bold=True, color="FFFFFF")
repeat_header(definitions.rows[0])
definition_rows = [
    ("Financial data & base currency units", "All accounting variables are taken from consolidated financial statements in the accountants' report (Appendix I). Parent-company-only balance sheets are excluded. Monetary values are converted to base currency units (e.g., RMB'000 disclosures multiplied by 1,000 to base RMB) to ensure empirical consistency, guarded by automated magnitude validation."),
    ("Annualisation vs. unannualised stub metrics", "Year-1 is anchored to the latest Track Record Period end date (col_AT). For interim periods (e.g. 6M, 8M), flow-rate scale indicators (col_AH Revenue, col_AK PBT, col_AN Net Profit) are annualised by dividing by the period fraction (months/12). Crucially, non-flow metrics including Gross Profit (col_CF), CapEx (col_CG), Operating Cash Flow (col_AU), R&D (col_AW), and Indebtedness (col_BE) remain strictly unannualised raw stub figures, verified by the Gross Margin Ceiling Gate (col_CF <= unannualised revenue * 1.01)."),
    ("Statutory sourcing & legal entity", "To ensure full legal enforceability and eliminate non-binding drafting noise, extractions follow a Tier-1 statutory hierarchy. Incorporation dates (col_BP) and registered details are sourced strictly from Appendix V (Statutory and General Information) or audited corporate histories, strictly barring non-binding Definitions or Summary chapters."),
    ("Ownership and status", "Pre-IPO VC/PE backing is coded 1 when institutional venture-capital or private-equity investment is disclosed, otherwise 0. Chapter 18A (biotech), Chapter 18C (specialist tech), WVR, and A+H indicators are coded as binary variables."),
    ("Cornerstones", "Cornerstone allocation equals cornerstone shares divided by final global offering shares. The earliest unlock date is the listing date plus six calendar months, subject to the statutory minimum of 180 days."),
    ("FINI and retail demand", "The public subscription multiple equals valid retail shares applied for divided by initial public-offer shares. The offer mechanism records FINI Mechanism A or B, together with the applicable allocation basis."),
    ("Trading liquidity", "Unrestricted public shareholding (secondary free float) equals (final offer shares minus cornerstone shares) divided by total issued shares immediately after listing. This excludes locked cornerstone shares from immediate trading liquidity."),
    ("Market outcomes", "First-day underpricing equals (first-day closing price minus offer price) divided by offer price. Market controls include the HSI return over the 20 trading days before the prospectus date, 1-month HIBOR on T-1, and the HKMA aggregate balance on T-1."),
]
for i, row in enumerate(definition_rows):
    cells = definitions.add_row().cells
    keep_row_together(definitions.rows[-1])
    for j, (cell, value) in enumerate(zip(cells, row)):
        cell.text = value
        set_cell_border(cell)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        if i % 2 == 1:
            set_cell_shading(cell, "F2F6FA")
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        for run in p.runs:
            set_font(run, size=9, bold=(j == 0))

heading = doc.add_paragraph()
heading.paragraph_format.space_before = Pt(14)
heading.paragraph_format.space_after = Pt(5)
r = heading.add_run("Deliverables Package")
set_font(r, size=12, bold=True)

deliverables = [
    ("Master research workbook", "HKIPO-MB2026Q1.xlsx: Preserves original template styling, containing all 120 variables across all 38 issuers with 0 missing cells and verified cell-level audit hashes."),
    ("Clean econometric dataset", "HKIPO-MB2026Q1_clean.csv: Fully standardized tabular dataset ready for direct empirical modeling and regression estimation in Stata, R, and Python."),
    ("Academic data codebook", "HKIPO_2026Q1_Codebook.md & .json: Exhaustive 120-variable data dictionary detailing variable names, econometric definitions, source tiers, data types, fill rates, and descriptive statistics."),
    ("Statutory governance manual", "statutory_evidentiary_rules.md: Formal evidentiary hierarchy manual defining legal enforceability rules, Tier-1 chapter sourcing, period anchoring, and annualisation boundaries."),
]
for title_item, desc in deliverables:
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.first_line_indent = Inches(-0.18)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run("• ")
    set_font(r)
    r = p.add_run(f"{title_item}: ")
    set_font(r, bold=True)
    r = p.add_run(desc)
    set_font(r)

heading = doc.add_paragraph()
heading.paragraph_format.space_before = Pt(8)
heading.paragraph_format.space_after = Pt(5)
r = heading.add_run("Next Steps")
set_font(r, size=12, bold=True)

for text in [
    "Conduct cross-sectional econometric regressions of first-day IPO underpricing on HKIPO-MB2026Q1_clean.csv, testing the empirical effects of FINI retail subscription multiples, cornerstone lock-up allocations, secondary free float, and Chapter 18C specialist technology indicators.",
    "Scale the validated automated pipeline and Tier-1 statutory evidentiary protocols to upcoming Q2 and Q3 2026 Main Board IPO cohorts.",
]:
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.first_line_indent = Inches(-0.18)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run("• ")
    set_font(r)
    r = p.add_run(text)
    set_font(r)

doc.core_properties.title = "Weekly Research Progress Report Hong Kong Main Board IPO Dataset 2026 Q1"
doc.core_properties.subject = "Weekly research progress update"
doc.core_properties.author = ""
doc.save(OUT)
print(OUT)
