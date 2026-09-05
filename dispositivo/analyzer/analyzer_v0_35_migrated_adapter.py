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
  headword records with class, paradigm availability and provenance;
- v0.35.10 VerbAnalysisBridge v0.2, exposing documentary non-headword verb-form
  candidates under a deliberately restricted AP/PDLMA comparison policy;
- v0.35.11 ValencyCompatibilityBridge v0.1, attaching only adjudicated lexical
  valency codes to verb entry IDs already linked by earlier layers;
- v0.35.12 ExplicitValencyRelationBridge v0.1, exposing only source-explicit
  PB2015 relation sets whose member has been strictly resolved to an already
  identified Dictionaria entry;
- v0.35.13 VerbMorphologicalHypothesisView v0.1, re-expressing already-produced
  v0.35.10 coordinates as explicit TAM/root/class hypotheses without turning
  them into token-level facts;
- v0.35.14 CausativeGroupCoordinateView v0.1, exposing PB2015 C1-C4 analytical
  causative resources only after source-explicit group membership is already
  established for an identified entry;
- v0.35.15 ContextualDocumentarySupportView v0.1, using explicitly supplied
  Didxazá context only to report overlap with Dictionaria examples that already
  support an existing verb hypothesis.

Exact surface evidence remains separate from rule-based morphological analysis.
The v0.35.11 layer does not infer valency from visible prefixes. The v0.35.12
layer may retrieve PB2015 V1–V3/C1–C4 membership only from HALL-0193's explicit
relation registry; it does not assign groups from surface form, resolve
MULTIPLE_STRICT rows, or treat NO_STRICT as negative evidence. The v0.35.13
layer does not add new relations or segment visible prefixes: TAM, root and class
remain documentary structural hypotheses. The v0.35.14 layer likewise never
detects causative material from visible strings: C1=-g-, C2=-u-, C3=-u-g- and
C4 larger concatenations are source-level analytical coordinates, not project
surface parses or generation recipes. The v0.35.15 layer can corroborate an
existing hypothesis with overlap inside its already-linked documentary examples,
but cannot create, rank or resolve hypotheses and cannot rewrite local evidence.
No layer grants correction, orthographic authority, generation license, or
rule-discovery authority.
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
from analyzer_v0_35_9_verb_analysis_bridge import VerbAnalysisBridgeAnalyzer
from analyzer_v0_35_10_documentary_verb_form_candidates import (
    BRIDGE_VERSION as VERB_ANALYSIS_BRIDGE_VERSION,
    DocumentaryVerbFormCandidateAnalyzer,
)
from analyzer_v0_35_11_valency_compatibility_bridge import (
    BRIDGE_VERSION as VALENCY_COMPATIBILITY_BRIDGE_VERSION,
    ValencyCompatibilityBridgeAnalyzer,
)
from analyzer_v0_35_12_explicit_valency_relations import (
    BRIDGE_VERSION as EXPLICIT_VALENCY_RELATION_BRIDGE_VERSION,
    DEFAULT_CROSSWALK_PATH as EXPLICIT_VALENCY_RELATION_CROSSWALK_PATH,
    ExplicitValencyRelationBridgeAnalyzer,
)
from analyzer_v0_35_13_verb_morphological_hypotheses import (
    VIEW_VERSION as VERB_MORPHOLOGICAL_HYPOTHESIS_VIEW_VERSION,
    VerbMorphologicalHypothesisViewAnalyzer,
)
from analyzer_v0_35_14_causative_group_coordinates import (
    VIEW_VERSION as CAUSATIVE_GROUP_COORDINATE_VIEW_VERSION,
    CausativeGroupCoordinateViewAnalyzer,
)
from analyzer_v0_35_15_contextual_documentary_support import (
    ADAPTER_VERSION,
    VIEW_VERSION as CONTEXTUAL_DOCUMENTARY_SUPPORT_VIEW_VERSION,
    ContextualDocumentarySupportViewAnalyzer,
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
) -> ContextualDocumentarySupportViewAnalyzer:
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
    verb_bridge_v01 = VerbAnalysisBridgeAnalyzer(documented_person)
    verb_bridge_v02 = DocumentaryVerbFormCandidateAnalyzer(verb_bridge_v01)
    valency_v01 = ValencyCompatibilityBridgeAnalyzer(verb_bridge_v02)
    explicit_relations = ExplicitValencyRelationBridgeAnalyzer(valency_v01)
    hypotheses = VerbMorphologicalHypothesisViewAnalyzer(explicit_relations)
    causative_coordinates = CausativeGroupCoordinateViewAnalyzer(hypotheses)
    return ContextualDocumentarySupportViewAnalyzer(causative_coordinates)


def migrated_execution_state(
    biyubi_path: str | Path | None = None,
) -> dict[str, Any]:
    engine = build_migrated_analyzer(biyubi_path=biyubi_path)
    try:
        return {
            "status": "REPRODUCIBLE_NON_LICENSING_PARTIAL_ANALYZER",
            "historical_implementation": "non_licensing_analyzer_orchestrator_v0_35.py",
            "current_adapter": "analyzer_v0_35_15_contextual_documentary_support.py",
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
            "documentary_verb_form_candidate_layer_enabled": True,
            "documentary_verb_form_candidate_index_stats": engine.base.base.base.base.base.documentary_candidate_index_stats,
            "valency_compatibility_bridge_enabled": True,
            "valency_compatibility_bridge_version": VALENCY_COMPATIBILITY_BRIDGE_VERSION,
            "valency_compatibility_index_stats": engine.base.base.base.base.valency_compatibility_index_stats,
            "explicit_valency_relation_bridge_enabled": True,
            "explicit_valency_relation_bridge_version": EXPLICIT_VALENCY_RELATION_BRIDGE_VERSION,
            "explicit_valency_relation_crosswalk_path": str(EXPLICIT_VALENCY_RELATION_CROSSWALK_PATH),
            "explicit_valency_relation_index_stats": engine.base.base.base.explicit_valency_relation_index_stats,
            "verb_morphological_hypothesis_view_enabled": True,
            "verb_morphological_hypothesis_view_version": VERB_MORPHOLOGICAL_HYPOTHESIS_VIEW_VERSION,
            "causative_group_coordinate_view_enabled": True,
            "causative_group_coordinate_view_version": CAUSATIVE_GROUP_COORDINATE_VIEW_VERSION,
            "contextual_documentary_support_view_enabled": True,
            "contextual_documentary_support_view_version": CONTEXTUAL_DOCUMENTARY_SUPPORT_VIEW_VERSION,
            "verb_analysis_bridge_policy": {
                "documented_single_token_headword_records": True,
                "exposes_documented_class": True,
                "exposes_documented_pdlma_paradigm_fields": True,
                "preserves_homography": True,
                "documentary_nonheadword_form_candidates": True,
                "candidate_requires_ap_example_token_match_under_candidate_key": True,
                "candidate_requires_unique_linked_verb_entry": True,
                "candidate_requires_pdlma_tam_match_after_ascii_hyphen_removal_under_same_candidate_key": True,
                "candidate_key_nfc": True,
                "candidate_key_casefold": True,
                "candidate_key_apostrophe_typography_unification": True,
                "candidate_match_is_exact_surface_evidence": False,
                "candidate_requires_explicit_example_tam_feature": False,
                "candidate_token_role_asserted": False,
                "candidate_tam_of_observed_surface_asserted": False,
                "candidate_root_segmentation_asserted": False,
                "candidate_promotes_analysis_status": False,
                "pdlma_recovery_coordinate_only": True,
                "ascii_morpheme_hyphen_comparison_only": True,
                "tone_stripping": False,
                "diacritic_stripping": False,
                "glottal_7_to_apostrophe": False,
                "bang_removal": False,
                "dot_removal": False,
                "segment_substitution": False,
                "vowel_change": False,
                "near_match": False,
                "edit_distance": False,
                "pdlma_to_ap": False,
                "nonheadword_tam_inference": False,
                "valency_analysis_in_v02": False,
                "context_resolution": False,
                "generation_license": False,
                "correction_authority": False,
            },
            "valency_compatibility_policy": {
                "requires_preexisting_verb_entry_link": True,
                "literal_adjudicated_codes_only": ["caus", "i", "t"],
                "exact_headword_entry_route": True,
                "documented_person_fusion_lemma_route": True,
                "nonheadword_structural_candidate_route": True,
                "structural_route_is_compatibility_only": True,
                "lexical_code_meaning_authority": "HALL-0192",
                "valency_architecture_authority": [
                    "HALL-0188", "HALL-0189", "HALL-0190", "HALL-0191"
                ],
                "pb2015_group_assignment": False,
                "group_assignment_from_surface": False,
                "numeric_valence_inference_from_transitivity": False,
                "basic_derived_relation_inference": False,
                "vers_interpretation": False,
                "undefined_modifier_interpretation": False,
                "surface_prefix_inference": False,
                "pdlma_to_ap": False,
                "generation_license": False,
                "correction_authority": False,
                "orthographic_authority": False,
                "rule_discovery_authority": False,
            },
            "explicit_valency_relation_policy": {
                "knowledge_authority": "HALL-0193",
                "knowledge_commit": "f17c5363caada6f8beb18fa99c39e37cd72c6f09",
                "requires_preexisting_documented_entry_identity": True,
                "eligible_entry_link_routes": [
                    "DOCUMENTED_EXACT_VERB_HEADWORD_ENTRY_LINK",
                    "SOURCE_DOCUMENTED_PERSON_FUSION_LEMMA_ENTRY_LINK",
                ],
                "structural_candidate_route_eligible": False,
                "strict_crosswalk_statuses": ["UNIQUE_STRICT", "NO_STRICT", "MULTIPLE_STRICT"],
                "unique_strict_can_assign_source_member_to_entry": True,
                "multiple_strict_auto_disambiguation": False,
                "no_strict_is_negative_evidence": False,
                "source_explicit_group_retrieval": True,
                "automatic_group_assignment": False,
                "surface_relation_inference": False,
                "pdlma_to_ap": False,
                "generation_license": False,
                "correction_authority": False,
                "orthographic_authority": False,
                "rule_discovery_authority": False,
            },
            "verb_morphological_hypothesis_policy": {
                "reexpresses_upstream_v03510_only": True,
                "exposes_tam_candidates": True,
                "exposes_analytical_root_candidates": True,
                "exposes_documented_class_candidates": True,
                "observed_token_is_verb_assertion": False,
                "tam_of_observed_token_assertion": False,
                "root_segmentation_of_observed_token_assertion": False,
                "verb_class_of_observed_token_assertion": False,
                "visible_prefix_segmentation": False,
                "candidate_resolves_token": False,
                "candidate_changes_exact_evidence": False,
                "candidate_changes_analysis_status": False,
                "pdlma_to_ap": False,
                "generation_license": False,
                "correction_authority": False,
                "orthographic_authority": False,
                "rule_discovery_authority": False,
            },
            "causative_group_coordinate_policy": {
                "knowledge_authority": ["HALL-0188", "HALL-0190", "HALL-0191"],
                "knowledge_commit": "f17c5363caada6f8beb18fa99c39e37cd72c6f09",
                "requires_source_explicit_c1_c4_membership": True,
                "group_resources_analytical": {
                    "C1": "-g-",
                    "C2": "-u-",
                    "C3": "-u-g-",
                    "C4": "-u(-g)-zi- / -zu-",
                },
                "surface_group_assignment": False,
                "visible_prefix_detection": False,
                "observed_surface_segmentation": False,
                "token_level_causative_parse_from_group_resource": False,
                "pdlma_to_ap": False,
                "productive_generation": False,
                "generation_license": False,
                "correction_authority": False,
                "orthographic_authority": False,
                "rule_discovery_authority": False,
            },
            "contextual_documentary_support_policy": {
                "requires_existing_verb_hypothesis": True,
                "requires_existing_supporting_dictionaria_example": True,
                "supported_context_surface_fields": ["surface", "surface_original", "didxaza"],
                "query_token_repetition_excluded": True,
                "candidate_key_nfc": True,
                "candidate_key_casefold": True,
                "candidate_key_apostrophe_typography_unification": True,
                "tone_stripping": False,
                "diacritic_stripping": False,
                "edit_distance": False,
                "pdlma_to_ap": False,
                "creates_hypothesis": False,
                "resolves_hypothesis": False,
                "ranks_hypotheses": False,
                "rewrites_local_evidence": False,
                "changes_analysis_status": False,
                "generation_license": False,
                "correction_authority": False,
                "orthographic_authority": False,
                "rule_discovery_authority": False,
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
                    "DICTIONARIA_AP_EXAMPLE_TOKEN_CANDIDATE_KEY_PLUS_UNIQUE_VERB_LINK_PLUS_PDLMA_TAM_ASCII_HYPHEN_COLLAPSE_CANDIDATE",
                    "DICTIONARIA_LITERAL_LEXICAL_VALENCY_CODE_COMPATIBILITY",
                    "PB2015_SOURCE_EXPLICIT_VALENCY_RELATION_RETRIEVAL",
                    "DOCUMENTARY_TAM_ROOT_CLASS_HYPOTHESIS_VIEW",
                    "PB2015_SOURCE_EXPLICIT_C1_C4_CAUSATIVE_GROUP_ANALYTICAL_COORDINATE",
                    "DICTIONARIA_SUPPORTING_EXAMPLE_CONTEXT_OVERLAP_FOR_EXISTING_HYPOTHESIS",
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