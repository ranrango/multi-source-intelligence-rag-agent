# 架构设计

## 目标

构建一个面向安全态势分析的 Agent。它需要把“问答”拆成可控步骤：检索证据、抽取实体、整理时间线、评估风险、生成报告，并记录每一步 trace。

## 模块说明

| 模块 | 职责 | 当前实现 | 生产替换 |
|---|---|---|---|
| Retriever | 从多源资料中召回证据 | 标准库关键词检索 | Embedding + FAISS/Chroma + Reranker |
| Planner | 决定下一步动作 | 固定流程编排 | LLM function calling / LangGraph |
| Tools | 执行结构化分析 | 规则工具 | LLM 工具、NER、风险模型 |
| Memory | 保存中间状态 | Python dict | Redis / 数据库 / LangGraph state |
| Evaluator | 判断结果质量 | 风险规则和证据数量 | 自动评测集、事实一致性检查 |
| Observability | 记录调用链 | JSONL trace | OpenTelemetry / LangSmith / 自研 trace |

## 数据流

```text
用户问题
  -> RAG 检索 Top-K 证据
  -> 实体抽取
  -> 时间线整理
  -> 风险评估
  -> 报告生成
  -> 输出证据引用和不确定性
```

## 为什么这样设计

安全态势分析不能只输出“看起来合理”的结论，必须回答三个问题：证据来自哪里、推理过程是什么、结论有多不确定。因此系统把每个动作拆成工具，并在报告中保留引用。
