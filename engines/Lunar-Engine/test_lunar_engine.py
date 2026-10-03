"""
Test Suite per LUNAR Engine: Verifica Sincronia di Fase, SLA < 12ms e Anti-Lobotomia.
"""

import unittest
import numpy as np
from lunar_engine import LunarEngine, LunarPhaseCertificate


class TestLunarEngine(unittest.TestCase):
    def setUp(self):
        self.engine = LunarEngine(fundamental_freq_hz=40.0, coupling_strength=8.5)

    def test_kuramoto_order_parameter(self):
        # 1. Fase identica -> r deve essere 1.0
        phases_sync = np.zeros(100)
        r_sync, _ = self.engine.compute_kuramoto_order(phases_sync)
        self.assertAlmostEqual(r_sync, 1.0, places=4)

        # 2. Fasi uniformemente distribuite -> r deve essere ~ 0.0
        phases_uniform = np.linspace(0, 2 * np.pi, 1000, endpoint=False)
        r_uniform, _ = self.engine.compute_kuramoto_order(phases_uniform)
        self.assertLess(r_uniform, 0.05)

    def test_harmonic_failover_sla_and_stability(self):
        # 256 neuroni in pieno cataclisma
        n_neurons = 256
        v_divergent = [29.8] * n_neurons
        w_divergent = [[1.8] * 5 for _ in range(n_neurons)]

        v_out, w_out, cert = self.engine.execute_harmonic_failover(
            membrane_potentials=v_divergent,
            synaptic_weights=w_divergent,
            divergent_lyapunov=4.25,
            shock_type="cataclysm"
        )

        # Verifiche formali:
        self.assertTrue(cert.is_phase_locked)
        self.assertGreaterEqual(cert.order_parameter_r, 0.95)
        self.assertLessEqual(cert.quench_latency_ms, 12.0)  # SLA < 12ms garantito
        self.assertLessEqual(cert.lyapunov_quenched, -0.65) # Profonda stabilità
        self.assertEqual(cert.synaptic_integrity_pct, 100.0) # Zero lobotomia
        self.assertEqual(len(v_out), n_neurons)
        self.assertEqual(v_out[0], -65.0)

    def test_rescue_telemetry_tracking(self):
        self.assertEqual(self.engine.state.total_rescues, 0)
        self.engine.execute_harmonic_failover([-60.0] * 64, [[0.5] * 3 for _ in range(64)], divergent_lyapunov=2.1)
        self.assertEqual(self.engine.state.total_rescues, 1)
        self.assertIsNotNone(self.engine.state.last_phase_certificate)


if __name__ == '__main__':
    unittest.main()
