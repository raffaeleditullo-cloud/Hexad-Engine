"""
Unit and Integration Test Suite for MNEME Engine.
Verifies Lyapunov stability conditions, Jacobian eigenvalue spectrum,
Ricci flow metric deformation, and topological attractor memory.
"""

import unittest
import numpy as np
from mneme_engine import MnemeEngine, StabilityCertificate, RicciFlowResult


class TestMnemeEngine(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)  # seed fisso: rende deterministici i test con perturbazione epsilon
        self.engine = MnemeEngine(state_dim=5, alpha=0.1)

    def test_stable_contractive_trajectory(self):
        """Testa una traiettoria contrattiva ideale verso l'equilibrio x* = 0."""
        state = [0.5, 0.2, 0.1, 0.05, 0.0]
        # Campo di velocità fortemente dissipativo: f(x) = -1.2 * x
        velocity = [-0.6, -0.24, -0.12, -0.06, 0.0]
        
        cert = self.engine.certify_trajectory_stability(
            current_state=state,
            velocity_vector=velocity
        )
        self.assertTrue(cert.is_stable)
        self.assertLess(cert.v_dot, 0.0)
        self.assertGreaterEqual(cert.alpha_decay_margin, -1e-5)
        self.assertLess(cert.max_real_eigenvalue, 0.0)

    def test_divergent_trajectory_rejection(self):
        """Testa il rigetto immediato di una traiettoria con dV/dt > 0 o autovalore instabile."""
        state = [1.0, 1.0, 0.5, 0.2, 0.1]
        # Campo divergente che spinge lontano dall'origine: f(x) = +0.5 * x
        divergent_velocity = [0.5, 0.5, 0.25, 0.1, 0.05]
        
        cert = self.engine.certify_trajectory_stability(
            current_state=state,
            velocity_vector=divergent_velocity
        )
        self.assertFalse(cert.is_stable)
        self.assertGreaterEqual(cert.v_dot, 0.0)
        self.assertIsNotNone(cert.rejection_reason)
        self.assertIn("DIVERGENZA DINAMICA", cert.rejection_reason)

    def test_unstable_jacobian_eigenvalue(self):
        """Testa il rigetto quando un autovalore ha parte reale positiva (modo di instabilità locale)."""
        state = [0.5, 0.5, 0.0, 0.0, 0.0]
        velocity = [-0.2, -0.2, 0.0, 0.0, 0.0]
        # Jacobiano con un autovalore positivo (es. sella o instabilità su asse 3)
        bad_jacobian = [
            [-0.5, 0.0, 0.0, 0.0, 0.0],
            [0.0, -0.4, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.8, 0.0, 0.0],  # Modo instabile lambda = +0.8
            [0.0, 0.0, 0.0, -0.3, 0.0],
            [0.0, 0.0, 0.0, 0.0, -0.2]
        ]
        cert = self.engine.certify_trajectory_stability(
            current_state=state,
            velocity_vector=velocity,
            jacobian_matrix=bad_jacobian
        )
        self.assertFalse(cert.is_stable)
        self.assertGreaterEqual(cert.max_real_eigenvalue, 0.0)
        self.assertIn("MODO DIVERGENTE RILEVATO", cert.rejection_reason)

    def test_ricci_curvature_flow(self):
        """Verifica la deformazione del flusso di Ricci e la regolarizzazione della metrica."""
        # Metrica iniziale fortemente distorta
        distorted_metric = [
            [3.0, 0.8, 0.1],
            [0.8, 2.0, 0.5],
            [0.1, 0.5, 1.2]
        ]
        res = self.engine.apply_ricci_curvature_flow(base_metric=distorted_metric, iterations=10, dt_step=0.04)
        
        self.assertIsInstance(res, RicciFlowResult)
        # La metrica deve rimanere simmetrica e definita positiva
        smoothed = np.array(res.smoothed_metric)
        eigvals = np.linalg.eigvalsh(smoothed)
        self.assertTrue(np.all(eigvals > 0), "Smoothed metric must be strictly positive definite")

    def test_topological_attractor_memory(self):
        """Testa la registrazione di attrattori stabili e il riconoscimento del bacino."""
        attractor = self.engine.register_stable_attractor(
            state_id="TASK_COMPLETION_EQUILIBRIUM",
            equilibrium_coords=[0.0, 0.0, 0.0, 0.0, 0.0],
            basin_radius=0.8,
            metadata={"objective": "SWE-bench fix applied"}
        )
        self.assertEqual(attractor.state_id, "TASK_COMPLETION_EQUILIBRIUM")
        
        # Stato dentro il bacino
        close_state = [0.2, 0.1, 0.0, 0.1, 0.0]
        match = self.engine.check_basin_membership(close_state)
        self.assertIsNotNone(match)
        self.assertEqual(match[0], "TASK_COMPLETION_EQUILIBRIUM")
        self.assertLessEqual(match[1], 0.8)

        # Stato fuori dal bacino
        far_state = [2.5, 3.0, 1.0, 0.0, 0.0]
        match_far = self.engine.check_basin_membership(far_state)
        self.assertIsNone(match_far)


if __name__ == "__main__":
    unittest.main()
