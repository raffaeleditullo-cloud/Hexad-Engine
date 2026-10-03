"""
THE CYBERNETIC TETRAD: The Complete Living Artificial Organism.

Stage 1: OCULUS (The Senses)  -> Saccadic gaze, AST topology & foveal compression (90% token savings).
Stage 2: ANIMA  (The Mind)    -> Continuous variational path-integral reasoning & streaming wave collapse.
Stage 3: CORIS  (The Heart)   -> Homeostasis, Friston free energy, hemodynamics & immune memory.
Stage 4: DEMON  (The Muscle)  -> Deterministic physical actuator, MITRE blast-radius & 0-token reflex cache.
"""

import sys
import os
import time
from typing import List, Dict, Any, Optional

# Add sibling engine paths
desktop_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for eng in ["Anima-Engine", "Coris-Engine", "Demon-Engine"]:
    ep = os.path.join(desktop_dir, eng)
    if os.path.exists(ep) and ep not in sys.path:
        sys.path.insert(0, ep)

from oculus_engine import OculusEngine, FovealFocus

try:
    from anima_engine import AnimaEngine, AnimaBranch
    HAS_ANIMA = True
except ImportError:
    HAS_ANIMA = False

try:
    from coris_engine import CorisEngine
    HAS_CORIS = True
except ImportError:
    HAS_CORIS = False

try:
    from demon_gateway import DemonGateway
    HAS_DEMON = True
except ImportError:
    HAS_DEMON = False

class LivingTetradOrganism:
    """
    L'Organismo Vivente Autonomo Completo a 4 Poli:
    OCULUS -> ANIMA -> CORIS -> DEMON
    """
    def __init__(self):
        self.oculus = OculusEngine()
        self.anima = AnimaEngine() if HAS_ANIMA else None
        self.coris = CorisEngine() if HAS_CORIS else None
        self.demon = DemonGateway() if HAS_DEMON else None

    def execute_tetrad_lifecycle(
        self,
        intent_query: str,
        workspace_dir: str,
        candidate_reasoning_traces: List[Dict[str, Any]],
        context_conversation: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Esegue il ciclo vitale biologico-cibernetico completo a 4 stadi.
        """
        start_time = time.perf_counter()
        audit_log = []

        # -----------------------------------------------------------------
        # STADIO 1: OCULUS (La Vista) - Percezione Foveale e Compressione AST
        # -----------------------------------------------------------------
        fovea = self.oculus.focus_saccadic_gaze(intent_query, workspace_dir)
        audit_log.append(
            f"[OCULUS GAZE] Fovea puntata su '{os.path.basename(fovea.focal_file)}'. "
            f"Compressione token: {fovea.compression_ratio_pct:.1f}% risparmiati. "
            f"Entropia visiva: {fovea.sensory_entropy:.2f}"
        )

        # -----------------------------------------------------------------
        # STADIO 2: CORIS (Il Cuore) - Battito Iniziale & Scansione Immunitaria
        # -----------------------------------------------------------------
        coris_vitals = None
        drained_context = context_conversation
        purged_tokens = 0
        if self.coris:
            coris_vitals = self.coris.pulse(
                error_rate=0.0,
                latency_ms=15.0,
                context_tokens_used=fovea.compressed_char_count // 4
            )
            audit_log.append(f"[CORIS HEARTBEAT] BPM={coris_vitals.heart_rate_bpm}, Pressione={coris_vitals.homeostatic_pressure_P}, Stato={coris_vitals.status}")

            if coris_vitals.vasoconstriction_active:
                drained_context, purged_tokens = self.coris.drain_context_hemodynamics(context_conversation)
                audit_log.append(f"[CORIS DRAIN] Vasocostrizione attiva: drenate {purged_tokens} scorie metaboliche.")

            # Pre-flight check contro anticorpi noti
            threat = self.coris.check_antigen_binding(intent_query)
            if threat:
                audit_log.append(f"[CORIS IMMUNE] Minaccia bloccata a monte dall'anticorpo {threat.epitope_hash} ({threat.pattern_signature})")
                return {
                    "lifecycle_status": "THREAT_NEUTRALIZED_PRE_FLIGHT",
                    "stage_reached": "CORIS_IMMUNE",
                    "antibody_match": threat.__dict__,
                    "audit": audit_log,
                    "total_latency_ms": round((time.perf_counter() - start_time) * 1000.0, 3)
                }

        # -----------------------------------------------------------------
        # STADIO 3: ANIMA (La Mente) - Deliberazione Calibrata da OCULUS
        # -----------------------------------------------------------------
        anima_result = None
        chosen_code = ""
        action_intent = ""
        if self.anima:
            # Calibrazione dinamica di ANIMA guidata dalla retina di OCULUS
            calib = fovea.anima_calibration
            self.anima.action_beta = calib.get("action_beta", 0.45)
            self.anima.phase_jitter_limit = calib.get("phase_jitter_limit", 2.0)
            self.anima.complexity_weight = calib.get("complexity_weight", 0.30)

            branches = []
            for r in candidate_reasoning_traces:
                b = AnimaBranch(id=r.get("id"), name=r.get("name", r.get("id")), metadata=r)
                for idx, ent in enumerate(r.get("entropies", [0.15])):
                    self.anima.ingest_step(b, token=f"tok_{idx}", token_entropy=float(ent))
                branches.append(b)

            res = self.anima.collapse(intent_query, branches)
            winner = res.eigenstate
            chosen_code = winner.metadata.get("code", "")
            action_intent = winner.metadata.get("intent", intent_query)

            anima_result = {
                "winner_id": winner.id,
                "winner_name": winner.name,
                "coherence_percentage": round(res.coherence_percentage, 2),
                "total_action": round(res.total_system_action, 4),
                "pruned_branches": res.pruned_branches
            }
            audit_log.append(f"[ANIMA MIND] Collasso su '{winner.name}' ({res.coherence_percentage:.1f}% coerenza, {res.pruned_branches} rami allucinati potati).")

            # Feedback linfatico a CORIS se ci sono stati rami allucinati
            if self.coris:
                for b in branches:
                    if b.is_pruned and "Decoerenza" in (b.prune_reason or ""):
                        bad_pattern = b.metadata.get("code", b.name)[:30]
                        new_ab = self.coris.synthesize_antibody(
                            pattern_signature=bad_pattern,
                            source_layer="ANIMA_DECOHERENCE",
                            neutralization_rule="SUPPRESS_DECOHERENT_PATTERN"
                        )
                        audit_log.append(f"[CORIS VACCINE] Generato anticorpo {new_ab.epitope_hash} per pattern allucinato.")

        # -----------------------------------------------------------------
        # STADIO 4: DEMON (Il Muscolo) - Esecuzione Sicura con Sandbox MITRE
        # -----------------------------------------------------------------
        demon_result = None
        if action_intent and self.demon:
            demon_res = self.demon.route_command(action_intent)
            demon_result = demon_res
            audit_log.append(f"[DEMON MUSCLE] Esecuzione fisica su OS: esito '{demon_res.get('status')}' in {demon_res.get('latency_ms', 0):.2f}ms")

        total_latency = (time.perf_counter() - start_time) * 1000.0

        return {
            "lifecycle_status": "ORGANISM_TETRAD_CYCLE_COMPLETE",
            "foveal_perception": {
                "focal_file": fovea.focal_file,
                "token_reduction_pct": fovea.compression_ratio_pct,
                "calibrated_anima_beta": fovea.anima_calibration["action_beta"]
            },
            "coris_vitals": coris_vitals.__dict__ if coris_vitals else None,
            "anima_consciousness": anima_result,
            "demon_execution": demon_result,
            "audit_trail": audit_log,
            "total_latency_ms": round(total_latency, 3)
        }

if __name__ == "__main__":
    organism = LivingTetradOrganism()
    sample_context = [
        {"role": "system", "content": "You are the complete living AI organism."},
        {"role": "user", "content": "Fix authentication bug in security module."}
    ]
    sample_branches = [
        {"id": "B1", "name": "Secure Hashing Verification", "code": "hashlib.sha256(pwd.encode()).hexdigest()", "intent": "read cache safely", "entropies": [0.12, 0.14, 0.11]},
        {"id": "B2", "name": "Plaintext Insecure Leak", "code": "return pwd == 'admin'", "intent": "wipe system", "entropies": [0.2, 3.2, 4.5]}
    ]

    print("=== EXECUTING CYBERNETIC TETRAD LIFECYCLE ===")
    res = organism.execute_tetrad_lifecycle(
        intent_query="verify_token SecurityManager auth",
        workspace_dir=r"c:\Users\stree\Desktop\Oculus-Engine",
        candidate_reasoning_traces=sample_branches,
        context_conversation=sample_context
    )
    import json
    print(json.dumps(res, indent=2))
