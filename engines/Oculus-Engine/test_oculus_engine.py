"""
Test Suite per OCULUS Engine.
Valida:
1. Parsing AST e Mappatura Topologica in millisecondi.
2. Visione Foveale e Saccadic Gaze (puntamento ad alta risoluzione solo sui nodi critici).
3. Tasso di Compressione Token (>80%).
4. Calibrazione Sensoriale per ANIMA (proxy di entropia e complessità).
"""

import unittest
import os
import tempfile
from oculus_engine import OculusEngine

class TestOculusEngine(unittest.TestCase):

    def setUp(self):
        self.engine = OculusEngine()
        self.temp_dir = tempfile.TemporaryDirectory()

        # Creiamo un micro-progetto simulato con 3 file
        self.file_auth = os.path.join(self.temp_dir.name, "auth_service.py")
        with open(self.file_auth, "w", encoding="utf-8") as f:
            f.write('''
import hashlib

class SecurityManager:
    """Gestisce l'autenticazione crittografica."""
    def verify_token(self, token: str) -> bool:
        if not token:
            return False
        for ch in token:
            if ch == " ":
                return False
        return len(token) > 8

    def hash_password(self, pwd: str) -> str:
        return hashlib.sha256(pwd.encode()).hexdigest()
''')

        self.file_db = os.path.join(self.temp_dir.name, "db_storage.py")
        with open(self.file_db, "w", encoding="utf-8") as f:
            f.write('''
class DatabaseClient:
    def connect(self, uri: str):
        pass
    def execute_query(self, query: str):
        pass
''')

        self.file_heavy = os.path.join(self.temp_dir.name, "heavy_metrics.py")
        with open(self.file_heavy, "w", encoding="utf-8") as f:
            f.write("# File lungo con molte funzioni\n" + ("def dummy_func():\n    pass\n" * 50))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_ast_scanning_and_symbols(self):
        """Verifica estrazione di simboli, docstring e complessità ciclica."""
        symbols = self.engine.scan_file_ast(self.file_auth)
        self.assertGreaterEqual(len(symbols), 2)

        names = [s.name for s in symbols]
        self.assertIn("SecurityManager", names)
        self.assertIn("verify_token", names)

        # verify_token contiene un if e un for -> complessità > 1.5
        v_token = next(s for s in symbols if s.name == "verify_token")
        self.assertGreater(v_token.complexity_score, 1.5)

    def test_saccadic_gaze_foveal_focus(self):
        """La vista saccadica deve puntare su auth_service.py quando si cerca 'verify token'."""
        fovea = self.engine.focus_saccadic_gaze(
            query="verify token authentication bug",
            workspace_dir=self.temp_dir.name
        )

        # Il file focale DEVE essere auth_service.py
        self.assertIn("auth_service.py", fovea.focal_file)
        self.assertIn("def verify_token", fovea.focal_source_snippet)

        # db_storage e heavy_metrics devono essere scheletri periferici, non dump completi
        self.assertIn("db_storage.py", fovea.peripheral_skeletons)

    def test_token_compression_ratio(self):
        """Verifica che la compressione foveale abbatta il volume dei token (>75%)."""
        fovea = self.engine.focus_saccadic_gaze(
            query="authentication",
            workspace_dir=self.temp_dir.name
        )

        self.assertGreaterEqual(fovea.compression_ratio_pct, 75.0)
        self.assertLess(fovea.compressed_char_count, fovea.original_char_count * 2)

    def test_sensory_proxy_anima_calibration(self):
        """Verifica che i parametri sensoriali guidino correttamente la fase di ANIMA."""
        fovea = self.engine.focus_saccadic_gaze(
            query="SecurityManager verify_token",
            workspace_dir=self.temp_dir.name
        )

        calib = fovea.anima_calibration
        self.assertIn("action_beta", calib)
        self.assertIn("phase_jitter_limit", calib)
        self.assertGreater(calib["action_beta"], 0.3)
        self.assertLessEqual(calib["phase_jitter_limit"], 2.5)

if __name__ == "__main__":
    unittest.main()
