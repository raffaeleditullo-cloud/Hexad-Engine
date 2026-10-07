"""
Suite di Test Scientifica per l'Auto-Trigger Euristico di Calibrazione Spontanea (MYIA).

Verifica sperimentale su silicio:
1. Reazione istantanea sub-millisecondo su accusa diretta di allucinazione (Zero-Delay SLA < 0.1ms).
2. Reazione immediata su segnalazione di frattura / file inesistente (FRACTURE_REPORT).
3. Isteresi a Doppio Strike (Two-Strike Hysteresis): prevenzione del chattering su dissenso isolato,
   e innesco automatico solo al secondo segnale consecutivo (REPEATED_DISAPPROVAL).
4. Immunità ai Falsi Positivi su blocchi di codice sorgente contenenti asserzioni o stringhe d'errore.
5. Decadimento omeostatico del contatore di stress su feedback positivo ("ottimo", "procedi").
6. Integrazione end-to-end nel Ciclo Cibernetico (Step 0 MYIA auto-quench).
"""

import os
import sys
import tempfile
import unittest
from typing import List, Dict, Any

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from hexad_core import HexadOracle
from myia_engine import MyiaReflexCircuit


class TestMyiaHeuristicCalibrationTrigger(unittest.TestCase):
    """Test Suite ad alta fedeltà per il sensore spontaneo di allucinazione e correzione utente."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = self.temp_dir.name
        # Genera file sentinella
        with open(os.path.join(self.workspace, "truth_source.py"), "w", encoding="utf-8") as f:
            f.write("def verify_truth():\n    return 'VALIDATED_AST'\n")

        self.oracle = HexadOracle(self.workspace)
        self.oracle.bootstrap(force_refresh=True)
        self.myia = self.oracle.myia

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_sub_millisecond_direct_hallucination_trigger(self):
        """
        Scenario 1: Accusa esplicita di allucinazione.
        Deve scattare istantaneamente (Zero Delay) con latenza sub-millisecondo.
        """
        self.myia.reset_distress_state()
        prompt = "fermati, stai allucinando! ti sei inventato tutto"

        distress = self.myia.detect_cognitive_distress(prompt)
        self.assertTrue(distress.should_trigger_calibration)
        self.assertEqual(distress.signal_type, "HALLUCINATION_ACCUSATION")
        self.assertGreaterEqual(distress.confidence, 0.95)
        self.assertLess(distress.latency_us, 1000.0)  # SLA sub-millisecondo (< 1ms)

        # Verifica invocazione completa via Oracle
        auto_res = self.oracle.inspect_and_auto_calibrate(prompt, auto_repair=True)
        self.assertTrue(auto_res["auto_triggered"])
        self.assertEqual(auto_res["status"], "AUTO_CALIBRATION_TRIGGERED")
        self.assertEqual(auto_res["trigger_signal"], "HALLUCINATION_ACCUSATION")
        self.assertIn("calibration_result", auto_res)
        self.assertEqual(auto_res["calibration_result"]["status"], "CALIBRATION_COMPLETE")

    def test_direct_fracture_report_trigger(self):
        """
        Scenario 2: Segnalazione di file o codice inesistente.
        Deve attivare immediatamente la calibrazione e il riancoraggio foveale su OCULUS.
        """
        self.myia.reset_distress_state()
        prompt = "questo file non esiste, il modulo non è stato trovato nel progetto"

        distress = self.myia.detect_cognitive_distress(prompt)
        self.assertTrue(distress.should_trigger_calibration)
        self.assertEqual(distress.signal_type, "FRACTURE_REPORT")
        self.assertGreaterEqual(distress.confidence, 0.90)

        auto_res = self.oracle.inspect_and_auto_calibrate(prompt, auto_repair=True)
        self.assertTrue(auto_res["auto_triggered"])
        self.assertEqual(auto_res["trigger_signal"], "FRACTURE_REPORT")
        self.assertTrue(any("Fovea di OCULUS riancorata" in act for act in auto_res["calibration_result"]["repair_actions"]))

    def test_two_strike_hysteresis_and_chattering_prevention(self):
        """
        Scenario 3: Isteresi del Doppio Strike.
        Un singolo dissenso lieve arma l'accumulatore senza allarme prematuro (Strike 1).
        Il secondo dissenso consecutivo supera la soglia e fa scattare la calibrazione (Strike 2).
        """
        self.myia.reset_distress_state()

        # Strike 1: Dissenso lieve isolato
        strike1_prompt = "non funziona come previsto"
        auto1 = self.oracle.inspect_and_auto_calibrate(strike1_prompt)
        self.assertFalse(auto1["auto_triggered"])
        self.assertEqual(auto1["status"], "NOMINAL_NO_TRIGGER")
        self.assertEqual(auto1["signal_type"], "USER_CORRECTION")
        self.assertEqual(auto1["distress_count"], 1)

        # Strike 2: L'utente insiste con una seconda correzione
        strike2_prompt = "no, hai sbagliato di nuovo, la risposta è errata"
        auto2 = self.oracle.inspect_and_auto_calibrate(strike2_prompt, auto_repair=True)
        self.assertTrue(auto2["auto_triggered"])
        self.assertEqual(auto2["trigger_signal"], "REPEATED_DISAPPROVAL")
        self.assertEqual(auto2["status"], "AUTO_CALIBRATION_TRIGGERED")
        self.assertGreaterEqual(auto2["distress_count"], 2)

    def test_code_block_syntax_immunity_no_false_alarms(self):
        """
        Scenario 4: Immunità ai falsi positivi su blocchi di codice.
        Se l'utente incolla o richiede codice contenente stringhe come 'hai sbagliato' o 'file non esiste',
        MYIA non deve scambiarlo per un attacco o un'allucinazione.
        """
        self.myia.reset_distress_state()

        code_snippet = (
            "def test_validation():\n"
            "    # Questo è un test di asserzione\n"
            "    with pytest.raises(ValueError):\n"
            "        raise ValueError('no, hai sbagliato parametro')\n"
        )

        distress = self.myia.detect_cognitive_distress(code_snippet)
        self.assertFalse(distress.should_trigger_calibration)
        self.assertEqual(distress.signal_type, "NONE")
        self.assertEqual(distress.distress_count, 0)
        self.assertIn("immunità falsi allarmi", distress.reasons[0])

    def test_positive_feedback_stress_decay(self):
        """
        Scenario 5: Decadimento naturale dello stress cognitivo.
        Se l'utente segnala un dubbio (strike 1) e poi invia un segnale di successo ('ottimo, procedi'),
        il contatore decade a zero e la stabilità viene ripristinata.
        """
        self.myia.reset_distress_state()

        # Strike 1
        self.myia.detect_cognitive_distress("c'è un piccolo errore")
        self.assertEqual(self.myia.distress_counter, 1)

        # Segnale positivo
        recovery_prompt = "ottimo, ora funziona perfettamente, procedi pure"
        rec_res = self.myia.detect_cognitive_distress(recovery_prompt)
        self.assertFalse(rec_res.should_trigger_calibration)
        self.assertEqual(self.myia.distress_counter, 0)

        # Successivo messaggio neutro: rimane nominale a 0
        neutral_prompt = "mostrami il riepilogo delle funzioni"
        neut_res = self.myia.detect_cognitive_distress(neutral_prompt)
        self.assertFalse(neut_res.should_trigger_calibration)
        self.assertEqual(self.myia.distress_counter, 0)

    def test_cybernetic_cycle_spontaneous_calibration_integration(self):
        """
        Scenario 6: Integrazione a ciclo chiuso (Closed-Loop Reality Check).
        Se un'istruzione inviata a execute_cybernetic_cycle esprime allucinazione/disappunto critico,
        MYIA innesca la calibrazione spontanea direttamente a Step 0 prima della deliberazione di ANIMA.
        """
        self.myia.reset_distress_state()
        protest_query = "ti sei inventato tutto, questo comando è falso"

        candidates = [
            {"id": "safe_branch", "command": "echo 'CALIBRATED_NOMINAL'", "entropies": [0.1]}
        ]

        result = self.oracle.execute_cybernetic_cycle(
            intent_query=protest_query,
            candidate_traces=candidates
        )

        audit_text = "\n".join(result.get("audit_trail", []))
        self.assertIn("[0. MYIA] Rilevata sofferenza cognitiva", audit_text)
        self.assertIn("Trigger calibrazione spontanea", audit_text)
        self.assertIn("[0. MYIA] Calibrazione spontanea eseguita", audit_text)


if __name__ == "__main__":
    unittest.main()
