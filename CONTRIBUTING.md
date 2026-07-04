# Contributing

## 开发流程

1. 创建虚拟环境并安装开发依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

2. 运行测试：

```bash
make test
```

3. 运行格式和静态检查：

```bash
make lint
make format
```

## 提交要求

- 不提交 `.env`、真实凭据、真实业务数据、模型权重和推理输出。
- 新增接口时同步更新 `docs/api.md`。
- 修改核心流程时同步更新 `docs/architecture.md` 和测试。
