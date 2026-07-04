from __future__ import annotations

from pathlib import Path

from .retriever import search
from .tools import assess_risk, build_timeline, extract_entities, generate_report, write_trace


def run_analysis(question: str, top_k: int = 6, data_dir: Path | str | None = None) -> dict[str, object]:
    evidence = search(question, top_k=top_k, data_dir=data_dir)
    write_trace("rag_search", {"question": question, "evidence_ids": [item.id for item in evidence]})

    entities = extract_entities(evidence)
    write_trace("extract_entities", entities)

    timeline = build_timeline(evidence)
    write_trace("build_timeline", {"events": len(timeline)})

    risk = assess_risk(evidence, entities)
    write_trace("assess_risk", risk)

    report = generate_report(question, evidence, entities, timeline, risk)
    return {
        "question": question,
        "evidence": [item.__dict__ for item in evidence],
        "entities": entities,
        "timeline": timeline,
        "risk": risk,
        "report": report,
    }
