# API 文档

## `GET /health`

检查服务状态。

返回：

```json
{"status":"ok","service":"multi-source-intelligence-rag-agent"}
```

## `POST /ask`

输入问题，返回完整分析结果。

请求：

```json
{
  "question": "北岭港夜间低空目标是否代表安全风险？",
  "top_k": 6
}
```

响应字段：

| 字段 | 说明 |
|---|---|
| `question` | 原始问题 |
| `evidence` | 召回证据列表 |
| `entities` | 抽取出的地点、资产、事件 |
| `timeline` | 时间线 |
| `risk` | 风险等级、分数和理由 |
| `report` | Markdown 报告 |

## `POST /report`

只返回 Markdown 报告，适合前端直接渲染。
