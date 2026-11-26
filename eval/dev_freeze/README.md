# 确认性评测冻结前的 Dev 复核

日期 **2026-11-26**。基线提交 5352f1d。以下结果来自33道可回答 Dev 题。

## 同分规则与影响

生产评测和单题查看器共用新的内容键。仅对完全相同的分数比较 SHA-256 及字符坐标。排序键先比较块文本，再比较来源单元全文，最后比较起止位置。法规名、块 ID、文件名及语料位置不参与键计算。当前语料在四档切块和整单元配置中均无重复完整键。未来语料若有完全相同的内容键，构建时会报错以便明确处理重复来源。这个确定性规则移除了法规名前缀优先级，结果仍可能受语料内容分布和模型数值差异影响。

| 检索器 | 排序数 | 有同分项 Top 5 / 10 / 50 | 第50与51名同分 | Top 50 AI Act 块数，原规则 → 反向同分 → 内容键 |
| --- | ---: | --- | ---: | --- |
| BM25（含整单元） | 165 | 0 / 0 / 2 | 1 | 4869 → 4868 → 4868 |
| Dense | 132 | 0 / 0 / 0 | 0 | 3944 → 3944 → 3944 |
| RRF（固定旧版两路上游） | 132 | 25 / 58 / 132 | 51 | 3915 → 3894 → 3900 |

BM25 / Dense 的反向对照对同一批分数倒转语料次序，在不重新构建分数的情况下隔离同分引起的排序偏向。BM25 的一次前50边界变化涉及跨法规，内容键同样让 GDPR 块入围，最终预算内 Recall 相同。Dense 在本批模型与数据中未见截点同分，统一使用内容键是为了让新语料出现同分时也有可复现规则。RRF 的反向对照只在同分时反转原 ID 顺序。前5的 AI Act 位置数为371 → 364 → 367，前10为753 → 740 → 745。位置变化只是同分反事实对照，无法说明语料整体是否平衡。

完整运行保存每题的候选 ID、预算内字符数、块数、RR、任意重叠 Recall 与50%覆盖 Recall。旧规则858行的 Recall、RR、块数和字符数逐值复现归档。全量中立规则858行，仅两行 Recall 变化，均可在保持原 BM25 / Dense 的 RRF 敏感性对照中复现。

| 8000 字符预算 | 切块字符 | 旧 Recall → 新 Recall |
| --- | ---: | --- |
| Q062 | 800 | 1 → 0 |
| Q022 | 2000 | 0 → 1 |

Hybrid 在8000预算的800切块均值从 .551 至 .520，2000切块从 .485 至 .515。四档等权均值仍为 .5354。4000预算的四档及 400 → 800 的原下降（.556 → .338）相同。BM25 与 Dense 的预算内任意重叠和50%覆盖 Recall 均逐题相同。

## 统计和功效

主协议使用 B=200000、seed 0，模拟 p 下限约0.000005。新旧规则的 Dev 试算中，均只有 H2(b) 两项 Low 对比通过主族 Holm。新版 Dense−BM25 效应 +.328、校正 p 约 .0030，Hybrid−BM25 效应 +.219、校正 p 约 .0033。H1、H2(a) 的主要界值和 H2(c) 仍缺足够证据。探索性表仍含多跳及其他原有对比。

H2(a) 的 Dev High 只有10题，8000字符四档等权的 BM25−Dense 均值 −.092、配对标准差 .318。用该标准差、真实差值0、非劣界值 .05 和80%功效按独立正态近似，单侧 α=.05 约需251道 High 题，按主族首步 α=.05/8 约需453道。估计基于小样本，尚未考虑共享证据造成的额外依赖。合并锁定集预计仅102道可回答题，High 更少。这个数量级说明功效风险，实际可检测差异在冻结时结合计划 High 构成和证据簇数另行估算。

预先声明的连续分析用全部33道 Dev 可回答题和31簇。词汇重合度每增加0.10，BM25−Dense 的拟合差值增加 **.102**，证据簇 Bootstrap 95%区间为 [.005, .201]。新旧结果相同。这是描述性关联，不能建立 High 组的非劣效性。

## 复现

BGE 本机快照为 `5c38ec7c405ec4b44b94cc5a9bb96e735b38267a`，权重 SHA-256 为 `3c9f31665447c8911517620762200d2245a2518d6e7208acc78cd9db317e21ad`。使用项目 eu-rag 环境和现有语料快照。运行时记录题库、JSONL 与模型权重哈希。

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 OMP_NUM_THREADS=4 python -m src.audit_dev_ties --model "$MODEL" --out-dir eval/dev_freeze
python -m src.analyze_dev --results eval/dev_freeze/dev_legacy.csv --out-dir eval/dev_freeze/legacy_stats
python -m src.analyze_dev --results eval/dev_freeze/dev_neutral.csv --out-dir eval/dev_freeze/neutral_stats
python -m pytest -q
```

- [旧规则逐题表](dev_legacy.csv) · [仅改变 RRF 同分规则](dev_rrf_only.csv) · [全量中立规则逐题表](dev_neutral.csv)
- [同分审计明细](tie_audit.csv) · [旧版主协议试算](legacy_stats/primary_protocol_dev.csv) · [新版主协议试算](neutral_stats/primary_protocol_dev.csv) · [连续分析](neutral_stats/continuous_overlap_dev.csv)
- [扩样与确认性评测协议](../dev_pilot_p1/expansion_protocol.md)
