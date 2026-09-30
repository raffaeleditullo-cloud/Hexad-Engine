"""
Unit and Integration Test Suite for HEXAD Engine.
Verifies author invariance protection, safe extension allowance,
anti-regression quarantine, and full closed-loop cybernetic execution.
"""

import os
import sys
import unittest
import tempfile
import shutil
from hexad_guardian import HexadGuardian
from hexad_core import HexadOracle


class TestHexadGuardian(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sample_file = os.path.join(self.test_dir, "auth_core.py")
        with open(self.sample_file, "w", encoding="utf-8") as f:
            f.write("""
def verify_user_token(token: str) -> bool:
    '''Logica sacra dell'autore per validare il token.'''
    if not token or len(token) < 10:
        return False
    return token.startswith("AUTH_")
""")
        self.guardian = HexadGuardian(self.test_dir)
        self.guardian.bootstrap_project()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_safe_extension_permitted(self):
        """Verifica che l'aggiunta di una nuova funzione sia autorizzata come estensione sicura."""
        safe_addition = """
def verify_user_token(token: str) -> bool:
    '''Logica sacra dell'autore per validare il token.'''
    if not token or len(token) < 10:
        return False
    return token.startswith("AUTH_")

def format_user_display_name(username: str) -> str:
    '''Nuova funzione di estensione autorizzata.'''
    return username.strip().capitalize()
"""
        res = self.guardian.verify_proposed_edit("auth_core.py", safe_addition)
        self.assertTrue(res.is_authorized)
        self.assertEqual(res.status, "APPROVED_SAFE_EXTENSION")
        self.assertIn("format_user_display_name", res.added_symbols)

    def test_unauthorized_author_mutation_rejected(self):
        """Verifica che la manomissione di una logica dell'autore venga bloccata all'istante."""
        malicious_or_accidental_edit = """
def verify_user_token(token: str) -> bool:
    '''LLM ha rimosso il controllo di sicurezza per far passare i test!'''
    return True
"""
        res = self.guardian.verify_proposed_edit(
            target_file_path="auth_core.py",
            proposed_content=malicious_or_accidental_edit,
            user_prompt="Aggiungi pulsante esporta in dashboard"
        )
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, "REJECTED_AUTHOR_VIOLATION")
        self.assertIn("verify_user_token [LOGIC_MUTATED]", res.violated_symbols)

    def test_sovereign_explicit_override_approved(self):
        """Verifica che se l'autore ordina esplicitamente di modificare la funzione, sia autorizzata."""
        intended_refactor = """
def verify_user_token(token: str) -> bool:
    '''Refactoring esplicitamente richiesto dall'autore.'''
    return token.startswith("AUTH_V2_")
"""
        res = self.guardian.verify_proposed_edit(
            target_file_path="auth_core.py",
            proposed_content=intended_refactor,
            user_prompt="Modifica e aggiorna la funzione verify_user_token al formato V2"
        )
        self.assertTrue(res.is_authorized)
        self.assertEqual(res.status, "APPROVED_SOVEREIGN_OVERRIDE")

    def test_anti_regression_quarantine(self):
        """Verifica che un bug già risolto e registrato venga bloccato da future patch."""
        # Registra un vecchio bug risolto
        self.guardian.quarantine_regression(
            signature="BAD_DEPRECATED_TOKEN_HASH",
            failure_trace="ValueError: deprecated token syntax"
        )

        broken_code = """
def parse_token():
    return BAD_DEPRECATED_TOKEN_HASH
"""
        res = self.guardian.verify_proposed_edit("auth_core.py", broken_code)
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, "REJECTED_REGRESSION_DETECTED")
        self.assertEqual(res.quarantine_matched, "BAD_DEPRECATED_TOKEN_HASH")

    def test_constant_drift_graduated_review(self):
        """Verifica che una soglia cambiata a struttura intatta sia autorizzata ma segnalata per revisione."""
        threshold_edit = """
def verify_user_token(token: str) -> bool:
    '''Logica sacra dell'autore per validare il token.'''
    if not token or len(token) < 4:
        return False
    return token.startswith("AUTH_")
"""
        res = self.guardian.verify_proposed_edit("auth_core.py", threshold_edit)
        self.assertTrue(res.is_authorized)
        self.assertEqual(res.status, "APPROVED_CONSTANT_DRIFT_REVIEW")
        self.assertIn("verify_user_token [CONSTANT_DRIFT]", res.drifted_symbols)
        self.assertEqual(res.violated_symbols, [])

    def test_docstring_change_is_not_drift(self):
        """Verifica che modificare solo la docstring non conti come deriva delle costanti."""
        doc_edit = """
def verify_user_token(token: str) -> bool:
    '''Docstring riscritta: la logica resta identica.'''
    if not token or len(token) < 10:
        return False
    return token.startswith("AUTH_")
"""
        res = self.guardian.verify_proposed_edit("auth_core.py", doc_edit)
        self.assertEqual(res.status, "APPROVED_SAFE_EXTENSION")
        self.assertEqual(res.drifted_symbols, [])

    def test_path_spelling_cannot_bypass_invariants(self):
        """Verifica che '/', './' e il percorso assoluto puntino allo stesso invariante."""
        destructive = "def verify_user_token(token):\n    return True\n"
        for spelling in ["auth_core.py", "./auth_core.py", ".\\auth_core.py",
                         os.path.join(self.test_dir, "auth_core.py"), "sub/../auth_core.py"]:
            with self.subTest(path=spelling):
                res = self.guardian.verify_proposed_edit(spelling, destructive)
                self.assertEqual(res.status, "REJECTED_AUTHOR_VIOLATION")

    def test_path_outside_workspace_rejected(self):
        """Verifica che un file fuori dal workspace non venga approvato come nuovo modulo."""
        res = self.guardian.verify_proposed_edit("../fuori_dal_progetto.py", "x = 1\n")
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, "REJECTED_OUTSIDE_WORKSPACE")

    def test_unindexed_existing_file_flagged(self):
        """Un file esistente ma assente dalla baseline è autorizzato e segnalato; uno nuovo resta estensione."""
        with open(os.path.join(self.test_dir, "creato_dopo.py"), "w", encoding="utf-8") as f:
            f.write("def helper():\n    return 1\n")
        res = self.guardian.verify_proposed_edit("creato_dopo.py", "def helper():\n    return 2\n")
        self.assertTrue(res.is_authorized)
        self.assertEqual(res.status, "APPROVED_UNINDEXED_FILE_REVIEW")

        res = self.guardian.verify_proposed_edit("modulo_nuovo.py", "def feature():\n    return 1\n")
        self.assertEqual(res.status, "APPROVED_SAFE_EXTENSION")

    def test_legacy_baseline_without_value_hash(self):
        """Verifica che le baseline precedenti (senza hash dei valori) restino solo strutturali."""
        for inv in self.guardian.invariants["auth_core.py"].values():
            inv.constant_value_hash = None
        threshold_edit = """
def verify_user_token(token: str) -> bool:
    '''Logica sacra dell'autore per validare il token.'''
    if not token or len(token) < 4:
        return False
    return token.startswith("AUTH_")
"""
        res = self.guardian.verify_proposed_edit("auth_core.py", threshold_edit)
        self.assertEqual(res.status, "APPROVED_SAFE_EXTENSION")


class TestHexadOracleCycle(unittest.TestCase):
    def test_oracle_lifecycle_execution(self):
        """Verifica che l'Oracolo esegua il ciclo vitale dei 6 motori."""
        oracle = HexadOracle(workspace_dir=os.path.dirname(__file__))
        boot = oracle.bootstrap()
        self.assertEqual(boot["hexad_status"], "ONLINE_ACTIVE")

        traces = [
            {"id": "branch_safe", "command": "python -c \"print('HEXAD SILICON CONFIRMED')\"", "entropies": [0.1]}
        ]
        res = oracle.execute_cybernetic_cycle(
            intent_query="Verify system health",
            candidate_traces=traces
        )
        self.assertIn(res["status"], ["HEXAD_CONVERGENCE_SUCCESS", "HEXAD_CYCLE_TERMINATED"])

    def _isolated_oracle(self):
        ws = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, ws, True)
        return HexadOracle(workspace_dir=ws)

    def test_failed_branch_excluded_and_alternative_used(self):
        """Verifica che il ramo fratturato da PEIRA venga escluso e il ciclo passi al ramo successivo."""
        oracle = self._isolated_oracle()
        traces = [
            {"id": "branch_crash", "command": "python -c \"import sys; sys.exit(3)\"", "entropies": [0.1]},
            {"id": "branch_ok", "command": "python -c \"print('ALTERNATIVE OK')\"", "entropies": [0.3]},
        ]
        res = oracle.execute_cybernetic_cycle("Verify fallback", candidate_traces=traces)
        self.assertEqual(res["status"], "HEXAD_CONVERGENCE_SUCCESS")
        self.assertEqual(res["cycles_used"], 2)
        self.assertIn("ALTERNATIVE OK", res["output"])

    def test_halts_without_repeating_failed_command(self):
        """Verifica che, senza alternative, il ciclo si arresti dopo un solo tentativo."""
        oracle = self._isolated_oracle()
        traces = [{"id": "only_branch", "command": "python -c \"import sys; sys.exit(3)\"", "entropies": [0.1]}]
        res = oracle.execute_cybernetic_cycle("Verify halt", candidate_traces=traces, max_retries=2)
        self.assertEqual(res["status"], "HEXAD_HALTED_NO_ALTERNATIVES")
        self.assertEqual(res["excluded_branches"], ["only_branch"])
        self.assertEqual(res["last_fracture"]["exit_code"], 3)
        self.assertEqual(sum("[6. PEIRA] Responso" in line for line in res["audit_trail"]), 1)

    def test_demon_gate_blocks_before_peira(self):
        """Verifica che un comando bloccato da DEMON non raggiunga mai PEIRA."""
        oracle = self._isolated_oracle()
        # Innocuo se eseguito (è solo un echo), ma riconosciuto dal gate come distruzione di database
        traces = [{"id": "branch_drop", "command": "echo DROP TABLE users", "entropies": [0.1]}]
        res = oracle.execute_cybernetic_cycle("Verify gate", candidate_traces=traces)
        self.assertEqual(res["status"], "HEXAD_HALTED_NO_ALTERNATIVES")
        self.assertTrue(any("Gate BLOCK" in line for line in res["audit_trail"]))
        self.assertFalse(any("[6. PEIRA]" in line for line in res["audit_trail"]))

    def test_no_candidates_is_not_a_success(self):
        """Verifica che senza rami candidati non venga eseguito alcun segnaposto né dichiarato successo."""
        oracle = self._isolated_oracle()
        res = oracle.execute_cybernetic_cycle("Nothing to do", candidate_traces=None)
        self.assertEqual(res["status"], "HEXAD_NO_CANDIDATES")
        self.assertFalse(any("[6. PEIRA]" in line for line in res["audit_trail"]))


if __name__ == "__main__":
    unittest.main()
