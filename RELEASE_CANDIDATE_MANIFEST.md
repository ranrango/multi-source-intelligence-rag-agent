# Release Candidate Manifest

Generated: 2026-07-04

## Included

- `README.md`
- `pyproject.toml`
- `Makefile`
- `Dockerfile`
- `docker-compose.yml`
- `.env.example`
- `.gitignore`
- `src/app/*.py`
- `scripts/*.py`
- `examples/*`
- `data/*.md`
- `tests/*.py`
- `docs/*.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `LICENSE`

## Intentionally Excluded

- `.env`
- `logs/`
- 真实情报数据
- 真实账号凭据
- 模型权重和大文件输出

## Release Notes

本版本用于本地审核和 GitHub 首次发布候选。默认检索和分析流程不依赖外部服务，适合面试现场演示。

## Post-Release Improvements

- 增加 `scripts/smoke_test.py` 一键自检。
- 增加 examples、评估方案和路线图文档。
- README 增加预期输出和项目展示说明。
