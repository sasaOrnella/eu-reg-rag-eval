# GDPR Locked Test · gdpr-03 v1 → v2 差异报告

- **基线版本（v1）**：`gdpr-03_candidates.csv`（SHA-256：`7c181cdde9c7e215b2e4a9032494aa5acb058298b10d957f3c4ee9bf35fcd254`）
- **修订版本（v2）**：`gdpr-03_candidates_v2.csv`（SHA-256：`e20088a66d28578940f852d4f5ede7666f57b3a1575c530ea2a44f307eb75cb5`）
- **不变题目（13 题，逐字段完全一致）**：`Q157, Q158, Q159, Q160, Q161, Q164, Q165, Q166, Q167, Q169, Q171, Q173, Q174`（经程序化逐行逐列比对，`id, split, type, question, gold_answer, gold_evidence, notes` 7 个字段 100% 一致）。
- **修订题目（5 题）**：`Q162, Q163, Q168, Q170, Q172`。

## 逐题修订对比

### 1. Q162（`multi_hop | article_only | high`）
- **修订动因**：限定“欧盟内部”（within the EU）而非模糊的“inside Europe”；精简 `gdpr:art:44` 引文至 331 字符，删除不考查的 `onward transfers` 尾句及答案中的 `(including onward transfers)`。
- **Question**：
  - v1：`How does the GDPR's approach to free movement of personal data inside Europe differ from sending records to a third country abroad?`
  - v2：`How does the GDPR's approach to free movement of personal data within the EU compare with sending records to a third country abroad?`
- **Gold Answer**：
  - v1 含 `(including onward transfers)`；v2 已删除，改为 `...whereas transfers to a third country or international organisation may occur only if the GDPR's transfer-chapter conditions are complied with.`
- **Gold Evidence**：
  - `gdpr:art:1` 引文不变（206 字符）；`gdpr:art:44` 引文由 503 字符精简为 331 字符（仅保留至 `complied with by the controller and processor`）。
- **重合度变化**：`0.429` → `0.500`（仍为 `high`，且 ≤ 0.60）。

### 2. Q163（`multi_hop | article_only | low`）
- **修订动因**：v1 题面偏重旧协议为何仍然有效（`gdpr:art:96` 可单独回答），`gdpr:art:48` 必要性不足；v2 改写为同时考查第三国法院裁决依赖有效国际协议的条件（`art:48`）与成员国 2016-05-24 前协议持续有效的条件（`art:96`）的联合法律问题，并与 Q168、Q169 形成清晰区隔。
- **Question**：
  - v1：`When an overseas tribunal demands customer files from a European firm under an old bilateral pact, what makes that pact still valid for enforcing the order under the GDPR?`
  - v2：`When an overseas court orders a firm to hand over customer records citing a Member State's pre-GDPR bilateral pact, what dual legal tests govern recognition and that pact's survival?`
- **Gold Answer**：
  - v2 明确区分两项独立且联合必要的规则：（1）第三国法院裁决仅在基于有效国际协议时方可能被认可或执行（`art:48`，必要条件、不自动保证可执行、不排除第五章其他传输依据）；（2）成员国 2016 年 5 月 24 日前订立的传输协议仅在符合此前欧盟法且未被修订、取代或撤销时继续有效（`art:96`）。
- **Gold Evidence**：单元不变（`gdpr:art:48` + `gdpr:art:96`），重合度由 `0.062` 变为 `0.190`（仍为 `low`）。

### 3. Q168（`conflicting_or_conditional | article_only | low`）
- **修订动因**：v1 使用 `"foreign agency's demand"` 可能涵盖非正式请求，扩大了 `gdpr:art:48` 仅适用于第三国法院/法庭裁决及行政机关正式决定的法律行为范围；v2 明确法律行为类型，并在答案中清晰区分必要条件、非自动可执行性及第五章其他传输依据不受排除。
- **Question**：
  - v1：`Is a foreign agency's demand that a European business hand over user records legally binding under the GDPR?`
  - v2：`When can a ruling from an overseas judicial body or a formal order from a foreign regulatory authority compelling customer file disclosure take legal effect under the GDPR?`
- **Gold Answer**：
  - v2 明确写出：仅在基于有效国际协议时方可能被认可或执行；拥有此类协议属于必要条件而非自动可执行保证，且不排除 GDPR 传输章下的其他合法传输依据。
- **Gold Evidence**：`gdpr:art:48` 两段引文不变（228 + 234 字符），重合度由 `0.000` 变为 `0.118`（仍为 `low`）。

### 4. Q170（`numeric_or_table | article_only | low`）
- **修订动因**：v1 使用 `"non-fine sanction laws"` 可能错误排除其他性质的罚款；v2 改写为针对 `other penalties`（特别是对不受 GDPR 行政罚款机制约束之违法情形）的国家国内法向**欧洲委员会**通知的截止期限，且不泄露条文编号。
- **Question**：
  - v1：`By what deadline did EU governments have to report their national non-fine sanction laws to Brussels under the GDPR?`
  - v2：`By what deadline did EU member governments have to report to the European Commission their domestic statutes establishing alternative sanctions, particularly for violations falling outside GDPR monetary penalties?`
- **Gold Answer**：
  - v2 将接收机关明确为 `the European Commission` 并表述为 `those national rules on other penalties`，保留 `25 May 2018` 与后续修订及时通知义务。
- **Gold Evidence**：`gdpr:art:84` 两段引文不变（208 + 194 字符），重合度由 `0.000` 变为 `0.150`（仍为 `low`）。

### 5. Q172（`unanswerable | none | na | absence_kind:a`）
- **修订动因**：独立审阅发现 v1 网络责任保险义务问题与历史 Q047 考查同一缺失事实，v2 完全更换为全新合规考点：**雇主在授予员工访问个人数据权限前，GDPR 是否强制要求进行员工背景调查（background checks）**。
- **Question**：
  - v1：`Does the GDPR require data controllers to maintain cyber liability insurance to cover damages from a personal data breach?`
  - v2：`Does the GDPR require businesses to conduct background checks on employees before granting them access to personal data?`
- **Gold Answer & Notes**：
  - v2 Gold Answer：`Not specified; the GDPR regulates employee data processing and criminal conviction data, and requires staff access controls, but does not mandate employee background checks.`
  - `hard_negative:gdpr:art:88`；`search:variants=background check, vetting, screening, criminal record, recruitment`；`inspected=gdpr:art:88, gdpr:rec:155, gdpr:art:10, gdpr:art:32`。
