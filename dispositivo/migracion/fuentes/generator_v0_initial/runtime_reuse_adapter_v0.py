#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable, Any

EXPECTED_RUNTIME_SHA256 = "6e5c3e8ee9bb5dbd04666537dc423724eb4bc402440e670e5be81cfa54b5d7e5"
EXPECTED_DB_SHA256 = "2379773426baf4e3eace87c61ec17f7a1e1b9164421e56cf736d35eb64a5ebed"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_canonical_inputs(runtime_zip: Path, db_path: Path) -> None:
    if sha256(runtime_zip) != EXPECTED_RUNTIME_SHA256:
        raise RuntimeError("CANONICAL_RUNTIME_SHA256_MISMATCH")
    if sha256(db_path) != EXPECTED_DB_SHA256:
        raise RuntimeError("CANONICAL_DB_SHA256_MISMATCH")
    with zipfile.ZipFile(runtime_zip) as z:
        if z.testzip() is not None:
            raise RuntimeError("CANONICAL_RUNTIME_ZIP_INTEGRITY_FAILURE")


def load_generator_view(runtime_zip: Path, db_path: Path):
    """Load the existing v0.2.6 generator_view only after canonical hash gate."""
    verify_canonical_inputs(runtime_zip, db_path)
    tmp = tempfile.TemporaryDirectory(prefix="didxaza_runtime_v0153_")
    with zipfile.ZipFile(runtime_zip) as z:
        z.extractall(tmp.name)
    roots = [p for p in Path(tmp.name).iterdir() if p.is_dir()]
    if len(roots) != 1:
        tmp.cleanup()
        raise RuntimeError("UNEXPECTED_RUNTIME_ARCHIVE_LAYOUT")
    sys.path.insert(0, str(roots[0]))
    try:
        mod = importlib.import_module("didxaza_runtime_v0_2_6_evidence_adjudication")
        v153 = importlib.import_module("didxaza_runtime_v0_2_15_3_surface_semantics_resolution_integrity")
    except Exception:
        if str(roots[0]) in sys.path:
            sys.path.remove(str(roots[0]))
        tmp.cleanup()
        raise
    return tmp, mod.generator_view, mod, v153


def safe_generator_claim_view(claims: Iterable[Any], *, generator_view) -> tuple[Any, ...]:
    return tuple(generator_view(claims))
