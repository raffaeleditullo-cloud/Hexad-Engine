import tempfile
import os
import json
from hexad_guardian import HexadGuardian
from hexad_core import HexadOracle

def run_tests():
    with tempfile.TemporaryDirectory() as td:
        # 1. Test Fail-Closed su corruzione baseline
        hexad_dir = os.path.join(td, ".hexad")
        os.makedirs(hexad_dir, exist_ok=True)
        with open(os.path.join(hexad_dir, "invariants.json"), "w", encoding="utf-8") as f:
            f.write("{ CORRUPTED JSON !!!")

        g = HexadGuardian(td)
        assert g.integrity_status == "INTEGRITY_FAILURE", f"Expected INTEGRITY_FAILURE, got {g.integrity_status}"
        res = g.verify_proposed_edit("test.py", "x = 1")
        assert res.is_authorized is False
        assert res.status == "REJECTED_INTEGRITY_FAILURE"
        print("[OK] Test 1: Fail-Closed Integrity Failure passed!")

        # 2. Test force_refresh reset
        boot = g.bootstrap_project(force_refresh=True)
        assert g.integrity_status == "READY"
        assert boot["status"] == "BOOTSTRAP_COMPLETE"
        print("[OK] Test 2: force_refresh baseline recovery passed!")

        # 3. Test Critical Constant Drift vs Config Constant Drift
        test_file = os.path.join(td, "sample.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("MAX_RETRIES = 3\nUI_THEME = 'dark'\ndef run():\n    return 42\n")
        
        g.bootstrap_project(force_refresh=True)
        
        # Proponi mutazione di MAX_RETRIES (Critical Security/Control Constant)
        critical_mod = "MAX_RETRIES = 99999\nUI_THEME = 'dark'\ndef run():\n    return 42\n"
        crit_res = g.verify_proposed_edit("sample.py", critical_mod)
        assert crit_res.is_authorized is False, f"Critical drift must be blocked, got {crit_res}"
        assert crit_res.status == "REJECTED_CRITICAL_CONSTANT_DRIFT"
        print("[OK] Test 3A: Critical Constant Drift (MAX_RETRIES) blocked!")

        # Proponi mutazione di UI_THEME (Config Constant)
        config_mod = "MAX_RETRIES = 3\nUI_THEME = 'light'\ndef run():\n    return 42\n"
        conf_res = g.verify_proposed_edit("sample.py", config_mod)
        assert conf_res.is_authorized is True, f"Config drift must be authorized with review, got {conf_res}"
        assert conf_res.status == "APPROVED_CONSTANT_DRIFT_REVIEW"
        print("[OK] Test 3B: Config Constant Drift (UI_THEME) allowed with review!")

        # 4. Test Oracle dynamic aggregated status & force_refresh
        oracle = HexadOracle(td)
        o_boot = oracle.bootstrap(force_refresh=True)
        assert "core_engines_ratio" in o_boot
        print(f"[OK] Test 4: Dynamic status = {o_boot['hexad_status']}, Ratio = {o_boot['core_engines_ratio']}")
        print("ALL AUDIT FIXES VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
