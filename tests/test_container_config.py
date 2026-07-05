from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_dockerfile_declares_http_healthcheck():
    dockerfile = (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert "HEALTHCHECK" in dockerfile
    assert "127.0.0.1:8010/health" in dockerfile


def test_compose_declares_service_healthcheck():
    compose = (REPO_ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    assert "healthcheck:" in compose
    assert "127.0.0.1:8010/health" in compose


def test_makefile_exposes_container_runtime_check():
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")

    assert "docker-smoke:" in makefile
    assert "container-check:" in makefile
    assert "docker-smoke" in makefile.split("container-check:", 1)[1]
