# v0.1.0 Release Notes

## Highlights

- 多源情报 RAG 分析闭环：检索证据、抽取实体、整理时间线、评估风险、生成报告。
- 提供 CLI、FastAPI、Docker、docker-compose、Makefile 和 smoke test。
- README 增加架构图和 smoke 输出图，便于 GitHub 展示和面试讲解。
- 文档包含 API、部署、复现、评估方案、路线图和面试讲述稿。

## Verification

```bash
python3 -m pytest tests/ -q
python3 scripts/smoke_test.py
```

期望 smoke 输出包含：

- `status: ok`
- `evidence_count: 6`
- `risk_level: 高`
- `report_contains_citations: true`

## Next

- 接入 Chroma/FAISS 和 hybrid search。
- 增加 Reranker、证据充足性判断和拒答。
- 用 LangGraph 改造 Agent 编排。
- 接入真实数据源、权限审计和可视化 trace。
