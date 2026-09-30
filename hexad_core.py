"""
HEXAD Core: The Master Nexus & Unified Cybernetic Orchestrator.

Integrates the 6 Autonomous Pillars of the Cybernetic Hexad:
1. OCULUS (The Senses)    -> Foveal Gaze & Topological Manifold Compression
2. CORIS  (The Heart)     -> Dissipative Homeostasis & Lymphatic Antibodies
3. ANIMA  (The Mind)      -> Variational Lagrangian Path Integrals (delta S = 0)
4. MNEME  (The Stability) -> Lyapunov Asymptotic Invariants (dV/dt < 0) & Ricci Flow
5. DEMON  (The Muscle)    -> Zero-Token Enclave Barrier & Sandbox Actuation
6. PEIRA  (The Crucible)  -> Silicon Friction Delta & Closed-Loop Reality Reset

Integrated with HEXAD Guardian for Author Invariance and Anti-Regression Enforcement.
"""

import sys
import os
import time
from typing import Dict, Any, List, Optional

# Percorso delle directory dei 6 motori sul Desktop o relative
desktop_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for eng in ["Oculus-Engine", "Coris-Engine", "Anima-Engine", "Mneme-Engine", "Demon-Engine", "Peira-Engine"]:
    ep = os.path.join(desktop_dir, eng)
    if os.path.exists(ep) and ep not in sys.path:
        sys.path.insert(0, ep)

from hexad_guardian import HexadGuardian, InvarianceVerificationResult

# Import condizionale dei 6 motori
try:
    from oculus_engine import OculusEngine
    HAS_OCULUS = True
except ImportError:
    HAS_OCULUS = False

try:
    from coris_engine import CorisEngine
    HAS_CORIS = True
except ImportError:
    HAS_CORIS = False

try:
    from anima_engine import AnimaEngine, AnimaBranch
    HAS_ANIMA = True
except ImportError:
    HAS_ANIMA = False

try:
    from mneme_engine import MnemeEngine
    HAS_MNEME = True
except ImportError:
    HAS_MNEME = False

try:
    from demon_gateway import DemonGateway
    HAS_DEMON = True
except ImportError:
    HAS_DEMON = False

try:
    from peira_engine import PeiraEngine
    HAS_PEIRA = True
except ImportError:
    HAS_PEIRA = False

# Gate di attuazione DEMON: senza dipendenze esterne, disponibile anche senza DemonGateway
try:
    from demon_action_gate import evaluate_command as demon_action_verdict
    HAS_DEMON_GATE = True
except ImportError:
    HAS_DEMON_GATE = False


class HexadOracle:
    """
    Il Nucleo Centrale dell'Oracolo Cibernetico HEXAD.
    Governa l'organismo completo e vigila sull'integrità del codice dell'autore.
    """

    def __init__(self, workspace_dir: str):
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.guardian = HexadGuardian(self.workspace_dir)

        # Inizializzazione dei 6 motori
        self.oculus = OculusEngine() if HAS_OCULUS else None
        self.coris = CorisEngine() if HAS_CORIS else None
        self.anima = AnimaEngine() if HAS_ANIMA else None
        self.mneme = MnemeEngine(state_dim=5, alpha=0.15) if HAS_MNEME else None
        self.demon = DemonGateway() if HAS_DEMON else None
        self.peira = PeiraEngine(timeout_sec=8.0) if HAS_PEIRA else None

    # =========================================================================
    # 1. INITIALIZATION & REPO DNA ONBOARDING
    # =========================================================================
    def bootstrap(self) -> Dict[str, Any]:
        """Esegue la scansione di primo avvio: indicizza il DNA del progetto e blocca gli invarianti."""
        guard_res = self.guardian.bootstrap_project()
        
        # Scansione foveale con OCULUS se disponibile
        topology_info = {}
        if self.oculus:
            topology_info = self.oculus.scan_directory_topology(self.workspace_dir)

        return {
            "hexad_status": "ONLINE_ACTIVE",
            "guardian_invariants": guard_res,
            "oculus_topology": topology_info,
            "engines_online": {
                "1_OCULUS": HAS_OCULUS,
                "2_CORIS": HAS_CORIS,
                "3_ANIMA": HAS_ANIMA,
                "4_MNEME": HAS_MNEME,
                "5_DEMON": HAS_DEMON,
                "6_PEIRA": HAS_PEIRA
            }
        }

    # =========================================================================
    # 2. SOVEREIGN EDIT GUARD: Pre-Flight Check Prima di Scrivere Codice
    # =========================================================================
    def evaluate_code_edit(
        self,
        file_path: str,
        proposed_code: str,
        user_intent: str = "",
        explicit_override: bool = False
    ) -> InvarianceVerificationResult:
        """
        Intercetta qualsiasi tentativo dell'LLM di scrivere su un file.
        Se l'azione viola una funzione sacra dell'autore, viene bloccata all'istante.
        """
        return self.guardian.verify_proposed_edit(
            target_file_path=file_path,
            proposed_content=proposed_code,
            user_prompt=user_intent,
            explicit_override=explicit_override
        )

    # =========================================================================
    # 3. IL CICLO CIBERNETICO AD ANELLO CHIUSO (THE CLOSED HEXAD LOOP)
    # =========================================================================
    def execute_cybernetic_cycle(
        self,
        intent_query: str,
        candidate_traces: Optional[List[Dict[str, Any]]] = None,
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Esegue il ciclo vitale a 6 fasi:
        OCULUS -> CORIS -> ANIMA -> MNEME -> DEMON -> PEIRA (con reset in caso di Delta != 0).

        Un ramo bloccato dal gate DEMON o fratturato da PEIRA viene escluso dai cicli
        successivi (azione lagrangiana infinita). Se non restano rami alternativi il ciclo
        si arresta e restituisce la frattura al chiamante, senza rieseguire lo stesso comando.
        """
        start_time = time.perf_counter()
        audit_log = []
        current_query = intent_query
        retries = 0
        excluded_branches: List[str] = []
        last_fracture: Optional[Dict[str, Any]] = None

        # Senza rami candidati non c'è nulla da verificare: nessun comando segnaposto
        # viene eseguito, così un "successo" significa sempre un'azione reale riuscita
        if not candidate_traces:
            audit_log.append("[3. ANIMA] Nessun ramo candidato fornito: nessuna azione da eseguire.")
            total_time = (time.perf_counter() - start_time) * 1000.0
            return {
                "status": "HEXAD_NO_CANDIDATES",
                "cycles_used": 0,
                "audit_trail": audit_log,
                "latency_ms": round(total_time, 2)
            }

        while retries <= max_retries:
            pass_label = f"Cycle #{retries + 1}"
            audit_log.append(f"=== [HEXAD {pass_label}] Inizio Sequenza Cibernetica ===")

            # 1. OCULUS: Foveal Compression
            sensory_entropy = 0.35
            focal_file = "core.py"
            compression_pct = 85.0
            if self.oculus and os.path.exists(self.workspace_dir):
                fovea = self.oculus.focus_saccadic_gaze(current_query, self.workspace_dir)
                focal_file = fovea.focal_file
                compression_pct = fovea.compression_ratio_pct
                sensory_entropy = fovea.sensory_entropy
                audit_log.append(f"[1. OCULUS] Fovea su '{os.path.basename(focal_file)}' ({compression_pct:.1f}% token risparmiati)")
            else:
                audit_log.append("[1. OCULUS] Retina sintetica attiva.")

            # 2. CORIS: Homeostasis & Antibody Scan
            if self.coris:
                vitals = self.coris.pulse(error_rate=0.0, latency_ms=10.0, context_tokens_used=120)
                threat = self.coris.check_antigen_binding(current_query)
                if threat:
                    audit_log.append(f"[2. CORIS] Antigene intercettato: {threat.epitope_hash}")
                    return {"status": "BLOCKED_BY_CORIS", "audit": audit_log}
                audit_log.append(f"[2. CORIS] Pressione={vitals.homeostatic_pressure_P:.2f}, Free Energy={vitals.free_energy_F:.2f}")

            # 3. ANIMA: Path Integral Minimization sui soli rami non ancora esclusi
            remaining = [
                (r.get("id") or f"trace_{t_idx}", r)
                for t_idx, r in enumerate(candidate_traces)
                if (r.get("id") or f"trace_{t_idx}") not in excluded_branches
            ]
            if not remaining:
                audit_log.append(f"[3. ANIMA] Nessun ramo residuo (esclusi: {', '.join(excluded_branches)}). Arresto del ciclo.")
                return self._halted_cycle_result(retries, excluded_branches, last_fracture, audit_log, start_time)

            action_val = 0.25
            if self.anima:
                branches = []
                for b_id, r in remaining:
                    b = AnimaBranch(id=b_id, name=r.get("name", b_id), metadata=r)
                    for idx, ent in enumerate(r.get("entropies", [0.15])):
                        self.anima.ingest_step(b, token=f"tok_{idx}", token_entropy=float(ent))
                    branches.append(b)
                res = self.anima.collapse(current_query, branches)
                winner = res.eigenstate
                chosen_branch_id, chosen_trace = winner.id, winner.metadata
                action_val = float(res.total_system_action)
                audit_log.append(f"[3. ANIMA] Collasso autostato su '{winner.name}' (Azione={action_val:.4f})")
            else:
                # Senza ANIMA: ordine dei candidati, deterministico
                chosen_branch_id, chosen_trace = remaining[0]
                audit_log.append(f"[3. ANIMA] Motore assente: selezione ordinale del ramo '{chosen_branch_id}'")
            # Le tracce possono portare il comando in "code" o in "command"
            chosen_command = chosen_trace.get("code") or chosen_trace.get("command") or ""

            # 4. MNEME: Lyapunov Stability Certification
            if self.mneme:
                st = [action_val, sensory_entropy, 0.2, 0.1, 0.0]
                vel = [-0.5 * s for s in st]
                cert = self.mneme.certify_trajectory_stability(st, velocity_vector=vel)
                if not cert.is_stable:
                    audit_log.append(f"[4. MNEME] Divergenza rilevata: {cert.rejection_reason}")
                    return {"status": "ABORTED_BY_MNEME", "audit": audit_log}
                audit_log.append(f"[4. MNEME] Stabilità certificata: dV/dt={cert.v_dot:+.4f}, max(Re(λ))={cert.max_real_eigenvalue:+.4f}")

            # 5. DEMON: Gate di attuazione prima dell'esecuzione fisica di PEIRA
            if not HAS_DEMON_GATE:
                audit_log.append("[5. DEMON] Gate di attuazione non disponibile: esecuzione negata (fail-closed).")
                return {"status": "BLOCKED_BY_DEMON", "reason": "DEMON_GATE_UNAVAILABLE", "audit_trail": audit_log}
            verdict = demon_action_verdict(chosen_command, workspace_dir=self.workspace_dir)
            if not verdict.allowed:
                audit_log.append(
                    f"[5. DEMON] Gate BLOCK su '{chosen_command}': {'; '.join(verdict.reasons)} "
                    f"(regole: {', '.join(verdict.matched_rules)})"
                )
                excluded_branches.append(chosen_branch_id)
                retries += 1
                continue
            audit_log.append(f"[5. DEMON] Gate ALLOW ({verdict.latency_ms:.3f} ms)")

            # 5b. DEMON: Muscle Enclave Actuation (telemetria del gateway)
            if self.demon:
                d_res = self.demon.route_command(chosen_command)
                audit_log.append(f"[5. DEMON] Gateway OS: status='{d_res.get('status')}' (Blast Radius=0.0)")

            # 6. PEIRA: Physical Silicon Impact
            if self.peira:
                impact = self.peira.execute_physical_trial(chosen_command, cwd=self.workspace_dir)
                audit_log.append(f"[6. PEIRA] Responso silicio: Exit Code={impact.exit_code}, Delta={impact.delta_empirico:.2f}")

                if impact.is_converged:
                    audit_log.append("[6. PEIRA] CONVERGENZA ASSOLUTA RAGGIUNTA. Il ciclo è terminato.")
                    total_time = (time.perf_counter() - start_time) * 1000.0
                    return {
                        "status": "HEXAD_CONVERGENCE_SUCCESS",
                        "cycles_used": retries + 1,
                        "delta": impact.delta_empirico,
                        "output": impact.stdout,
                        "audit_trail": audit_log,
                        "latency_ms": round(total_time, 2)
                    }

                # Frattura rilevata: Iniezione retroattiva
                audit_log.append(f"[6. PEIRA] FRATTURA TERMODINAMICA! Trigger reset foveale.")
                inj = self.peira.build_fracture_injection(impact)
                if self.coris and impact.antigen_signature:
                    self.coris.synthesize_antibody(impact.antigen_signature, "PEIRA_CRASH", "BLOCK")
                current_query = inj.target_fovea_query
                last_fracture = {
                    "command": impact.command,
                    "exit_code": impact.exit_code,
                    "fault_epicenter": inj.fault_epicenter,
                    "diagnostic_summary": inj.diagnostic_summary,
                    "stderr": impact.stderr[-400:]
                }

                # Reality Reset: il ramo fallito riceve azione infinita ed esce dalla sovrapposizione
                excluded_branches.append(chosen_branch_id)
                audit_log.append(f"[3. ANIMA] Ramo '{chosen_branch_id}' escluso (azione lagrangiana infinita).")

            retries += 1

        total_time = (time.perf_counter() - start_time) * 1000.0
        return {
            "status": "HEXAD_CYCLE_TERMINATED",
            "cycles_used": retries,
            "excluded_branches": excluded_branches,
            "last_fracture": last_fracture,
            "audit_trail": audit_log,
            "latency_ms": round(total_time, 2)
        }

    def _halted_cycle_result(
        self,
        cycles_used: int,
        excluded_branches: List[str],
        last_fracture: Optional[Dict[str, Any]],
        audit_log: List[str],
        start_time: float
    ) -> Dict[str, Any]:
        """Esito di arresto: nessuna alternativa residua, la frattura torna al chiamante."""
        total_time = (time.perf_counter() - start_time) * 1000.0
        return {
            "status": "HEXAD_HALTED_NO_ALTERNATIVES",
            "cycles_used": cycles_used,
            "excluded_branches": excluded_branches,
            "last_fracture": last_fracture,
            "audit_trail": audit_log,
            "latency_ms": round(total_time, 2)
        }
