# 复现指南

## 1. 运行 CLI

```bash
python3 -m src.app.cli --json
```

## 2. 运行测试

```bash
python3 -m pytest tests/ -q
```

## 3. 启动 API

```bash
pip install -e ".[dev]"
uvicorn src.app.main:app --reload --port 8010
```

## 4. 验证输出

重点检查：

- 是否召回多来源证据。
- 报告是否包含风险等级。
- 结论是否包含引用来源。
- `logs/agent_trace.jsonl` 是否生成调用记录。
