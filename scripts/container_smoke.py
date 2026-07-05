from __future__ import annotations

import argparse
import subprocess
import sys
import time
import urllib.request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run container and verify /health.")
    parser.add_argument("--image", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--host-port", required=True)
    parser.add_argument("--container-port", required=True)
    parser.add_argument("--health-url", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=45)
    return parser.parse_args()


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, capture_output=True, text=True)


def wait_for_health(url: str, timeout_seconds: int) -> str:
    deadline = time.time() + timeout_seconds
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                body = response.read().decode("utf-8")
                if response.status == 200:
                    return body
        except Exception as exc:  # pragma: no cover - exercised in CI with Docker
            last_error = exc
        time.sleep(1)
    raise RuntimeError(f"health check failed for {url}: {last_error}")


def main() -> int:
    args = parse_args()
    run(["docker", "rm", "-f", args.name], check=False)
    try:
        run(
            [
                "docker",
                "run",
                "-d",
                "--name",
                args.name,
                "-p",
                f"{args.host_port}:{args.container_port}",
                args.image,
            ]
        )
        body = wait_for_health(args.health_url, args.timeout_seconds)
        print(body)
        return 0
    except Exception as exc:
        logs = run(["docker", "logs", args.name], check=False)
        if logs.stdout:
            print(logs.stdout, file=sys.stderr)
        if logs.stderr:
            print(logs.stderr, file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    finally:
        run(["docker", "rm", "-f", args.name], check=False)


if __name__ == "__main__":
    raise SystemExit(main())
