# Task C: 48-Issuer Stratified Pilot Sample Design & Source Availability Probe Report

**Execution Date**: 2026-11-12  
**Universe**: 2,637 pre-2025 Hong Kong IPOs (1994–2024) from `clean_33y_hkipo_panel_1994_2026.csv`  
**Pilot Sample Size**: Exactly 48 issuers (4 stratified batches × 12 issuers = 36 Main Board + 12 GEM)  
**Random Seed**: `20261112` (100% deterministic & reproducible)  

---

## 1. Executive Summary & Source Discovery Architecture

This probe evaluates the historical feasibility of scaling the Hong Kong IPO collection pipeline across the 33-year study horizon (1994–2026).

### Key Archaeological Findings on HKEX Electronic Disclosure
1. **The April 1, 1999 Digital Discontinuity**:
   - HKEX's electronic disclosure database (`www1.hkexnews.hk`) begins on **April 1, 1999**.
   - All pre-April 1999 IPOs (e.g. 1994–1998) were published strictly as physical newspaper advertisements (in South China Morning Post, Wen Wei Po, Ta Kung Pao) and printed booklets distributed to bank branches.
   - Online title search returns zero records for pre-April 1999 dates. These issuers require alternative archival lookup via ISIN, Bloomberg Action ID, and university microfiche archives.
2. **The June 25, 2007 Taxonomy Overhaul**:
   - Modern HKEX searches rely on Headline Categories (`rbAfter2006`, `searchType=1`). Prior to June 25, 2007, filings were categorized by legacy Document Types (`rbPrior2006`, `searchType=2`).
   - **Critical Breakthrough**: Setting `searchType=0` (`rbAll`) in `titleSearchServlet.do` allows programmatic querying across the entire digital lifespan (April 1999 through present), unlocking pre-2007 prospectuses and allotment announcements.
3. **Active vs Inactive Securities Query Architecture**:
   - HKEX segregates active securities (`activestock_sehk_e.json`, 17,581 items) and delisted/inactive securities (`inactivestock_sehk_e.json`, 893 items).
   - Querying an inactive `stockId` with `category='0'` returns 0 results; it requires `category='1'`. Our dual category search dynamically handles active and inactive entities without silent omissions.
4. **Generic Headline Conventions in Early Digital Era (1999–2003)**:
   - During 1999–2003, issuers frequently filed allotment results announcements and prospectuses under the generic title `" Announcement "` or `" New Listing "` (or in early `.doc` binary OLE format).
   - Automated harvesting must evaluate internal HTML text strings (`"Announcement of Offer Price..."`) and date proximity to the listing date.

## 2. 48-Issuer Stratified Sample Architecture

| Batch ID | Epoch | Total N | Pilot MB | Pilot GEM | Total Pilot | Key Stratification Criteria Satisfied |
|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **Batch 1** | 2018–2024 | 819 | 9 | 3 | 12 | 3 Small, 3 Mid, 3 Large terciles; 2 H-shares, 7 Cayman/Red-chip; Ch. 8A WVR (9988 Alibaba) & Ch. 18A Biotech (1672 Ascletis); 2 Delisted (1712, 1821); 3 near PN18 15x (6119, 2025, 1672) |
| **Batch 2** | 2008–2017 | 933 | 9 | 3 | 12 | 3 Small, 3 Mid, 3 Large terciles; 3 H-shares, 6 non-H; GEM placing-only (8325, 8348) vs public offer (8267); 4 Delisted/Recycled (1989, 1318, 0968, 1333); 3 near PN18 15x (1246, 2289, 1318); AIA large-cap clawback waiver |
| **Batch 3** | 2002–2007 | 447 | 9 | 3 | 12 | 3 Small, 3 Mid, 3 Large terciles; SOE mega-deals (0939 CCB, 2628 China Life) vs landmark private tech (0700 Tencent); 3 GEM 2002–2004 tech (8159, 8077, 8160); 3 Delisted/Recycled (0587, 0249, 0999); covers both 2002–2004 (6) and 2005–2007 (3) |
| **Batch 4** | 1994–2001 | 438 | 9 | 3 | 12 | Exactly 5 MB pre-1999 cutoff (1033, 0992, 0987, 0345, 0297); 4 MB post-1999 (0857 PetroChina, 0066 MTR, 0100 Clear Media, 0934); 3 GEM 1999–2001 dot-com (8005 Yuxing, 8006 Sunevision, 8028 Timeless); covers H-shares, Red-chips, Local HK ISINs, Recycled tickers |
| **Total** | **1994–2024** | **2,637** | **36** | **12** | **48** | **100% of stratification constraints strictly satisfied** |

## 3. Source Availability Probe Results by Batch

### Batch 1 (2018-2024, N=12)

| Stock Code | Company Name | Board | Cohort | Size Tercile | Funds Raised (HKD) | HKEX Status | Prospectus Format | Allotment Format | Stratification Role |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `1712.HK` | Dragon Mining Limited | Main Board | 2018 | Small | 101.5M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Small Tercile, Delisted/Acquired, Cayman |
| `6119.HK` | Tian Yuan Group Holdings  | Main Board | 2018 | Small | 127.5M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Small Tercile, PN18 near 15x (16.88x), Cayman |
| `1749.HK` | Shanshan Brand Management | Main Board | 2018 | Small | 126.3M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Small Tercile, H-share (PRC joint stock) |
| `2025.HK` | Ruifeng Power Group Compa | Main Board | 2018 | Mid | 336.0M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Mid Tercile, PN18 near 15x (17.0x), Cayman |
| `1743.HK` | Zhejiang Cangnan Instrume | Main Board | 2019 | Mid | 282.8M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Mid Tercile, H-share (PRC joint stock) |
| `3738.HK` | Vobile Group Limited | Main Board | 2018 | Mid | 236.6M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Mid Tercile, Cayman Industrial |
| `9988.HK` | Alibaba Group Holding Lim | Main Board | 2019 | Large | 101,200.0M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Large Tercile, Chapter 8A WVR Mega-deal, Cayman |
| `1821.HK` | ESR Cayman Limited | Main Board | 2019 | Large | 14,064.7M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Large Tercile, Delisted/Acquired, Cayman |
| `1672.HK` | Ascletis Pharma Inc. - B | Main Board | 2018 | Large | 3,137.9M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Large Tercile, Chapter 18A Biotech, PN18 10.0x, Cayman |
| `8447.HK` | MS Concept Ltd. | GEM | 2018 | N/A (GEM) | 67.5M | online_query_success | `single_pdf` | `multi_section_html_pdf` | GEM Public Offer, F&B |
| `8516.HK` | Grand Talents Group Holdi | GEM | 2018 | N/A (GEM) | 48.0M | online_query_success | `single_pdf` | `multi_section_html_pdf` | GEM Public Offer, Manufacturing |
| `8645.HK` | Nomad Technologies Holdin | GEM | 2019 | N/A (GEM) | 60.0M | online_query_success | `single_pdf` | `multi_section_html_pdf` | GEM Public Offer, Tech |

### Batch 2 (2008-2017, N=12)

| Stock Code | Company Name | Board | Cohort | Size Tercile | Funds Raised (HKD) | HKEX Status | Prospectus Format | Allotment Format | Stratification Role |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `1246.HK` | Ngai Shun Holdings Limite | Main Board | 2013 | Small | 107.0M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Small Tercile, PN18 near 15x (21.2x), Cayman |
| `2289.HK` | Chuangmei Pharmaceutical  | Main Board | 2015 | Small | 240.8M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Small Tercile, H-share, PN18 near 15x (22.93x) |
| `1989.HK` | Pine Care Group Limited | Main Board | 2017 | Small | 205.7M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Small Tercile, Recycled Ticker (Sun Hing Vision) |
| `1318.HK` | Greens Holdings Limited | Main Board | 2009 | Mid | 558.9M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Mid Tercile, Recycled Ticker, PN18 near 15x (15.63x) |
| `2722.HK` | Chongqing Machinery & Ele | Main Board | 2008 | Mid | 1,306.4M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Mid Tercile, H-share (Chongqing Machinery) |
| `0968.HK` | Little Sheep Group Limite | Main Board | 2008 | Mid | 779.7M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Mid Tercile, Recycled Ticker (Little Sheep), Cayman |
| `1299.HK` | AIA Group Limited | Main Board | 2010 | Large | 159,078.0M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Large Tercile, Mega-deal, Large-cap Clawback Waiver |
| `1288.HK` | Agricultural Bank of Chin | Main Board | 2010 | Large | 93,515.3M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Large Tercile, Landmark SOE H-share Mega-deal (AgBank) |
| `1333.HK` | China Zhongwang Holdings  | Main Board | 2009 | Large | 9,844.1M | online_query_success | `single_pdf` | `multi_section_html_pdf` | MB Large Tercile, Delisted/Acquired Mega-deal (China Zhongwang) |
| `8325.HK` | Oriental City Group Holdi | GEM | 2009 | N/A (GEM) | 34.5M | online_query_success | `single_pdf` | `single_pdf` | GEM Placing-Only (Target Storage) |
| `8267.HK` | Linekong Interactive Co., | GEM | 2014 | N/A (GEM) | 826.6M | online_query_success | `single_pdf` | `single_pdf` | GEM Public Offer (Linekong Interactive) |
| `8348.HK` | Tianjin Binhai Teda Logis | GEM | 2008 | N/A (GEM) | 176.8M | online_query_success | `single_pdf` | `single_pdf` | GEM Placing-Only (Binmiao Brand) |

### Batch 3 (2002-2007, N=12)

| Stock Code | Company Name | Board | Cohort | Size Tercile | Funds Raised (HKD) | HKEX Status | Prospectus Format | Allotment Format | Stratification Role |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `0612.HK` | China Investment Fund Co  | Main Board | 2002 | Small | 30.0M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Early 2002-2004 Small Tercile, Cayman |
| `0587.HK` | Hua Han Bio-Pharmaceutica | Main Board | 2002 | Small | 117.0M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Early 2002-2004 Small Tercile, Recycled Ticker (Hua Han Bio) |
| `0483.HK` | Bauhaus International (Ho | Main Board | 2005 | Small | 130.8M | online_query_success | `multi_section_html_pdf` | `single_pdf` | MB Late 2005-2007 Small Tercile, Retail (Bauhaus) |
| `0249.HK` | Harbin Brewery Group Ltd | Main Board | 2002 | Mid | 434.1M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Early 2002-2004 Mid Tercile, Recycled Ticker (Harbin Brewery) |
| `1126.HK` | Dream International Ltd | Main Board | 2002 | Mid | 195.0M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Early 2002-2004 Mid Tercile, Industrial (Dream Int) |
| `0999.HK` | I.T Limited | Main Board | 2005 | Mid | 667.0M | online_query_success | `multi_section_html_pdf` | `single_pdf` | MB Late 2005-2007 Mid Tercile, Delisted/Acquired (I.T Limited) |
| `0700.HK` | Tencent Holdings Ltd | Main Board | 2004 | Large | 1,787.8M | online_query_success | `multi_section_html_pdf` | `single_pdf` | MB Early 2002-2004 Large Tercile, Landmark Private Tech Firm (Tencent) |
| `2628.HK` | China Life Insurance Comp | Main Board | 2003 | Large | 26,713.8M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Early 2002-2004 Large Tercile, Landmark SOE Mega-deal (China Life) |
| `0939.HK` | China Construction Bank C | Main Board | 2005 | Large | 71,578.3M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Late 2005-2007 Large Tercile, Landmark SOE Mega-deal (CCB) |
| `8159.HK` | Glory Mark Hi-Tech (Holdi | GEM | 2002 | N/A (GEM) | 34.4M | online_query_success | `multi_section_html_pdf` | `single_pdf` | GEM 2002-2004 Tech/Small-cap, Public Offer (Glory Mark) |
| `8077.HK` | Infoserve Technology Corp | GEM | 2002 | N/A (GEM) | 50.7M | online_query_success | `multi_section_html_pdf` | `single_pdf` | GEM 2002-2004 Tech/Small-cap, Placing-only, Recycled Ticker |
| `8160.HK` | MediaNation Inc. | GEM | 2002 | N/A (GEM) | 445.6M | online_query_success | `multi_section_html_pdf` | `single_pdf` | GEM 2002-2004 Tech/Small-cap, Public Offer, Recycled Ticker |

### Batch 4 (1994-2001, N=12)

| Stock Code | Company Name | Board | Cohort | Size Tercile | Funds Raised (HKD) | HKEX Status | Prospectus Format | Allotment Format | Stratification Role |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `1033.HK` | Yizheng Chemical Fibre Co | Main Board | 1994 | Pre-1999 | 2,380.0M | pre_1999_hkexnews_cutoff | `missing_on_hkexnews` | `missing_on_hkexnews` | MB Pre-1999 (1994) Landmark H-share (Sinopec Yizheng) |
| `0992.HK` | Legend Holdings Ltd | Main Board | 1994 | Pre-1999 | 242.4M | pre_1999_hkexnews_cutoff | `missing_on_hkexnews` | `missing_on_hkexnews` | MB Pre-1999 (1994) Local HK Industrial (Legend / Lenovo, HK ISIN) |
| `0987.HK` | Albatronics (Far East) Co | Main Board | 1994 | Pre-1999 | 89.0M | pre_1999_hkexnews_cutoff | `missing_on_hkexnews` | `missing_on_hkexnews` | MB Pre-1999 (1994) Delisted/Recycled Ticker (Albatronics) |
| `0345.HK` | Vitasoy Int'l Holdings Lt | Main Board | 1994 | Pre-1999 | 290.0M | pre_1999_hkexnews_cutoff | `missing_on_hkexnews` | `missing_on_hkexnews` | MB Pre-1999 (1994) Local HK Consumer/Industrial (Vitasoy, HK ISIN) |
| `0297.HK` | Wah Tak Fung Holdings Ltd | Main Board | 1996 | Pre-1999 | 259.4M | pre_1999_hkexnews_cutoff | `missing_on_hkexnews` | `missing_on_hkexnews` | MB Pre-1999 (1996) Red-chip / Bermuda (Wah Tak Fung) |
| `0857.HK` | PetroChina Co Ltd - H Sha | Main Board | 2000 | Post-1999 | 22,329.7M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Post-1999 (2000) Landmark H-share Mega-deal (PetroChina) |
| `0066.HK` | MTR Corporation Ltd | Main Board | 2000 | Post-1999 | 10,787.0M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Post-1999 (2000) Landmark HK Privatisation (MTR, HK ISIN) |
| `0100.HK` | Clear Media Ltd | Main Board | 2001 | Post-1999 | 874.9M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Post-1999 (2001) Recycled Ticker (Clear Media) |
| `0934.HK` | Sinopec Kantons Holdings  | Main Board | 1999 | Post-1999 | 293.2M | online_query_success | `multi_section_html_pdf` | `multi_section_html_pdf` | MB Post-1999 (1999) Red-chip / Sinopec Kantons |
| `8005.HK` | Yuxing InfoTech Holdings  | GEM | 2000 | N/A (GEM) | 420.0M | online_query_success | `single_pdf` | `single_pdf` | GEM 1999-2001 Dot-com Tech (Yuxing Info) |
| `8006.HK` | hongkong.com Corporation | GEM | 2000 | N/A (GEM) | 1,383.7M | online_query_success | `multi_section_html_pdf` | `single_pdf` | GEM 1999-2001 Dot-com Tech (Sunevision) |
| `8028.HK` | Timeless Software Ltd | GEM | 1999 | N/A (GEM) | 450.0M | online_query_success | `multi_section_html_pdf` | `single_pdf` | GEM 1999-2001 First Batch Nov 1999 (Timeless Software) |

## 4. Overall Source Availability & Format Summary

- **Total Pilot Sample**: 48 issuers
- **Pre-April 1999 Cutoff (Physical Newspaper / Microfiche Only)**: 5 issuers (10.4%)
- **Eligible for HKEXnews Electronic Retrieval (1999–2024)**: 43 issuers
  * **Prospectus Discovered Online**: 43 / 43 (100.0%)
  * **Allotment Results Discovered Online**: 43 / 43 (100.0%)

### Online Document Format Breakdown (1999–2024 Eligible Issuers)

| Document Type | `single_pdf` | `multi_section_html_pdf` | `ms_word_doc` / Other | `missing_on_hkexnews` | Total Online Discovered |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Prospectus** | 22 | 21 | 0 | 5 | 43 |
| **Allotment Results** | 12 | 31 | 0 | 5 | 43 |

## 5. Engineering Guidance for Historical Pipeline Scaling

1. **Pre-1999 Ingestion Standard**:
   - Automated web querying of `hkexnews.hk` must be bypassed for `listing_date < 1999-04-01`.
   - Primary evidence sources for 1994–1998 are: (i) Bloomberg Corporate Actions / Prospectus Archive (`bbg_action_id`), (ii) Scanned historical prospectuses in university library special collections (HKU, CUHK, HKUST), and (iii) South China Morning Post / Ta Kung Pao public offer announcement scans.
2. **Multi-Section HTML/PDF Harvester**:
   - For 1999–2006 prospectuses, `ltn*.htm` wrapper pages must be fetched and parsed to extract internal PDF bundle section links (e.g. `Prospectus - Business.pdf`, `Prospectus - Financial Information.pdf`).
3. **Delisted & Recycled Ticker Ingestion**:
   - The extraction orchestrator must preload `inactivestock_sehk_e.json` to map delisted tickers directly to their immutable historical `stockId`, preventing modern ticker reuse collisions.

---
**Artifacts Generated**:  
- Stratified Sample Table: `/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026/pilot_48_stratified_sample.csv`  
- Source Probe Table: `/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026/pilot_48_source_probe.csv`  
- Full Documentation: `/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026/pilot_48_design_and_probe_report.md`  
