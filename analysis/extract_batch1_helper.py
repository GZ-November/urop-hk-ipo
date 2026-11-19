import os
import glob
import pymupdf

RAW_DOCS_DIR = "analysis/out/pilot_48_raw_docs"
PACKETS_DIR = "analysis/out/pilot_48_packets"
OUT_FILE = "/tmp/batch1_full_targets.txt"

deals = [
    "1_1672_HK", "1_1712_HK", "1_1743_HK", "1_1749_HK",
    "1_1821_HK", "1_2025_HK", "1_3738_HK", "1_6119_HK",
    "1_8447_HK", "1_8516_HK", "1_8645_HK", "1_9988_HK"
]

with open(OUT_FILE, "w", encoding="utf-8") as out:
    for deal in deals:
        deal_dir = os.path.join(RAW_DOCS_DIR, deal)
        out.write(f"\n{'='*80}\nISSUER: {deal}\n{'='*80}\n")
        print(f"Processing {deal}...")

        # 1. Process Allotment Result files
        allot_files = sorted(glob.glob(os.path.join(deal_dir, "allot_*.pdf")) + glob.glob(os.path.join(deal_dir, "allot_*.PDF")))
        out.write(f"\n--- ALLOTMENT RESULTS ({len(allot_files)} files) ---\n")
        for af in allot_files:
            fname = os.path.basename(af)
            doc = pymupdf.open(af)
            out.write(f"\n>> FILE: {fname} ({len(doc)} pages)\n")
            # For allot_sec_1 and allot_sec_2, dump first 6 pages which contain all key numbers & wording
            for pno in range(min(len(doc), 6)):
                text = doc[pno].get_text()
                # If it contains key allotment phrases, dump it
                out.write(f"\n[Allot Page {pno+1}]\n{text}\n")
            # Check if cornerstone or basis of allocation appears on later pages
            for pno in range(6, len(doc)):
                text = doc[pno].get_text()
                if any(w in text.lower() for w in ["cornerstone", "reallocation", "clawback", "basis of allocation", "basis of allotment"]):
                    out.write(f"\n[Allot Page {pno+1} - Key Terms Match]\n{text}\n")
            doc.close()

        # 2. Process Prospectus files
        # Can be prospectus_full.pdf OR modular pros_sec_*.pdf
        pros_files = sorted(glob.glob(os.path.join(deal_dir, "pros*.pdf")) + glob.glob(os.path.join(deal_dir, "pros*.PDF")))
        out.write(f"\n--- PROSPECTUS FILES ({len(pros_files)} files) ---\n")
        
        for pf in pros_files:
            pf_name = os.path.basename(pf)
            doc = pymupdf.open(pf)
            out.write(f"\n>> PROSPECTUS DOC: {pf_name} ({len(doc)} pages)\n")
            
            # If modular, examine all pages of relevant sections, or search keywords
            is_full = "prospectus_full" in pf_name.lower()
            
            # Page range or selective scanning
            if is_full:
                # 1. Cover pages (0 to 6)
                for pno in range(min(7, len(doc))):
                    txt = doc[pno].get_text()
                    out.write(f"\n[Cover Page {pno+1}]\n{txt}\n")
                
                # 2. Search for Share Capital table
                sc_found = 0
                for pno in range(len(doc)):
                    txt = doc[pno].get_text()
                    if "SHARE CAPITAL" in txt and ("Issued and to be issued" in txt or "Shares to be issued" in txt or "Capitalisation Issue" in txt):
                        out.write(f"\n[Share Capital Page {pno+1}]\n{txt}\n")
                        sc_found += 1
                        if sc_found >= 2:
                            break
                            
                # 3. Search for Corporate Information & History
                corp_found = 0
                for pno in range(len(doc)):
                    txt = doc[pno].get_text()
                    if ("CORPORATE INFORMATION" in txt or "Registered office" in txt) and ("Principal place of business" in txt or "Headquarters" in txt):
                        out.write(f"\n[Corporate Info Page {pno+1}]\n{txt}\n")
                        corp_found += 1
                        if corp_found >= 2:
                            break
                            
                hist_found = 0
                for pno in range(len(doc)):
                    txt = doc[pno].get_text()
                    if ("HISTORY AND CORPORATE STRUCTURE" in txt or "HISTORY, DEVELOPMENT AND" in txt or "HISTORY, REORGANISATION AND" in txt) and ("commenced" in txt.lower() or "established" in txt.lower() or "founded" in txt.lower() or "incorporated" in txt.lower()):
                        out.write(f"\n[History Page {pno+1}]\n{txt}\n")
                        hist_found += 1
                        if hist_found >= 2:
                            break

                # 4. Controlling Shareholders
                ctrl_found = 0
                for pno in range(len(doc)):
                    txt = doc[pno].get_text()
                    if ("CONTROLLING SHAREHOLDERS" in txt or "RELATIONSHIP WITH CONTROLLING" in txt) and ("immediate controlling" in txt.lower() or "ultimate controlling" in txt.lower() or "controlling shareholder" in txt.lower()):
                        out.write(f"\n[Controlling Shareholders Page {pno+1}]\n{txt}\n")
                        ctrl_found += 1
                        if ctrl_found >= 2:
                            break

                # 5. Underwriting commission and listing expenses
                und_found = 0
                for pno in range(len(doc)):
                    txt = doc[pno].get_text()
                    if ("UNDERWRITING" in txt) and ("commission" in txt.lower() or "listing expenses" in txt.lower()):
                        if "underwriting commission" in txt.lower() or "total listing expenses" in txt.lower() or "estimated listing expenses" in txt.lower():
                            out.write(f"\n[Underwriting Page {pno+1}]\n{txt}\n")
                            und_found += 1
                            if und_found >= 3:
                                break

                # 6. Accountants' report / Financial Information Statements
                # We need Statement of Profit or Loss / Comprehensive Income, Statement of Financial Position, Statement of Cash flows
                fin_found = 0
                for pno in range(len(doc)):
                    txt = doc[pno].get_text()
                    is_income = ("statement of profit or loss" in txt.lower() or "statements of profit or loss" in txt.lower() or "statement of comprehensive income" in txt.lower() or "statements of comprehensive income" in txt.lower()) and ("revenue" in txt.lower() or "turnover" in txt.lower()) and ("profit before" in txt.lower())
                    is_pos = ("statement of financial position" in txt.lower() or "statements of financial position" in txt.lower() or "balance sheet" in txt.lower()) and ("total assets" in txt.lower() or "total equity" in txt.lower() or "net assets" in txt.lower())
                    is_cf = ("statement of cash flows" in txt.lower() or "cash flows from operating activities" in txt.lower() or "cash generated from operations" in txt.lower()) and ("operating activities" in txt.lower())
                    
                    if is_income or is_pos or is_cf:
                        # Ensure it is a table (has numbers / columns)
                        out.write(f"\n[Financial Table Page {pno+1} - Income/Pos/CF]\n{txt}\n")
                        fin_found += 1
                        if fin_found >= 10:
                            break
            else:
                # Modular section PDF: dump all pages or key pages
                for pno in range(len(doc)):
                    txt = doc[pno].get_text()
                    out.write(f"\n[{pf_name} Page {pno+1}]\n{txt}\n")
            doc.close()

print(f"Extraction complete. Target file written to {OUT_FILE} (size: {os.path.getsize(OUT_FILE)} bytes)")
