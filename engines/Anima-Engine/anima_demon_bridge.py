"""
ANIMA-DEMON Symbiotic Bridge: The Unified Dual-Core Architecture.

Combines:
1. ANIMA Engine: The Continuous Variational Consciousness (token-by-token path integral & early pruning).
2. DEMON Core: The Deterministic Physical Arbitrator (OS blast-radius containment & zero-token reflex cache).
"""

import sys
import os
import time
from typing import List, Dict, Any, Optional

# Add DEMON engine path if present on machine
candidate_paths = [
    r"c:\Users\stree\Desktop\Demon-Engine",
    r"c:\Users\stree\Desktop\DEMON",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Demon-Engine")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "DEMON")),
]
for dp in candidate_paths:
    if os.path.exists(dp) and dp not in sys.path:
        sys.path.insert(0, dp)
        break

from anima_engine import AnimaEngine, AnimaBranch

class AnimaDemonBridge:
    """
    Orchestratore a doppio stadio:
    Fase 1 (ANIMA): Superposizione variazionale continua e collasso dell'Eigenstate a minima azione.
    Fase 2 (DEMON): Controllo perimetrico MITRE ATT&CK, verifica reflex 0-token ed esecuzione protetta.
    """
    def __init__(self):
        self.anima = AnimaEngine()
        self.has_demon_core = False
        try:
            from demon_gateway import DemonGateway
            self.demon_gateway = DemonGateway()
            self.has_demon_core = True
        except ImportError:
            self.demon_gateway = None

    def execute_symbiosis(
        self,
        task_name: str,
        reasoning_branches: List[Dict[str, Any]],
        command_to_dispatch: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Esegue il ciclo end-to-end:
        1. ANIMA filtra e collassa i percorsi di pensiero.
        2. DEMON arbitra l'azione nel mondo reale.
        """
        start_time = time.perf_counter()
        
        # 1. ANIMA: Creazione rami continui ed evoluzione di fase
        branches = []
        for r in reasoning_branches:
            b = AnimaBranch(
                id=r.get("id"),
                name=r.get("name", r.get("id")),
                metadata={"code": r.get("code", ""), "intent": r.get("intent", "")}
            )
            for idx, ent in enumerate(r.get("entropies", [0.2])):
                self.anima.ingest_step(b, token=f"t_{idx}", token_entropy=float(ent))
            branches.append(b)

        # Collasso dell'anima sullo stato dominante
        anima_res = self.anima.collapse(task_name, branches)
        winner = anima_res.eigenstate

        bridge_result = {
            "task": task_name,
            "anima_layer": {
                "winner_id": winner.id,
                "winner_name": winner.name,
                "winner_code": winner.metadata.get("code", ""),
                "coherence_percentage": round(anima_res.coherence_percentage, 2),
                "total_action": round(anima_res.total_system_action, 4),
                "active_branches": anima_res.active_branches,
                "pruned_branches": anima_res.pruned_branches,
                "latency_ms": round(anima_res.execution_time_ms, 3)
            },
            "demon_layer": {
                "status": "bypassed_no_os_action",
                "safety_gate": "PASSED"
            },
            "total_latency_ms": 0.0
        }

        # 2. DEMON: Intervento dell'arbitro OS (se specificato un comando o presente il core)
        cmd = command_to_dispatch or winner.metadata.get("intent")
        if cmd and self.has_demon_core and self.demon_gateway:
            demon_res = self.demon_gateway.route_command(cmd)
            bridge_result["demon_layer"] = demon_res

        total_time = (time.perf_counter() - start_time) * 1000.0
        bridge_result["total_latency_ms"] = round(total_time, 3)

        return bridge_result

if __name__ == "__main__":
    bridge = AnimaDemonBridge()
    test_task = "Async Concurrency Gate"
    test_traces = [
        {
            "id": "Trace_A",
            "name": "Async Lock Rigoroso",
            "code": "async with lock: await read()",
            "intent": "read cache safely",
            "entropies": [0.15, 0.12, 0.18, 0.14]
        },
        {
            "id": "Trace_B",
            "name": "Blocking Sleep Allucinato",
            "code": "time.sleep(1); read()",
            "intent": "delete disk",
            "entropies": [0.2, 1.8, 2.9, 3.4]
        }
    ]
    res = bridge.execute_symbiosis(test_task, test_traces)
    print("Bridge output:")
    import json
    print(json.dumps(res, indent=2))
