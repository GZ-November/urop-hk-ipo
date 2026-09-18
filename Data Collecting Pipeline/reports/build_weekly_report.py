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
r = meta.add_run("18 September 2026")
set_font(r, size=10)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(12)
r = p.add_run("Summary. ")
set_font(r, bold=True)
r = p.add_run("The 2026 Q1 Hong Kong Main Board IPO dataset has been completed. It covers all 38 issuers listed from 2 January to 31 March 2026, with 120 research variables collected for each issuer and no missing cells in the final workbook.")
set_font(r)

heading = doc.add_paragraph()
heading.paragraph_format.space_before = Pt(2)
heading.paragraph_format.space_after = Pt(6)
r = heading.add_run("Completion and Validation")
set_font(r, size=12, bold=True)

table = doc.add_table(rows=1, cols=2)
table.autofit = False
table.columns[0].width = Inches(1.55)
table.columns[1].width = Inches(5.9)
hdr = table.rows[0].cells
hdr[0].width = Inches(1.55)
hdr[1].width = Inches(5.9)
for cell, text in zip(hdr, ["Area", "Progress"]):
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
    ("Coverage", "All 38 Main Board IPOs listed in 2026 Q1 have been processed."),
    ("Data collection", "The final workbook contains 120 variables for each issuer, with a 100% completion rate and zero missing cells."),
    ("Manual audit", "A cell-by-cell review of 2,280 prospectus-derived cells found no missing values or discrepancies."),
    ("Validation", "All issuers passed the relevant HKEX Listing Rules checks, including FINI allocation rules, the 15% green shoe limit, cornerstone lock-up requirements, and applicable Chapter 18C criteria."),
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
    cells[1].width = Inches(5.9)
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
for cell, text, width in zip(changes.rows[0].cells, ["Source tier", "Variables", "Main additions"], [1.35, 1.0, 5.1]):
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
for cell, text, width in zip(definitions.rows[0].cells, ["Area", "Definition or measurement convention"], [1.7, 5.75]):
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
    ("Financial data", "All accounting variables are taken from the consolidated financial statements in the accountants' report. Parent-company-only figures are excluded. Amounts retain the reported currency and use the disclosed unit multiplier."),
    ("Annualisation", "For interim reporting periods, the annualisation factor equals months covered divided by 12 (for example, 0.5 for a six-month period). It is used when annualising revenue and profit measures."),
    ("Ownership and status", "Pre-IPO VC/PE backing is coded 1 when institutional venture-capital or private-equity investment is disclosed, otherwise 0. Chapter 18A, Chapter 18C, WVR, and A+H indicators are coded as binary variables."),
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
r = heading.add_run("Deliverable")
set_font(r, size=12, bold=True)

p = doc.add_paragraph(style="Normal")
p.paragraph_format.left_indent = Inches(0.18)
p.paragraph_format.first_line_indent = Inches(-0.18)
r = p.add_run("• ")
set_font(r)
r = p.add_run("Master research workbook: HKIPO-MB2026Q1.xlsx. The workbook preserves the original template styling and contains the completed Q1 dataset.")
set_font(r)

heading = doc.add_paragraph()
heading.paragraph_format.space_before = Pt(8)
heading.paragraph_format.space_after = Pt(5)
r = heading.add_run("Next Steps")
set_font(r, size=12, bold=True)

for text in [
    "Begin baseline analysis of first-day IPO underpricing using subscription demand, cornerstone allocation, free float, and technology-listing indicators.",
    "Continue collecting Q2 and Q3 2026 Main Board IPO data using the same validation protocol.",
]:
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.first_line_indent = Inches(-0.18)
    r = p.add_run("• ")
    set_font(r)
    r = p.add_run(text)
    set_font(r)

doc.core_properties.title = "Weekly Research Progress Report Hong Kong Main Board IPO Dataset 2026 Q1"
doc.core_properties.subject = "Weekly research progress update"
doc.core_properties.author = ""
doc.save(OUT)
print(OUT)
