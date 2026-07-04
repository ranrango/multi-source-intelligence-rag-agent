from __future__ import annotations

import argparse
import json

from .agent import run_analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="多源情报 RAG 分析 Agent")
    parser.add_argument("--question", default="北岭港东侧堤坝无人机活动是否异常？请说明证据和风险。")
    parser.add_argument("--top-k", type=int, default=6)
    parser.add_argument("--json", action="store_true", help="输出完整 JSON")
    args = parser.parse_args()

    result = run_analysis(args.question, top_k=args.top_k)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["report"])


if __name__ == "__main__":
    main()
