PYTHON ?= python3
PORT ?= 8010

.PHONY: help install install-dev run api test lint format docker-build docker-run

help:
	@echo "可用命令："
	@echo "  install      安装运行依赖"
	@echo "  install-dev  安装开发依赖"
	@echo "  run          运行 CLI 示例"
	@echo "  api          启动 FastAPI 服务"
	@echo "  test         运行测试"
	@echo "  lint         运行 ruff 检查"
	@echo "  format       运行 black 格式检查"
	@echo "  docker-build 构建镜像"
	@echo "  docker-run   运行容器"

install:
	$(PYTHON) -m pip install -e .

install-dev:
	$(PYTHON) -m pip install -e ".[dev]"

run:
	$(PYTHON) -m src.app.cli --question "北岭港东侧堤坝无人机活动是否异常？请说明证据和风险。"

api:
	uvicorn src.app.main:app --reload --port $(PORT)

test:
	$(PYTHON) -m pytest tests/ --tb=short -q

lint:
	ruff check src/ tests/

format:
	black --check src/ tests/

docker-build:
	docker build -t multi-source-intelligence-rag-agent:latest .

docker-run:
	docker run --rm -p $(PORT):8010 multi-source-intelligence-rag-agent:latest
