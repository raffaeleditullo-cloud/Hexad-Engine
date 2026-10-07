"""
LUNAR MCP Server: Model Context Protocol (MCP) Server for LUNAR Engine.
The 7th Sovereign Pillar (Secret Reserve Armament / Quantum Subconscious Phase-Locking).

Protocol: stdio JSON-RPC 2.0 (compatible with Claude, Cursor, Windsurf, Antigravity)

Exposed Tools:
1. lunar_compute_phase_order: Computes Kuramoto phase order parameter r and phase synchrony.
2. lunar_execute_failover: Ultra-fast O(1) harmonic phase-lock failover quench (< 12ms SLA) when macro engines diverge.
3. lunar_get_telemetry: Retrieves lifetime rescue count, mean latency, and last phase certificate.
"""

import sys
import os
import json
import time
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lunar_engine import LunarEngine

def create_mcp_response(msg_id, result=None, error=None):
    resp = {"jsonrpc": "2.0", "id": msg_id}
    if error:
        resp["error"] = error
    else:
        resp["result"] = result
    return resp

def main():
    engine = LunarEngine()

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
                        "name": "lunar-engine-mcp",
                        "version": "1.0.0"
                    }
                }
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, result)) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                tools = [
                    {
                        "name": "lunar_compute_phase_order",
                        "description": "Computes the Kuramoto order parameter r (0..1) measuring global phase coherence across neural micro-agents.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "phase_angles": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "List of phase angles (radians) for each agent in the colony."
                                }
                            },
                            "required": ["phase_angles"]
                        }
                    },
                    {
                        "name": "lunar_execute_failover",
                        "description": "Executes emergency LUNAR harmonic phase-locking failover when HEXAD macro-engines experience SLA breach or divergence. Quenches in < 12ms with zero lobotomy.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "membrane_potentials": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Array of current membrane potentials (mV)."
                                },
                                "synaptic_weights": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "number"}
                                    },
                                    "description": "Adjacency matrix of synaptic weights."
                                },
                                "divergent_lyapunov": {
                                    "type": "number",
                                    "description": "Current positive divergent Lyapunov exponent (> 0)."
                                },
                                "shock_type": {
                                    "type": "string",
                                    "description": "Label of the adversary shock that breached macro defenses."
                                }
                            },
                            "required": ["membrane_potentials", "synaptic_weights", "divergent_lyapunov"]
                        }
                    },
                    {
                        "name": "lunar_get_telemetry",
                        "description": "Returns lifetime failover rescue statistics, activation counts, and mean quench latencies.",
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
                args = params.get("arguments", {})

                if tool_name == "lunar_compute_phase_order":
                    phases = args.get("phase_angles", [])
                    import numpy as np
                    r, psi = engine.compute_kuramoto_order(np.array(phases))
                    res = {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({"order_parameter_r": r, "mean_phase_angle": psi, "is_coherent": (r >= 0.85)}, indent=2)
                            }
                        ]
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, res)) + "\n")
                    sys.stdout.flush()

                elif tool_name == "lunar_execute_failover":
                    v_in = args.get("membrane_potentials", [])
                    w_in = args.get("synaptic_weights", [])
                    lyap = args.get("divergent_lyapunov", 3.0)
                    shock = args.get("shock_type", "adversarial_cataclysm")

                    v_out, w_out, cert = engine.execute_harmonic_failover(v_in, w_in, lyap, shock)
                    res = {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "verdict": "LUNAR_RESCUE_SUCCESS",
                                    "certificate": cert.__dict__,
                                    "sample_membrane_potential": v_out[:5] if v_out else []
                                }, indent=2)
                            }
                        ]
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, res)) + "\n")
                    sys.stdout.flush()

                elif tool_name == "lunar_get_telemetry":
                    res = {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "is_armed": engine.state.is_armed,
                                    "total_rescues": engine.state.total_rescues,
                                    "mean_rescue_latency_ms": round(engine.state.mean_rescue_latency_ms, 2),
                                    "last_certificate": engine.state.last_phase_certificate.__dict__ if engine.state.last_phase_certificate else None
                                }, indent=2)
                            }
                        ]
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, res)) + "\n")
                    sys.stdout.flush()

                else:
                    err = {"code": -32601, "message": f"Tool '{tool_name}' not found."}
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, error=err)) + "\n")
                    sys.stdout.flush()

        except Exception as e:
            err = {"code": -32603, "message": str(e)}
            sys.stdout.write(json.dumps(create_mcp_response(None, error=err)) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
