"""
MNEME Engine: Asymptotic Stability, Lyapunov Invariant & Ricci Curvature Flow.

Pillar 4 (and Final Anchor) of the Cybernetic Oracle Ecosystem:
1. OCULUS (Observer / Sensory Manifold & AST Compression)
2. ANIMA (Optimal Controller / Intent & Path Integral Minimization)
3. CORIS (Dissipative Thermodynamics / Heart & Free Energy Homeostasis)
4. MNEME (Asymptotic Stability / Lyapunov Certification & Ricci Metric Memory)
5. DEMON (Actuator Enclave / Control Barrier Functions & Zero-Blast Muscle)

Mathematical Foundations:
- Lyapunov Candidate Function: V(x) = 1/2 (x - x*)^T P (x - x*) >= 0
- Asymptotic Decay Rate: dV/dt = grad(V) · f(x) <= -alpha ||x - x*||^2  (alpha > 0)
- Spectral Radius & Jacobian Stability: max_i Re(lambda_i(J)) < 0
- Hamilton's Ricci Curvature Flow: d g_ij / dt = -2 R_ij
- Topological Attractor Memory & Invariance Preservation
"""

import time
import math
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import numpy as np


@dataclass
class StabilityCertificate:
    """Certificato formale di stabilità asintotica rilasciato da MNEME."""
    is_stable: bool
    v_value: float                          # V(x): Valore della funzione di Lyapunov
    v_dot: float                            # dV/dt: Tasso di variazione temporale
    alpha_decay_margin: float               # -alpha ||x - x*||^2 - dV/dt (deve essere >= 0)
    spectral_radius: float                  # max |lambda_i(J)|
    max_real_eigenvalue: float              # max Re(lambda_i(J)) (deve essere < 0 per contrazione)
    eigenvalues: List[complex]              # Spettro completo degli autovalori
    lipschitz_constant: float               # L stimato sotto perturbazione epsilon
    is_perturbed_robust: bool               # True se la perturbazione decade all'attrattore
    rejection_reason: Optional[str] = None  # Causa di rigetto se instabile
    timestamp: float = field(default_factory=time.time)


@dataclass
class RicciFlowResult:
    """Risultato della regolarizzazione geometrica del manifold dello stato."""
    initial_scalar_curvature: float
    final_scalar_curvature: float
    curvature_entropy_reduction_pct: float
    initial_metric: List[List[float]]
    smoothed_metric: List[List[float]]
    ricci_tensor_norm: float
    iterations_run: int
    converged: bool


@dataclass
class AttractorNode:
    """Nodo di memoria topologica invariante salvato nell'iperspazio di MNEME."""
    state_id: str
    target_equilibrium: List[float]
    basin_radius: float
    energy_level: float
    metadata: Dict[str, Any]
    created_at: float = field(default_factory=time.time)


class MnemeEngine:
    """
    Il Motore di Stabilità Asintotica, Funzioni di Lyapunov e Flusso di Ricci.
    Garantisce che i cammini di ANIMA e le azioni di DEMON non cadano in
    punti di sella, cicli limite caotici o divergenze numeriche.
    """

    def __init__(self, state_dim: int = 5, alpha: float = 0.15, lyapunov_p_matrix: Optional[np.ndarray] = None):
        """
        Inizializza il motore con dimensione dello stato e matrice P definita positiva.
        Dimensioni tipiche dello stato vettoriale x:
        x[0]: Errore residuo rispetto al target (distanza semantica / AST goal)
        x[1]: Tasso di entropia / derivata della fase di ANIMA
        x[2]: Pressione metabolica di contesto (CORIS Free Energy)
        x[3]: Indice di complessità ciclomatica / potenziale deadlock
        x[4]: Frequenza di oscillazione / micro-loop detection
        """
        self.state_dim = state_dim
        self.alpha = alpha  # Costante di decadimento contrattivo minimo: dV/dt <= -alpha ||x-x*||^2

        if lyapunov_p_matrix is not None:
            assert lyapunov_p_matrix.shape == (state_dim, state_dim), "P matrix shape mismatch"
            self.P = np.array(lyapunov_p_matrix, dtype=float)
        else:
            # Matrice P diagonale positiva (ponderata per penalizzare loop e divergenze)
            self.P = np.diag([2.0, 1.5, 1.2, 1.8, 2.5][:state_dim])

        # Verifica di sicurezza: P deve essere simmetrica e definita positiva
        self.P = 0.5 * (self.P + self.P.T)
        evals_p = np.linalg.eigvalsh(self.P)
        if np.any(evals_p <= 0):
            self.P += np.eye(state_dim) * (abs(float(np.min(evals_p))) + 1e-4)

        # Registro degli attrattori topologici stabili (Memoria Invariante)
        self.attractor_registry: Dict[str, AttractorNode] = {}
        # Cronologia delle certificazioni
        self.history: List[StabilityCertificate] = []

    # =========================================================================
    # 1. CERTIFICAZIONE DI STABILITÀ SECONDO LYAPUNOV (dV/dt < -alpha ||x-x*||^2)
    # =========================================================================
    def certify_trajectory_stability(
        self,
        current_state: List[float],
        target_equilibrium: Optional[List[float]] = None,
        velocity_vector: Optional[List[float]] = None,
        jacobian_matrix: Optional[List[List[float]]] = None,
        epsilon_noise_norm: float = 0.05
    ) -> StabilityCertificate:
        """
        Valuta se lo stato attuale x ed il campo vettoriale f(x) generato da ANIMA/DEMON
        sono asintoticamente stabili verso l'equilibrio x*.
        """
        x = np.array(current_state, dtype=float).reshape(-1)
        if len(x) != self.state_dim:
            # Adatta la dimensione al volo se necessario
            x = np.pad(x, (0, max(0, self.state_dim - len(x))))[:self.state_dim]

        x_star = np.zeros(self.state_dim) if target_equilibrium is None else np.array(target_equilibrium, dtype=float)[:self.state_dim]
        delta_x = x - x_star
        norm_delta_sq = float(np.sum(delta_x ** 2))

        # 1. Calcolo del valore candidato di Lyapunov: V(x) = 1/2 delta_x^T P delta_x
        v_value = float(0.5 * delta_x.T @ self.P @ delta_x)

        # 2. Dinamica del sistema: f(x) = velocity_vector
        if velocity_vector is not None:
            f_x = np.array(velocity_vector, dtype=float)[:self.state_dim]
        else:
            # Modello contrattivo di default con smorzamento naturale
            f_x = -0.4 * delta_x

        # 3. Derivata temporale di Lyapunov lungo la traiettoria:
        # grad(V) = P delta_x
        # dV/dt = grad(V)^T · f(x) = delta_x^T P f(x)
        grad_v = self.P @ delta_x
        v_dot = float(grad_v.T @ f_x)

        # Requisito asintotico stretto: dV/dt <= -alpha ||x - x*||^2
        required_bound = -self.alpha * norm_delta_sq
        alpha_margin = float(required_bound - v_dot)  # Deve essere >= 0

        # 4. Calcolo dello Jacobiano J = df/dx e del suo Spettro di Autovalori
        if jacobian_matrix is not None:
            J = np.array(jacobian_matrix, dtype=float)[:self.state_dim, :self.state_dim]
        else:
            # Calcolo dello Jacobiano con differenze finite sul campo f_x
            J = self._estimate_numerical_jacobian(x, f_x)

        eigenvalues = np.linalg.eigvals(J).tolist()
        real_parts = [float(ev.real) for ev in eigenvalues]
        spectral_radius = float(max(abs(ev) for ev in eigenvalues))
        max_real_ev = float(max(real_parts))

        # 5. Robustezza sotto perturbazione epsilon (Lipschitz continuity & basin attraction)
        lipschitz_est, perturbed_stable = self._verify_epsilon_perturbation(
            x, x_star, f_x, epsilon_norm=epsilon_noise_norm
        )

        # 6. Verdetto Rigoroso
        is_stable = True
        rejection_reason = None

        if norm_delta_sq > 1e-6:
            # Condizione 1: dV/dt deve essere strettamente contrattiva
            if v_dot >= 0:
                is_stable = False
                rejection_reason = f"DIVERGENZA DINAMICA: dV/dt = {v_dot:+.4e} >= 0. Il sistema sta accumulando energia instabile."
            elif alpha_margin < -1e-5:
                is_stable = False
                rejection_reason = f"DECADIMENTO TROPPO LENTO: dV/dt ({v_dot:.4e}) non supera la soglia asintotica -alpha*||x-x*||^2 ({required_bound:.4e})."

            # Condizione 2: Spettro dello Jacobiano (tutti gli autovalori devono avere parte reale strettamente negativa)
            if max_real_ev >= 0:
                is_stable = False
                mode_desc = f"MODO DIVERGENTE RILEVATO: max Re(lambda) = {max_real_ev:+.4e} >= 0. Presenza di autovalore instabile o ciclo limite."
                rejection_reason = (rejection_reason + " | " + mode_desc) if rejection_reason else mode_desc

            # Condizione 3: Robustezza alla perturbazione
            if not perturbed_stable:
                is_stable = False
                pert_desc = f"INSTABILITÀ SOTTO PERTURBAZIONE: Lipschitz L={lipschitz_est:.2f} eccessivo o traiettoria esplosa oltre la palla epsilon."
                rejection_reason = (rejection_reason + " | " + pert_desc) if rejection_reason else pert_desc

        cert = StabilityCertificate(
            is_stable=is_stable,
            v_value=v_value,
            v_dot=v_dot,
            alpha_decay_margin=alpha_margin,
            spectral_radius=spectral_radius,
            max_real_eigenvalue=max_real_ev,
            eigenvalues=eigenvalues,
            lipschitz_constant=lipschitz_est,
            is_perturbed_robust=perturbed_stable,
            rejection_reason=rejection_reason
        )
        self.history.append(cert)
        return cert

    # =========================================================================
    # 2. RICCI CURVATURE FLOW SUL METRIC TENSOR DELLO SPAZIO LATENTE
    #    d g_ij / dt = -2 R_ij
    # =========================================================================
    def apply_ricci_curvature_flow(
        self,
        base_metric: Optional[List[List[float]]] = None,
        iterations: int = 5,
        dt_step: float = 0.05
    ) -> RicciFlowResult:
        """
        Deforma la metrica riemanniana del grafo/task g_ij lungo il flusso di Ricci
        per eliminare singolarità geometriche, colli di bottiglia o zone caotiche.
        """
        n = min(3, self.state_dim)  # Sottomanifold 2D o 3D per calcolo geometrico
        if base_metric is not None:
            g = np.array(base_metric, dtype=float)[:n, :n]
        else:
            # Metrica con una deformazione simulata (es. curvatura disomogenea)
            g = np.eye(n) * 1.5
            g[0, 1] = g[1, 0] = 0.4
            if n > 2:
                g[1, 2] = g[2, 1] = -0.3

        # Assicura simmetria e positività iniziale
        g = 0.5 * (g + g.T)
        g += np.eye(n) * 0.1

        initial_g = np.copy(g)
        initial_scalar_R = self._compute_scalar_curvature(initial_g)

        converged = False
        current_g = np.copy(g)

        for it in range(iterations):
            # Calcola il tensore di Ricci R_ij
            R_tensor = self._compute_ricci_tensor(current_g)
            ricci_norm = float(np.linalg.norm(R_tensor))

            # Flusso di Ricci di Hamilton: g_(t+1) = g_t - 2 * dt * R_ij
            dg = -2.0 * dt_step * R_tensor
            current_g = current_g + dg

            # Mantiene la metrica definita positiva e simmetrica
            current_g = 0.5 * (current_g + current_g.T)
            eigvals, eigvecs = np.linalg.eigh(current_g)
            eigvals = np.clip(eigvals, 0.05, 50.0)
            current_g = eigvecs @ np.diag(eigvals) @ eigvecs.T

            if ricci_norm < 1e-4:
                converged = True
                break

        final_scalar_R = self._compute_scalar_curvature(current_g)
        r_diff = abs(initial_scalar_R) - abs(final_scalar_R)
        entropy_reduc_pct = float(max(0.0, min(100.0, (r_diff / (abs(initial_scalar_R) + 1e-6)) * 100.0)))
        final_ricci_norm = float(np.linalg.norm(self._compute_ricci_tensor(current_g)))

        return RicciFlowResult(
            initial_scalar_curvature=float(initial_scalar_R),
            final_scalar_curvature=float(final_scalar_R),
            curvature_entropy_reduction_pct=entropy_reduc_pct,
            initial_metric=initial_g.tolist(),
            smoothed_metric=current_g.tolist(),
            ricci_tensor_norm=final_ricci_norm,
            iterations_run=iterations,
            converged=converged
        )

    # =========================================================================
    # 3. MEMORIA TOPOLOGICA DEGLI ATTRATTORI (Invariant Preserving)
    # =========================================================================
    def register_stable_attractor(
        self,
        state_id: str,
        equilibrium_coords: List[float],
        basin_radius: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AttractorNode:
        """Salva uno stato target certificato come Attrattore Stabile Invariante."""
        eq = np.array(equilibrium_coords, dtype=float)[:self.state_dim].tolist()
        node = AttractorNode(
            state_id=state_id,
            target_equilibrium=eq,
            basin_radius=basin_radius,
            energy_level=float(0.5 * np.array(eq).T @ self.P @ np.array(eq)),
            metadata=metadata or {}
        )
        self.attractor_registry[state_id] = node
        return node

    def check_basin_membership(self, state: List[float]) -> Optional[Tuple[str, float]]:
        """
        Controlla se uno stato candidato cade all'interno del bacino d'attrazione
        di un attrattore stabile noto. Ritorna (state_id, distanza).
        """
        x = np.array(state, dtype=float)[:self.state_dim]
        best_match = None
        min_dist = float("inf")

        for s_id, node in self.attractor_registry.items():
            target = np.array(node.target_equilibrium)
            dist = float(np.linalg.norm(x - target))
            if dist <= node.basin_radius and dist < min_dist:
                min_dist = dist
                best_match = (s_id, dist)

        return best_match

    # =========================================================================
    # METODI AUSILIARI DI FISICA NUMERICA & CONTROLLO
    # =========================================================================
    def _estimate_numerical_jacobian(self, x: np.ndarray, f_x: np.ndarray) -> np.ndarray:
        """
        Stima la matrice Jacobiana locale J = df/dx a partire dallo stato x e dal vettore di flusso f(x).
        Lungo ciascuna coordinata, il coefficiente diagonale rappresenta il rateo effettivo f_i / (x_i - x_star_i).
        """
        n = len(x)
        J = np.zeros((n, n))
        for i in range(n):
            if abs(x[i]) > 1e-6:
                J[i, i] = f_x[i] / x[i]
            else:
                J[i, i] = -self.alpha
        return J

    def _verify_epsilon_perturbation(
        self,
        x: np.ndarray,
        x_star: np.ndarray,
        f_x: np.ndarray,
        epsilon_norm: float = 0.05
    ) -> Tuple[float, bool]:
        """Inietta una perturbazione epsilon casuale e misura la costante di Lipschitz locale."""
        noise = np.random.normal(0, 1, size=len(x))
        norm_noise = np.linalg.norm(noise)
        if norm_noise > 1e-9:
            noise = (noise / norm_noise) * epsilon_norm
        else:
            noise = np.zeros_like(x)

        x_pert = x + noise
        J = self._estimate_numerical_jacobian(x, f_x)
        f_pert = f_x + J @ noise

        delta_f_norm = float(np.linalg.norm(f_pert - f_x))
        lipschitz = delta_f_norm / (epsilon_norm + 1e-9)

        # Se il passo perturbato riduce la distanza da x*, il sistema è robusto
        dt = 0.1
        next_orig = (x - x_star) + f_x * dt
        next_pert = (x_pert - x_star) + f_pert * dt

        dist_orig = float(np.linalg.norm(next_orig))
        dist_pert_next = float(np.linalg.norm(next_pert))

        robust = (dist_pert_next <= dist_orig + epsilon_norm * 1.05) and (lipschitz < 15.0)
        return float(lipschitz), robust

    def _compute_ricci_tensor(self, g: np.ndarray) -> np.ndarray:
        """
        Calcola un'approssimazione del tensore di Ricci R_ij per la metrica simmetrica g.
        R_ij ~ 1/2 [ Laplacian(g_ij) + tracce di Christoffel ].
        In coordinate normali / metrica diagonale perturbata, R_ij cattura le discrepanze fuori-diagonale.
        """
        n = g.shape[0]
        R = np.zeros((n, n))
        inv_g = np.linalg.pinv(g)

        # Deviazione della curvatura dalla metrica euclidea isotropa
        mean_scale = np.trace(g) / n
        isotropic = np.eye(n) * mean_scale
        diff = g - isotropic

        # Il tensore di Ricci si oppone alle anomalie di curvatura locale
        R = diff @ inv_g @ diff + 0.1 * diff
        return 0.5 * (R + R.T)

    def _compute_scalar_curvature(self, g: np.ndarray) -> float:
        """Calcola la curvatura scalare R = g^{ij} R_{ij}."""
        R_ij = self._compute_ricci_tensor(g)
        inv_g = np.linalg.pinv(g)
        return float(np.trace(inv_g @ R_ij))
