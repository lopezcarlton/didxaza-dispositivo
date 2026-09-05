#!/usr/bin/env python3
"""Read-only batch runner for arbitrary NEW_WRITTEN_ANALYSIS_TARGET material.

This entry point exists to make blind written probes reproducible against the
current Analyzer without hard-coding probe text into tests or treating the
material as benchmark, gold, regression, rule-discovery, correction, or
orthographic authority.

Input is accepted from exactly one of --surface, --file, or --stdin. Output is a
single JSON envelope on stdout. The runner does not modify repository artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

from analyzer_v0_35_migrated_adapter import build_migrated_analyzer


TARGET_ROLE = "NEW_WRITTEN_ANALYSIS_TARGET"
SCHEMA_VERSION = "1.0"


def _git_commit() -> str | None:
    github_sha = os.environ.get("GITHUB_SHA")
    if github_sha:
        return github_sha
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).resolve().parents[2],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _nonempty_lines(text: str) -> list[tuple[int, str]]:
    return [
        (line_number, line)
        for line_number, line in enumerate(text.splitlines(), 1)
        if line.strip()
    ]


def analyze_target_text(
    text: str,
    *,
    input_kind: str,
    item_prefix: str = "NEW_WRITTEN_TARGET",
    biyubi_path: str | Path | None = None,
    require_biyubi: bool = False,
) -> dict[str, Any]:
    """Analyze non-empty input lines and return a non-licensing JSON envelope."""

    encoded = text.encode("utf-8")
    lines = _nonempty_lines(text)
    engine = build_migrated_analyzer(
        biyubi_path=biyubi_path,
        require_biyubi=require_biyubi,
    )
    try:
        results = []
        for ordinal, (source_line_number, surface) in enumerate(lines, 1):
            analysis = engine.analyze(surface, item_id=f"{item_prefix}_L{ordinal:03d}")
            results.append(
                {
                    "source_line_number": source_line_number,
                    "original_surface": surface,
                    "analysis": analysis,
                }
            )
    finally:
        engine.close()

    return {
        "schema_version": SCHEMA_VERSION,
        "target_role": TARGET_ROLE,
        "repository_commit": _git_commit(),
        "input_kind": input_kind,
        "input_sha256": hashlib.sha256(encoded).hexdigest(),
        "input_bytes": len(encoded),
        "analyzed_nonempty_line_count": len(results),
        "benchmark_use": False,
        "gold_use": False,
        "regression_source_use": False,
        "rule_discovery": False,
        "correction_authority": False,
        "generation_license": False,
        "orthographic_authority": False,
        "knowledge_promotion_from_target": False,
        "results": results,
    }


def _read_input(args: argparse.Namespace) -> tuple[str, str]:
    selected = sum(
        option is not None
        for option in (args.surface, args.file)
    ) + int(args.stdin)
    if selected != 1:
        raise SystemExit("Choose exactly one input source: --surface, --file, or --stdin")

    if args.surface is not None:
        return args.surface, "surface_argument"
    if args.file is not None:
        return Path(args.file).read_text(encoding="utf-8"), "utf8_file"
    import sys

    return sys.stdin.read(), "stdin"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read-only batch execution of arbitrary NEW_WRITTEN_ANALYSIS_TARGET text",
    )
    parser.add_argument("--surface", help="Analyze one surface string")
    parser.add_argument("--file", help="Analyze non-empty lines from a UTF-8 text file")
    parser.add_argument("--stdin", action="store_true", help="Read UTF-8 text from stdin")
    parser.add_argument("--item-prefix", default="NEW_WRITTEN_TARGET")
    parser.add_argument("--biyubi-xlsx")
    parser.add_argument("--require-biyubi", action="store_true")
    args = parser.parse_args()

    text, input_kind = _read_input(args)
    payload = analyze_target_text(
        text,
        input_kind=input_kind,
        item_prefix=args.item_prefix,
        biyubi_path=args.biyubi_xlsx,
        require_biyubi=args.require_biyubi,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
