# GDPR Locked Test · gdpr-03 全批校验报告

- **Batch ID**：`gdpr-03`（`Q157–Q174`，共 18 题，Split = `test`）
- **生成规范版本**：`v3.1-2026-11-27`（严格以 `gemini_gdpr-03_blind_v3_1.zip` 为唯一规范）
- **审阅标记**：全部 18 题均已标记 `author:ai | human_review:pending`
- **盲生成隔离**：未参考任何 Dev/Test 检索成绩、历史错例或已有问题题面；未运行任何 Locked Test 检索或评分。

## 1. 输入文件 SHA-256 核验（全部 9 项一致）

| 文件相对路径 | SHA-256 | 校验状态 |
| --- | --- | --- |
| `blind_generation_spec.md` | `acaa19db40db5cbb8ba65e3d1b86cc807e700bc9f1cf023f360376c012489ccd` | PASS |
| `data/processed/ai_act.jsonl` | `c4a5b3999f5af5e37f301ceb7f9b1ab2ec311b96583d53044871a9e7089dfa8f` | PASS |
| `data/processed/gdpr.jsonl` | `e8bbb70c2be3890d8f8307ad26cf583c9b41b17b291094851913806ac3de0df6` | PASS |
| `data/raw/ai_act.html` | `26482ecee82f549262c1b259120b2b03d3e0addb86584c056b145aa4997e2fba` | PASS |
| `data/raw/gdpr.html` | `fde27ea4627c51465d51a45268c18f05ed772ab0163382ca34ed3e83d9f98126` | PASS |
| `excluded_evidence_units.csv` | `e81403b63a5db45939c1ca407554713a75b45a67537fafa26e11aa5c2bd4cffc` | PASS |
| `locked_test_batch_schedule_v3_1.csv` | `e698303c4fbe3621c599cc1b5c936ce3a3918e43456d52f62ddc0f1c87490ad5` | PASS |
| `locked_test_quotas_v3.json` | `e8f2fde72b36298e030c416bc090e86d95db1afbdde7fcf6616b1f9ba0c2cc4c` | PASS |
| `question_rules.md` | `7381a76b2bc6957d8b74f374f178a81d61b00a3e6f2fd44e3d30c0515b77b606` | PASS |

## 2. 精确联合配额核验（题型 × 证据类型 × High/Low）

按 `locked_test_quotas_v3.json` 与 `locked_test_batch_schedule_v3_1.csv` 核对 `gdpr-03` 全部配额单元：

| 题型 (`type`) | 证据类型 (`evidence_type`) | 重合度分桶 (`overlap`) | 规范配额 | 实际数量 | 对应题号 | 状态 |
| --- | --- | --- | ---: | ---: | --- | --- |
| `single_hop` | `article_only` | `high` | 1 | 1 | Q157 | PASS |
| `single_hop` | `article_only` | `low` | 2 | 2 | Q158, Q159 | PASS |
| `single_hop` | `recital_only` | `high` | 1 | 1 | Q160 | PASS |
| `single_hop` | `recital_only` | `low` | 1 | 1 | Q161 | PASS |
| `multi_hop` | `article_only` | `high` | 1 | 1 | Q162 | PASS |
| `multi_hop` | `article_only` | `low` | 2 | 2 | Q163, Q164 | PASS |
| `multi_hop` | `mixed` | `low` | 1 | 1 | Q165 | PASS |
| `conflicting_or_conditional` | `article_only` | `high` | 1 | 1 | Q166 | PASS |
| `conflicting_or_conditional` | `article_only` | `low` | 2 | 2 | Q167, Q168 | PASS |
| `numeric_or_table` | `article_only` | `high` | 1 | 1 | Q169 | PASS |
| `numeric_or_table` | `article_only` | `low` | 2 | 2 | Q170, Q171 | PASS |
| `unanswerable` | `none` | `na` | 3 | 3 | Q172, Q173, Q174 | PASS |
| **合计** | — | **High 5 / Low 10 / N/A 3** | **18** | **18** | **Q157–Q174** | **EXACT MATCH** |

其余在规范中配额为 0 的组合（`multi_hop/mixed/high`、`conflicting_or_conditional/recital_only/*`、`numeric_or_table/recital_only/*` 等）实际数量均为 `0`。

## 3. 历史证据排除与单元复用隔离核验

- **166 个排除单元隔离**：`excluded_evidence_units.csv` 中全部 166 个单元（含 105 个 GDPR 单元）在 Q157–Q171 正证据中出现次数为 **0**（PASS）。
- **单单元最大复用上限（≤2 次）**：本批共引用 16 个不同可用 GDPR 单元（13 条 Articles + 3 条 Recitals），其中 `gdpr:art:18`、`gdpr:art:48`、`gdpr:art:96` 各被引用 2 次（且均考查不同法律维度或组合逻辑），其余 13 个单元均仅引用 1 次，无任何单元超过 2 次（PASS）。
- **后段条文覆盖**：本批有 6 题（Q158, Q163, Q167, Q169, Q170, Q171）使用后段条文（`gdpr:art:84, 86, 88, 90, 96`）作为正证据。

## 4. 逐题自动化指标与格式审计

| ID | Type | EvType | Bucket (Score) | Q词数 | A词数 | 引文字符数 | 正证据单元 | 逐字唯一 | 结构编号 | 状态 |
| --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| Q157 | `single_hop` | `article_only` | `high` (0.308) | 21 | 23 | [171] | `gdpr:art:31` | 1/1 | 无 | PASS |
| Q158 | `single_hop` | `article_only` | `low` (0.077) | 17 | 35 | [435]* | `gdpr:art:86` | 1/1 | 无 | PASS (软提示>400) |
| Q159 | `single_hop` | `article_only` | `low` (0.000) | 18 | 36 | [305] | `gdpr:art:32` | 1/1 | 无 | PASS |
| Q160 | `single_hop` | `recital_only` | `high` (0.500) | 16 | 36 | [310] | `gdpr:rec:51` | 1/1 | 无 | PASS |
| Q161 | `single_hop` | `recital_only` | `low` (0.077) | 22 | 34 | [245] | `gdpr:rec:22` | 1/1 | 无 | PASS |
| Q162 | `multi_hop` | `article_only` | `high` (0.429) | 22 | 41 | [206, 503]* | `gdpr:art:1`, `gdpr:art:44` | 1/1, 1/1 | 无 | PASS (软提示>400) |
| Q163 | `multi_hop` | `article_only` | `low` (0.062) | 29 | 45 | [463*, 298] | `gdpr:art:48`, `gdpr:art:96` | 1/1, 1/1 | 无 | PASS (软提示>400) |
| Q164 | `multi_hop` | `article_only` | `low` (0.111) | 23 | 48 | [255, 377] | `gdpr:art:29`, `gdpr:art:18` | 1/1, 1/1 | 无 | PASS |
| Q165 | `multi_hop` | `mixed` | `low` (0.125) | 29 | 37 | [323, 168] | `gdpr:rec:67`, `gdpr:art:18` | 1/1, 1/1 | 无 | PASS |
| Q166 | `conflicting_or_conditional` | `article_only` | `high` (0.462) | 20 | 34 | [132, 134] | `gdpr:art:23` (×2) | 1/1, 1/1 | 无 | PASS |
| Q167 | `conflicting_or_conditional` | `article_only` | `low` (0.125) | 23 | 46 | [498*, 189] | `gdpr:art:90` (×2) | 1/1, 1/1 | 无 | PASS (软提示>400) |
| Q168 | `conflicting_or_conditional` | `article_only` | `low` (0.000) | 18 | 51 | [228, 234] | `gdpr:art:48` (×2) | 1/1, 1/1 | 无 | PASS |
| Q169 | `numeric_or_table` | `article_only` | `high` (0.474) | 25 | 34 | [298] | `gdpr:art:96` | 1/1 | 无 | PASS |
| Q170 | `numeric_or_table` | `article_only` | `low` (0.000) | 19 | 21 | [208, 194] | `gdpr:art:84` (×2) | 1/1, 1/1 | 无 | PASS |
| Q171 | `numeric_or_table` | `article_only` | `low` (0.000) | 20 | 22 | [224, 196] | `gdpr:art:88` (×2) | 1/1, 1/1 | 无 | PASS |
| Q172 | `unanswerable` | `none` | `na` (N/A) | 19 | 24 | [] | — | — | 无 | PASS (`kind:a`) |
| Q173 | `unanswerable` | `none` | `na` (N/A) | 24 | 24 | [] | — | — | 无 | PASS (`kind:b`) |
| Q174 | `unanswerable` | `none` | `na` (N/A) | 18 | 22 | [] | — | — | 无 | PASS (`kind:c`) |

*注：Q158（435 字符）、Q162（503 字符）、Q163（463 字符）、Q167（498 字符）各含 1 句不可拆分的完整法规单句，均低于 600 字符硬上限；未做断句截断以确保法律语义完整与证据充分性（R-E1），已列入独立审阅清单重点复核。*

- **词数与问句形式（R-Q2, R-A2）**：全部 18 题均为单一英文问句且以 `?` 结尾，词数范围 16–29 词（要求 8–40 词）；全部 18 题答案词数范围 21–51 词（要求 ≤60 词）。
- **重合度分布（R-Q3）**：5 道 High 题重合度均位于 `[0.308, 0.500]`（全部 ≤0.60，零抄袭预警）；10 道 Low 题重合度均位于 `[0.000, 0.125]`（全部 <0.30）。
- **去重与句式多样性（R-Q7, R-Q8）**：全批任意两题内容词 Jaccard 相似度最大值为 **0.250**（Q170 与 Q171，远低于 0.60 阈值）；首词分布最高仅占 3/18（`what` 3 次，16.7%，远低于 30% 上限）。

## 5. 专项法律语义与证据必要性审计

### 5.1 Multi-hop 删减必要性检验（Q162–Q165）
- **Q162 (`gdpr:art:1` + `gdpr:art:44`)**：对比欧盟内部数据自由流动原则与向第三国/国际组织传输（含再传输）的条件。删去 `art:1` 无法说明内部不得因个保理由限制/禁止；删去 `art:44` 无法说明向第三国传输及再传输须满足第五章条件。
- **Q163 (`gdpr:art:48` + `gdpr:art:96`)**：第三国法院依据成员国既有双边协议要求披露数据时，协议需满足何种条件方能支撑执行。删去 `art:48` 无法得出外国裁判仅在依据“有效国际协议”（且不损害本章其他传输依据）时方可执行；删去 `art:96` 无法得出 2016 年 5 月 24 日前缔结的成员国协议须符合当时欧盟法且未经修订/取代/撤销方持续有效。
- **Q164 (`gdpr:art:29` + `gdpr:art:18`)**：受托处理者持有已被限制处理的数据时，在存储之外进行处理的双重法律约束。删去 `art:29` 缺失“仅按控制者指令处理（除非欧盟或成员国法律要求）”的处理者义务；删去 `art:18(2)` 缺失限制状态下除存储外仅限同意/法律主张/保护他人权利/重大公共利益的法定情形。
- **Q165 (`gdpr:rec:67` + `gdpr:art:18`)**：自动化系统中如何从技术上落实处理限制，以及解除限制前控制者的义务。`gdpr:rec:67` 提供条文未规定的自动化系统技术锁定方式与明确标注要求；`gdpr:art:18(3)` 提供解除限制前必须通知数据主体的强制义务。删去任一单元均无法得出完整答案。

### 5.2 Conditional 条件与例外保留检验（Q166–Q168）
- **Q166 (`gdpr:art:23`)**：完整保留“where relevant”前提及“unless that may be prejudicial to the purpose of the restriction”例外，未将通知条款表述为无条件义务。
- **Q167 (`gdpr:art:90`)**：同时保留“necessary and proportionate to reconcile...”的立法前提与“apply only with regard to personal data received or obtained in an activity covered by that obligation of secrecy”的适用范围限制，未将职业保密身份表述为全面豁免的充分条件。
- **Q168 (`gdpr:art:48`)**：准确保留“only ... if based on an international agreement ... in force”的必要条件以及“without prejudice to other grounds for transfer pursuant to this Chapter”的保留条款，未将国际协议误述为唯一或充分条件。

### 5.3 Unanswerable 全语料检索与真实缺失检验（Q172–Q174）
- **Q172 (`absence_kind:a`)**：网络责任险/数据泄露保险义务。检索变体：`insurance, cyber liability, indemnity, financial guarantee`；实际查看：`gdpr:art:82, gdpr:rec:146, gdpr:rec:54, gdpr:art:32`；`hard_negative:gdpr:art:82`。GDPR 全文仅在公共卫生/社会保险语境提及 insurance，未要求控制者购买网络责任保险。
- **Q173 (`absence_kind:b`)**：向欧洲数据保护委员会（EDPB）预先登记常规客户数据处理活动的程序（自然虚假前提）。检索变体：`register, registration, general notification, prior consultation, records of processing`；实际查看：`gdpr:art:36, gdpr:art:30, gdpr:art:70, gdpr:rec:89`；`hard_negative:gdpr:art:36`。Recital 89 明确废除普遍事前申报义务，Art 30 仅要求内部记录，Art 36 仅针对高风险未缓释情形向监管机构事前咨询，Art 70 未赋予 EDPB 产品/常规处理登记程序。
- **Q174 (`absence_kind:c`)**：ENISA 在 GDPR 下审批欧洲数据保护印章或认可认证机构的职责（缺席命名实体）。检索变体：`ENISA, cybersecurity, Network and Information Security, certification`；实际查看：`gdpr:art:43, gdpr:art:42, gdpr:rec:49, gdpr:art:70`；`hard_negative:gdpr:art:43`。GDPR 全文未出现 ENISA，Recital 49 仅提及 CERTs/CSIRTs，Art 42–43 将认证与认可职权分配给监管机构、国家认可机构与委员会。
- 三题均无 `exact/precise/universal/specific` 等提示词，均以 `Not specified` 开头，未使用 `kind:d`（不占用全法规 ≤4 题的 `kind:d` 限额）。
