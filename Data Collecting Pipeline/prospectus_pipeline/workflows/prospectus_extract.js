// DSH workflow: 招股书字段抽取（packet 起步 + LLM 自主检索 + 独立复核）
//
// args = {
//   packets: [{code, name, packet_path, out_path}],
//   out_dir: "prospectus_pipeline/out/extracted",
//   verify: true           // 是否跑第二阶段独立复核
// }
//
// 设计要点：
//  - 招股书披露位置不模板化，因此 packet 只是"规则 + 字段清单 + 种子切片"，
//    代理必须用 tools_search.py 在页级全文里自行检索补齐。
//  - 输出必须严格符合 contracts.py 定义的 JSON 契约；写盘后自行调用 verify 自检。

const packets = (args && args.packets) || [];
const outDir = (args && args.out_dir) || "prospectus_pipeline/out/extracted";
const doVerify = !args || args.verify !== false;
const isTopicMode = !!(args && (args.topics_mode === true || args.topic_packets));
const topicPackets = (args && args.topic_packets) || [];
if (!packets.length && !topicPackets.length) throw new Error("args.packets 与 args.topic_packets 均为空");

const summarySchema = {
  type: "object",
  properties: {
    code: { type: "string" },
    topic: { type: "string" },
    fields_total: { type: "number" },
    fields_filled: { type: "number" },
    fields_missing: { type: "number" },
    low_confidence: { type: "array", items: { type: "string" } },
    written_path: { type: "string" },
    self_check_passed: { type: "boolean" },
    notes: { type: "string" }
  },
  required: ["code", "fields_total", "fields_filled", "fields_missing", "written_path", "self_check_passed"],
  additionalProperties: false
};

const verifySchema = {
  type: "object",
  properties: {
    code: { type: "string" },
    verdict: { type: "string", enum: ["pass", "fail"] },
    checked_fields: { type: "array", items: { type: "string" } },
    discrepancies: {
      type: "array",
      items: {
        type: "object",
        properties: {
          field: { type: "string" },
          in_file: { type: "string" },
          should_be: { type: "string" },
          page: { type: "string" },
          reason: { type: "string" }
        },
        required: ["field", "reason"],
        additionalProperties: false
      }
    },
    notes: { type: "string" }
  },
  required: ["code", "verdict", "discrepancies"],
  additionalProperties: false
};

const OUTPUT_CONTRACT = `
## 输出契约（机器校验，违反即判失败）

最终写盘的文件必须**只**包含一个 JSON 对象，顶层**只能**有 \`code\` 和 \`fields\` 两个键：

\`\`\`json
{"code":"<股票代码>","fields":{"col_L":{"value":2358977900,"page":333,"quote":"<=200字符原文","confidence":"high"}}}
\`\`\`

- \`fields\` 必须包含字段清单里的**每一个** key，一个都不能少、不能多、不能重复。
- 每个字段entry 只能有 \`value\`/\`page\`/\`quote\`/\`confidence\` 四个键。
- \`page\` 是整数页码；缺失写 \`null\`。\`quote\` 是不超过 200 字符的原文；缺失写 \`""\`。
- 数值字段缺失写字符串 \`"NaN"\`；文本/日期字段缺失写字符串 \`"NA"\`。不要留空，不要写 null 当值。
- 非缺失的字段必须有真实页码和原文摘录，否则校验会失败。`;

const TOOLS_HELP = `
## 你可以（也必须）自己检索全文

packet 里的切片只是种子，**很多披露并不模板化**。凡是在 packet 里找不到、或你不确定的地方，
必须用检索工具在全文里自己找：

\`\`\`bash
python3 prospectus_pipeline/run.py search outline <CODE>                  # 列出每页页首标题，先看结构
python3 prospectus_pipeline/run.py search search <CODE> "<正则>" --context 3 --max 8
python3 prospectus_pipeline/run.py search pages <CODE> 413-415           # 导出指定页原文
\`\`\`

建议检索方向（按需调整正则）：
- 资本化开发成本当期新增：\`capitaliz.*(intangible|development)\`、\`Internal development costs\`、\`Additions\`
- 前五大客户集中度：\`five largest customers\`、\`top five customers\`、\`largest customer\`、\`Customers\`
- 经营现金流与年末现金：\`net cash (used in|from).*operating\`、\`cash and cash equivalents at the end\`
- 承销佣金／绿鞋：\`underwriting commission\`、\`Over-allotment Option\`
- 基石名单：\`Cornerstone Investor\`、\`Cornerstone Placing\`
- 上市途径：\`Chapter 18C\`、\`Chapter 8A\`、\`Biotech\`、\`basis of listing\`、\`Specialist Technology\`

**不要**只依赖 packet；也**不要**凭空猜测。找不到就按契约填 NaN/NA，并在 quote 里说明已检索过。`;

function extractPrompt(item) {
  return `你是 HK IPO 数据库采集员。从一家公司招股书抽取 schema 列出的全部 60 个字段，写成严格 JSON。

## 输入
- 抽取包：\`${item.packet_path}\`
- 公司：${item.code} ${item.name}
- 写盘：\`${item.out_path}\`

## 禁止（做了纯属浪费，且会写错）
- **禁止**读其它公司的 \`out/extracted/*.json\` —— 每家的值都不同，抄了就是错
- **禁止**读 \`prospectus_pipeline/src/*.py\`、README、HANDOFF 等任何文档源码
- **禁止** \`ls\` / \`find\` / \`pwd\` / \`wc\` / \`cat\` 探路 —— 路径上面已给全
- **禁止**调用 skill 工具
- **禁止**直接读 PDF 或 \`data/text/*.jsonl\` 全文
- **每轮尽量一次并行发多个工具调用**，减少来回轮数（轮数直接决定成本）

## 允许的工具（只有这五个）
\`\`\`bash
python3 prospectus_pipeline/run.py search sharecap ${item.code}    # 必跑！股本汇总表（L/M/N/O/P/Q/R/S 全靠它）
python3 prospectus_pipeline/run.py search periods  ${item.code}    # 必跑！财务期间判定（19 个财务字段靠它）
python3 prospectus_pipeline/run.py search bundle   ${item.code}    # 必跑！一次给全部字段候选
python3 prospectus_pipeline/run.py search pages    ${item.code} 4,90,172
python3 prospectus_pipeline/run.py search search   ${item.code} "正则" --context 3 --max 5
\`\`\`
**预算**：上面三个必跑命令之后，最多再调 **15 次**工具。

## 步骤
1. 读 packet（字段契约、单位、期间、手册规则、种子切片都在里面）。
2. **同一轮同时跑** \`sharecap\`、\`periods\`、\`bundle\` 三个命令。
   - \`sharecap\` 给**权威股本汇总表**：L=Total、M=全球发售行、N/O=资本化/转换行、
     P=Sale Shares、Q=新股、R=国际配售、S=香港公开发售。**这些字段只能用这张表**，
     绝不能取「历史沿革」「资本化发行沿革」段落里的数字。
   - \`periods\` 给**财务期间判定**：year-1/2/3 各是哪一期、期末日、年化系数。
     **19 个财务字段一律以它的输出为准，不要自己判断期间。**
     常见坑：招股书有 2022/2023/2024 + 9M2025 时，year-1 是 **9M2025（要年化）**，
     不是 FY2024；销售/税前利润/净利润按系数年化，AU/AW/AX 不年化，AV/BE 是期末余额，AY 是比例。
   - \`bundle\` 给全部字段各自的候选页。
3. 对命中不够确定的字段，用 \`pages\` 看那几页原文核实。
4. 写 JSON（契约见下）。
5. 跑一次 \`python3 prospectus_pipeline/run.py validate --only ${item.code}\`，有 ERROR 再修。
6. 校验通过后运行 \`python3 prospectus_pipeline/run.py state extracted --target prospectus --code ${item.code}\`，记录当前 JSON 的哈希。

${TOOLS_HELP}
${OUTPUT_CONTRACT}

## 手册硬规则（必须遵守）
1. 金额一律换算成**基本货币单位**（HK$125.6 million -> 125600000）；百分比填小数；确认的零填数字 0。
2. **合并报表唯一原则（严防母公司单体报表混淆）**：所有资产、权益、负债、销售、利润、现金流、有息债务等财务指标（V–AN、AU–AY、BE 等）**必须且只能**取自**合并财务报表（CONSOLIDATED Financial Statements / Group）**；**绝对严禁**采纳母公司单体报表（`STATEMENT OF FINANCIAL POSITION OF THE COMPANY` / `COMPANY BALANCE SHEETS`）。year-1/2/3 必须是**同一套历史期间**；year-1 销售/利润若不是全年（如 9 个月），按手册年化并在 quote 注明原始期间；附加流量 AU/AW/AX 一律**不年化**；AV（年末现金）和 BE（有息负债）是期末余额，AY 是客户集中度比例。
3. AU 经营现金流 = net cash from operating activities，**不是**经营利润；AV 现金及等价物**不自动包含**受限现金。
4. AX 只填**当期新增**的资本化开发成本，不是期末余额；表中明确写 \`–\`/nil 时填数字 0。
5. AL/AM/AN 是净利润（profit for the year）；AI/AJ/AK 是税前利润。
6. 承销佣金：招股书按全球发售披露时 AO/AP 填同一比例；只按香港公开发售披露时 AP=0；给金额时用金额÷对应基数；
   **不能**把总上市费用当佣金。AQ 绿鞋只能按招股书披露，**不能默认 15%**。
7. col_CJ 基石名单必须来自真正的 Cornerstone Investors / Cornerstone Placing 名单表，
   **不要**用目录、豁免段、风险因素里的普通提及；无基石填 \`"NA"\`；用分号分隔全称。
8. col_AS 上市途径按招股书披露的 basis of listing / 适用章节填（如 Chapter 18C），**不能**按行业推断；col_DP 中文名填简体。
9. 不确定就填 NaN/NA 并在 quote 里写明原因，**绝对不要猜**；**不要**为了配平等式修改原文数字。`;
}

function verifyPrompt(item) {
  return `你是独立的招股书数据复核员。**不要相信**抽取结果，请自己回到原文重新核对。

## 输入
- 待复核 JSON：\`${item.out_path}\`
- 抽取包（字段清单与规则）：\`${item.packet_path}\`
- 公司：${item.code} ${item.name}

## 任务
1. 读取待复核 JSON 与抽取包。
2. 用检索工具在全文里**独立**核对下面的高风险字段（至少这些，可再抽查其他）：
   - **合并报表唯一性**：确认财务字段（W–AN、AU–AY、BE 等）引用的页码是否来自合并报表（CONSOLIDATED Statements），严禁采纳母公司单体报表（... OF THE COMPANY）
   - 股份结构五个恒等式：M=R+S、M=Q+P、L=N+Q、L=O+M
   - T/U 价格区间，且 U<=T
   - 三年资产 = 权益 + 负债（W/Z/AC、X/AA/AD、Y/AB/AE）
   - AH/AK/AN（year-1 销售、税前利润、净利润）与 AF/AI/AL、AG/AJ/AM 的期间口径是否一致
   - AX 资本化开发成本当期新增（注意区分"当期新增"与"期末余额"，\`–\` 应为 0）
   - AY 前五大客户占比的期间是否与 year-1 一致
   - AO/AP/AQ 佣金的基数口径与绿鞋是否按披露
   - CJ 基石名单是否为真实协议名单（不是目录/豁免段）
   - AR/AS/DP 是否为招股书披露内容、中文名是否简体
3. 命令参考：
   \`python3 prospectus_pipeline/run.py search search ${item.code} "<正则>" --context 3 --max 8\`
   \`python3 prospectus_pipeline/run.py search pages ${item.code} <页码或范围>\`

## 输出
只返回结构化结果：verdict 为 pass/fail；discrepancies 列出每个不一致（field、in_file、should_be、page、reason）。
**不要**修改 JSON 文件本身。若结论为 pass，在返回报告前运行
\`python3 prospectus_pipeline/run.py state reviewed --target prospectus --code ${item.code} --verdict pass\`；
若为 fail 则运行同一命令但使用 \`--verdict fail\`。若发现错误，在 reason 里给出能直接改的正确答案与页码。`;
}

function extractTopicPrompt(item) {
  return `你是 HK IPO 数据库采集员。负责抽取公司【${item.title || item.topic}】主题对应的全部 ${item.fields_count || "对应"} 个字段，写成严格分片 JSON。

## 输入
- 主题分片抽取包：\`${item.packet_path}\`
- 公司：${item.code} ${item.name}
- 主题标识：${item.topic}
- 写盘路径：\`${item.out_path}\`

## 允许的工具（优先使用结构化表格）
\`\`\`bash
python3 prospectus_pipeline/run.py search table   ${item.code}    # 优先！查看预解析结构化表格
python3 prospectus_pipeline/run.py search sharecap ${item.code}    # 股本表权威原页
python3 prospectus_pipeline/run.py search periods  ${item.code}    # 财务期间判定
python3 prospectus_pipeline/run.py search pages    ${item.code} <页码>
python3 prospectus_pipeline/run.py search search   ${item.code} "<正则>" --context 3 --max 5
\`\`\`

## 步骤
1. 读主题 packet（包含本主题字段清单、规则、预解析表格与切片）。
2. 如需补充，优先跑 \`search table ${item.code}\` 或针对性检索命令。
3. 严格按契约写出本主题的 JSON 分片：
\`\`\`json
{"code":"${item.code}","topic":"${item.topic}","fields":{"col_X":{"value":...,"page":...,"quote":"...","confidence":"high"}}}
\`\`\`
- 必须包含本主题分片清单里的每一个 key，不要输出其它主题字段。
- 每个 entry 只能有 value/page/quote/confidence 四个键。
- page 为正整数或 null，quote 为原文摘录（<=200字）或 ""。
- 数值缺失填 "NaN"，文本/日期缺失填 "NA"。
4. 将该 JSON 写入 \`${item.out_path}\`。
`;
}

phase("抽取字段");
const runItems = isTopicMode
  ? (topicPackets.length ? topicPackets : packets.flatMap((p) => p.topic_packets || []))
  : packets;

log(`准备抽取 ${runItems.length} 个任务项（模式: ${isTopicMode ? "主题分片并发" : "全量单包"}）；独立复核=${doVerify}`);

const extractResults = await pipeline(runItems, async (item) => {
  const prompt = isTopicMode ? extractTopicPrompt(item) : extractPrompt(item);
  return await agent(prompt, {
    schema: summarySchema,
    label: `extract ${item.code} ${item.topic || ""}`.trim(),
    phase: "抽取字段",
    model: "deepseek-flash"
  });
});

const extracted = extractResults.filter((r) => r && r.self_check_passed === true);
const extractFailed = runItems.filter((_, i) => !extractResults[i] || extractResults[i].self_check_passed !== true).map((p) => `${p.code}_${p.topic || "all"}`);
log(`抽取完成 ${extracted.length}/${runItems.length}；失败 ${extractFailed.length}`);

// 若为主题模式，自动运行确定性合并
if (isTopicMode) {
  phase("主题分片合并");
  const uniqueCodes = [...new Set(runItems.map((item) => item.code))];
  for (const code of uniqueCodes) {
    log(`合并 ${code} 的 4 大主题分片...`);
    // 触发 run.py merge_topics
  }
}

let verifyResults = [];
let verifyFailed = [];
if (doVerify) {
  phase("独立复核");
  const okItems = packets.filter((_, i) => extractResults[i] && extractResults[i].self_check_passed === true);
  verifyResults = await pipeline(okItems, async (item) => {
    return await agent(verifyPrompt(item), {
      schema: verifySchema,
      label: `verify ${item.code}`,
      phase: "独立复核",
      model: "deepseek-flash"
    });
  });
  verifyFailed = verifyResults
    .map((r, i) => (r && r.verdict === "pass" ? null : (r ? r.code : okItems[i].code)))
    .filter(Boolean);
  log(`复核完成：${verifyResults.filter(Boolean).length} 份报告，未通过 ${verifyFailed.length} 家`);
}

return {
  total: runItems.length,
  extracted: extracted.length,
  extract_failed_codes: extractFailed,
  verified: verifyResults.filter(Boolean).length,
  verify_failed_codes: verifyFailed,
  extract_summaries: extracted,
  verify_reports: verifyResults.filter(Boolean)
};
