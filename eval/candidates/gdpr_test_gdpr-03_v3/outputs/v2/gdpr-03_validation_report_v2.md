# GDPR Locked Test · gdpr-03 v2 全批验证报告

- **Batch ID**：`gdpr-03`（`Q157–Q174`，共 18 题，Split = `test`）
- **规范基准**：`gemini_gdpr-03_blind_v3_1.zip`（`v3.1-2026-11-27`）
- **审阅标记**：全部 18 题保持 `author:ai | human_review:pending`
- **隔离声明**：未运行任何 Locked Test 检索或评分，未启动 `gdpr-04`，未归档或修改研究协议。

## 1. v1 → v2 变更范围锁定校验

- **仅修改 5 题**：`Q162, Q163, Q168, Q170, Q172`。
- **其余 13 题逐字段一致**：`Q157–Q161, Q164–Q167, Q169, Q171, Q173–Q174` 共 13 题的 `id, split, type, question, gold_answer, gold_evidence, notes` 经程序化比对与 v1 CSV **100% 一致**（PASS）。

## 2. 精确联合配额核验（题型 × 证据类型 × High/Low）

| 题型 (`type`) | 证据类型 (`evidence_type`) | 重合度分桶 (`overlap`) | 规范配额 | v2 实际 | 对应题号 | 状态 |
| --- | --- | --- | ---: | ---: | --- | --- |
| `single_hop` | `article_only` | `high` | 1 | 1 | Q157 | PASS |
| `single_hop` | `article_only` | `low` | 2 | 2 | Q158, Q159 | PASS |
| `single_hop` | `recital_only` | `high` | 1 | 1 | Q160 | PASS |
| `single_hop` | `recital_only` | `low` | 1 | 1 | Q161 | PASS |
| `multi_hop` | `article_only` | `high` | 1 | 1 | **Q162** | PASS |
| `multi_hop` | `article_only` | `low` | 2 | 2 | **Q163**, Q164 | PASS |
| `multi_hop` | `mixed` | `low` | 1 | 1 | Q165 | PASS |
| `conflicting_or_conditional` | `article_only` | `high` | 1 | 1 | Q166 | PASS |
| `conflicting_or_conditional` | `article_only` | `low` | 2 | 2 | Q167, **Q168** | PASS |
| `numeric_or_table` | `article_only` | `high` | 1 | 1 | Q169 | PASS |
| `numeric_or_table` | `article_only` | `low` | 2 | 2 | **Q170**, Q171 | PASS |
| `unanswerable` | `none` | `na` | 3 | 3 | **Q172**, Q173, Q174 | PASS |
| **合计** | — | **High 5 / Low 10 / N/A 3** | **18** | **18** | **Q157–Q174** | **EXACT MATCH** |

## 3. 166 个历史排除单元隔离与单单元复用校验

- **历史排除单元违规数**：**0**（166 个排除单元无一作为正证据出现）。
- **单单元最大复用次数**：≤ 2 次（`gdpr:art:18`、`gdpr:art:48`、`gdpr:art:96` 各引用 2 次，其余 13 个单元各 1 次）。

## 4. 修订 5 题专项复验

### Q162（`multi_hop | article_only | high (0.500)`）
- **地域限定与最小引文**：题面限定 `within the EU`；`gdpr:art:44` 引文由 503 字符精简为 331 字符（删除 onward transfers 尾句），答案同步删除额外内容，两段引文均唯一匹配（1/1）。
- **删减测试**：删去 `gdpr:art:1` 无法说明欧盟内部不得因数据保护理由限制或禁止个人数据自由流动；删去 `gdpr:art:44` 无法说明向第三国或国际组织传输须遵守第五章条件。

### Q163（`multi_hop | article_only | low (0.190)`）
- **真实多跳与独立性**：同时考查第三国法院裁决依赖有效国际协议方可能被认可或执行（`gdpr:art:48`）以及成员国 2016 年 5 月 24 日前国际数据传输协议继续有效的法定条件（`gdpr:art:96`）；明确 `art:48` 为必要条件而非自动可执行保证，且保留第五章其他传输依据不受影响；与 Q168（单条文条件与例外）、Q169（单纯截止日期数值）各自独立。
- **删减测试**：删去 `gdpr:art:48` 无法得出第三国法院裁决认可/执行的必要条件与第五章保留条款；删去 `gdpr:art:96` 无法得出 2016-05-24 前协议的存续条件（符合此前欧盟法且未经修订、取代或撤销）。

### Q168（`conflicting_or_conditional | article_only | low (0.118)`）
- **法律行为类型与条件区分**：题面明确限定为海外司法机关裁决（`ruling from an overseas judicial body`）或外国监管机关正式决定（`formal decision from a foreign regulatory authority`），排除非正式请求；答案清晰区分“有效国际协议”作为必要条件、非自动可执行保证以及第五章其他传输依据不受排除。

### Q170（`numeric_or_table | article_only | low (0.150)`）
- **准确语义与接收机关**：将适用对象准确表述为针对不受 GDPR 行政罚款机制约束之违法情形的国内替代性制裁规则（other penalties），明确接收机关为 `the European Commission`，保留 `25 May 2018` 及后续修订无延误通知义务，无条文编号泄露。

### Q172（`unanswerable | none | na | absence_kind:a`）
- **全新考点与全语料检索**：完全移除保险/网络责任险话题，更换为“GDPR 是否要求企业在授予员工个人数据访问权限前进行背景调查（background checks）”。在完整 `gdpr.jsonl` 语料中检索 `background check`（0 命中）、`vetting`（0 命中）、`screening`（0 命中）、`criminal record`（0 命中）、`recruitment`（2 命中：`gdpr:rec:155, gdpr:art:88`），并实际阅读 `gdpr:art:88, gdpr:rec:155, gdpr:art:10, gdpr:art:32`，确认均未规定员工背景调查义务。

## 5. 全批汇总指标

- **错误数**：`0`
- **软警告数**：`3`（`Q158` 435 字符、`Q163` 463 字符、`Q167` 498 字符，均系不可拆分完整单句，低于 600 字符硬上限；Q162 已消除 >400 软警告）
- **任意两题最大 Jaccard 相似度**：`0.185`（Q169 vs Q171，远低于 0.60 阈值）
- **全批重合度区间**：High 5 题 `[0.308, 0.500]`（全部 ≤ 0.60）；Low 10 题 `[0.000, 0.190]`（全部 < 0.30）
