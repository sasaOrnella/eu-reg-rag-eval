# GDPR Locked Test · gdpr-03 v3 全批验证报告

- **Batch ID**：`gdpr-03`（`Q157–Q174`，共 18 题，Split = `test`）
- **规范基准**：`gemini_gdpr-03_blind_v3_1.zip`（`v3.1-2026-11-27`）
- **审阅标记**：全部 18 题保持 `author:ai | human_review:pending`
- **隔离与停机声明**：保留 v1、v2 原始文件未改动；未运行任何 Locked Test 检索或评分，未修改研究协议，未启动 `gdpr-04`。

## 1. v2 → v3 变更范围锁定校验

- **仅替换 1 题**：`Q163`（完全更换考点为 `gdpr:art:32(1)` + `gdpr:art:88(1)-(2)`）。
- **其余 17 题逐字段一致**：`Q157–Q162, Q164–Q174` 共 17 题的 `id, split, type, question, gold_answer, gold_evidence, notes` 经磁盘回读逐字段比对与 v2 CSV **100% 一致**（PASS）。

## 2. 12 个非零联合配额格精确核验（High 5 / Low 10 / N/A 3）

| 题型 (`type`) | 证据类型 (`evidence_type`) | 重合度分桶 (`overlap`) | 规范配额 | v3 实际 | 对应题号 | 状态 |
| --- | --- | --- | ---: | ---: | --- | --- |
| `single_hop` | `article_only` | `high` | 1 | 1 | Q157 | PASS |
| `single_hop` | `article_only` | `low` | 2 | 2 | Q158, Q159 | PASS |
| `single_hop` | `recital_only` | `high` | 1 | 1 | Q160 | PASS |
| `single_hop` | `recital_only` | `low` | 1 | 1 | Q161 | PASS |
| `multi_hop` | `article_only` | `high` | 1 | 1 | Q162 | PASS |
| `multi_hop` | `article_only` | `low` | 2 | 2 | **Q163**, Q164 | PASS |
| `multi_hop` | `mixed` | `low` | 1 | 1 | Q165 | PASS |
| `conflicting_or_conditional` | `article_only` | `high` | 1 | 1 | Q166 | PASS |
| `conflicting_or_conditional` | `article_only` | `low` | 2 | 2 | Q167, Q168 | PASS |
| `numeric_or_table` | `article_only` | `high` | 1 | 1 | Q169 | PASS |
| `numeric_or_table` | `article_only` | `low` | 2 | 2 | Q170, Q171 | PASS |
| `unanswerable` | `none` | `na` | 3 | 3 | Q172, Q173, Q174 | PASS |
| **合计（12 非零格）** | — | **High 5 / Low 10 / N/A 3** | **18** | **18** | **Q157–Q174** | **EXACT MATCH** |

## 3. 166 个历史排除单元隔离与单单元复用校验

- **历史排除单元违规数**：**0**（全部 166 个排除单元无一作为正证据出现）。
- **单单元最大复用次数**：**2**（符合 ≤ 2 上限）。全批 16 个正证据单元分布：`gdpr:art:18`（2：Q164/Q165）、`gdpr:art:32`（2：Q159 `32(2)` / Q163 `32(1)`）、`gdpr:art:88`（2：Q171 `88(3)` / Q163 `88(1)-(2)`）；其余 13 个单元（`art:1, 23, 29, 31, 44, 48, 84, 86, 90, 96` 与 `rec:22, 51, 67`）均仅引用 **1 次**。

## 4. 新 Q163 专项核验（双向删除测试与独立性）

- **逐字唯一性**：`gdpr:art:32`（386 字符）、`gdpr:art:88` 第 1 款（224 字符）、`gdpr:art:88` 第 2 款（376 字符）均在 `gdpr.jsonl` 对应单元中出现且仅出现 **1 次**。
- **双向删除测试**：
  - 仅保留 `gdpr:art:88`（删除 `gdpr:art:32`）：无法回答雇主作为控制者/处理者在 GDPR 项下须采取与风险相匹配的技术和组织安全措施这一层面。
  - 仅保留 `gdpr:art:32`（删除 `gdpr:art:88`）：无法回答成员国雇佣法或集体协议须包含维护人格尊严、合法权益、基本权利、透明度、集团内传输与职场监控系统专门保障措施这一层面。
- **重合度与去重**：未舍入 overlap = `0.150`（< 0.30，满足 `low`）；与本批其余 17 题最大内容词 Jaccard = `0.100`；与 Q168（`art:48`）、Q169（`art:96`）零重合，与 Q159（`art:32(2)`）、Q171（`art:88(3)`）无事实重叠。

## 5. 全批汇总指标（磁盘回读终检）

- **硬错误数**：`0`
- **软警告数**：`2`（仅余未改动的 `Q158` 435 字符与 `Q167` 498 字符完整单句，均 < 600 字符硬上限）
- **任意两题最大 Jaccard 相似度**：`0.185`（Q169 vs Q171，远低于 0.60 阈值）
- **重合度分布**：High 5 题 `[0.308, 0.500]`；Low 10 题 `[0.000, 0.150]`
