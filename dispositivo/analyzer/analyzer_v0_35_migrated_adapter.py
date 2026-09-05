#!/usr/bin/env python3
"""Current execution adapter for the migrated Analyzer.

The historical v0.35 orchestrator remains unchanged. This module supplies
explicit paths to its verified runtime, SQLite and verb inventory dependencies,
then layers:
- v0.35.2 punctuation-light exact existing-source fallback;
- v0.35.3 optional exact Biyubi controlled-source evidence;
- v0.35.7 exact documentary surface attestations already promoted in Voces;
- v0.35.4 candidate-only documentary/person/possession observations over the
  latest unresolved exact-evidence boundary;
- v0.35.5 source-backed person-fusion candidates over documented verb bases;
- v0.35.8 documented 1SG fusion analysis when lemma + person rule + prosodic
  condition are independently licensed;
- v0.35.9 VerbAnalysisBridge v0.1, exposing already-documented exact verb
  headword records with class, paradigm availability and provenance.

Exact surface evidence remains separate from rule-based morphological analysis.
PDLMA paradigm fields remain analytical documentary fields and are not projected
onto AP surface. No layer grants correction, orthographic authority, generation
license, or rule-discovery authority.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from analyzer_v0_35_2_punctuation_light_fallback_adapter import (
    PunctuationLightExactFallbackAnalyzer,
)
from analyzer_v0_35_3_biyubi_exact_fallback_adapter import (
    BiyubiExactFallbackAnalyzer,
)
from analyzer_v0_35_7_voces_documentary_exact_adapter import (
    DEFAULT_REGISTRY_PATH as VOCES_DOCUMENTARY_REGISTRY_PATH,
    VocesDocumentaryExactFallbackAnalyzer,
)
from analyzer_v0_35_4_documentary_candidate_adapter import DocumentaryCandidateAnalyzer
from analyzer_v0_35_5_person_fusion_candidate_adapter import PersonFusionCandidateAnalyzer
from analyzer_v0_35_8_documented_person_fusion_analysis_adapter import (
    DocumentedPersonFusionAnalysisAnalyzer,
)
from analyzer_v0_35_9_verb_analysis_bridge import (
    ADAPTER_VERSION,
    BRIDGE_VERSION as VERB_ANALYSIS_BRIDGE_VERSION,
    VerbAnalysisBridgeAnalyzer,
)
from biyubi_exact_source import (
    BiyubiControlledSource,
    EXPECTED_NONEMPTY_ROWS as BIYUBI_EXPECTED_DATA_ROWS,
    EXPECTED_SNAPSHOT_SHA256 as BIYUBI_EXPECTED_SHA256,
    SOURCE_ENV_VAR as BIYUBI_SOURCE_ENV_VAR,
    SOURCE_ID as BIYUBI_SOURCE_ID,
)
from non_licensing_analyzer_orchestrator_v0_35 import NonLicensingAnalyzerOrchestrator


HERE = Path(__file__).resolve().parent
RUNTIME_ROOT = HERE.parent / "runtime" / "v0_2_15_3"
SQLITE_PATH = RUNTIME_ROOT / "BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite"
VERB_INVENTORY_PATH = HERE / "DIC_VERB_2385_v0_1.csv"


def _resolved_biyubi_path(biyubi_path: str | Path | None = None) -> Path | None:
    if biyubi_path is not None:
        return Path(biyubi_path).expanduser()
    env_value = os.environ.get(BIYUBI_SOURCE_ENV_VAR)
    if env_value:
        return Path(env_value).expanduser()
    return None


def build_migrated_analyzer(
    biyubi_path: str | Path | None = None,
    *,
    require_biyubi: bool = False,
) -> VerbAnalysisBridgeAnalyzer:
    """Instantiate the current Analyzer over repository/source artifacts."""

    historical = NonLicensingAnalyzerOrchestrator(
        runtime_root=RUNTIME_ROOT,
        sqlite_path=SQLITE_PATH,
        verb_inventory_path=VERB_INVENTORY_PATH,
    )
    existing_exact = PunctuationLightExactFallbackAnalyzer(historical)

    source_path = _resolved_biyubi_path(biyubi_path)
    if source_path is None:
        if require_biyubi:
            existing_exact.close()
            raise FileNotFoundError(
                f"Biyubi controlled source is required; pass --biyubi-xlsx or set {BIYUBI_SOURCE_ENV_VAR}"
            )
        biyubi_exact = BiyubiExactFallbackAnalyzer(existing_exact, None)
    else:
        try:
            biyubi_source = BiyubiControlledSource(source_path)
        except Exception:
            existing_exact.close()
            raise
        biyubi_exact = BiyubiExactFallbackAnalyzer(existing_exact, biyubi_source)

    voces_documentary_exact = VocesDocumentaryExactFallbackAnalyzer(biyubi_exact)
    documentary = DocumentaryCandidateAnalyzer(voces_documentary_exact)
    person_candidates = PersonFusionCandidateAnalyzer(documentary)
    documented_person = DocumentedPersonFusionAnalysisAnalyzer(person_candidates)
    return VerbAnalysisBridgeAnalyzer(documented_person)


def migrated_execution_state(
    biyubi_path: str | Path | None = None,
) -> dict[str, Any]:
    engine = build_migrated_analyzer(biyubi_path=biyubi_path)
    try:
        return {
            "status": "REPRODUCIBLE_NON_LICENSING_PARTIAL_ANALYZER",
            "historical_implementation": "non_licensing_analyzer_orchestrator_v0_35.py",
            "current_adapter": "analyzer_v0_35_9_verb_analysis_bridge.py",
            "current_adapter_version": ADAPTER_VERSION,
            "exact_existing_layer_fallback_enabled": True,
            "punctuation_light_fallback_lookup_enabled": True,
            "voces_documentary_exact_layer_enabled": True,
            "voces_documentary_registry_path": str(VOCES_DOCUMENTARY_REGISTRY_PATH),
            "documentary_candidate_layer_enabled": True,
            "documented_person_fusion_candidate_layer_enabled": True,
            "documented_person_fusion_analysis_enabled": True,
            "verb_analysis_bridge_enabled": True,
            "verb_analysis_bridge_version": VERB_ANALYSIS_BRIDGE_VERSION,
            "verb_analysis_bridge_policy": {
                "documented_single_token_headword_records": True,
                "exposes_documented_class": True,
                "exposes_documented_pdlma_paradigm_fields": True,
                "preserves_homography": True,
                "tone_stripping": False,
                "diacritic_stripping": False,
                "apostrophe_normalization": False,
                "near_match": False,
                "pdlma_to_ap": False,
                "nonheadword_tam_inference": False,
                "valency_analysis": False,
                "context_resolution": False,
                "generation_license": False,
                "correction_authority": False,
            },
            "documented_morphology_policy": {
                "exact_surface_evidence_kept_separate": True,
                "requires_documented_lemma": True,
                "requires_explicit_source_rule": True,
                "requires_independent_prosodic_license": True,
                "generation_license": False,
                "correction_authority": False,
                "implemented_rules": [
                    {
                        "knowledge_rule_id": "HALL-0022",
                        "knowledge_commit": "c555732061cfb4bc29a8fa7f746b3bc4157c1fcb",
                        "source_id": "BIB004_GRAMATICA_POPULAR",
                        "source_locations": ["§3.6 El acento", "Cuadro 17"],
                        "rule": "1SG grave final i -> e'",
                    }
                ],
            },
            "candidate_layer_policy": {
                "candidate_is_exact_evidence": False,
                "candidate_promotes_analysis_status": False,
                "generic_edit_distance": False,
                "near_match_ranking": False,
                "operations_enabled": [
                    "FINAL_GLOTTAL_MARK_PRESENCE_CANDIDATE",
                    "SINGLE_ADJACENT_IDENTICAL_VOWEL_LENGTH_CANDIDATE",
                    "EXISTING_GRAPHICAL_PERSON_SUFFIX_CANDIDATE",
                    "EXISTING_GRAPHICAL_POSSESSION_PREFIX_CANDIDATE",
                    "GP_1SG_FINAL_I_TO_E_GLOTTAL_REVERSE_LINK_CANDIDATE",
                ],
            },
            "fallback_layers": [
                "surface_attestation_v029",
                "pickett_lexical_record_v0211",
                "cross_source_exact_surface_v0212",
                "documentary_alignment_v0210",
                "voces_promoted_documentary_exact_v0357",
            ],
            "controlled_external_sources": [
                {
                    "source_id": BIYUBI_SOURCE_ID,
                    "source_role": [
                        "SURFACE_EVIDENCE_SECONDARY",
                        "CONTRAST_EVIDENCE",
                        "PARADIGM_CANDIDATE",
                    ],
                    "payload_in_public_repository": False,
                    "mount_env_var": BIYUBI_SOURCE_ENV_VAR,
                    "registered_snapshot_sha256": BIYUBI_EXPECTED_SHA256,
                    "registered_data_rows": BIYUBI_EXPECTED_DATA_ROWS,
                    "mount_status": engine.biyubi_source_status,
                    "mounted_snapshot_sha256": (
                        engine.biyubi_source.snapshot_sha256
                        if engine.biyubi_source is not None
                        else None
                    ),
                    "orthographic_authority": False,
                }
            ],
            "runtime_profile": "runtime/v0_2_15_3",
            "dictionaria_entries": len(engine.retrieval.entries),
            "dictionaria_senses": sum(len(rows) for rows in engine.retrieval.senses.values()),
            "dictionaria_examples": len(engine.retrieval.examples),
            "verb_inventory_rows": len(engine.morph1.records),
            "verb_metadata_rows": len(engine.verb_meta),
            "person_possession_exact_rows": len(engine.person_exact),
            "generation_license_assertion": False,
            "correction_assertion": False,
            "orthographic_authority_assertion": False,
            "rule_discovery_assertion": False,
            "cor001_benchmark_allowed": False,
            "research_authority_assertion": False,
        }
    finally:
        engine.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface")
    parser.add_argument("--item-id", default="AD_HOC_NON_LICENSING_ANALYSIS")
    parser.add_argument(
        "--biyubi-xlsx",
        help=f"Controlled Biyubi XLSX; alternatively set {BIYUBI_SOURCE_ENV_VAR}",
    )
    parser.add_argument(
        "--require-biyubi",
        action="store_true",
        help="Fail rather than run without the controlled Biyubi snapshot",
    )
    args = parser.parse_args()

    if args.surface is None:
        if args.require_biyubi and _resolved_biyubi_path(args.biyubi_xlsx) is None:
            raise FileNotFoundError(
                f"Biyubi controlled source is required; pass --biyubi-xlsx or set {BIYUBI_SOURCE_ENV_VAR}"
            )
        payload = migrated_execution_state(biyubi_path=args.biyubi_xlsx)
    else:
        engine = build_migrated_analyzer(
            biyubi_path=args.biyubi_xlsx,
            require_biyubi=args.require_biyubi,
        )
        try:
            payload = engine.analyze(args.surface, item_id=args.item_id)
        finally:
            engine.close()
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
