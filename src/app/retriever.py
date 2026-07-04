from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]")
DEFAULT_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


@dataclass(frozen=True)
class EvidenceChunk:
    id: str
    source: str
    source_type: str
    confidence: float
    text: str
    score: float = 0.0


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def _parse_document(path: Path) -> tuple[dict[str, str], str]:
    metadata: dict[str, str] = {"source": path.stem, "source_type": "unknown", "confidence": "0.70"}
    lines = path.read_text(encoding="utf-8").splitlines()
    body_start = 0
    for index, line in enumerate(lines):
        if not line.strip():
            body_start = index + 1
            break
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata, "\n".join(lines[body_start:]).strip()


def load_chunks(data_dir: Path | str | None = None) -> list[EvidenceChunk]:
    root = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    chunks: list[EvidenceChunk] = []
    for path in sorted(root.glob("*.md")):
        metadata, body = _parse_document(path)
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
        for number, paragraph in enumerate(paragraphs, start=1):
            chunks.append(
                EvidenceChunk(
                    id=f"{path.stem}-{number}",
                    source=metadata.get("source", path.stem),
                    source_type=metadata.get("source_type", "unknown"),
                    confidence=float(metadata.get("confidence", "0.70")),
                    text=paragraph,
                )
            )
    return chunks


def search(query: str, top_k: int = 6, data_dir: Path | str | None = None) -> list[EvidenceChunk]:
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    chunks = load_chunks(data_dir)
    document_frequency: dict[str, int] = {}
    chunk_tokens: dict[str, list[str]] = {}
    for chunk in chunks:
        tokens = tokenize(chunk.text + " " + chunk.source + " " + chunk.source_type)
        chunk_tokens[chunk.id] = tokens
        for token in set(tokens):
            document_frequency[token] = document_frequency.get(token, 0) + 1

    scored: list[EvidenceChunk] = []
    total_docs = max(len(chunks), 1)
    for chunk in chunks:
        tokens = chunk_tokens[chunk.id]
        token_count = len(tokens) or 1
        score = 0.0
        for token in query_tokens:
            tf = tokens.count(token) / token_count
            idf = math.log((total_docs + 1) / (document_frequency.get(token, 0) + 1)) + 1
            score += tf * idf
        if score > 0:
            scored.append(
                EvidenceChunk(
                    id=chunk.id,
                    source=chunk.source,
                    source_type=chunk.source_type,
                    confidence=chunk.confidence,
                    text=chunk.text,
                    score=round(score * chunk.confidence * 100, 4),
                )
            )

    return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]
