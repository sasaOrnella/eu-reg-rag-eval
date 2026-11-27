# GDPR Locked Test · gdpr-03 v2 未解决问题与独立审阅清单

全部 18 题已标记 `author:ai | human_review:pending`，尚待合格独立审阅人完成最终法律审阅后方能决定是否纳入 Locked Test。

## 一、v2 修订题独立审阅要点（5 题）

1. **Q162**（`multi_hop | article_only | high (0.500)` | `gdpr:art:1`, `gdpr:art:44`）
   - 核查 `within the EU` 地域限定是否准确，且精简后的 `gdpr:art:44` 引文（331 字符，不含 onward transfers）是否仍充分支撑答案。
2. **Q163**（`multi_hop | article_only | low (0.190)` | `gdpr:art:48`, `gdpr:art:96`）
   - 核查联合问法是否自然、两项规则是否均不可替代，且答案中 `without guaranteeing automatic enforceability or excluding other Chapter V transfer grounds` 表述与 `gdpr:art:48` 语义完全一致；复核 `gdpr:art:48` 完整单句长度（463 字符，>400 软提示）。
3. **Q168**（`conflicting_or_conditional | article_only | low (0.118)` | `gdpr:art:48` ×2）
   - 核查题面中 `ruling from an overseas judicial body or a formal order from a foreign regulatory authority` 是否准确对应 `judgment of a court or tribunal and any decision of an administrative authority` 且排除了非正式请求；核查答案三层区分（必要条件 / 非自动可执行 / 不排除第五章其他依据）。
4. **Q170**（`numeric_or_table | article_only | low (0.150)` | `gdpr:art:84` ×2）
   - 核查 `"domestic statutes establishing alternative sanctions, particularly for violations falling outside GDPR monetary penalties"` 是否准确对应 `other penalties ... in particular for infringements which are not subject to administrative fines`，且接收机关明确为欧洲委员会、未泄露条文编号。
5. **Q172**（`unanswerable | none | na | absence_kind:a` | `hard_negative:gdpr:art:88`）
   - 核查“员工背景调查义务”是否与历史题库（Q001–Q156）完全无语义重复，并确认 `art:88, rec:155, art:10, art:32` 确未规定该义务。

## 二、Q172 备选缺失事实（仅作后续语义去重参考，未写入正式 CSV）

若独立审阅发现 Q172 仍与历史题库存在潜在语义邻近，可参考以下两个已通过 `gdpr.jsonl` 全语料检索验证的 `absence_kind:a` 备选缺失事实：

1. **备选 A：勒索软件赎金支付禁令（Ransomware ransom payments）**
   - **缺失事实**：GDPR 是否禁止组织在遭受勒索软件攻击时向攻击者支付赎金以恢复被加密的个人数据。
   - **全语料检索验证**：`ransom`（0 命中）、`extortion`（0 命中）、`cyberattack`（0 命中）、`malicious code`（1 命中：`gdpr:rec:49`）、`encryption`（4 命中：`gdpr:rec:83, art:6, art:32, art:34`）。
   - **建议 Hard Negative**：`gdpr:art:32`（或 `gdpr:rec:49`）；关联条文仅涉及防范恶意代码、加密与恢复可用性，未规定是否允许或禁止支付赎金。
2. **备选 B：强制性漏洞赏金或协调披露计划（Mandatory bug bounty / coordinated vulnerability disclosure programs）**
   - **缺失事实**：GDPR 是否要求在线平台或控制者建立面向外部安全研究人员的漏洞赏金或协调漏洞披露计划。
   - **全语料检索验证**：`bounty`（0 命中）、`vulnerabilit`（0 命中）、`coordinated disclosure`（0 命中）、`security researcher`（0 命中）。
   - **建议 Hard Negative**：`gdpr:art:32`（常规安全措施定期测试与评估要求，未提及外部安全研究人员或漏洞赏金计划）。

## 三、其余待审阅项（未改动 13 题）

- `Q158`（`gdpr:art:86`，435 字符）与 `Q167`（`gdpr:art:90` 首段，498 字符）仍保留完整单句引文（>400 字符软提示，<600 硬上限），维持 v1 状态等待独立审阅确认。
