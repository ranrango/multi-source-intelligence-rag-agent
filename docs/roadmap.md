# Roadmap

## v0.1 当前版本

- 标准库关键词检索。
- 多源样例情报资料。
- 规则化实体抽取、时间线整理、风险评估。
- CLI、FastAPI、Docker、smoke test 和项目文档。

## v0.2 检索增强

- 引入 Chroma 或 FAISS 保存向量。
- 增加关键词 + 向量 hybrid search。
- 增加 Reranker，提升复杂问题下的证据排序。
- 增加 evidence sufficiency 判断，证据不足时拒答。

## v0.3 Agent 编排升级

- 将固定流程升级为 LangGraph 状态机。
- 工具注册表改为显式 schema。
- 增加 max steps、工具白名单和失败重试。
- 将 trace 结构化为可视化调用链。

## v0.4 生产交付

- 接入文件上传、网页采集、传感器日志和工单系统。
- 增加用户身份、权限控制和审计日志。
- 支持异步报告生成和 PDF/HTML 导出。
- 建立评测集，监控召回率、引用准确率、幻觉率和延迟。
