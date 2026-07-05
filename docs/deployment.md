# 部署交付说明

## 本地部署

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn src.app.main:app --host 0.0.0.0 --port 8010
```

## Docker 部署

```bash
docker compose up --build
```

## 交付验收命令

本地常规验收：

```bash
make check
```

交付前完整验收：

```bash
make release-check
```

`release-check` 会额外执行 Docker 镜像构建；CI 会执行同样的交付验收命令，确保 API、离线 smoke、代码格式和 Docker 镜像构建都能通过。

## 交付给业务方

建议交付内容：

- API 地址和 `/docs` 文档。
- 样例请求与样例报告。
- 数据源接入说明。
- 日志和 trace 查看方式。
- 模型、检索库和规则配置说明。

## 生产化改造

- 将 `data/` 替换为对象存储、数据库或文档上传服务。
- 将检索替换为向量库，并保留关键词检索作为 hybrid search。
- 增加权限控制，避免敏感情报被越权访问。
- 加入异步任务队列，长报告生成走后台任务。
- 增加评测集，监控召回率、引用准确率、幻觉率和延迟。
