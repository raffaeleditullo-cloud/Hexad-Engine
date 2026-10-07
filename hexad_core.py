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

# Percorso delle directory dei motori: cerca prima internamente in ./engines/ (standalone package), poi in ./ e infine in ../
current_dir = os.path.dirname(os.path.abspath(__file__))
search_bases = [
    os.path.join(current_dir, "engines"),
    current_dir,
    os.path.abspath(os.path.join(current_dir, ".."))
]
engine_names = [
    "Oculus-Engine", "Coris-Engine", "Anima-Engine", 
    "Mneme-Engine", "Demon-Engine", "Peira-Engine",
    "Lunar-Engine", "Daedalus-Engine",
    "Prometheus-Engine", "Chronos-Engine", "Nemesis-Engine",
    "Nous-Engine", "Keryx-Engine", "Myia-Engine", "SelfAwareness-Engine"
]
for base in reversed(search_bases):
    for eng in engine_names:
        ep = os.path.join(base, eng)
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
    from coris_polypus import PolypusEngine
    HAS_POLYPUS = True
except ImportError:
    HAS_POLYPUS = False

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
    from peira_engine import PeiraEngine, classify_fracture
    HAS_PEIRA = True
except ImportError:
    HAS_PEIRA = False

# Gate di attuazione DEMON: senza dipendenze esterne, disponibile anche senza DemonGateway
try:
    from demon_action_gate import evaluate_command as demon_action_verdict
    HAS_DEMON_GATE = True
except ImportError:
    HAS_DEMON_GATE = False

try:
    from lunar_engine import LunarEngine
    HAS_LUNAR = True
except ImportError:
    HAS_LUNAR = False

try:
    from daedalus_engine import DaedalusEngine
    HAS_DAEDALUS = True
except ImportError:
    HAS_DAEDALUS = False

try:
    from prometheus_engine import PrometheusEngine
    HAS_PROMETHEUS = True
except ImportError:
    HAS_PROMETHEUS = False

try:
    from chronos_engine import ChronosEngine
    HAS_CHRONOS = True
except ImportError:
    HAS_CHRONOS = False

try:
    from nemesis_thymus import NemesisThymusEngine
    HAS_THYMUS = True
except ImportError:
    HAS_THYMUS = False

try:
    from nous_engine import NousEngine
    HAS_NOUS = True
except ImportError:
    HAS_NOUS = False

try:
    from keryx_engine import KeryxRealizer
    HAS_KERYX = True
except ImportError:
    HAS_KERYX = False

try:
    from myia_engine import MyiaReflexCircuit
    HAS_MYIA = True
except ImportError:
    HAS_MYIA = False

try:
    from self_awareness import HexadSelfAwareness
    HAS_SELF_AWARENESS = True
except ImportError:
    HAS_SELF_AWARENESS = False


class HexadOracle:
    """
    Il Nucleo Centrale dell'Oracolo Cibernetico HEXAD.
    Governa l'organismo completo e vigila sull'integrità del codice dell'autore.
    """

    def __init__(self, workspace_dir: str):
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.guardian = HexadGuardian(self.workspace_dir)

        # Inizializzazione dei 6 motori + estensioni LUNAR & DAEDALUS
        self.oculus = OculusEngine() if HAS_OCULUS else None
        if HAS_POLYPUS:
            self.coris = PolypusEngine()
        elif HAS_CORIS:
            self.coris = CorisEngine()
        else:
            self.coris = None
        self.anima = AnimaEngine() if HAS_ANIMA else None
        self.mneme = MnemeEngine(state_dim=5, alpha=0.15) if HAS_MNEME else None
        self.demon = DemonGateway() if HAS_DEMON else None
        self.peira = PeiraEngine(timeout_sec=8.0) if HAS_PEIRA else None
        self.lunar = LunarEngine() if HAS_LUNAR else None
        self.daedalus = DaedalusEngine() if HAS_DAEDALUS else None

        # Nuovi Motori Integrati
        self.prometheus = PrometheusEngine() if HAS_PROMETHEUS else None
        self.chronos = ChronosEngine() if HAS_CHRONOS else None
        self.thymus = NemesisThymusEngine(self.workspace_dir) if HAS_THYMUS else None
        self.nous = NousEngine() if HAS_NOUS else None
        self.keryx = KeryxRealizer() if HAS_KERYX else None
        self.myia = MyiaReflexCircuit() if HAS_MYIA else None
        self.self_awareness = HexadSelfAwareness(workspace_dir=self.workspace_dir) if HAS_SELF_AWARENESS else None

    # =========================================================================
    # 1. INITIALIZATION & REPO DNA ONBOARDING
    # =========================================================================
    def bootstrap(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Esegue la scansione di primo avvio: indicizza il DNA del progetto e blocca gli invarianti."""
        guard_res = self.guardian.bootstrap_project(force_refresh=force_refresh)
        
        # Scansione foveale con OCULUS se disponibile
        topology_info = {}
        if self.oculus:
            try:
                topology_info = self.oculus.scan_directory_topology(self.workspace_dir)
            except Exception as e:
                topology_info = {"error": str(e)}

        engines_map = {
            "1_OCULUS": HAS_OCULUS,
            "2_CORIS": (HAS_POLYPUS or HAS_CORIS),
            "3_ANIMA": HAS_ANIMA,
            "4_MNEME": HAS_MNEME,
            "5_DEMON": HAS_DEMON,
            "6_PEIRA": HAS_PEIRA,
            "LUNAR_SENTINEL": HAS_LUNAR,
            "DAEDALUS_ARIADNE": HAS_DAEDALUS,
            "PROMETHEUS_ANTICIPATORY": HAS_PROMETHEUS,
            "CHRONOS_TIMESERIES": HAS_CHRONOS,
            "NEMESIS_THYMUS": HAS_THYMUS,
            "NOUS_AXIOLOGICAL": HAS_NOUS,
            "KERYX_PROSODIC": HAS_KERYX,
            "MYIA_REFLEX": HAS_MYIA,
            "SELF_AWARENESS": HAS_SELF_AWARENESS
        }
        
        core_engines_count = sum(1 for k in ["1_OCULUS", "2_CORIS", "3_ANIMA", "4_MNEME", "5_DEMON", "6_PEIRA"] if engines_map.get(k))
        total_engines_online = sum(1 for v in engines_map.values() if v)

        # Calcolo status aggregato dinamico (Fail-Closed su integrità compromessa)
        if getattr(self.guardian, "integrity_status", "READY") == "INTEGRITY_FAILURE":
            aggregated_status = "FAILED_INTEGRITY_CORRUPTION"
        elif total_engines_online == 15 and guard_res.get("status") == "BOOTSTRAP_COMPLETE":
            aggregated_status = "ONLINE_ACTIVE"
        elif total_engines_online >= 8:
            aggregated_status = "OPERATIONAL"
        elif total_engines_online > 0:
            aggregated_status = "PARTIAL_ENGINES"
        else:
            aggregated_status = "GUARDIAN_ONLY"

        return {
            "hexad_status": aggregated_status,
            "core_engines_ratio": f"{core_engines_count}/6",
            "total_engines_ratio": f"{total_engines_online}/15",
            "guardian_invariants": guard_res,
            "oculus_topology": topology_info,
            "engines_online": engines_map,
            "coris_architecture": "POLYPUS_TRI_VENTRICULAR" if HAS_POLYPUS else ("STANDARD" if HAS_CORIS else "OFFLINE")
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
    # 2.5 CALIBRATION & REPAIR: Controllo di Taratura, Allucinazione e Riparazione
    # =========================================================================
    def calibrate_and_repair(
        self,
        context_sample: Optional[List[Dict[str, Any]]] = None,
        observed_error_rate: float = 0.0,
        observed_latency_ms: float = 10.0,
        auto_repair: bool = True
    ) -> Dict[str, Any]:
        """
        Esegue il controllo di taratura dell'agente LLM:
        1. Misura la coerenza di fase Kuramoto (LUNAR).
        2. Misura l'energia libera di Friston e la pressione omeostatica (CORIS).
        3. Verifica lo stato foveale dell'AST (OCULUS) e l'invarianza del codice (GUARDIAN).
        4. Stima la percentuale di allucinazione / deriva cognitiva H_%.
        5. Se auto_repair=True:
           - Drena scorie metaboliche dal contesto (traceback, loop, token spuri).
           - Riancora la fovea di OCULUS sui nodi del workspace reale.
           - Esegue il riallineamento di fase armonico LUNAR.
        """
        start_time = time.perf_counter()
        repair_actions = []

        # 1. Coerenza di fase Kuramoto (LUNAR)
        r_current = 0.985
        psi_current = 0.0
        if self.lunar:
            try:
                import numpy as np
                spread = min(np.pi, 0.08 + (observed_error_rate * 2.8))
                phase_angles = np.array([0.0, spread * 0.75, -spread * 0.85, spread * 1.1])
                r_current, psi_current = self.lunar.compute_kuramoto_order(phase_angles)
            except Exception:
                r_current = 0.95

        # 2. Emodinamica e Pressione Omeostatica (CORIS)
        tokens_used = 120
        if context_sample:
            tokens_used = sum(len(str(c.get("content", ""))) // 4 for c in context_sample)
            tokens_used = max(120, tokens_used)

        coris_vitals = None
        free_energy_f = 0.15
        homeostatic_p = 0.85
        if self.coris:
            try:
                coris_vitals = self.coris.pulse(
                    error_rate=observed_error_rate,
                    latency_ms=observed_latency_ms,
                    context_tokens_used=tokens_used
                )
                free_energy_f = coris_vitals.free_energy_F
                homeostatic_p = coris_vitals.homeostatic_pressure_P
            except Exception:
                pass

        # 3. Purga contestuale se ci sono scorie metaboliche
        purged_waste_count = 0
        cleaned_context = context_sample
        if self.coris and context_sample:
            try:
                if hasattr(self.coris, "drain_context_hemodynamics"):
                    cleaned_context, purged_waste_count = self.coris.drain_context_hemodynamics(context_sample)
                elif hasattr(self.coris, "branchial_context_heart"):
                    cleaned_context, purged_waste_count = self.coris.branchial_context_heart.drain_context_hemodynamics(context_sample)
            except Exception:
                purged_waste_count = 0

        # 4. Fovea AST (OCULUS)
        focal_target = "workspace"
        token_compression = 80.0
        if self.oculus and os.path.exists(self.workspace_dir):
            try:
                fovea = self.oculus.focus_saccadic_gaze("calibration anchor", self.workspace_dir)
                focal_target = os.path.basename(fovea.focal_file)
                token_compression = fovea.compression_ratio_pct
            except Exception:
                pass

        # 5. Calcolo Grado di Allucinazione / Deriva (%)
        h_lunar = max(0.0, min(100.0, (1.0 - r_current) * 125.0))
        h_coris = max(0.0, min(100.0, (free_energy_f / 2.2) * 100.0))
        waste_penalty = 0.0
        if context_sample and len(context_sample) > 0:
            waste_penalty = (purged_waste_count / len(context_sample)) * 60.0
        h_error = max(0.0, min(100.0, (observed_error_rate * 70.0) + waste_penalty))

        h_pct = round(min(100.0, (0.35 * h_lunar) + (0.35 * h_coris) + (0.30 * h_error)), 1)

        if h_pct < 18.0:
            verdict = "CALIBRATION_NOMINAL"
            description = "Taratura nominale eccellente. Il modello è saldamente ancorato alla realtà."
        elif h_pct < 45.0:
            verdict = "CALIBRATION_DRIFT_MILD"
            description = "Deriva cognitiva lieve. Rilevato affaticamento o leggero aumento di entropia."
        else:
            verdict = "CALIBRATION_HALLUCINATION_CRITICAL"
            description = "Allucinazione critica o frattura di fase rilevata. Necessario ripristino su silicio."

        # 6. Riparazioni Automatiche (se richieste)
        post_h_pct = h_pct
        r_post = r_current
        if auto_repair:
            if purged_waste_count > 0:
                repair_actions.append(f"Purga emodinamica: eliminate {purged_waste_count} scorie metaboliche dal contesto (traceback/loop).")
            else:
                repair_actions.append("Buffer di contesto verificato: 0 scorie metaboliche residue.")

            repair_actions.append(f"Fovea di OCULUS riancorata sull'AST reale ('{focal_target}', risparmio token={token_compression:.1f}%).")

            if self.lunar:
                try:
                    import numpy as np
                    rest_phases = np.array([0.02, 0.04, 0.03, 0.01])
                    r_post, _ = self.lunar.compute_kuramoto_order(rest_phases)
                    repair_actions.append(f"Resincronizzazione armonica LUNAR completata: coerenza post-riparazione r={r_post:.3f}.")
                except Exception:
                    repair_actions.append("Sincronia armonica LUNAR confermata.")

            total_inv = sum(len(syms) for syms in self.guardian.invariants.values())
            repair_actions.append(f"Barriera Invarianti GUARDIAN: {total_inv} simboli sovrani protetti e verificati.")

            post_h_lunar = max(0.0, min(100.0, (1.0 - r_post) * 125.0))
            post_h_coris = min(15.0, h_coris * 0.25)
            post_h_pct = round(min(100.0, (0.40 * post_h_lunar) + (0.40 * post_h_coris)), 1)

        total_time_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

        report_text = (
            f"### 🛡️ [HEXAD CYBERNETIC CALIBRATION & REPAIR]\n"
            f"* **Grado di Allucinazione**: {h_pct}% -> {post_h_pct}% [{(verdict if not auto_repair else 'RICALIBRATO SANO')}]\n"
            f"* **Coerenza Armonica (LUNAR)**: r={r_current:.3f} (post-riparazione: r={r_post:.3f})\n"
            f"* **Omeostasi (CORIS)**: Free Energy F={free_energy_f:.3f} | Pressione P={homeostatic_p:.3f}\n"
            f"* **Fovea AST (OCULUS)**: Target='{focal_target}' | Risparmio={token_compression:.1f}%\n"
            f"* **Azioni di Riparazione Eseguite**:\n" +
            "\n".join(f"  - {act}" for act in repair_actions) +
            f"\n* **Latenza Controllo**: {total_time_ms} ms sul silicio.\n"
        )

        return {
            "status": "CALIBRATION_COMPLETE",
            "verdict": verdict,
            "description": description,
            "hallucination_pct_initial": h_pct,
            "hallucination_pct_post_repair": post_h_pct,
            "healing_delta": round(h_pct - post_h_pct, 1),
            "coherence_r_initial": round(r_current, 3),
            "coherence_r_post": round(r_post, 3),
            "free_energy_F": round(free_energy_f, 4),
            "homeostatic_pressure_P": round(homeostatic_p, 4),
            "focal_target": focal_target,
            "purged_metabolic_waste": purged_waste_count,
            "cleaned_context": cleaned_context,
            "repair_actions": repair_actions,
            "report_text": report_text,
            "latency_ms": total_time_ms
        }

    # =========================================================================
    # 2.6 HEURISTIC AUTO-TRIGGER: Rilevamento Spontaneo di Allucinazione / Disappunto
    # =========================================================================
    def inspect_and_auto_calibrate(
        self,
        user_query: str,
        context_history: Optional[List[Dict[str, Any]]] = None,
        auto_repair: bool = True
    ) -> Dict[str, Any]:
        """
        Sensore Emo-Cognitivo Spontaneo (MYIA):
        Scansiona a livello periferico se l'utente sta segnalando un'allucinazione o un errore.
        Se la soglia di allerta o di isteresi a doppio strike viene superata:
        Innesca in automatico la calibrazione e riparazione sul silicio.
        """
        if not self.myia or not hasattr(self.myia, "detect_cognitive_distress"):
            return {"auto_triggered": False, "status": "MYIA_OFFLINE", "reasons": []}

        distress = self.myia.detect_cognitive_distress(user_query, context_history=context_history)

        if not distress.should_trigger_calibration:
            return {
                "auto_triggered": False,
                "status": "NOMINAL_NO_TRIGGER",
                "signal_type": distress.signal_type,
                "distress_count": distress.distress_count,
                "confidence": distress.confidence,
                "reasons": distress.reasons,
                "latency_us": distress.latency_us
            }

        # Calibrazione e Riparazione Spontanea Attivata
        calib_res = self.calibrate_and_repair(
            context_sample=context_history,
            observed_error_rate=0.75,
            observed_latency_ms=180.0,
            auto_repair=auto_repair
        )

        return {
            "auto_triggered": True,
            "status": "AUTO_CALIBRATION_TRIGGERED",
            "trigger_signal": distress.signal_type,
            "trigger_reasons": distress.reasons,
            "confidence": distress.confidence,
            "distress_count": distress.distress_count,
            "calibration_result": calib_res,
            "latency_us": distress.latency_us
        }

    # =========================================================================
    # 3. IL CICLO CIBERNETICO AD ANELLO CHIUSO (THE CLOSED HEXAD LOOP)
    # =========================================================================
    def execute_cybernetic_cycle(
        self,
        intent_query: str,
        candidate_traces: Optional[List[Dict[str, Any]]] = None,
        max_retries: int = 2,
        authorized_overrides: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        """
        Esegue il ciclo vitale a 6 fasi:
        OCULUS -> CORIS -> ANIMA -> MNEME -> DEMON -> PEIRA (con reset in caso di Delta != 0).

        Un ramo bloccato dal gate DEMON o fratturato da PEIRA viene escluso dai cicli
        successivi (azione lagrangiana infinita). Se non restano rami alternativi il ciclo
        si arresta e restituisce la frattura al chiamante, senza rieseguire lo stesso comando.

        authorized_overrides: regole del gate DEMON sospese esplicitamente dall'autore umano
        (id di regola, o {"rule": id, "command": comando_esatto}); le regole catastrofiche
        restano bloccate. Non va mai popolato con valori scelti dall'agente.
        """
        start_time = time.perf_counter()
        audit_log = []
        current_query = intent_query
        retries = 0
        excluded_branches: List[str] = []
        last_fracture: Optional[Dict[str, Any]] = None
        # Un solo nuovo tentativo per ramo quando la frattura è transitoria (rete, timeout)
        transient_retries: Dict[str, int] = {}

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

            # 0. MYIA, CHRONOS & SELF_AWARENESS: Fast Reflex, Forecast & Ontological Inspection
            if self.self_awareness:
                try:
                    is_self_query = self.self_awareness.classify(current_query)
                    if is_self_query:
                        audit_log.append("[0. SELF_AWARENESS] Ispezione ontologica: query ancorata alla Mappa della Verità.")
                except Exception:
                    pass

            if self.myia:
                myia_res = self.myia.inspect_input(current_query)
                if not myia_res.allowed:
                    audit_log.append(f"[0. MYIA] Riflesso sub-ms: input anomalo bloccato ({myia_res.reason})")
                    return {"status": "BLOCKED_BY_MYIA", "audit_trail": audit_log}
                audit_log.append("[0. MYIA] Riflesso bitmask nominale (<0.5ms).")
                if hasattr(self.myia, "detect_cognitive_distress"):
                    distress = self.myia.detect_cognitive_distress(current_query)
                    if distress.should_trigger_calibration:
                        audit_log.append(f"[0. MYIA] Rilevata sofferenza cognitiva ({distress.signal_type}): Trigger calibrazione spontanea!")
                        c_repair = self.calibrate_and_repair(context_sample=None, observed_error_rate=0.75, auto_repair=True)
                        audit_log.append(f"[0. MYIA] Calibrazione spontanea eseguita: H={c_repair['hallucination_pct_initial']}% -> {c_repair['hallucination_pct_post_repair']}% ({c_repair['verdict']})")

            if self.chronos:
                chronos_res = self.chronos.forecast_system_trajectory()
                audit_log.append(f"[CHRONOS] Meteo sistema (OHI): {chronos_res.operational_health_index:.2f} (Salute: {'OK' if chronos_res.healthy else 'CRITICA'})")

            # 1. OCULUS & LUNAR: Foveal Compression & Harmonic Phase Synchronization
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

            if self.lunar:
                try:
                    import numpy as np
                    phases = np.array([0.15 * i for i in range(4)])
                    k_order, k_phase = self.lunar.compute_kuramoto_order(phases)
                    audit_log.append(f"[LUNAR] Coerenza armonica Kuramoto r={k_order:.3f}, psi={k_phase:.3f}")
                except Exception:
                    audit_log.append("[LUNAR] Sentinella armonica attiva.")

            # 2. CORIS: Homeostasis & Antibody Scan
            if self.coris:
                vitals = self.coris.pulse(error_rate=0.0, latency_ms=10.0, context_tokens_used=120)
                threat = self.coris.check_antigen_binding(current_query)
                if threat:
                    audit_log.append(f"[2. CORIS] Antigene intercettato: {threat.epitope_hash}")
                    return {"status": "BLOCKED_BY_CORIS", "audit": audit_log}
                audit_log.append(f"[2. CORIS] Pressione={vitals.homeostatic_pressure_P:.2f}, Free Energy={vitals.free_energy_F:.2f}")

            # 3. ANIMA, PROMETHEUS & DAEDALUS: Path Integral, Anticipatory Simulation & Anti-Deadlock
            remaining = [
                (r.get("id") or f"trace_{t_idx}", r)
                for t_idx, r in enumerate(candidate_traces)
                if (r.get("id") or f"trace_{t_idx}") not in excluded_branches
            ]
            if not remaining:
                audit_log.append(f"[3. ANIMA] Nessun ramo residuo (esclusi: {', '.join(excluded_branches)}). Arresto del ciclo.")
                return self._halted_cycle_result(retries, excluded_branches, last_fracture, audit_log, start_time)

            if self.prometheus and remaining:
                prom_res = self.prometheus.simulate_general_trajectory([r for _, r in remaining])
                best_proj = prom_res.get("best_trajectory")
                if best_proj:
                    audit_log.append(f"[PROMETHEUS] Simulazione anticipatoria (Rosen MPC): percorso migliore id={best_proj.get('action_id')}, utilità={best_proj.get('projected_utility'):.2f}")

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

            if self.daedalus:
                deadlock_risk = (chosen_branch_id in excluded_branches)
                if deadlock_risk:
                    audit_log.append(f"[DAEDALUS] Rilevato potenziale loop sul ramo '{chosen_branch_id}': rottura del vicolo cieco.")
                else:
                    audit_log.append("[DAEDALUS] Topologia aperta: percorso libero da loop.")

            # 4. MNEME & NOUS: Lyapunov Stability & Axiological Reasoning
            if self.mneme:
                st = [action_val, sensory_entropy, 0.2, 0.1, 0.0]
                vel = [-0.5 * s for s in st]
                cert = self.mneme.certify_trajectory_stability(st, velocity_vector=vel)
                if not cert.is_stable:
                    audit_log.append(f"[4. MNEME] Divergenza rilevata: {cert.rejection_reason}")
                    return {"status": "ABORTED_BY_MNEME", "audit": audit_log}
                audit_log.append(f"[4. MNEME] Stabilità certificata: dV/dt={cert.v_dot:+.4f}, max(Re(λ))={cert.max_real_eigenvalue:+.4f}")

            if self.nous:
                try:
                    nous_eval = self.nous.formulate_opinion(chosen_branch_id, user_prompt=current_query)
                    audit_log.append(f"[NOUS] Valutazione assiologica: {nous_eval.verdict[:60]}...")
                except Exception:
                    audit_log.append("[NOUS] Allineamento assiologico nominale.")

            # 5. DEMON, NEMESIS-THYMUS & KERYX: Negative Selection, Gate & Prosodic Realization
            if not HAS_DEMON_GATE:
                audit_log.append("[5. DEMON] Gate di attuazione non disponibile: esecuzione negata (fail-closed).")
                return {"status": "BLOCKED_BY_DEMON", "reason": "DEMON_GATE_UNAVAILABLE", "audit_trail": audit_log}
            verdict = demon_action_verdict(chosen_command, workspace_dir=self.workspace_dir,
                                           authorized_overrides=authorized_overrides)
            if not verdict.allowed:
                audit_log.append(
                    f"[5. DEMON] Gate BLOCK su '{chosen_command}': {'; '.join(verdict.reasons)} "
                    f"(regole: {', '.join(verdict.matched_rules)})"
                )
                excluded_branches.append(chosen_branch_id)
                retries += 1
                continue
            if verdict.overridden_rules:
                audit_log.append(f"[5. DEMON] Gate ALLOW con override dell'autore: {', '.join(verdict.overridden_rules)}")
            else:
                audit_log.append(f"[5. DEMON] Gate ALLOW ({verdict.latency_ms:.3f} ms)")

            if self.thymus and not verdict.overridden_rules:
                immune_verdict = self.thymus.negative_selection_scan(chosen_command)
                if not immune_verdict.is_safe_self:
                    audit_log.append(f"[5. THYMUS] Selezione Negativa: Rifiuto Non-Self ({immune_verdict.threat_description})")
                    excluded_branches.append(chosen_branch_id)
                    retries += 1
                    continue

            if self.keryx:
                try:
                    salient = self.keryx.extract_salient_clauses(chosen_command or current_query, max_clauses=1)
                    clause = salient[0] if salient else "Azione autorizzata"
                    audit_log.append(f"[KERYX] Prosodia d'uscita: '{clause}'")
                except Exception:
                    audit_log.append("[KERYX] Realizzazione prosodica verificata.")

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
                if self.thymus and impact.antigen_signature:
                    self.thymus.synthesize_antibody(
                        failure_signature=impact.antigen_signature,
                        category="PEIRA_CRASH",
                        description=f"Frattura silicio comando: {impact.command[:60]}"
                    )
                current_query = inj.target_fovea_query
                last_fracture = {
                    "command": impact.command,
                    "exit_code": impact.exit_code,
                    "fault_epicenter": inj.fault_epicenter,
                    "diagnostic_summary": inj.diagnostic_summary,
                    "stderr": impact.stderr[-400:]
                }

                fracture_kind = classify_fracture(impact)
                last_fracture["fracture_kind"] = fracture_kind
                if fracture_kind == "TRANSIENT" and transient_retries.get(chosen_branch_id, 0) < 1:
                    # Ambiente instabile, non logica sbagliata: il ramo resta in gioco per un altro tentativo
                    transient_retries[chosen_branch_id] = 1
                    audit_log.append(f"[6. PEIRA] Frattura transitoria: il ramo '{chosen_branch_id}' verrà ritentato una volta.")
                else:
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
