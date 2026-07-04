from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.app.agent import run_analysis


DEFAULT_QUESTION = "北岭港东侧堤坝无人机活动是否异常？请说明证据和风险。"


def run_smoke_test() -> dict[str, object]:
    result = run_analysis(DEFAULT_QUESTION, top_k=6)
    report = str(result["report"])
    evidence_count = len(result["evidence"])
    risk = result["risk"]
    checks = {
        "service": "multi-source-intelligence-rag-agent",
        "status": "ok" if evidence_count >= 3 and "[" in report else "failed",
        "question": DEFAULT_QUESTION,
        "evidence_count": evidence_count,
        "risk_level": risk["level"],
        "risk_score": risk["score"],
        "report_contains_citations": "[" in report and "]" in report,
    }
    return checks


def main() -> None:
    print(json.dumps(run_smoke_test(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
