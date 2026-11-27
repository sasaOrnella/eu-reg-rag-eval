# Locked Test 生成与验收规则变更

## v3.1 · 2026-11-27

- 保持总量300与 Dev 80／Locked Test 220。根据项目所有者的定向修订，替换原来每法相同的新增联合配额，采用各90题的新题型与精确证据 × High/Low 格。
- 每法拆为五批，每批18题。登记批次 ID、题号范围与逐格累计配额。
- 修改不可回答题规则。每部法规完整队列覆盖四类，数量或细节未规定类最多四题。结构化核对 absence_kind、hard_negative 和查询记录，独立审核其法律语义。
- 校验器支持部分批次、完整90题及全180题。部分批次可载入已通过批次做累计校验。保留既有正证据排除范围，并复核两部法规可用单元的容量。
- Gemini 专用包按 v3.1 重建，内附更新的 SHA256SUMS。既有统计协议段落和冻结配置与 v3.0 相同。

[v3.0 协议](history/v3.0/expansion_protocol_v3.md) · [v3.0 配额](history/v3.0/locked_test_quotas_v3.json) · [v3.0 校验器](history/v3.0/check_locked_test_quotas.py.txt) · [v3.0 证据池核查](history/v3.0/locked_test_evidence_pool_v3.md)
