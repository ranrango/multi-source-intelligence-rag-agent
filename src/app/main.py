from __future__ import annotations

from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .agent import run_analysis

app = FastAPI(title="多源情报 RAG 分析 Agent", version="0.1.0")


class AskRequest(BaseModel):
    question: str = Field(..., description="需要分析的问题")
    top_k: int = Field(6, ge=1, le=12, description="召回证据数量")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "multi-source-intelligence-rag-agent"}


@app.post("/ask")
def ask(request: AskRequest) -> Dict[str, object]:
    return run_analysis(request.question, top_k=request.top_k)


@app.post("/report")
def report(request: AskRequest) -> Dict[str, str]:
    result = run_analysis(request.question, top_k=request.top_k)
    return {"report": str(result["report"])}
