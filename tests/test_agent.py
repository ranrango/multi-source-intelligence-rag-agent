from src.app.agent import run_analysis


def test_run_analysis_returns_report_and_risk():
    result = run_analysis("北岭港东侧堤坝无人机活动是否异常？", top_k=4)
    assert result["evidence"]
    assert result["risk"]["level"] in {"低", "中", "高"}
    assert "多源情报分析报告" in result["report"]
