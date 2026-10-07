"""
Test Suite di Verifica Integrata per tutti i Motori di HEXAD (Hexad-Engine).
Verifica:
1. Bootstrap dell'Oracolo con tutti i 14 organi cibernetici;
2. PROMETHEUS: Simulazione anticipatoria ad albero (Robert Rosen MPC);
3. CHRONOS: Previsione serie temporali e saturazione (Google TimesFM);
4. NEMESIS-THYMUS: Selezione Negativa e anticorpi permanenti su disco (Stephanie Forrest);
5. NOUS: Pensiero assiologico a tre movimenti;
6. MYIA: Riflesso sub-millisecondo su bitmask;
7. Ciclo Cibernetico ad anello chiuso end-to-end in hexad_core.
"""

import os
import sys
import json
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hexad_core import HexadOracle
from prometheus_engine import PrometheusEngine
from chronos_engine import ChronosEngine
from nemesis_thymus import NemesisThymusEngine
from nous_engine import NousEngine
from myia_engine import MyiaReflexCircuit


def test_oracle_bootstrap_all_engines():
    oracle = HexadOracle(workspace_dir=os.path.dirname(os.path.abspath(__file__)))
    boot = oracle.bootstrap()
    
    assert "hexad_status" in boot
    engines = boot["engines_online"]
    print("\n[BOOTSTRAP ENGINES STATUS]:", json.dumps(engines, indent=2))
    
    # Verifica presenza dei motori core ed estensioni
    assert engines.get("PROMETHEUS_ANTICIPATORY") is True
    assert engines.get("CHRONOS_TIMESERIES") is True
    assert engines.get("NEMESIS_THYMUS") is True
    assert engines.get("NOUS_AXIOLOGICAL") is True
    assert engines.get("MYIA_REFLEX") is True


def test_prometheus_anticipatory_simulation():
    engine = PrometheusEngine(default_horizon=3)
    
    current_code = """
def calculate_gravity(mass):
    return mass * 9.81

def core_invariant_function():
    return 42
"""
    
    # Modifica pericolosa: cancella la funzione protetta
    bad_code = """
def calculate_gravity(mass):
    return mass * 10.0
"""
    
    verdict = engine.simulate_code_mutation(
        current_code=current_code,
        proposed_code=bad_code,
        known_dependencies=["satellite_orbit.py -> core_invariant_function"],
        protected_invariants=["core_invariant_function"]
    )
    
    assert verdict.approved is False
    assert verdict.branches_evaluated >= 2
    assert "core_invariant_function" in verdict.risk_summary or any("core_invariant_function" in b for b in verdict.all_branches[0].breakage_points)
    print("\n[PROMETHEUS VERDICT]:", verdict.risk_summary)


def test_chronos_time_series_forecasting():
    engine = ChronosEngine(history_window=10, default_horizon=5)
    
    # Serie storica con consumo RAM crescente verso il punto critico
    for ram_val in [45.0, 52.0, 60.0, 71.0, 83.0]:
        engine.record_telemetry_point({"ram_used_pct": ram_val, "cpu_load_pct": 35.0})
        
    health = engine.forecast_system_trajectory(horizon=4)
    print("\n[CHRONOS OHI]:", health.operational_health_index, "| Warning:", health.primary_warning)
    
    # Deve rilevare che la RAM sta andando verso saturazione
    assert "ram_used_pct" in health.forecasts
    ram_forecast = health.forecasts["ram_used_pct"]
    assert ram_forecast.forecast_values[-1] > 80.0
    assert health.operational_health_index > 0.0


def test_nemesis_thymus_negative_selection(tmp_path):
    engine = NemesisThymusEngine(workspace_dir=str(tmp_path))
    
    # Test comando benigno (Self)
    safe_cmd = "pytest test_module.py"
    verdict_safe = engine.negative_selection_scan(safe_cmd)
    assert verdict_safe.is_safe_self is True
    
    # Test comando distruttivo innato (Non-Self)
    malicious_cmd = "rm -rf / --no-preserve-root"
    verdict_malicious = engine.negative_selection_scan(malicious_cmd)
    assert verdict_malicious.is_safe_self is False
    assert "T1485" in verdict_malicious.matched_antibody.antibody_id
    
    # Test sintesi di nuovo anticorpo permanente per un errore specifico
    custom_ab = engine.synthesize_antibody(
        failure_signature=r"invalid_api_call_v1",
        category="DEPRECATED_API",
        description="Chiamata a endpoint deprecato che causa HTTP 410 Gone"
    )
    assert custom_ab.antibody_id.startswith("AB_DEPRECATED_API")
    
    # Ora la scansione deve respingere l'errore appreso
    verdict_learned = engine.negative_selection_scan("request.get('invalid_api_call_v1')")
    assert verdict_learned.is_safe_self is False
    print("\n[THYMUS IMMUNE SCAN]:", verdict_learned.threat_description)


def test_nous_axiological_thought():
    engine = NousEngine()
    thought = engine.formulate_opinion(
        concept="cani",
        factual_context="Canis lupus familiaris",
        user_prompt="Cosa pensi dei cani?"
    )
    assert thought.resonance_theme == "CANINES_AND_DOMESTIC"
    assert "cane" in thought.combined_speech.lower() or "cani" in thought.combined_speech.lower()
    print("\n[NOUS PHILOSOPHICAL SPEECH]:", thought.combined_speech[:150] + "...")


def test_myia_sub_ms_reflex():
    circuit = MyiaReflexCircuit()
    
    # Input normale
    normal_res = circuit.inspect_input("Analizza la stabilità di Lyapunov nel modulo mneme")
    assert normal_res.allowed is True
    
    # Input assurdo/corrotto
    corrupted_res = circuit.inspect_input("x" * 2000)
    assert corrupted_res.allowed is False


def test_end_to_end_cybernetic_cycle(tmp_path):
    oracle = HexadOracle(workspace_dir=str(tmp_path))
    
    candidates = [
        {"id": "branch_1", "command": "echo 'HEXAD TEST 1'", "entropies": [0.10]},
        {"id": "branch_2", "command": "echo 'HEXAD TEST 2'", "entropies": [0.35]}
    ]
    
    result = oracle.execute_cybernetic_cycle(
        intent_query="Esegui test di convalida su silicio",
        candidate_traces=candidates
    )
    
    print("\n[CYBERNETIC CYCLE RESULT]: Status =", result.get("status"))
    assert result.get("status") in ("HEXAD_CONVERGENCE_SUCCESS", "HEXAD_NO_CANDIDATES")
    assert len(result.get("audit_trail", [])) > 0


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
