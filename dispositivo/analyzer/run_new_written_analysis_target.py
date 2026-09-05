#!/usr/bin/env python3
"""Read-only batch runner for arbitrary NEW_WRITTEN_ANALYSIS_TARGET material.

This entry point exists to make blind written probes reproducible against the
current Analyzer without hard-coding probe text into tests or treating the
material as benchmark, gold, regression, rule-discovery, correction, or
orthographic authority.

Input is accepted from exactly one of --surface, --file, or --stdin. Output is a
single JSON envelope on stdout. The runner does not modify repository artifacts.

From schema v1.1, each analyzed non-empty line may receive nearby non-empty lines
from the same target as `context_segments`. This is target-internal context only:
it is not authority, does not create rules, and cannot by itself resolve an
analysis. The current Analyzer may use it only through its explicitly
non-resolving contextual documentary-support layer.
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
SCHEMA_VERSION = "1.1"
DEFAULT_CONTEXT_RADIUS = 1


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


def _neighbor_context_segments(
    lines: list[tuple[int, str]],
    current_index: int,
    *,
    radius: int,
) -> list[dict[str, Any]]:
    """Return nearby analyzed lines as non-authoritative Didxazá context.

    Radius is measured over the sequence of non-empty analyzed lines. Blank input
    lines remain preserved indirectly through each segment's source line number,
    but they are not themselves analysis/context segments.
    """

    if radius < 0:
        raise ValueError("context_radius must be >= 0")
    if radius == 0 or not lines:
        return []

    start = max(0, current_index - radius)
    stop = min(len(lines), current_index + radius + 1)
    out = []
    for index in range(start, stop):
        if index == current_index:
            continue
        source_line_number, surface = lines[index]
        out.append(
            {
                "surface": surface,
                "source_line_number": source_line_number,
                "target_role": TARGET_ROLE,
                "authority_scope": "TARGET_INTERNAL_CONTEXT_NON_AUTHORITATIVE",
            }
        )
    return out


def analyze_target_text(
    text: str,
    *,
    input_kind: str,
    item_prefix: str = "NEW_WRITTEN_TARGET",
    biyubi_path: str | Path | None = None,
    require_biyubi: bool = False,
    context_radius: int = DEFAULT_CONTEXT_RADIUS,
) -> dict[str, Any]:
    """Analyze non-empty input lines and return a non-licensing JSON envelope."""

    if context_radius < 0:
        raise ValueError("context_radius must be >= 0")

    encoded = text.encode("utf-8")
    lines = _nonempty_lines(text)
    engine = build_migrated_analyzer(
        biyubi_path=biyubi_path,
        require_biyubi=require_biyubi,
    )
    try:
        results = []
        for line_index, (source_line_number, surface) in enumerate(lines):
            ordinal = line_index + 1
            context_segments = _neighbor_context_segments(
                lines,
                line_index,
                radius=context_radius,
            )
            analysis = engine.analyze(
                surface,
                item_id=f"{item_prefix}_L{ordinal:03d}",
                context_segments=context_segments,
            )
            results.append(
                {
                    "source_line_number": source_line_number,
                    "original_surface": surface,
                    "context_source_line_numbers": [
                        int(segment["source_line_number"])
                        for segment in context_segments
                    ],
                    "context_segment_count": len(context_segments),
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
        "target_internal_context_enabled": context_radius > 0,
        "target_internal_context_radius_nonempty_lines": context_radius,
        "target_internal_context_excludes_current_line": True,
        "target_internal_context_is_authority": False,
        "target_internal_context_can_create_rules": False,
        "target_internal_context_can_promote_knowledge": False,
        "target_internal_context_can_resolve_hypothesis_by_itself": False,
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
    parser.add_argument(
        "--context-radius",
        type=int,
        default=DEFAULT_CONTEXT_RADIUS,
        help="Nearby non-empty target lines supplied as non-authoritative context on each side (default: 1)",
    )
    args = parser.parse_args()

    if args.context_radius < 0:
        parser.error("--context-radius must be >= 0")

    text, input_kind = _read_input(args)
    payload = analyze_target_text(
        text,
        input_kind=input_kind,
        item_prefix=args.item_prefix,
        biyubi_path=args.biyubi_xlsx,
        require_biyubi=args.require_biyubi,
        context_radius=args.context_radius,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
