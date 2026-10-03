"""
OCULUS Phase 1: Model Context Protocol (MCP) Server
The Spatial Perception, Saccadic Gaze & Foveal Compression Eye.

Protocol: stdio JSON-RPC 2.0 (compatible with Claude Code, Cursor, Windsurf, Antigravity)

Exposed Tools:
1. oculus_foveal_scan: Compresses reality into a high-res foveal point + peripheral skeleton (85-95% token savings).
2. oculus_project_ast_graph: Maps the structural AST dependency graph of a codebase in <10ms.
3. oculus_calibrate_sensory_proxy: Evaluates code entropy and outputs calibrated parameters for ANIMA.
4. oculus_inspect_symbol: Instantly pinpoints any symbol (class/function) with cyclomatic complexity metrics.
"""

import sys
import os
import json
import time
from typing import Dict, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oculus_engine import OculusEngine

def create_mcp_response(msg_id, result=None, error=None):
    resp = {"jsonrpc": "2.0", "id": msg_id}
    if error:
        resp["error"] = error
    else:
        resp["result"] = result
    return resp

def main():
    engine = OculusEngine()

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
                        "name": "oculus-engine-mcp",
                        "version": "1.0.0"
                    }
                }
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, result)) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                tools = [
                    {
                        "name": "oculus_foveal_scan",
                        "description": "Applica la vista saccadica foveale: individua il nodo critico ad altissima risoluzione e riduce il resto del repository a scheletro a costo quasi zero (risparmio 90% token).",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "L'intento, il bug o la funzione da cercare"},
                                "workspace_dir": {"type": "string", "description": "Percorso della cartella di progetto"}
                            },
                            "required": ["query", "workspace_dir"]
                        }
                    },
                    {
                        "name": "oculus_project_ast_graph",
                        "description": "Mappa l'intera topologia AST del codice sorgente (classi, funzioni, complessità e import) in millisecondi.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "root_dir": {"type": "string", "description": "Percorso radice del progetto"}
                            },
                            "required": ["root_dir"]
                        }
                    },
                    {
                        "name": "oculus_calibrate_sensory_proxy",
                        "description": "Analizza l'entropia di Shannon e la complessità ciclomatica di un blocco di codice per calibrare i parametri di fase di ANIMA.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "file_path": {"type": "string", "description": "File da analizzare"}
                            },
                            "required": ["file_path"]
                        }
                    },
                    {
                        "name": "oculus_inspect_symbol",
                        "description": "Ispezione chirurgica di un simbolo (funzione o classe) per visualizzarne complessità, chiamate interne e signature.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "symbol_name": {"type": "string", "description": "Nome del simbolo"},
                                "workspace_dir": {"type": "string", "description": "Cartella di progetto"}
                            },
                            "required": ["symbol_name", "workspace_dir"]
                        }
                    }
                ]
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"tools": tools})) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})

                if tool_name == "oculus_foveal_scan":
                    q = tool_args.get("query", "")
                    ws = tool_args.get("workspace_dir", ".")
                    fovea = engine.focus_saccadic_gaze(q, ws)

                    payload = {
                        "focal_file": fovea.focal_file,
                        "focal_symbols": [s.__dict__ for s in fovea.focal_symbols],
                        "focal_snippet": fovea.focal_source_snippet,
                        "peripheral_skeletons": fovea.peripheral_skeletons,
                        "token_reduction_pct": fovea.compression_ratio_pct,
                        "sensory_entropy": fovea.sensory_entropy,
                        "anima_calibration": fovea.anima_calibration
                    }
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps(payload, ensure_ascii=False, indent=2)
                    }]
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                    sys.stdout.flush()

                elif tool_name == "oculus_project_ast_graph":
                    rd = tool_args.get("root_dir", ".")
                    topo = engine.scan_directory_topology(rd)
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps(topo, ensure_ascii=False, indent=2)
                    }]
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                    sys.stdout.flush()

                elif tool_name == "oculus_calibrate_sensory_proxy":
                    fp = tool_args.get("file_path", "")
                    syms = engine.scan_file_ast(fp)
                    content = ""
                    if os.path.exists(fp):
                        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                    entropy = engine.compute_shannon_entropy(content)
                    avg_c = sum(s.complexity_score for s in syms) / max(1, len(syms)) if syms else 1.0
                    payload = {
                        "file": fp,
                        "symbols_count": len(syms),
                        "shannon_entropy": round(entropy, 3),
                        "average_cyclomatic_complexity": round(avg_c, 2),
                        "recommended_anima_calibration": {
                            "action_beta": round(0.40 + (avg_c * 0.05), 3),
                            "phase_jitter_limit": round(max(1.4, 2.5 - (entropy * 0.15)), 2),
                            "complexity_weight": round(min(0.6, 0.2 + (avg_c * 0.05)), 2)
                        }
                    }
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps(payload, ensure_ascii=False, indent=2)
                    }]
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                    sys.stdout.flush()

                elif tool_name == "oculus_inspect_symbol":
                    sname = tool_args.get("symbol_name", "").lower()
                    ws = tool_args.get("workspace_dir", ".")
                    if not engine.symbol_table:
                        engine.scan_directory_topology(ws)

                    matches = []
                    for fp, syms in engine.symbol_table.items():
                        for s in syms:
                            if sname in s.name.lower():
                                matches.append(s.__dict__)

                    tool_content = [{
                        "type": "text",
                        "text": json.dumps({"matches_count": len(matches), "symbols": matches[:8]}, ensure_ascii=False, indent=2)
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
