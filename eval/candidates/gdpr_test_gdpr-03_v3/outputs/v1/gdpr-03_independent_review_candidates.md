# GDPR Locked Test · gdpr-03 需独立审阅的候选题清单

本批次全部 18 道候选题（`Q157–Q174`）均标记为 `author:ai | human_review:pending`，在正式纳入 Locked Test 前均需经合格独立审阅人完成法律支持度、证据必要性、改写自然度、歧义与真实缺失审阅。以下按**重点复核优先级**分类列出全部 18 题及核查要点。

## 一、高优先级独立审阅项（10 题）

### 1. Multi-hop 证据删减必要性与跨条文逻辑复核（4 题）
- **Q162**（`multi_hop | article_only | high (0.429)` | `gdpr:art:1`, `gdpr:art:44`）
  - **审阅要点**：核查欧盟内部自由流动（`art:1(3)`）与第三国/国际组织传输及再传输（`art:44`）的对比是否构成单一信息需求且双向必要；同时复核 `gdpr:art:44` 单句引文长度为 503 字符（<600 硬上限，>400 软提示）是否可保持完整单句不截断。
- **Q163**（`multi_hop | article_only | low (0.062)` | `gdpr:art:48`, `gdpr:art:96`）
  - **审阅要点**：核查“第三国法院依据成员国旧双边协议要求披露数据”这一跨条文桥梁（`art:48` 的 `in force` 要求 + `art:96` 的 2016-05-24 前合规存续条件）是否严谨无歧义；同时复核 `gdpr:art:48` 单句引文长度为 463 字符（>400 软提示）以及与 Q168（均引用 `art:48`）及 Q169（均引用 `art:96`）的语义区分度。
- **Q164**（`multi_hop | article_only | low (0.111)` | `gdpr:art:29`, `gdpr:art:18`）
  - **审阅要点**：核查受托处理者持有受限数据时的双重约束（`art:29` 控制者指令/法律要求 + `art:18(2)` 除存储外的法定例外）是否准确且删除任一条均无法完整作答；复核与 Q165（均引用 `art:18` 不同条款：`18(2)` vs `18(3)`）无事实重叠。
- **Q165**（`multi_hop | mixed | low (0.125)` | `gdpr:rec:67`, `gdpr:art:18`）
  - **审阅要点**：核查 `gdpr:rec:67` 提供的自动化系统技术锁定与标识说明是否确为条文未载明的必要信息（符合 R-E5），并与 `gdpr:art:18(3)` 解除限制前通知义务构成真正混合多跳。

### 2. Conditional 条件/例外边界复核（3 题）
- **Q166**（`conflicting_or_conditional | article_only | high (0.462)` | `gdpr:art:23` ×2）
  - **审阅要点**：核查 `gdpr:art:23(2)` 导言与 `(h)` 项分段引用是否充分，且答案准确反映 `where relevant` 前提与 `unless prejudicial to the purpose of the restriction` 例外。
- **Q167**（`conflicting_or_conditional | article_only | low (0.125)` | `gdpr:art:90` ×2）
  - **审阅要点**：核查题面中 “lawyers or doctors” 作为职业保密自然语境举例是否无误导性，答案是否准确限定在 `necessary and proportionate` 前提与“因保密活动取得之数据”范围；复核首段引文 498 字符（>400 软提示）。
- **Q168**（`conflicting_or_conditional | article_only | low (0.000)` | `gdpr:art:48` ×2）
  - **审阅要点**：核查 `gdpr:art:48` 拆分为规则段与条件/保留段（`without prejudice to other grounds for transfer pursuant to this Chapter`）后，答案是否准确区分必要条件与不排除第五章其他传输依据的法律效果。

### 3. Unanswerable 真实缺失与 Hard Negative 复核（3 题）
- **Q172**（`unanswerable | absence_kind:a | hard_negative:gdpr:art:82`）
  - **审阅要点**：确认 GDPR 全文（含 `art:82`, `rec:146`, `rec:54`, `art:32`）确未规定控制者须购买网络责任保险，且问法自然无提示词。
- **Q173**（`unanswerable | absence_kind:b | hard_negative:gdpr:art:36`）
  - **审阅要点**：确认询问“向 EDPB 预先登记常规客户数据处理活动的程序”属于自然虚假前提（而非可由 `rec:89` 直接用“No”回答的是非题），且 `art:30, 36, 70` 与 `rec:89` 结合阅读后确无此程序。
- **Q174**（`unanswerable | absence_kind:c | hard_negative:gdpr:art:43`）
  - **审阅要点**：确认 `ENISA` 在 GDPR 全文零出现，且 `art:42, 43, 70` 与 `rec:49`（仅提 CERTs/CSIRTs）未赋予 ENISA 印章审批或认证机构认可职责。

## 二、常规独立审阅项（8 题）

- **Q157**（`single_hop | article_only | high (0.308)` | `gdpr:art:31`）：复核 High 重合度接近阈值（0.308 ≥ 0.30）且无无关引文凑分，主体范围（controller, processor, representatives）准确。
- **Q158**（`single_hop | article_only | low (0.077)` | `gdpr:art:86`）：复核 `gdpr:art:86` 完整单句（435 字符，>400 软提示）及 `public authority / public body / private body performing a public-interest task` 涵盖完整性。
- **Q159**（`single_hop | article_only | low (0.000)` | `gdpr:art:32`）：复核零词面重合下语义对应是否自然准确（`cybersecurity safeguards` ↔ `appropriate level of security`），答案是否完整覆盖 `art:32(2)` 所列全部风险类型。
- **Q160**（`single_hop | recital_only | high (0.500)` | `gdpr:rec:51`）：复核照片是否构成生物识别数据/特殊类别数据的解释确仅见于 `gdpr:rec:51`（无对应条文直接规定，符合 R-E5）。
- **Q161**（`single_hop | recital_only | low (0.077)` | `gdpr:rec:22`）：复核“分支机构 vs 具备法人资格的子公司法律形式并非决定因素”的解释确仅见于 `gdpr:rec:22`（符合 R-E5）。
- **Q169**（`numeric_or_table | article_only | high (0.474)` | `gdpr:art:96`）：复核 `24 May 2016` 日期精确一致，且答案同步保留“符合该日前适用欧盟法”的条件。
- **Q170**（`numeric_or_table | article_only | low (0.000)` | `gdpr:art:84` ×2）：复核同时引用 `art:84(1)` 与 `art:84(2)` 对证明 `25 May 2018` 通知期限的充分性，以及“Brussels”指代欧盟委员会的日常问法自然度。
- **Q171**（`numeric_or_table | article_only | low (0.000)` | `gdpr:art:88` ×2）：复核同时引用 `art:88(1)` 与 `art:88(3)` 对证明 `25 May 2018` 通知期限的充分性，及与 Q170 的主题区隔度（非罚款处罚规则 vs 雇佣语境数据保护规则，Jaccard = 0.250）。
