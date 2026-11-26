# Dev Pilot P1 统计与诊断

日期 **2026-11-20**。所有比较均为探索性。原预注册假设见项目 README。[扩样与 amendment 草案](expansion_protocol.md)

收尾更新 **2026-11-20**。前瞻性检验定义见 [扩样与确认性评测协议](expansion_protocol.md)。本页原有比较继续作为探索性复现，新增主检验表为在 Dev 上试算该协议的输出。[收尾核查结果](closeout.md)

2026-11-26 的冻结前修复、B=200000 与新旧同分对照见 [Dev 复核](../dev_freeze/README.md)。下方保留历史 P1 分析口径。

## 分析口径

- 观测单位为题。按 QID 对齐方法和配置，重复或不完整的配置矩阵会报错。四档固定切块 400、800、1200、2000 字符。8000 字符是与原假设对应的近似主预算，4000 是另一分析预算。整单元 BM25 保存在原始快照中。
- H1 采用题内 C = (R800 + R1200)/2 − (R400 + R2000)/2；另检验中间两档平均值分别减 R400 与 R2000。C 为正只说明相对两端的平均优势，评估倒 U 形时同时检查两个端点及四档原均值。当前资料没有附 Claude 的公式原文，采用上述明确的平均中段减平均端点定义。
- H2 效应为同题 Recall 差。每档单独给结果，并给四档等权的题内均值比较。H2(a) 的高重合组在阈值处归 High，检验 BM25 − Dense 是否超过 −0.05。H2(b) 在低重合与多跳组比较 Dense − BM25、Hybrid − BM25。不同题型的三个方法对均输出双侧差异检验，作为 H2(c) 的描述，正式非劣效方案见草案。
- 逐题差值有放回 Bootstrap 10000 次，seed 0，95% 百分位区间使用项目现有 bootstrap_ci。p 值用在原假设边界中心化的题内差值重抽样分布，按相应单侧或双侧尾部计数，加一平滑。区间为逐比较区间，Holm 作用于 p 值。有效配对小于2时保留该行且不估计 p 值；校正时保留其计划占位。少量样本及常量差值会使 Bootstrap 区间退化，需结合 n 与分布阅读。
- Holm 族对每个指标和队列固定。H1 形状为3种方法 × 2预算 × 3对比，共18项。H2 整体为3方法对 × 2预算 × 5档（含四尺寸汇总），共30项。H2(a) 每阈值10项，H2(b) Low 每阈值20项，H2(b) Multi-hop 20项，题型比较4题型 × 3方法对 × 2预算 × 5档，共120项。敏感性阈值、排除检视题及覆盖指标各自列全族。扫描不同版本后挑选命中的推断不在这些族的控制范围内。
- 主队列33道可回答 Dev，移除已检视7题后26道。依原 CSV 中的 overlap 值考察0.20、0.25、0.30、0.40。它在检索时已舍入到3位。25道 AI 起草题保留原 pending human review。
- 原 CSV 仅给每题 n_chunks、ctx_chars、Recall、RR 和重合度等，无入选块与 span 坐标，故无法从原 CSV 本身推出50%覆盖。重算 Dev 时，按同单元、半开坐标裁至 gold span，并合并入选块之间的重合部分。覆盖至少一半算该 span 命中。原指标“任意字符重叠即命中”保持为主指标。重算版同口径结果和覆盖指标各自输出。

## 文件与复现

| 文件 | 用途 |
| --- | --- |
| [pilot_input.csv](pilot_input.csv) | 原始 Dev 表的逐字节快照，含整单元对照。 |
| [coverage_replay.csv](coverage_replay.csv) | 同口径和50%覆盖重算，以及两档 Hybrid 诊断。rank 数组按 gold span 顺序排列，null 表示候选池内未命中。 |
| [means.csv](means.csv) | 按方法、尺寸、预算、队列和指标输出均值及置信区间。 |
| [contrasts.csv](contrasts.csv) | 全部配对对比，含效应量、有效 n、原始及 Holm 校正 p 值。 |
| [primary_protocol_dev.csv](primary_protocol_dev.csv) | 预定主族与次要界值族在 Dev 上的试算。一个交并声明保留两条分量，共享其声明级 Holm p。 |
| [rrf_ties.csv](rrf_ties.csv) | Dev 每题每尺寸的 top-5、10、50 精确同分与反转 tie-break 对照。 |
| [findings.md](findings.md) | 实测统计与 Hybrid 诊断。 |

从项目根目录运行，依赖为项目 eu-rag 环境。MODEL 指向本地 BAAI/bge-small-en-v1.5 快照 5c38ec7c405ec4b44b94cc5a9bb96e735b38267a。

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 OMP_NUM_THREADS=4 python -m src.replay_dev --model "$MODEL" --out results/coverage_replay.csv --rrf-ties results/rrf_ties.csv
python -m src.analyze_dev --results eval/dev_pilot_p1/pilot_input.csv --coverage results/coverage_replay.csv --out-dir results/dev_analysis
python -m pytest -q
```

Python 3.10.22、NumPy 2.2.6、pandas 2.3.3、torch 2.14.1、sentence-transformers 6.2.0。输入快照 SHA-256 为 af67184affc8e73a38c8ca887b7217334d4b7f5629498f2176d1461092b775de。重算时记录题库、语料和模型权重哈希。
