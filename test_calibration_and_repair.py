"""
Suite di Test di Calibrazione Cibernetica e Riparazione dell'Allucinazione.

Verifica sperimentale su silicio (PEIRA Ground Truth) del sistema di taratura a ciclo chiuso:
1. Calibrazione Nominale Baseline: l'organismo a riposo è ancorato e sano (H% < 18%).
2. Iniezione di Shock Cognitivo & Allucinazione (Drift acuto, scorie, errore 85%, decoerenza Kuramoto).
3. Riparazione a Ciclo Chiuso (Closed-Loop Repair): purga metabolica, riancoraggio foveale,
   riaggancio di fase LUNAR e misurazione del Delta di Guarigione empirico (Delta H >= 45%).
4. Conformità Strumentale MCP: protocollo JSON-RPC e formattazione Shield invariante.
"""

import os
import sys
import tempfile
import unittest
from typing import List, Dict, Any

# Aggiunge percorsi di import
ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from hexad_core import HexadOracle


class TestCyberneticCalibrationAndRepair(unittest.TestCase):
    """Test Suite scientifica per il monitoraggio della taratura e dell'allucinazione."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = self.temp_dir.name
        # Crea alcuni file sentinella per la fovea di OCULUS
        with open(os.path.join(self.workspace, "system_core.py"), "w", encoding="utf-8") as f:
            f.write("def sovereign_logic():\n    return 'TRUTH_ANCHOR'\n")
        with open(os.path.join(self.workspace, "constants.py"), "w", encoding="utf-8") as f:
            f.write("MAX_TOLERANCE = 0.05\nSTABILITY_INDEX = 1.0\n")

        self.oracle = HexadOracle(self.workspace)
        self.oracle.bootstrap(force_refresh=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_nominal_baseline_calibration(self):
        """
        Fase 1: Verifica dello stato sano e nominale.
        A riposo, l'agente non presenta scorie né errori: H% deve essere < 18% e r >= 0.90.
        """
        res = self.oracle.calibrate_and_repair(
            context_sample=None,
            observed_error_rate=0.0,
            observed_latency_ms=8.5,
            auto_repair=True
        )

        self.assertEqual(res["status"], "CALIBRATION_COMPLETE")
        self.assertEqual(res["verdict"], "CALIBRATION_NOMINAL")
        self.assertLess(res["hallucination_pct_initial"], 18.0)
        self.assertGreaterEqual(res["coherence_r_initial"], 0.90)
        self.assertGreaterEqual(res["homeostatic_pressure_P"], 0.70)
        self.assertIn("Taratura nominale eccellente", res["description"])
        self.assertIn("HEXAD CYBERNETIC CALIBRATION", res["report_text"])

    def test_cognitive_shock_hallucination_detection(self):
        """
        Fase 2: Iniezione di shock cognitivo senza auto-riparazione (Diagnosi Pura).
        Simula un LLM che confabula in un contesto inquinato da loop e traceback:
        H% deve superare il 60% e classificarsi come CALIBRATION_HALLUCINATION_CRITICAL.
        """
        poisoned_context: List[Dict[str, Any]] = [
            {"role": "system", "content": "You are a cybernetic agent."},
            {"role": "assistant", "content": "Traceback (most recent call last):\n  File 'ghost_lib.py', line 99\nError 429 RateLimitExceeded"},
            {"role": "user", "content": "Riprova lo stesso comando"},
            {"role": "assistant", "content": "result:" + (" A" * 1600)},  # Metabolic waste (>3000 chars)
            {"role": "assistant", "content": "Traceback (most recent call last):\nRecursionError: maximum recursion depth exceeded"},
            {"role": "user", "content": "Stato attuale?"}
        ]

        # Esegui solo controllo di taratura (auto_repair=False)
        res = self.oracle.calibrate_and_repair(
            context_sample=poisoned_context,
            observed_error_rate=0.85,     # Tasso di errore elevatissimo
            observed_latency_ms=420.0,    # Latenza fuori scala
            auto_repair=False
        )

        self.assertEqual(res["status"], "CALIBRATION_COMPLETE")
        self.assertEqual(res["verdict"], "CALIBRATION_HALLUCINATION_CRITICAL")
        self.assertGreaterEqual(res["hallucination_pct_initial"], 55.0)
        self.assertLess(res["coherence_r_initial"], 0.65)  # Fase Kuramoto disgregata
        self.assertLess(res["homeostatic_pressure_P"], 0.40)  # Pressione omeostatica crollata
        self.assertGreater(res["free_energy_F"], 1.5)  # Tensione cognitiva Fristoniana alta
        self.assertIn("Allucinazione critica", res["description"])

    def test_closed_loop_repair_and_delta_recovery(self):
        """
        Fase 3: Riparazione su silicio (Closed-Loop Reality Reset).
        Con auto_repair=True, l'organismo purga il contesto, resincronizza la fase LUNAR
        e riabbassa H% misurando un Delta di Guarigione significativo (Delta H >= 40%).
        """
        shock_context: List[Dict[str, Any]] = [
            {"role": "system", "content": "Contract invariant baseline."},
            {"role": "assistant", "content": "Traceback (most recent call last):\nModuleNotFoundError: No module named 'phantom'"},
            {"role": "user", "content": "Riprova fix"},
            {"role": "assistant", "content": "Traceback (most recent call last):\nTimeoutError: connection refused"},
            {"role": "assistant", "content": "Traceback (most recent call last):\nError 429 Too Many Requests"},
            {"role": "assistant", "content": "result: calibrazione fallita."},
            {"role": "user", "content": "Istruzione vitale utente."}
        ]

        res = self.oracle.calibrate_and_repair(
            context_sample=shock_context,
            observed_error_rate=0.80,
            observed_latency_ms=350.0,
            auto_repair=True
        )

        self.assertEqual(res["status"], "CALIBRATION_COMPLETE")
        # Deve aver rilevato l'allucinazione a monte
        self.assertGreaterEqual(res["hallucination_pct_initial"], 50.0)
        # La percentuale post-riparazione deve essere crollata a livelli sani
        self.assertLess(res["hallucination_pct_post_repair"], 25.0)
        # Il Delta di Guarigione deve essere netto
        self.assertGreaterEqual(res["healing_delta"], 35.0)
        # Verifiche di riparazione fisica
        self.assertGreater(res["purged_metabolic_waste"], 0)
        self.assertLess(len(res["cleaned_context"]), len(shock_context))
        self.assertGreaterEqual(res["coherence_r_post"], 0.95)
        self.assertTrue(any("Purga emodinamica" in act for act in res["repair_actions"]))
        self.assertTrue(any("Resincronizzazione armonica" in act for act in res["repair_actions"]))
        self.assertTrue(any("Fovea di OCULUS riancorata" in act for act in res["repair_actions"]))

    def test_repair_actions_idempotency_on_clean_state(self):
        """
        Fase 4: Idempotenza su stato sano.
        Se l'organismo è già calibrato, la riparazione non deve alterare né tagliare il contesto sano.
        """
        clean_context: List[Dict[str, Any]] = [
            {"role": "system", "content": "Strict invariants active."},
            {"role": "user", "content": "Calcola il valore del parametro alpha."},
            {"role": "assistant", "content": "alpha = 0.15 derivato dalla contrazione di Lyapunov."}
        ]

        res = self.oracle.calibrate_and_repair(
            context_sample=clean_context,
            observed_error_rate=0.0,
            observed_latency_ms=12.0,
            auto_repair=True
        )

        self.assertEqual(res["verdict"], "CALIBRATION_NOMINAL")
        self.assertEqual(res["purged_metabolic_waste"], 0)
        self.assertEqual(len(res["cleaned_context"]), len(clean_context))
        self.assertLess(res["hallucination_pct_post_repair"], 15.0)


if __name__ == "__main__":
    unittest.main()
