#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYZER_DIR = HERE.parent / "analyzer"
sys.path.insert(0, str(ANALYZER_DIR))

from analyzer_v0_35_migrated_adapter import build_migrated_analyzer  # noqa: E402


def main() -> None:
    input_path = HERE / "REAL_TEXT_PROBE_001.txt"
    lines = [line for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    engine = build_migrated_analyzer()
    results = []
    try:
        for idx, surface in enumerate(lines, start=1):
            item_id = f"REAL_TEXT_PROBE_001_L{idx:02d}"
            try:
                analysis = engine.analyze(surface, item_id=item_id)
                results.append({
                    "item_id": item_id,
                    "surface_exact": surface,
                    "status": "ANALYZED",
                    "analysis": analysis,
                })
            except Exception as exc:
                results.append({
                    "item_id": item_id,
                    "surface_exact": surface,
                    "status": "EXCEPTION",
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                })
    finally:
        engine.close()

    payload = {
        "probe_id": "REAL_TEXT_PROBE_001",
        "mode": "EXACT_TEXT_NO_NORMALIZATION",
        "cor001_policy": "ANALYSIS_TARGET_ONLY",
        "rule_discovery_from_probe": False,
        "input_line_count": len(lines),
        "results": results,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
