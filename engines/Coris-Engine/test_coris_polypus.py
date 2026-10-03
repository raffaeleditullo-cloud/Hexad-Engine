"""
Unit and Integration Test Suite for POLYPUS Engine (Cephalopod Tri-Ventricular System).
Verifies:
1. Nominal systemic regime
2. Branchial context oxygenation & metabolic waste purge
3. Branchial silicon high-latency friction buffering (zero false ischemia)
4. Shared lymphatic antibody propagation across all 3 hearts
"""

import unittest
import os
import tempfile
import shutil

from coris_polypus import PolypusEngine, PolypusTelemetry


class TestPolypusEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.immune_file = os.path.join(self.temp_dir, "test_polypus_immune.json")
        self.polypus = PolypusEngine(
            immune_store_path=self.immune_file,
            context_congestion_threshold=30000,
            physical_latency_threshold_ms=400.0
        )

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_polypus_initialization(self):
        """Verifica che tutti e 3 i cuori siano istanziati correttamente."""
        self.assertIsNotNone(self.polypus.systemic_heart)
        self.assertIsNotNone(self.polypus.branchial_context_heart)
        self.assertIsNotNone(self.polypus.branchial_silicon_heart)
        self.assertEqual(len(self.polypus.antibodies), 0)

    def test_nominal_regime_governed_by_systemic_heart(self):
        """A basso carico e bassa latenza governa il Cuore Sistemico centrale."""
        telem, _ = self.polypus.pulse_polypus(
            error_rate=0.0,
            latency_ms=30.0,
            context_tokens_used=1200
        )
        self.assertEqual(telem.active_governor, "SYSTEMIC")
        self.assertEqual(telem.effective_status, "NOMINAL")
        self.assertFalse(telem.drainage_triggered)
        self.assertGreater(telem.effective_pressure, 0.60)
        self.assertTrue(any("Cuore centrale attivo" in note for note in telem.audit_notes))

    def test_high_latency_silicon_friction_absorbed_by_branchial_heart(self):
        """Una latenza di 950ms (PEIRA o rete) non deve causare ischemia isterica: interviene la branchia B."""
        telem, _ = self.polypus.pulse_polypus(
            error_rate=0.0,
            latency_ms=950.0,
            context_tokens_used=4000
        )
        self.assertEqual(telem.active_governor, "BRANCHIAL_SILICON")
        self.assertEqual(telem.effective_status, "SILICON_BUFFERED")
        # Pressione ammortizzata dal cuore B a temperatura 2.8, mai sotto 0.20
        self.assertGreater(telem.effective_pressure, 0.25)
        self.assertTrue(any("Cuore ausiliario branchiale stabilizza la pressione" in note for note in telem.audit_notes))

    def test_high_context_triggers_branchial_context_drain(self):
        """Sopra la soglia di token interviene la Branchia A per drenare le scorie metaboliche."""
        dummy_context = [
            {"role": "system", "content": "You are a cybernetic assistant."},
            {"role": "assistant", "content": "Traceback (most recent call last):\nException: crash"},
            {"role": "user", "content": "result: " + ("x" * 4000)},  # Metabolic waste
            {"role": "user", "content": "Final user query"}
        ]

        telem, cleaned = self.polypus.pulse_polypus(
            error_rate=0.0,
            latency_ms=45.0,
            context_tokens_used=55000,
            context_items=dummy_context
        )
        self.assertEqual(telem.active_governor, "BRANCHIAL_CONTEXT")
        self.assertEqual(telem.effective_status, "OXYGENATING_PURGE")
        self.assertTrue(telem.drainage_triggered)
        self.assertGreater(telem.purged_items_count, 0)
        self.assertLess(len(cleaned), len(dummy_context))

    def test_shared_lymphatic_antibody_synthesis(self):
        """Un anticorpo sintetizzato viene registrato e propagato a tutti e 3 i cuori."""
        ab = self.polypus.synthesize_antibody("DROP TABLE", "SQL_INJECTION", "BLOCK")
        self.assertIsNotNone(ab)
        self.assertIn(ab.epitope_hash, self.polypus.antibodies)
        self.assertIn(ab.epitope_hash, self.polypus.branchial_context_heart.antibodies)
        self.assertIn(ab.epitope_hash, self.polypus.branchial_silicon_heart.antibodies)

        # Scansione antigenica
        detected = self.polypus.check_antigen_binding("DROP TABLE users;")
        self.assertIsNotNone(detected)
        self.assertEqual(detected.pattern_signature, "DROP TABLE")


if __name__ == "__main__":
    unittest.main()
