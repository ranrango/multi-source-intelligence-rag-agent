PYTHON ?= python3
PORT ?= 8010
IMAGE ?= multi-source-intelligence-rag-agent:latest
CONTAINER_NAME ?= multi-source-intelligence-rag-agent-smoke
INTERNAL_PORT ?= 8010
HEALTH_URL ?= http://127.0.0.1:$(PORT)/health

.PHONY: help install install-dev check release-check container-check run api smoke test lint format docker-build docker-smoke docker-run

help:
	@echo "可用命令："
	@echo "  install      安装运行依赖"
	@echo "  install-dev  安装开发依赖"
	@echo "  run          运行 CLI 示例"
	@echo "  api          启动 FastAPI 服务"
	@echo "  check        本地常规验收"
	@echo "  release-check 交付验收，包含 Docker 构建"
	@echo "  container-check 容器启动与健康检查验收"
	@echo "  smoke        运行一键自检"
	@echo "  test         运行测试"
	@echo "  lint         运行 ruff 检查"
	@echo "  format       运行 black 格式检查"
	@echo "  docker-build 构建镜像"
	@echo "  docker-run   运行容器"

install:
	$(PYTHON) -m pip install -e .

install-dev:
	$(PYTHON) -m pip install -e ".[dev]"

check: test smoke lint format

release-check: check container-check

container-check: docker-build docker-smoke

run:
	$(PYTHON) -m src.app.cli --question "北岭港东侧堤坝无人机活动是否异常？请说明证据和风险。"

api:
	uvicorn src.app.main:app --reload --port $(PORT)

smoke:
	$(PYTHON) scripts/smoke_test.py

test:
	$(PYTHON) -m pytest tests/ --tb=short -q

lint:
	ruff check src/ scripts/ tests/

format:
	black --check src/ scripts/ tests/

docker-build:
	docker build -t $(IMAGE) .

docker-smoke:
	$(PYTHON) scripts/container_smoke.py --image $(IMAGE) --name $(CONTAINER_NAME) --host-port $(PORT) --container-port $(INTERNAL_PORT) --health-url $(HEALTH_URL)

docker-run:
	docker run --rm -p $(PORT):$(INTERNAL_PORT) $(IMAGE)
