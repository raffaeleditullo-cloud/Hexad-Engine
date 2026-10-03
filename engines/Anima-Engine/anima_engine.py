"""
ANIMA Engine: Continuous Variational Consciousness & Path-Integral Wave Collapse.

Replaces discrete pairwise Jaccard metrics with continuous Action Phase Accumulation:
    phi_i = (1 / hbar_eff) * int_C (H_token(t) - lambda * C_complexity(t)) dt

- Principle of Least Action: Optimal reasoning follows paths of minimal entropy variance.
- O(N) Superposition: Global state vector Psi = sum_i A_i * exp(i * phi_i).
- Streaming Early Decoherence: Self-extinguishes hallucinated branches mid-sentence.
- Euclidean Path Integral Weighting: exp(-beta * S_i) ensures stationary action dominance.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
import math
import time
import cmath

@dataclass
class AnimaStep:
    """Rappresenta un singolo passo di decoding / emissione token lungo una traiettoria."""
    step_index: int
    token: str
    token_entropy: float        # H(t) = -sum p * log2(p), misura di sorpresa / incertezza
    complexity_delta: float = 0.0  # Variazione di complessità sintattica / strutturale
    timestamp_ms: float = field(default_factory=lambda: time.perf_counter() * 1000.0)

@dataclass
class AnimaBranch:
    """Ramo di pensiero continuo in evoluzione nello spazio di Hilbert."""
    id: str
    name: str
    initial_amplitude: float = 1.0
    steps: List[AnimaStep] = field(default_factory=list)
    accumulated_action: float = 0.0
    accumulated_phase: float = 0.0
    effective_amplitude: float = 1.0
    is_pruned: bool = False
    prune_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def complex_state(self) -> complex:
        """Stato quantistico complesso psi_i = A_i * e^(i * phi_i)."""
        if self.is_pruned:
            return 0.0 + 0.0j
        return self.effective_amplitude * cmath.exp(1j * self.accumulated_phase)

    @property
    def generated_text(self) -> str:
        return "".join(s.token for s in self.steps)

@dataclass
class AnimaCollapseResult:
    scenario_name: str
    active_branches: int
    pruned_branches: int
    eigenstate: AnimaBranch
    coherence_percentage: float
    total_system_action: float
    execution_time_ms: float
    audit_trail: List[str]

class AnimaEngine:
    """
    Motore variazionale continuo che arbitra percorsi di pensiero
    in O(N) tramite la fase d'azione e la Regola di Born.
    """
    def __init__(
        self,
        hbar_eff: float = 1.0,           # Costante d'azione efficace
        complexity_weight: float = 0.30,  # lambda: peso della complessità strutturale
        action_beta: float = 0.45,        # beta: peso dell'azione (Principio di Minima Azione)
        entropy_damping: float = 0.85,    # gamma: sensibilità alla turbolenza entropica
        prune_threshold: float = 0.04,   # Taglio rami con ampiezza coerente < 4%
        phase_jitter_limit: float = 2.0   # Limite di oscillazione rapida di fase
    ):
        self.hbar_eff = hbar_eff
        self.complexity_weight = complexity_weight
        self.action_beta = action_beta
        self.entropy_damping = entropy_damping
        self.prune_threshold = prune_threshold
        self.phase_jitter_limit = phase_jitter_limit

    def ingest_step(
        self,
        branch: AnimaBranch,
        token: str,
        token_entropy: float,
        complexity_delta: float = 0.0
    ) -> Tuple[bool, float, float]:
        """
        Ingerisce un token in streaming, accumula l'azione infinitesima dS e aggiorna la fase.
        Ritorna: (keep_alive: bool, current_phase: float, effective_amplitude: float)
        """
        if branch.is_pruned:
            return False, branch.accumulated_phase, 0.0

        step_idx = len(branch.steps) + 1
        step = AnimaStep(
            step_index=step_idx,
            token=token,
            token_entropy=token_entropy,
            complexity_delta=complexity_delta
        )
        branch.steps.append(step)

        # Lagrangiana d'azione: L(t) = H_token(t) - lambda * C_complexity(t)
        action_differential = max(0.01, token_entropy - (self.complexity_weight * complexity_delta))
        branch.accumulated_action += action_differential

        # Fase accumulata lungo la curva C_i: phi = S / hbar
        branch.accumulated_phase = (branch.accumulated_action / self.hbar_eff) % (2.0 * math.pi)

        # Calcolo varianza locale dell'entropia (misura di turbolenza microscopica)
        recent_steps = branch.steps[-6:]
        entropies = [s.token_entropy for s in recent_steps]
        mean_h = sum(entropies) / len(entropies)
        variance_h = sum((h - mean_h) ** 2 for h in entropies) / len(entropies) if len(entropies) > 1 else 0.0

        # Damping combinato: Feynman-Kac (minima azione) + Soppressione turbolenza
        action_penalty = math.exp(-self.action_beta * branch.accumulated_action)
        variance_penalty = math.exp(-self.entropy_damping * variance_h)
        branch.effective_amplitude = branch.initial_amplitude * action_penalty * variance_penalty

        # Controllo divergenza o jitter di fase (salto stocastico violento)
        if len(branch.steps) >= 2:
            d_phi = abs(branch.steps[-1].token_entropy - branch.steps[-2].token_entropy)
            if d_phi >= self.phase_jitter_limit:
                branch.is_pruned = True
                branch.prune_reason = f"Divergenza stocastica della fase (d_phi={d_phi:.2f} >= {self.phase_jitter_limit})"
                return False, branch.accumulated_phase, branch.effective_amplitude

        # Controllo decoerenza istantanea (Streaming Early Prune)
        if branch.effective_amplitude < self.prune_threshold:
            branch.is_pruned = True
            branch.prune_reason = f"Decoerenza entropica critica (Amp={branch.effective_amplitude:.4f} < {self.prune_threshold})"
            return False, branch.accumulated_phase, branch.effective_amplitude

        return True, branch.accumulated_phase, branch.effective_amplitude

    def compute_state_vector(self, branches: List[AnimaBranch]) -> complex:
        """
        Calcola il vettore di stato globale di sovrapposizione in O(N):
            Psi = sum_i A_i * exp(i * phi_i)
        """
        psi_total = 0.0 + 0.0j
        for b in branches:
            if not b.is_pruned:
                psi_total += b.complex_state
        return psi_total

    def collapse(self, scenario_name: str, branches: List[AnimaBranch]) -> AnimaCollapseResult:
        """
        Esegue il collasso deterministico dello stato a minima azione / massima coerenza.
        Complessità rigorosamente O(N).
        """
        start_time = time.perf_counter()
        audit: List[str] = [f"=== ANIMA CONTINUOUS COLLAPSE: {scenario_name} ==="]

        active = [b for b in branches if not b.is_pruned]
        pruned_count = len(branches) - len(active)

        if not active:
            audit.append("ATTENZIONE: Tutti i rami sono andati in decoerenza. Ripristino del ramo a minima azione.")
            best_branch = min(branches, key=lambda b: abs(b.accumulated_action))
            exec_time = (time.perf_counter() - start_time) * 1000.0
            return AnimaCollapseResult(
                scenario_name=scenario_name,
                active_branches=0,
                pruned_branches=len(branches),
                eigenstate=best_branch,
                coherence_percentage=0.0,
                total_system_action=sum(b.accumulated_action for b in branches),
                execution_time_ms=exec_time,
                audit_trail=audit
            )

        # 1. Calcolo del vettore globale Psi in O(N)
        psi_global = self.compute_state_vector(active)
        psi_norm = abs(psi_global)
        global_energy = psi_norm ** 2
        audit.append(f"Vettore globale di Hilbert: |Psi|^2 = {global_energy:.4f} (Rami attivi: {len(active)}/{len(branches)})")

        # 2. Punteggio di risonanza per singolo ramo
        densities = []
        for b in active:
            # Proiezione di fase normalizzata [-1, +1]
            phase_alignment = (b.complex_state.conjugate() * psi_global).real / (psi_norm + 1e-9) if psi_norm > 0 else 0.0
            resonance_boost = 1.0 + max(0.0, phase_alignment)
            
            # Densità coerente di Born |psi|^2 modulata dalla risonanza collettiva
            density = (b.effective_amplitude ** 2) * resonance_boost
            densities.append((b, max(1e-9, density)))

        total_density = sum(s for _, s in densities)
        audit.append(f"Densità di probabilità totale coerente: {total_density:.4f}")

        # Normalizzazione
        ranked = []
        for b, density in densities:
            prob = (density / total_density) * 100.0 if total_density > 0 else 0.0
            ranked.append((b, prob, density))
            audit.append(
                f"  Ramo [{b.id}] '{b.name}': Azione={b.accumulated_action:.3f} | "
                f"Amp={b.effective_amplitude:.3f} | Fase={math.degrees(b.accumulated_phase):5.1f}° | Probabilità={prob:5.1f}%"
            )

        # 3. Elezione dell'Eigenstate Dominante (Minima Azione / Massima Ampiezza Coerente)
        winner_branch, win_prob, _ = max(ranked, key=lambda x: x[1])
        exec_time = (time.perf_counter() - start_time) * 1000.0

        audit.append(
            f"Collasso O(N) completato in {exec_time:.3f}ms. "
            f"Eigenstate Eletto: [{winner_branch.id}] '{winner_branch.name}' con {win_prob:.1f}% di coerenza."
        )

        return AnimaCollapseResult(
            scenario_name=scenario_name,
            active_branches=len(active),
            pruned_branches=pruned_count,
            eigenstate=winner_branch,
            coherence_percentage=win_prob,
            total_system_action=sum(b.accumulated_action for b in branches),
            execution_time_ms=exec_time,
            audit_trail=audit
        )
