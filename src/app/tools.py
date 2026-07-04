from __future__ import annotations

import re
from collections import Counter
from datetime import datetime
from pathlib import Path

from .retriever import EvidenceChunk

TRACE_DIR = Path(__file__).resolve().parents[2] / "logs"

ENTITY_KEYWORDS = {
    "locations": ["北岭港", "东侧堤坝", "仓储区", "雷达站", "码头", "巡检航线"],
    "assets": ["无人机", "低空目标", "雷达", "摄像头", "通信车", "货运车辆"],
    "events": ["悬停", "绕飞", "维修", "误报", "干扰", "巡检", "报警", "封控"],
}

DATE_RE = re.compile(r"(?:2026[-年])?\d{1,2}[月-]\d{1,2}日?|\d{2}:\d{2}")


def extract_entities(evidence: list[EvidenceChunk]) -> dict[str, list[str]]:
    text = "\n".join(item.text for item in evidence)
    entities: dict[str, list[str]] = {}
    for group, words in ENTITY_KEYWORDS.items():
        entities[group] = [word for word in words if word in text]
    return entities


def build_timeline(evidence: list[EvidenceChunk]) -> list[dict[str, str]]:
    events: list[dict[str, str]] = []
    for item in evidence:
        matches = DATE_RE.findall(item.text)
        if matches:
            events.append({"time": matches[0], "event": item.text, "source": item.source})
    return events or [{"time": "未知", "event": item.text, "source": item.source} for item in evidence[:3]]


def assess_risk(evidence: list[EvidenceChunk], entities: dict[str, list[str]]) -> dict[str, object]:
    source_counter = Counter(item.source_type for item in evidence)
    joined = "\n".join(item.text for item in evidence)
    risk_score = 35

    if "传感器" in source_counter or "sensor" in source_counter:
        risk_score += 20
    if any(word in joined for word in ["连续", "多次", "重复", "三次"]):
        risk_score += 15
    if any(word in joined for word in ["夜间", "低空", "悬停", "绕飞"]):
        risk_score += 15
    if any(word in joined for word in ["维修", "计划", "演练"]):
        risk_score -= 10
    if entities.get("locations") and entities.get("assets"):
        risk_score += 10

    risk_score = max(0, min(100, risk_score))
    level = "高" if risk_score >= 75 else "中" if risk_score >= 50 else "低"
    return {
        "level": level,
        "score": risk_score,
        "reasons": [
            f"命中 {len(evidence)} 条证据，来源类型包括：{', '.join(sorted(source_counter))}",
            "检测到低空目标、港区位置或巡检相关实体" if entities.get("assets") else "实体信息不足，需要补充数据源",
            "存在内部通知或维修计划，结论需要区分真实威胁与计划活动" if "维修" in joined or "计划" in joined else "缺少明确的计划活动解释",
        ],
    }


def write_trace(step: str, payload: dict[str, object]) -> None:
    TRACE_DIR.mkdir(exist_ok=True)
    path = TRACE_DIR / "agent_trace.jsonl"
    line = {"time": datetime.utcnow().isoformat() + "Z", "step": step, "payload": payload}
    path.open("a", encoding="utf-8").write(str(line) + "\n")


def generate_report(question: str, evidence: list[EvidenceChunk], entities: dict[str, list[str]], timeline: list[dict[str, str]], risk: dict[str, object]) -> str:
    evidence_lines = [
        f"- [{item.id}] {item.source} / {item.source_type} / confidence={item.confidence:.2f}: {item.text}"
        for item in evidence
    ]
    timeline_lines = [f"- {item['time']}：{item['event']}（来源：{item['source']}）" for item in timeline]
    entity_lines = [f"- {key}: {', '.join(value) if value else '未明显命中'}" for key, value in entities.items()]

    return "\n".join(
        [
            f"# 多源情报分析报告",
            "",
            f"## 问题",
            question,
            "",
            "## 核心结论",
            f"当前风险等级为 **{risk['level']}**，风险分数 {risk['score']}/100。建议进入人工复核，并优先核查传感器日志、巡检计划和现场视频。",
            "",
            "## 关键证据",
            *evidence_lines,
            "",
            "## 时间线",
            *timeline_lines,
            "",
            "## 实体识别",
            *entity_lines,
            "",
            "## 风险理由",
            *(f"- {reason}" for reason in risk["reasons"]),
            "",
            "## 不确定性",
            "- 当前报告基于样例数据和规则评分，不能替代现场处置。",
            "- 若证据之间冲突，应以高可信传感器、原始视频和人工复核为准。",
        ]
    )
