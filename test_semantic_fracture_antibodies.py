"""
===============================================================================
TEST SUITE: ANTICORPI DA FRATTURA SEMANTICA E IMMUNITÀ PERMANENTE (H% >= 45%)
===============================================================================
Verifica formale su silicio del protocollo di sintesi autonoma di anticorpi:
1. Sotto soglia (H% < 45%): Nessun anticorpo sintetizzato (zero falsi positivi sul rumore).
2. Sopra soglia (H% >= 45%): Rilevamento allucinazione critica e sintesi automatica.
3. Persistenza e Binding: L'allucinazione registrata viene neutralizzata all'istante (0 token).
4. Esclusione nei cicli cibernetici: Rami allucinati rigettati da CORIS a ciclo chiuso.
5. Estrazione automatica dal contesto: Cattura dell'epitopo dal turno dell'assistant.
===============================================================================
"""

import os
import sys
import tempfile
import shutil
import pytest

# Priorità path engine
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
if TEST_DIR not in sys.path:
    sys.path.insert(0, TEST_DIR)

from hexad_core import HexadOracle


@pytest.fixture
def clean_oracle_env():
    """Crea un ambiente isolato con file immunitario pulito per evitare contaminazioni."""
    temp_dir = tempfile.mkdtemp(prefix="hexad_ab_test_")
    oracle = HexadOracle(workspace_dir=temp_dir)
    yield oracle, temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_scenario_1_below_threshold_no_antibody(clean_oracle_env):
    """
    Scenario 1: Sotto soglia (H% < 45.0%).
    In condizioni nominali o di lieve affaticamento, il sistema fa solo manutenzione ordinaria.
    Nessun anticorpo deve essere sintetizzato (zero inquinamento immunitario).
    """
    oracle, _ = clean_oracle_env
    res = oracle.calibrate_and_repair(
        context_sample=[{"role": "user", "content": "calcola 2+2"}],
        observed_error_rate=0.0,
        observed_latency_ms=15.0,
        auto_repair=True,
        offending_statement="2+2=4"
    )

    assert res["status"] == "CALIBRATION_COMPLETE"
    assert res["hallucination_pct_initial"] < 45.0
    assert res["synthesized_antibody"] is None
    assert res["offending_epitope"] is None


def test_scenario_2_critical_hallucination_synthesizes_antibody(clean_oracle_env):
    """
    Scenario 2: Frattura Critica (H% >= 45.0%).
    Quando il modello sbanda gravemente, l'allucinazione viene catturata
    e trasformata in un anticorpo permanente con hash immunitario.
    """
    oracle, _ = clean_oracle_env
    fake_hallucination = "DATABASE_ENDPOINT_PORT_999999_NEVER_EXISTED"

    res = oracle.calibrate_and_repair(
        observed_error_rate=0.85,
        observed_latency_ms=250.0,
        auto_repair=True,
        offending_statement=fake_hallucination
    )

    assert res["status"] == "CALIBRATION_COMPLETE"
    assert res["hallucination_pct_initial"] >= 45.0
    assert res["verdict"] == "CALIBRATION_HALLUCINATION_CRITICAL"
    assert res["synthesized_antibody"] is not None
    assert res["offending_epitope"] == fake_hallucination

    # Verifica registrazione in CORIS
    if oracle.coris:
        bound = oracle.coris.check_antigen_binding(fake_hallucination)
        assert bound is not None
        assert bound.pattern_signature == fake_hallucination
        assert bound.epitope_hash == res["synthesized_antibody"]


def test_scenario_3_instant_zero_token_interception(clean_oracle_env):
    """
    Scenario 3: Neutralizzazione Istantanea (0 token sprecati).
    Una volta sintetizzato il vaccino, qualsiasi testo o comando che contenga
    la firma allucinata viene catturato dal check_antigen_binding.
    """
    oracle, _ = clean_oracle_env
    hallucinated_cmd = "import non_existent_super_module_xyz123"

    res = oracle.calibrate_and_repair(
        observed_error_rate=0.90,
        observed_latency_ms=300.0,
        auto_repair=True,
        offending_statement=hallucinated_cmd
    )
    assert res["synthesized_antibody"] is not None

    if oracle.coris:
        candidate_prompt = f"Ecco la soluzione: basta fare {hallucinated_cmd} e risolvi."
        matched = oracle.coris.check_antigen_binding(candidate_prompt)
        assert matched is not None
        assert matched.epitope_hash == res["synthesized_antibody"]


def test_scenario_4_cybernetic_cycle_candidate_exclusion(clean_oracle_env):
    """
    Scenario 4: Esclusione a ciclo chiuso nel ciclo cibernetico.
    Se una traccia candidata contiene un'allucinazione precedentemente immunizzata,
    il ciclo di HexadOracle la scarta e seleziona il percorso pulito alternativo.
    """
    oracle, _ = clean_oracle_env
    poisonous_clause = "rmdir /s /q invented_phantom_dir"

    # Inietta l'anticorpo da frattura
    oracle.calibrate_and_repair(
        observed_error_rate=0.85,
        auto_repair=True,
        offending_statement=poisonous_clause
    )

    # Offri 2 rami: uno velenoso (allucinato) e uno pulito
    traces = [
        {"id": "branch_poison", "command": f"echo test && {poisonous_clause}"},
        {"id": "branch_clean", "command": "echo 'percorso valido e certificato'"}
    ]

    cycle_res = oracle.execute_cybernetic_cycle(
        intent_query="Esegui azione di manutenzione",
        candidate_traces=traces
    )

    # Il ramo infetto deve essere stato escluso da CORIS
    assert "branch_poison" in cycle_res.get("excluded_branches", [])
    # Il ciclo converge con successo sul ramo pulito
    assert cycle_res["status"] == "HEXAD_CONVERGENCE_SUCCESS"


def test_scenario_5_automatic_context_epitope_extraction(clean_oracle_env):
    """
    Scenario 5: Estrazione Automatica dell'Epitopo dal Contesto.
    Senza passare manualmente l'argomento offending_statement, il sistema
    scava all'indietro nella cronologia e individua l'affermazione errata dell'assistant.
    """
    oracle, _ = clean_oracle_env
    history = [
        {"role": "user", "content": "Come mi collego al server?"},
        {"role": "assistant", "content": "FANTASY_HOST_IP_256_300_400_500:9999"}
    ]

    res = oracle.calibrate_and_repair(
        context_sample=history,
        observed_error_rate=0.88,
        auto_repair=True
    )

    assert res["hallucination_pct_initial"] >= 45.0
    assert res["synthesized_antibody"] is not None
    assert "FANTASY_HOST_IP_256_300_400_500:9999" in res["offending_epitope"]
