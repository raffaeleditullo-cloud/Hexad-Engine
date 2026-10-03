"""
Test Suite per CORIS Engine.
Valida:
1. Battito Omeostatico ed Energia Libera Variazionale (Friston Active Inference).
2. Emodinamica e Vasocostrizione (drenaggio delle scorie metaboliche del contesto).
3. Sistema Linfatico e Sintesi Anticorpale (scansione e neutralizzazione antigenica).
4. Tensore di Necrosi Tissutale e Autolisi con Rigenerazione Staminale.
"""

import unittest
import os
import shutil
import pathlib
from coris_engine import CorisEngine

class TestCorisEngine(unittest.TestCase):

    def setUp(self):
        self.test_immune_file = os.path.join(os.path.dirname(__file__), "test_immune_memory.json")
        if os.path.exists(self.test_immune_file):
            os.remove(self.test_immune_file)
        self.coris = CorisEngine(immune_store_path=self.test_immune_file)

    def tearDown(self):
        if os.path.exists(self.test_immune_file):
            os.remove(self.test_immune_file)

    def test_homeostatic_pulse_nominal_and_stress(self):
        """Verifica il battito cardiaco nominale e l'insorgenza di tachicardia sotto stress."""
        # 1. Condizioni nominali
        v_nominal = self.coris.pulse(
            error_rate=0.01,
            latency_ms=25.0,
            context_tokens_used=4000,
            context_tokens_max=128000
        )
        self.assertEqual(v_nominal.status, "NOMINAL")
        self.assertFalse(v_nominal.is_tachycardic)
        self.assertFalse(v_nominal.vasoconstriction_active)
        self.assertGreater(v_nominal.homeostatic_pressure_P, 0.6)

        # 2. Picco di stress (error rate alto, latenza 800ms, contesto quasi saturo)
        v_stress = self.coris.pulse(
            error_rate=0.85,
            latency_ms=850.0,
            context_tokens_used=115000,
            context_tokens_max=128000
        )
        self.assertTrue(v_stress.is_tachycardic)
        self.assertTrue(v_stress.vasoconstriction_active)
        self.assertIn(v_stress.status, ["ISCHEMIA", "ELEVATED_STRESS"])
        self.assertLess(v_stress.homeostatic_pressure_P, 0.25)

    def test_hemodynamic_context_drain(self):
        """Verifica che la vasocostrizione elimini i traceback e i log spuri preservando il sistema."""
        raw_context = [
            {"role": "system", "content": "You are a specialized mathematical assistant."},
            {"role": "user", "content": "Calcola il valore di x."},
            {"role": "assistant", "content": "Traceback (most recent call last):\nIndexError: pop from empty list"},
            {"role": "user", "content": "Riprova correggendo l'indice."},
            {"role": "assistant", "content": "result: " + ("0" * 3500)}, # Scoria voluminosa
            {"role": "user", "content": "Dammi il valore finale."},
            {"role": "assistant", "content": "x = 42"}
        ]

        cleaned, purged = self.coris.drain_context_hemodynamics(raw_context)

        self.assertEqual(purged, 2)
        self.assertEqual(len(cleaned), 5)
        # Il prompt di sistema e l'ultimo messaggio devono essere intatti
        self.assertEqual(cleaned[0]["role"], "system")
        self.assertEqual(cleaned[-1]["content"], "x = 42")

    def test_immune_antibody_synthesis_and_binding(self):
        """Verifica la sintesi di anticorpi e la neutralizzazione istantanea di allucinazioni/minacce."""
        # Sintetizza un anticorpo per un comando o pattern killer
        ab = self.coris.synthesize_antibody(
            pattern_signature="rm -rf /",
            source_layer="DEMON_BLAST_RADIUS",
            neutralization_rule="BLOCK_INSTANTLY_AND_RAISE_ALARM"
        )
        self.assertEqual(ab.pattern_signature, "rm -rf /")

        # Scansione immunitaria su un candidato malevolo
        candidate_bad = "Sto per eseguire: sudo rm -rf / sul server"
        match = self.coris.check_antigen_binding(candidate_bad)
        self.assertIsNotNone(match)
        self.assertEqual(match.epitope_hash, ab.epitope_hash)

        # Scansione immunitaria su un candidato pulito
        candidate_clean = "git status e lettura file di configurazione"
        no_match = self.coris.check_antigen_binding(candidate_clean)
        self.assertIsNone(no_match)

    def test_necrosis_and_phagocytosis(self):
        """Verifica il tracking della necrosi tissutale e la fagositosi rigenerativa."""
        module = "database_driver.py"

        # Accumula fallimenti consecutivi
        for _ in range(4):
            self.coris.track_tissue_necrosis(module, has_failed=True, latency_ms=1200.0)

        # Il modulo deve essere segnalato come necrotico
        vitals = self.coris.pulse(error_rate=0.1, latency_ms=100.0, context_tokens_used=5000)
        self.assertIn(module, vitals.necrotic_modules)
        self.assertEqual(vitals.status, "AUTOPHAGY")

        # Intervento di autolisi e guarigione
        heal_report = self.coris.trigger_phagocytosis_and_healing(module)
        self.assertEqual(heal_report["phagocytosis_status"], "CELL_AUTOLYSIS_COMPLETED")

        # Dopo l'intervento il modulo non è più necrotico
        vitals_post = self.coris.pulse(error_rate=0.01, latency_ms=20.0, context_tokens_used=5000)
        self.assertNotIn(module, vitals_post.necrotic_modules)

if __name__ == "__main__":
    unittest.main()
