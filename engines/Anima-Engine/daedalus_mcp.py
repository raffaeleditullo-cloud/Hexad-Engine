"""
DAEDALUS MCP Server: Model Context Protocol Server per DAEDALUS Engine.
Strumento Sovrano di Navigazione Topologica, Anti-Loop e Anti-Deadlock.

Protocollo: stdio JSON-RPC 2.0 (compatibile con Claude, Cursor, Windsurf, Antigravity)

Tool Esposti:
1. daedalus_evaluate_trajectory_safety: Valuta se un piano di navigazione o catena di azioni rischia autointrappolamento o loop vizioso.
2. daedalus_compute_reachability: Calcola lo spazio residuo libero e le vie di fuga garantite.
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from daedalus_engine import DaedalusEngine

def create_mcp_response(msg_id, result=None, error=None):
    resp = {"jsonrpc": "2.0", "id": msg_id}
    if error:
        resp["error"] = error
    else:
        resp["result"] = result
    return resp

def main():
    engine = DaedalusEngine(grid_size=24)

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
                        "name": "daedalus-engine-mcp",
                        "version": "1.0.0"
                    }
                }
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, result)) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                tools = [
                    {
                        "name": "daedalus_evaluate_trajectory_safety",
                        "description": "Valuta la sicurezza topologica di una traiettoria per impedire dead-end, loop ricorsivi o autointrappolamento.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "head": {"type": "array", "items": {"type": "integer"}},
                                "target": {"type": "array", "items": {"type": "integer"}},
                                "body_segments": {"type": "array", "items": {"type": "array", "items": {"type": "integer"}}}
                            },
                            "required": ["head", "target", "body_segments"]
                        }
                    }
                ]
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"tools": tools})) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})

                if tool_name == "daedalus_evaluate_trajectory_safety":
                    head = tuple(args.get("head", [0, 0]))
                    target = tuple(args.get("target", [5, 5]))
                    body = [tuple(b) for b in args.get("body_segments", [])]
                    cert = engine.evaluate_move_safety(head, target, body)
                    res = {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(cert.__dict__, indent=2)
                            }
                        ]
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, res)) + "\n")
                    sys.stdout.flush()
                else:
                    err = {"code": -32601, "message": f"Tool '{tool_name}' non trovato."}
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, error=err)) + "\n")
                    sys.stdout.flush()

        except Exception as e:
            err = {"code": -32603, "message": str(e)}
            sys.stdout.write(json.dumps(create_mcp_response(None, error=err)) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
