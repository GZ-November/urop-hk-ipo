// DSH workflow: 配发结果公告字段抽取（整篇读取，无需检索）
//
// args 二选一：
//   { codes: ["6082.HK", "0100.HK", ...], verify: true }        ← 推荐，路径自动推导
//   { packets: [{code, name, packet_path, out_path}], verify }   ← 显式指定
//   可选 python_executable / run_script / config_path，用于指定环境、入口和 cohort。
//   使用自定义 paths 时，传入 packet_dir 和 out_dir。
//
// 与招股书流程的区别：公告只有 12–50 页，packet 里**已经是全文**，
// 代理不需要切片检索；重点是「最终值 vs 初始值」的口径与基石/回拨的核对。

function buildPackets(a) {
  if (a && Array.isArray(a.packets) && a.packets.length) return a.packets;
  const codes = (a && a.codes) || [];
  const packetDir = (a && a.packet_dir) || "prospectus_pipeline/data/allot/packets";
  const outDir = (a && a.out_dir) || "prospectus_pipeline/out/allot/extracted";
  return codes.map((code) => {
    const digits = String(code).replace(/[^0-9]/g, "");
    const safe = "HKIPO-MB" + digits;
    return {
      code,
      name: "",
      packet_path: `${packetDir}/${safe}.md`,
      out_path: `${outDir}/${safe}.json`
    };
  });
}

const packets = buildPackets(args);
const shellArg = (value) => `'${String(value).replace(/'/g, "'\\''")}'`;
const PY = shellArg((args && args.python_executable) || "python3");
const RUN = shellArg((args && args.run_script) || "prospectus_pipeline/run.py");
const CONFIG = args && args.config_path ? ` --config ${shellArg(args.config_path)}` : "";
const doVerify = !args || args.verify !== false;
if (!packets.length) throw new Error("args.codes 或 args.packets 为空");

const summarySchema = {
  type: "object",
  properties: {
    code: { type: "string" },
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

function extractPrompt(item) {
  return `你是 HK IPO 数据库采集员。任务：从**配发结果公告**里抽取指定字段。

## 输入
- 抽取包（含字段清单、单位口径、以及**公告全文**）：\`${item.packet_path}\`
- 公司：${item.code} ${item.name}
- 写盘路径：\`${item.out_path}\`

## 工作步骤
1. 完整读取抽取包。**全文就在包里**，不需要去别处检索。
2. 逐字段确定「值、页码、原文短摘录、置信度」。页码用包内的 \`<<<PAGE n>>>\` 编号。
3. 写成严格 JSON 后，先运行确定性派生，再运行自检并修到通过：
   \`${PY} ${RUN}${CONFIG} derive_allot --only ${item.code}\`
   \`${PY} ${RUN}${CONFIG} validate --target allot --only ${item.code}\`
   若有 errors，回到原文修正后重跑，直到该条不是 ERROR。
4. 校验通过后运行 \`${PY} ${RUN}${CONFIG} state extracted --target allot --code ${item.code}\`，记录当前 JSON 的哈希。

## 输出契约（机器校验，违反即失败）

顶层**只能**有 \`code\` 和 \`fields\`：

\`\`\`json
{"code":"${item.code}","fields":{"col_CK":{"value":0.6886,"page":4,"quote":"<=200字符原文","confidence":"high"}}}
\`\`\`

- \`fields\` 必须包含字段清单里的**每一个** key，不多不少不重复。
- 每个 entry 只能有 \`value\`/\`page\`/\`quote\`/\`confidence\`。
- \`page\` 为整数页码；缺失写 \`null\`。\`quote\` ≤200 字符；缺失写 \`""\`。
- 数值缺失写 \`"NaN"\`；文本/日期缺失写 \`"NA"\`。
- 非缺失字段必须有**本包内**的真实页码与原文摘录。

## 关键口径（这批最常见出错的地方）

1. **这是配发结果公告，不是招股书**：要**最终值**，不要招股书的初始发售规模或估计值。
2. **超额配售（绿鞋）≠ 发售规模调整**：\`col_CS\` 的 base offer **包含已行使的规模调整、排除绿鞋**。
   公告里常给「假设超额配售权未行使」与「假设全面行使」两套数字——取**未行使绿鞋**那套。
3. \`col_CK\` 分母是 **base offer（不含绿鞋）**；基石表若已给「假设绿鞋未行使」的百分比列，取该列合计。
4. \`col_CV\` 绿鞋**实际**行使股数；公告若只写"未行使"就填 \`0\`。
5. \`col_CM\` 认购倍数填倍数；公告可能同时有「超额认购 N 倍」与「认购 N 倍」，
   **以原文表述为准**并把原文放进 \`col_CP\`，避免差 1 倍的口径混淆。
6. \`col_CR\` 直接填包首给出的港交所刊发时间，不要用正文里其它日期。
7. \`col_CX\` 是**发行人净募资额**，不含售股股东所得；公告给区间时取对应最终发售价的数值。
8. 基石禁售期以**6 个月**为准（港交所 2025-08-04 改革明确未采纳分阶段解禁）。
9. 公告可能中英双语重复排版，同一数字出现两次属正常。
10. 不确定就填 \`NaN\`/\`NA\` 并在 quote 说明，**不要猜**。`;
}

function verifyPrompt(item) {
  return `你是独立的配发结果公告复核员。**不要相信**抽取结果，回到公告原文自己核对。

## 输入
- 待复核 JSON：\`${item.out_path}\`
- 抽取包（含公告全文）：\`${item.packet_path}\`
- 公司：${item.code} ${item.name}

## 必查项
- \`col_CT\` + \`col_CU\` 是否等于 \`col_CS\`（最终公开发售 + 最终配售 = 最终全球发售）
- \`col_CS\` 是否用的是**未行使绿鞋**的口径（不是"假设全面行使"那套）
- \`col_CV\`：绿鞋实际行使股数；未行使应为 0（注意区分"未行使"与"未披露"）
- \`col_CK\`：是否 = 基石表股数 ÷ base offer（不含绿鞋），与公告百分比列是否吻合
- \`col_CM\`：倍数口径与 \`col_CP\` 原文是否一致（"超额认购 N 倍" vs "认购 N 倍"）
- \`col_CN\`/\`col_CO\`：申请**人数**与申请**股数**有没有弄反
- \`col_CX\`：是否为发行人净募资（不是毛募资、不含售股股东所得）
- \`col_CY\`/\`col_DA\`：是否小数；\`col_DA\` 是否 ≤ \`col_CY\`
- \`col_CR\`：是否等于包首的港交所刊发时间
- 每个非缺失字段的 page/quote 是否真能在公告里对上

## 输出
只返回结构化结果：verdict 为 pass/fail；discrepancies 列出不一致项
（field、in_file、should_be、page、reason），reason 里给出可直接采用的正确答案与页码。
**不要**修改 JSON 文件。若结论为 pass，在返回报告前运行
\`${PY} ${RUN}${CONFIG} state reviewed --target allot --code ${item.code} --verdict pass\`；
若为 fail 则运行同一命令但使用 \`--verdict fail\`。`;
}

phase("抽取公告字段");
log(`准备处理 ${packets.length} 份配发公告；独立复核=${doVerify}`);

const extractResults = await pipeline(packets, async (item) => {
  return await agent(extractPrompt(item), {
    schema: summarySchema,
    label: `allot ${item.code}`,
    phase: "抽取公告字段"
  });
});

const extracted = extractResults.filter((r) => r && r.self_check_passed === true);
const extractFailed = packets.filter((_, i) => !extractResults[i] || extractResults[i].self_check_passed !== true).map((p) => p.code);
log(`抽取完成 ${extracted.length}/${packets.length}；失败 ${extractFailed.length}`);

let verifyResults = [];
let verifyFailed = [];
if (doVerify) {
  phase("独立复核");
  const okItems = packets.filter((_, i) => extractResults[i] && extractResults[i].self_check_passed === true);
  verifyResults = await pipeline(okItems, async (item) => {
    return await agent(verifyPrompt(item), {
      schema: verifySchema,
      label: `verify ${item.code}`,
      phase: "独立复核"
    });
  });
  verifyFailed = verifyResults
    .map((r, i) => (r && r.verdict === "pass" ? null : (r ? r.code : okItems[i].code)))
    .filter(Boolean);
  log(`复核完成：${verifyResults.filter(Boolean).length} 份报告，未通过 ${verifyFailed.length} 家`);
}

return {
  total: packets.length,
  extracted: extracted.length,
  extract_failed_codes: extractFailed,
  verify_failed_codes: verifyFailed,
  extract_summaries: extracted,
  verify_reports: verifyResults.filter(Boolean)
};
