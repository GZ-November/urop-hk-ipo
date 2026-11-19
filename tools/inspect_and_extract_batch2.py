from pathlib import Path

ROOT = Path("/Users/georgezhu/Desktop/UROP HK IPO")
RAW_DOCS = ROOT / "analysis" / "out" / "pilot_48_raw_docs"

issuers = [
    ("0968.HK", "Little Sheep Group Limited", "Main Board", 2008, "2_0968_HK"),
    ("1246.HK", "Ngai Shun Holdings Limited", "Main Board", 2013, "2_1246_HK"),
    ("1288.HK", "Agricultural Bank of China Limited - H Shares", "Main Board", 2010, "2_1288_HK"),
    ("1299.HK", "AIA Group Limited", "Main Board", 2010, "2_1299_HK"),
    ("1318.HK", "Greens Holdings Limited", "Main Board", 2009, "2_1318_HK"),
    ("1333.HK", "China Zhongwang Holdings Limited", "Main Board", 2009, "2_1333_HK"),
    ("1989.HK", "Pine Care Group Limited", "Main Board", 2017, "2_1989_HK"),
    ("2289.HK", "Chuangmei Pharmaceutical Co., Ltd.", "Main Board", 2015, "2_2289_HK"),
    ("2722.HK", "Chongqing Machinery & Electric Co., Ltd. - H Shares", "Main Board", 2008, "2_2722_HK"),
    ("8267.HK", "Linekong Interactive Co., Ltd.", "GEM", 2014, "2_8267_HK"),
    ("8325.HK", "Oriental City Group Holdings Ltd.", "GEM", 2009, "2_8325_HK"),
    ("8348.HK", "Tianjin Binhai Teda Logistics (Group) Corporation Ltd. - H Shares", "GEM", 2008, "2_8348_HK")
]

for code, name, board, cohort, dir_name in issuers:
    print(f"\n{'='*70}\n[{code}] {name} ({cohort}, {board})\n{'='*70}")
    p = RAW_DOCS / dir_name
    files = sorted(list(p.glob("*.pdf")) + list(p.glob("*.PDF")), key=lambda x: x.name)
    
    # Check what files exist
    print("Files:", [f.name for f in files])
