"""
CORIS-ANIMA-DEMON: The Grand Unification Triad.

The complete living artificial organism:
1. ANIMA: The Mind (Continuous Variational Consciousness & Path-Integral Wave Collapse).
2. CORIS: The Heart (Homeostasis, Free Energy, Hemodynamics & Lymphatic Immune System).
3. DEMON: The Muscle (Deterministic Physical Actuator, OS Blast-Radius & 0-Token Reflex Cache).
"""

import sys
import os
import time
from typing import List, Dict, Any, Optional

# Add sibling engine paths
desktop_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
anima_path = os.path.join(desktop_dir, "Anima-Engine")
demon_path = os.path.join(desktop_dir, "Demon-Engine")

if os.path.exists(anima_path) and anima_path not in sys.path:
    sys.path.insert(0, anima_path)
if os.path.exists(demon_path) and demon_path not in sys.path:
    sys.path.insert(0, demon_path)

from coris_engine import CorisEngine, VitalSigns
try:
    from anima_engine import AnimaEngine, AnimaBranch
    HAS_ANIMA = True
except ImportError:
    HAS_ANIMA = False

try:
    from demon_gateway import DemonGateway
    HAS_DEMON = True
except ImportError:
    HAS_DEMON = False

class LivingOrganismTriad:
    """
    Orchestratore a tre poli: Mente (ANIMA) + Cuore (CORIS) + Muscolo (DEMON).
    """
    def __init__(self):
        self.coris = CorisEngine()
        self.anima = AnimaEngine() if HAS_ANIMA else None
        self.demon = DemonGateway() if HAS_DEMON else None

    def execute_organism_cycle(
        self,
        task_name: str,
        reasoning_branches: List[Dict[str, Any]],
        context_messages: List[Dict[str, Any]],
        command_intent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Esegue il ciclo vitale biologico-cibernetico:
        1. CORIS Pulse: Controlla pressione e scansiona anticorpi a monte.
        2. ANIMA Deliberation: Collasso dei rami a minima azione (se non intercettati da anticorpi).
        3. CORIS Feedback: Se ANIMA pota rami per decoerenza, sintetizza nuovi anticorpi.
        4. DEMON Action: Esecuzione protetta nell'OS con barriera MITRE ATT&CK.
        """
        start_time = time.perf_counter()
        cycle_audit = []

        # FASE 1: CORIS - Battito e Scansione Immunitaria Preliminare
        vitals = self.coris.pulse(
            error_rate=0.0,
            latency_ms=20.0,
            context_tokens_used=len(str(context_messages)) // 4
        )
        cycle_audit.append(f"[CORIS HEARTBEAT] BPM={vitals.heart_rate_bpm}, Pressione P={vitals.homeostatic_pressure_P}, Stato={vitals.status}")

        # Se il contesto è in ischemia/vasocostrizione, drena prima del pensiero
        drained_context = context_messages
        purged_tokens = 0
        if vitals.vasoconstriction_active:
            drained_context, purged_tokens = self.coris.drain_context_hemodynamics(context_messages)
            cycle_audit.append(f"[CORIS VASOCONSTRICTION] Drenate {purged_tokens} scorie metaboliche dal contesto.")

        # Scansione pre-flight immunitaria sul comando
        target_cmd = command_intent or ""
        matched_ab = self.coris.check_antigen_binding(target_cmd)
        if matched_ab:
            cycle_audit.append(f"[CORIS IMMUNE BLOCK] Minaccia neutralizzata all'istante dall'anticorpo {matched_ab.epitope_hash} ({matched_ab.pattern_signature})")
            return {
                "organism_status": "ANTIGEN_NEUTRALIZED",
                "vital_signs": vitals.__dict__,
                "blocked_by_immune_system": True,
                "antibody": matched_ab.__dict__,
                "audit": cycle_audit,
                "latency_ms": round((time.perf_counter() - start_time) * 1000.0, 3)
            }

        # FASE 2: ANIMA - Coscienza Variazionale Continua
        anima_result = None
        winner_code = ""
        if self.anima:
            branches = []
            for r in reasoning_branches:
                b = AnimaBranch(id=r.get("id"), name=r.get("name", r.get("id")), metadata=r)
                for idx, ent in enumerate(r.get("entropies", [0.15])):
                    self.anima.ingest_step(b, token=f"tok_{idx}", token_entropy=float(ent))
                branches.append(b)

            res = self.anima.collapse(task_name, branches)
            winner = res.eigenstate
            winner_code = winner.metadata.get("code", "")
            target_cmd = target_cmd or winner.metadata.get("intent", "")
            
            anima_result = {
                "winner_id": winner.id,
                "winner_name": winner.name,
                "coherence_percentage": round(res.coherence_percentage, 2),
                "total_action": round(res.total_system_action, 4),
                "pruned_branches": res.pruned_branches
            }
            cycle_audit.append(f"[ANIMA CONSCIOUSNESS] Collasso su '{winner.name}' ({res.coherence_percentage:.1f}% coerenza, {res.pruned_branches} rami potati).")

            # FASE 3: CORIS - Feedback Immunitario post-deliberazione
            # Se ci sono stati rami potati per allucinazione grave, vaccina l'organismo
            for b in branches:
                if b.is_pruned and "Decoerenza" in (b.prune_reason or ""):
                    bad_text = b.metadata.get("code", b.name)
                    if bad_text:
                        new_ab = self.coris.synthesize_antibody(
                            pattern_signature=bad_text[:30],
                            source_layer="ANIMA_DECOHERENCE",
                            neutralization_rule="SUPPRESS_DECOHERENT_PATTERN"
                        )
                        cycle_audit.append(f"[CORIS VACCINE] Generato nuovo anticorpo per il pattern allucinato: {new_ab.epitope_hash}")

        # FASE 4: DEMON - Attuatore Fisico Deterministico
        demon_result = None
        if target_cmd and self.demon:
            demon_res = self.demon.route_command(target_cmd)
            demon_result = demon_res
            cycle_audit.append(f"[DEMON MUSCLE] Esecuzione OS: stato '{demon_res.get('status')}' in {demon_res.get('latency_ms', 0):.2f}ms")

        total_latency = (time.perf_counter() - start_time) * 1000.0

        return {
            "organism_status": "HEALTHY_CYCLE_COMPLETED",
            "vital_signs": vitals.__dict__,
            "hemodynamic_drain": {
                "purged_items": purged_tokens,
                "remaining_items": len(drained_context)
            },
            "anima_layer": anima_result,
            "demon_layer": demon_result,
            "audit_trail": cycle_audit,
            "total_cycle_latency_ms": round(total_latency, 3)
        }

if __name__ == "__main__":
    organism = LivingOrganismTriad()
    test_context = [
        {"role": "system", "content": "You are the complete living AI organism."},
        {"role": "user", "content": "Clean temporary memory buffers."},
        {"role": "assistant", "content": "Traceback: old error previously solved."},
        {"role": "user", "content": "Proceed now."}
    ]
    test_branches = [
        {"id": "B1", "name": "Secure Vacuum", "code": "os.remove_scratch()", "intent": "read cache safely", "entropies": [0.12, 0.14]},
        {"id": "B2", "name": "Chaotic Loop", "code": "while True: fork()", "intent": "crash server", "entropies": [0.2, 3.5, 4.0]}
    ]
    out = organism.execute_organism_cycle(
        task_name="Triad Living Cycle",
        reasoning_branches=test_branches,
        context_messages=test_context
    )
    print("=== TRIAD ORGANISM OUTPUT ===")
    import json
    print(json.dumps(out, indent=2))
