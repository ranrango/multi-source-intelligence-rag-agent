from fastapi.testclient import TestClient

from src.app.main import app


client = TestClient(app)


def test_health_endpoint_reports_service_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "multi-source-intelligence-rag-agent",
    }


def test_ask_endpoint_returns_evidence_risk_and_report():
    response = client.post(
        "/ask",
        json={"question": "北岭港东侧堤坝无人机活动是否异常？", "top_k": 4},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["question"]
    assert len(payload["evidence"]) >= 3
    assert payload["risk"]["level"] in {"低", "中", "高"}
    assert "多源情报分析报告" in payload["report"]


def test_report_endpoint_returns_markdown_report_only():
    response = client.post(
        "/report",
        json={"question": "北岭港夜间低空目标是否代表安全风险？", "top_k": 3},
    )

    payload = response.json()
    assert response.status_code == 200
    assert set(payload) == {"report"}
    assert payload["report"].startswith("# 多源情报分析报告")
