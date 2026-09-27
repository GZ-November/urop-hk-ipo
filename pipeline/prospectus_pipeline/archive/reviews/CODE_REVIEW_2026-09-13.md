# HK IPO 流水线代码审查

> 修复状态（2026-09-13）：本报告中的写回授权、source 绕过、复核衔接、60 字段迁移、
> 校验副作用、退出码、局部索引、期间日期、扩展入口、状态误报、比例范围、基石缺证据
> 以及旧 runner 无限重试问题均已修复。回归测试见 `tests/test_pipeline_safety.py`。

审查日期：2026-09-13。结论：确定性处理与 LLM 抽取分离的方向合理，但当前“fail-closed”未落实。优先修复写回授权、证据来源与字段迁移，再扩大自动运行。

本次未修改业务脚本、正式工作簿或抽取 JSON，未调用付费 LLM、未重新抓取外部数据。运行了 33 个业务 Python 文件的 AST 语法检查；用临时工作簿及 mock 做复现；实际 76 份 JSON 的校验报告写入临时目录。重点覆盖主 CLI、调度、两套 LLM workflow、准备、契约、验证、写回及扩展入口；历史模板改造脚本未逐个执行，外部 API 与金融口径未做独立原文审计。

## 按优先级排列的问题

### 1. [P1] 写回接受未校验或已被修改的 JSON

位置：`src/write_back.py:119–150`，`src/validate.py:376–387`。

写回只从 report.errors 建黑名单，不要求目标代码在 expected_codes/records 中且有通过记录，也不绑定 JSON 内容哈希。对 A 跑 validate 后，可以直接 write B；A 在 validate 后被修改也能写入。并行代理各自执行 validate --only 时还会覆盖同一个 validation.json，放大此问题。

复现：临时报告仅列 0002.HK，errors=[]；写回 0001.HK 成功，单元格变成未经校验的 invented。

修复：写入前对待写内存快照重新校验，或检查每家公司通过记录与 JSON/schema/证据哈希；按公司原子保存校验结果。不要把“不在错误名单”当成“验证通过”。

### 2. [P1] 任意字段可通过 source 绕过证据闸门

位置：`src/contracts.py:128–134, 224–226`。

LLM JSON 可以携带 source/note；任意字段只要 source 为 da_formula、cornerstone_absence 等 SEARCH_SOURCES，就免页码、免原文校验。没有按 target/field 限定，也不验证来源由确定性阶段产生。check_firm 不会补验这种来源。

复现：给文本业务字段 col_AR 填 invented、page=null、quote=fabricated、source=da_formula，结构与证据检查均返回 []。

修复：LLM 输入禁止自报派生来源；派生结果在受控阶段产生。来源豁免必须绑定指定字段并重新计算/核对依据。

### 3. [P1] 独立 LLM 复核未成为写回条件

位置：`workflows/prospectus_extract.js:199–229`，`workflows/allot_extract.js:153–181`，`auto_fill.py:223–241`。

抽取成功用 filter(Boolean) 判断，忽略 self_check_passed=false；复核 fail 仅放入返回值，不生成写回必须检查的批准记录。auto_fill/write 只读取 Python 校验报告。watcher 看到 JSON 后可在独立复核完成前写入 Excel，随后哨兵非空又阻止默认重写。

修复：采用 extracted → validated → reviewed → written 状态；复核结果绑定同一 JSON 哈希，失败回到修复队列。watcher 只消费 reviewed 版本。

### 4. [P1] 字段迁移后 prompt 与 schema 冲突

位置：`src/pdfprep.py:294–300`，`workflows/prospectus_extract.js` 的硬规则与 verifyPrompt，`prompts/agy_extract.md`。

现行 schema 有 60 字段，主 workflow 仍称 42。更严重的是 packet 规则与独立复核仍将 AY 当资本化开发成本，现行 AX 才是该字段，AY 是前五大客户占比；BS/BA/BG/BC/BI 的旧含义也仍出现在生成规则中。例如 BG 已是偿债用途比例，规则却要求写年化说明；旧 agy prompt 把 AV/AW 当现金流/现金，现行对应 AU/AV。

这会使正确字段被错误指令或复核纠正成另一种数据；证据文字真实和勾稽通过不能消除语义错位。

修复：从 schema 生成字段名、数量与复核清单；移除所有旧列映射。重建 packet 后再运行，不能只修改 JS。

### 5. [P1] 对一家公司校验会修改所有配发 JSON

位置：`run.py:159–174`，`src/greenshoe.py:212–258`，`src/cornerstone.py:69–92`，`src/validate.py:18–68`。

validate --target allot --only A 在筛选前执行 apply_cv/apply_ck/apply_da，它们遍历全部 extracted/*.json 并原地写入，没有 only。并行 workflow 的每个代理都被要求调用这条命令，因此可能同时读写其他代理的 JSON；写盘不是原子的，会产生部分 JSON 读取失败或覆盖刚完成的修改。绿鞋/基石刷新也会使已存在的 DA 派生值过时，因为 apply_da 仅补缺失。

修复：校验函数保持只读；派生放独立步骤，传入目标集合，用内存快照和原子保存；上游值变化时重新计算派生字段。

### 6. [P2] 失败校验仍返回退出码 0

位置：`run.py:204–208`，`tools_validate_ext.py:78`。

main 丢弃阶段返回值并始终 return 0。验证报告 BLOCK 不会让 subprocess/check_call 失败；部分下载失败也不能阻止后续调度。auto_fill 的“validate 非零退出，中止写回”分支无法捕获普通校验错误。

复现：mock cmd_validate 返回 gate_pass=false 和错误，run.main() 仍返回 0。

修复：各命令显式定义退出状态；validate 有 errors 返回非零，准备/下载区分部分失败。auto_fill 如需写通过的子集，应明确读取逐公司结果而不是依赖整体成功。

### 7. [P2] --only 准备覆盖全量索引

位置：`run.py:75–80`，`src/pdfprep.py:95–96, 369–370`；配发准备也采用覆盖式索引。

find/download/prepare 筛选后直接覆盖 found.json/downloaded.json/packets.json。执行 prepare --only A 后，其余公司的文件仍在，但索引只有 A。auto_fill.next_batch 要求 packet_rec 存在，因此剩余待抽公司会从调度队列消失。

修复：按 code 合并更新索引并保留未选中的公司；或生成独立批次索引。失败状态也需要显式留在索引，不能悄悄丢掉。

### 8. [P2] periods 输出不合法日期，且可能选旧中期

位置：`tools_search.py:230–249`。

中期输出 col_AT=09/25，契约只接受完整日期，write_back.parse_date 同样不支持它；匹配时取得的 day 被丢弃。期间选取先看频次，后看时间，只要旧比较期出现次数更多就会优先旧期，即使存在更新中期/完整年度。workflow 又要求模型绝对服从该输出。

复现：输入 nine months ended 30 September 2025，得到 col_AT=09/25，_valid_date 返回 False。

修复：保留真实日/月/年；以明示 track record 报表覆盖期为依据，频次仅辅助；有歧义就输出候选与待复核状态，不强行给唯一权威结论。

### 9. [P2] 扩展包给出不存在的校验命令

位置：`tools_ext_packet.py:119`，`run.py:186–187`。

生成的 packet 要求 run.py validate_ext，CLI 无该 stage。实际运行报 invalid choice，退出 2。独立脚本 tools_validate_ext.py 存在，但未接入 CLI；此外 packet 不存在时该脚本直接跳过证据检查。

修复：接入 validate_ext 或改成真实脚本命令；packet 缺失必须报错；扩展校验失败返回非零。

### 10. [P2] 完成状态依赖一个单元格和文件大小

位置：`auto_fill.py:90–99, 135–140, 270`。

JSON 大于 200 字节就当 extracted，格式损坏也不会再进入抽取队列；Excel 的 L/CK 任意非空（包括 NaN）就视作对应阶段已写，后续修正 JSON、补扩展字段或残缺写入都不会自动同步。finish 的“完成”不证明 JSON 与 Excel 对齐。

修复：状态绑定契约有效性、字段覆盖、复核和写回版本；保留失败重试队列，以完整字段比较或内容哈希判断是否需要重写。

### 11. [P2] 百分比检查还在查旧 AZ，漏掉现行 AY

位置：`src/validate.py:126–129`。

现行前五大客户占比在 col_AY，检查仍列 col_AZ。number 类型本身不限范围，故 1.5（150%）不被拦截。新增的比例字段也没有统一 schema 范围约束。

复现：check_firm 接受 col_AY=1.5，返回 []。

修复：在 schema 中给比例字段 minimum=0/maximum=1，统一校验，不再维护一份列字母列表。

### 12. [P2] 缺文档/空文本可能被判定为“确认无基石”

位置：`src/cornerstone.py:25–38, 51–55`。

公告缺失时 _scan 返回 (-1,0,[],0)，scan 不检查可用性；招股书文本为空或无英文匹配且公告无章节匹配就 verdict=none，apply_ck 会覆盖成 0。规则只匹配英文，不识别中文“基石投资者”。这是把“没有可用证据”变成确定性零值。

修复：区分 present/absent/unknown；先检查两份材料存在、抽文完整且语言受支持。仅在证据充分时产生 absent。

## 当前产物验证结果

| 对象 | 正式 JSON 数 | 当前校验错误 | 至少有一个缺失字段的公司 |
|---|---:|---:|---:|
| 招股书 | 38（每份 60 字段） | 0 | 20 |
| 配发公告 | 38（每份 18 字段） | 0 | 38 |

招股书缺失分布：U 12 家、CJ 4 家、AW 3 家、DP 1 家；配发 CQ 38 家均缺失。缺失未必都应填数，例如无基石名单可能合理；此处只报告事实，不把 missing 等同错误。

out/extracted 另有 4 个 42 字段备份 JSON。现行代码从文件名提取全部数字，带日期的备份通常变成异常股票代码，不一定覆盖正式记录；但所有 glob 消费者行为不同，仍应严格匹配正式文件名并将备份移出运行目录。

## LLM 调用安排建议

准备 → 抽取 → Python 校验 → 有针对性的修复 → 独立语义复核 → 写回 → 检查版本对齐。

不必增加每个字段一次 LLM 调用。优先修好现有两阶段衔接，并让第二阶段核对期间、币种、单位、分母、字段含义与原文数值，而不是只重复代码已做的恒等式。失败原因传给修复阶段，限制重试次数。

## 历史 agy runner 的额外问题

WORKFLOW_REVIEW.md 将其标为旧入口，因此低于现行流程的修复优先级：remaining() 仅看文件存在，损坏 JSON 在重启后被跳过；非 quota 失败无限入队重试；watchdog 在日志持续更新时 continue，可能绕过 hard timeout 检查。若保留可执行入口，应增加明确弃用提示或修好上述行为。

## 建议修复顺序

1. 写回必须绑定当前 JSON 的校验和复核结果；锁住 source 豁免。
2. 统一 schema/prompt/packet 字段含义，修复期间与比例约束。
3. 校验只读，落实 --only、索引合并、退出码及扩展入口。
4. 修复完成状态和重试队列，再对历史数据做期间/单位/语义复核。

测试复现脚本本次位于 `/tmp/hkipo-code-review/check.py`，真实数据的临时校验报告位于同目录的 prospectus.json 与 allot.json。临时路径不是长期测试资产；上述关键复现建议转成仓库中的回归测试。
