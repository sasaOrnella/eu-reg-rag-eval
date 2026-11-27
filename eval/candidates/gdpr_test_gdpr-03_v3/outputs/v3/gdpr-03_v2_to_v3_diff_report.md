# GDPR Locked Test · gdpr-03 v2 → v3 差异报告（Q163 独立考点替换）

- **基线版本（v2）**：`gdpr-03_candidates_v2.csv`（SHA-256：`e20088a66d28578940f852d4f5ede7666f57b3a1575c530ea2a44f307eb75cb5`）
- **修订版本（v3）**：`gdpr-03_candidates_v3.csv`（SHA-256：`0c1200e70d19a38dad33f5321560996c3ec189eb411c3059e7028b4f3f839174`）
- **不变题目（17 题，逐字段 100% 一致）**：`Q157–Q162, Q164–Q174`（经程序化逐行逐列比对，全部 7 个字段与 v2 完全一致）。
- **替换题目（1 题）**：`Q163`（完全更换考点，保留 `id=Q163`、`split=test` 及 `multi_hop × article_only × low` 配额格）。

## 一、三个不同考点候选方案评估与择优

在排除 166 个历史排除单元及已达 2 次上限的 `gdpr:art:18` 后，针对剩余 14 条可用 GDPR 条文中**尚未被其余 17 题考查的实质条款**，设计并评估了三个完全不同的 `multi_hop × article_only × low` 候选方案：

### 候选方案 1（最终入选）：`gdpr:art:32(1)` + `gdpr:art:88(1)-(2)` — 职场监控工具处理员工数据时的双层保障义务
- **法律依据**：
  - `gdpr:art:32(1)`：控制者与处理者须结合技术水平、实施成本、处理性质/范围/背景/目的及自然人权利自由风险，采取适当技术与组织安全措施以确保与风险相匹配的安全水平。
  - `gdpr:art:88(1)-(2)`：成员国可通过法律或集体协议制定雇佣语境下员工个人数据处理的专门规则，且此类规则须包含适当且具体的保障措施，以维护数据主体的人格尊严、合法权益与基本权利，尤其针对处理透明度、企业集团内部传输及工作场所监控系统。
- **证据最小必要性与双向删除测试**：
  - 删去 `gdpr:art:32`：无法得出控制者/处理者在 GDPR 层面的风险匹配型技术与组织安全措施义务。
  - 删去 `gdpr:art:88`：无法得出成员国雇佣法或集体协议在职场监控系统场景下必须内置的人格尊严、合法权益、基本权利与透明度等专门保障要求（`88(1)` 导言为理解 `88(2)` 的 `"Those rules"` 所必需）。
  - 三段引文长度分别为 386、224、376 字符，全部 ≤ 400 字符（无超长软提示），且均在各自单元中逐字唯一（1/1）。
- **与本批其余 17 题的区别**：
  - Q159 仅考查 `gdpr:art:32(2)` 评估安全水平时应重点考虑的风险类型（意外或非法毁损、丢失、篡改、未经授权披露或访问），未涉及 `art:32(1)` 的措施义务。
  - Q171 仅考查 `gdpr:art:88(3)` 成员国向欧委会通知国内法的 `25 May 2018` 截止日期，未涉及 `art:88(2)` 的实质保障内容。
  - 与其余 17 题最大内容词 Jaccard 相似度仅为 **0.100**（Q171），完全脱离 Q168（`art:48`）与 Q169（`art:96`）。
- **Low 重合度验证**：未舍入 overlap = **0.150**（< 0.30，满足 `low`）。

### 候选方案 2（备选未入选）：`gdpr:art:44`（再传输与保护水平不被削弱原则）+ `gdpr:art:88(1)-(2)`（集团内员工数据传输）
- **法律依据**：`gdpr:art:88(2)` 要求成员国雇佣专门规则针对企业集团内部传输提供人格尊严与基本权利保障；`gdpr:art:44` 后半段要求包括再传输在内的所有第三国传输须遵守第五章规定，以确保 GDPR 保障的自然人保护水平不被削弱。
- **评估与未入选原因**：虽满足 Low（overlap = **0.286** < 0.30，接近 0.30 边界）与双向删除，但 `gdpr:art:44` 已在 Q162 中用于考查第三国传输条件，且所引 `art:44` 后半段以 `"including for onward transfers..."` 开头（非独立句首），在自包含性与与 Q162 的主题距离上弱于方案 1。

### 候选方案 3（备选未入选）：`gdpr:art:80(2)` + `gdpr:art:84(1)` — 公益组织无委托独立维权与国内“其他处罚”实质标准
- **法律依据**：`gdpr:art:84(1)` 要求成员国对不受行政罚款约束的违法情形规定有效、相称且具劝阻性的其他处罚；`gdpr:art:80(2)` 允许成员国授权公益数据保护组织在无数据主体委托时独立提起投诉及司法救济。
- **评估与未入选原因**：虽满足 Low（overlap = **0.150** < 0.30）且启用了未使用的 `gdpr:art:80`，但 `art:80(2)` 文本包含 `"referred to in paragraph 1 of this Article"` 回指（若补引 `80(1)` 全句则达 640 字符，超 600 字符硬上限），单独引用 `80(2)` 在 R-E1 充分性上存在隐患，且两条文更接近两项并列追问而非单一场景下的联合约束。

**综合结论**：候选方案 1 在法律自然度、双向删除不可替代性、引文充分最小性（全段 ≤ 386 字符）、与其余 17 题独立性（最大 Jaccard 0.100）及 Low 裕度（0.150）上均最优，选定写入正式 v3 CSV。

## 二、Q163 v2 → v3 逐字段变化

- **Question**：
  - v2：`When an overseas court orders a firm to hand over customer records citing a Member State's pre-GDPR bilateral pact, what dual legal tests govern recognition and that pact's survival?`
  - v3：`When a company deploys workplace surveillance tools handling staff files, what two layers of safeguards govern its technical security controls and any national labour rules under the GDPR?`
- **Gold Answer**：
  - v3：`The controller and processor must implement risk-appropriate technical and organisational security measures, while any specific Member State laws or collective agreements governing employee data processing must include suitable and specific measures safeguarding human dignity, legitimate interests, and fundamental rights, particularly regarding transparency, intra-group transfers, and workplace monitoring systems.`
- **Gold Evidence**：
  - v2：`gdpr:art:48`（463 字符）+ `gdpr:art:96`（298 字符）
  - v3：`gdpr:art:32`（第 1 款，386 字符）+ `gdpr:art:88`（第 1 款 224 字符 + 第 2 款 376 字符）
- **Overlap**：`0.190` → `0.150`（均满足 `low`）；同时消除了原 Q163 的 463 字符超 400 软提示。
