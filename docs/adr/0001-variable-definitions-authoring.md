# ADR-0001: 变量定义以 variable_catalog.py 为编辑本体，registry YAML 为派生快照

日期：2026-09-27 · 状态：已接受

## 背景

变量的 202 列定义（表头、中文释义、类型、层级）此前散在四处：codebook.py 内的定义 dict、schema/fields.json、渲染出的季度 Markdown Codebook、以及 `pipeline/registry/HKIPO_Variable_Registry.yaml`。registry 曾宣称"单一事实来源"，实际是经 dict → markdown → regex 解析的循环推导产物（架构评审候选 ③）。

架构梳理后已消除无感知副本：定义 dict 迁入 `variable_catalog.py`（纯数据 module，正典），`build_registry` 在构建时核对 Codebook 定义与 catalog 的一致性并记录漂移。

## 决策

**不**把 registry YAML 升级为手工维护的本体。变量定义的编辑继续发生在 `variable_catalog.py`（catalog-as-code）：

1. 定义变更低频（每季度 0~3 次），且每次变更都与代码变更绑定（新列 = 新 enrichment 逻辑），"不碰 Python 就能改"的收益买不回 YAML 本体化的成本（生成/校验机制、手改 YAML 静默破坏流水线的风险）。
2. 作为补偿，新增 `run.py registry --check`：只读三方一致性校验（variable_catalog ↔ 最新 Codebook ↔ registry），失败非零退出，已挂入 `make check` 与 CI —— 漂移从"能被发现"升级为"会阻塞合并"。
3. git 中的 `registry/HKIPO_Variable_Registry.yaml` 是**派生快照**：供审稿人阅读口径、供 panel.py 加载 slug，其变更永远由 `run.py registry` 生成。

## 后果

- 正面：无生成代码步骤；定义变更天然经过 152+ 项测试；漂移阻塞合并。
- 负面：编辑定义必须改 Python（对非程序员略涩）；registry 文件的 diff 不应手工编辑（会在 --check 暴露）。
- 重新评估触发条件：如果定义编辑变得高频且与代码变更脱钩（例如由非工程角色批量维护口径表），应重新开启"YAML 本体化"设计，届时从本 ADR 的状态出发，而非重新推导。
