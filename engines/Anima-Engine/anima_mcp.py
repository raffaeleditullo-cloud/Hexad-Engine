"""
ANIMA Phase 1: Model Context Protocol (MCP) Server
Continuous Variational Consciousness & Path-Integral Wave Collapse Server.

Protocol: stdio JSON-RPC 2.0 (compatible with Claude Code, Cursor, Windsurf, Antigravity)

Exposed Tools:
1. anima_stream_step: Ingest token-by-token entropy & complexity, returns keep_alive & phase.
2. anima_collapse_stream: Performs O(N) Born collapse across all surviving active branches.
3. anima_batch_evaluate: Evaluates multiple complete reasoning traces with continuous action.
4. anima_reset: Clears in-memory stream buffers for a new task.
"""

import sys
import os
import json
import time
from typing import Dict, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anima_engine import AnimaEngine, AnimaBranch

def create_mcp_response(msg_id, result=None, error=None):
    resp = {"jsonrpc": "2.0", "id": msg_id}
    if error:
        resp["error"] = error
    else:
        resp["result"] = result
    return resp

def main():
    engine = AnimaEngine()
    active_branches: Dict[str, AnimaBranch] = {}

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            request = json.loads(line)
            msg_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})

            if method == "initialize":
                result = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "anima-engine-mcp",
                        "version": "1.0.0"
                    }
                }
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, result)) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                tools = [
                    {
                        "name": "anima_stream_step",
                        "description": "Ingerisce un token lungo una traiettoria di decoding, calcola l'azione e restituisce se il ramo deve continuare o essere potato per decoerenza stocastica.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "branch_id": {"type": "string", "description": "Identificativo univoco del ramo parallelo"},
                                "name": {"type": "string", "description": "Nome descrittivo dell'ipotesi"},
                                "token": {"type": "string", "description": "Il token emesso"},
                                "token_entropy": {"type": "number", "description": "Entropia dei logit H(t) = -sum p * log2(p)"},
                                "complexity_delta": {"type": "number", "description": "Variazione di complessità sintattica/strutturale (default 0.0)"}
                            },
                            "required": ["branch_id", "token", "token_entropy"]
                        }
                    },
                    {
                        "name": "anima_collapse_stream",
                        "description": "Esegue il collasso deterministico in O(N) su tutti i rami attivi accumulati in memoria, eleggendo l'Eigenstate a minima azione.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "scenario_name": {"type": "string", "description": "Nome dello scenario decisionale"}
                            },
                            "required": ["scenario_name"]
                        }
                    },
                    {
                        "name": "anima_batch_evaluate",
                        "description": "Valuta simultaneamente un batch di N tracce di ragionamento con le rispettive sequenze di entropia, collassando il migliore in <0.05ms.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "scenario_name": {"type": "string"},
                                "candidates": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "string"},
                                            "name": {"type": "string"},
                                            "text": {"type": "string"},
                                            "entropies": {
                                                "type": "array",
                                                "items": {"type": "number"}
                                            }
                                        },
                                        "required": ["id", "entropies"]
                                    }
                                }
                            },
                            "required": ["scenario_name", "candidates"]
                        }
                    },
                    {
                        "name": "anima_reset",
                        "description": "Ripristina i buffer di memoria dei rami in streaming per iniziare una nuova sessione.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }
                ]
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"tools": tools})) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})

                if tool_name == "anima_stream_step":
                    b_id = tool_args.get("branch_id")
                    b_name = tool_args.get("name", f"Branch_{b_id}")
                    tok = tool_args.get("token", "")
                    ent = float(tool_args.get("token_entropy", 0.0))
                    comp = float(tool_args.get("complexity_delta", 0.0))

                    if b_id not in active_branches:
                        active_branches[b_id] = AnimaBranch(id=b_id, name=b_name)

                    branch = active_branches[b_id]
                    keep_alive, phase, amp = engine.ingest_step(branch, tok, ent, comp)

                    payload = {
                        "branch_id": b_id,
                        "keep_alive": keep_alive,
                        "is_pruned": branch.is_pruned,
                        "prune_reason": branch.prune_reason,
                        "accumulated_action": round(branch.accumulated_action, 4),
                        "accumulated_phase_rad": round(phase, 4),
                        "effective_amplitude": round(amp, 4),
                        "steps_count": len(branch.steps)
                    }
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps(payload, ensure_ascii=False, indent=2)
                    }]
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                    sys.stdout.flush()

                elif tool_name == "anima_collapse_stream":
                    scen = tool_args.get("scenario_name", "Streaming Collapse")
                    branches_list = list(active_branches.values())
                    if not branches_list:
                        tool_content = [{
                            "type": "text",
                            "text": json.dumps({"error": "Nessun ramo attivo registrato in memoria."}, indent=2)
                        }]
                        sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                        sys.stdout.flush()
                        continue

                    res = engine.collapse(scen, branches_list)
                    payload = {
                        "winner_branch_id": res.eigenstate.id,
                        "winner_name": res.eigenstate.name,
                        "winner_text": res.eigenstate.generated_text,
                        "coherence_percentage": round(res.coherence_percentage, 2),
                        "total_action": round(res.total_system_action, 4),
                        "active_branches": res.active_branches,
                        "pruned_branches": res.pruned_branches,
                        "latency_ms": round(res.execution_time_ms, 3)
                    }
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps(payload, ensure_ascii=False, indent=2)
                    }]
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                    sys.stdout.flush()

                elif tool_name == "anima_batch_evaluate":
                    scen = tool_args.get("scenario_name", "Batch Action Collapse")
                    candidates = tool_args.get("candidates", [])
                    branches = []
                    for c in candidates:
                        b = AnimaBranch(
                            id=c.get("id"),
                            name=c.get("name", c.get("id")),
                            metadata={"text": c.get("text", "")}
                        )
                        ents = c.get("entropies", [])
                        for idx, e in enumerate(ents):
                            engine.ingest_step(b, token=f"tok_{idx}", token_entropy=float(e))
                        branches.append(b)

                    res = engine.collapse(scen, branches)
                    payload = {
                        "winner_id": res.eigenstate.id,
                        "winner_name": res.eigenstate.name,
                        "winner_text": res.eigenstate.metadata.get("text", ""),
                        "coherence_percentage": round(res.coherence_percentage, 2),
                        "total_action": round(res.total_system_action, 4),
                        "latency_ms": round(res.execution_time_ms, 3)
                    }
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps(payload, ensure_ascii=False, indent=2)
                    }]
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                    sys.stdout.flush()

                elif tool_name == "anima_reset":
                    active_branches.clear()
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps({"status": "reset_completed", "active_branches": 0})
                    }]
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                    sys.stdout.flush()

                else:
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, error={"code": -32601, "message": "Method not found"})) + "\n")
                    sys.stdout.flush()

        except Exception as e:
            sys.stdout.write(json.dumps(create_mcp_response(None, error={"code": -32603, "message": str(e)})) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
