"""
CORIS Phase 1: Model Context Protocol (MCP) Server
Homeostatic, Lymphatic & Autopoietic Heart Server for AI Agents.

Protocol: stdio JSON-RPC 2.0 (compatible with Claude Code, Cursor, Windsurf, Antigravity)

Exposed Tools:
1. coris_vital_pulse: Calculates Friston free energy, heart rate, and homeostatic pressure.
2. coris_hemodynamic_drain: Performs vasoconstriction, purging metabolic waste from context.
3. coris_synthesize_antibody: Immunizes system against crash/hallucination patterns.
4. coris_immune_scan: Pre-flight check against known antibodies (0-token threat block).
5. coris_cellular_repair: Heals necrotic software modules via autolysis and regeneration.
"""

import sys
import os
import json
import time
from typing import Dict, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coris_engine import CorisEngine

def create_mcp_response(msg_id, result=None, error=None):
    resp = {"jsonrpc": "2.0", "id": msg_id}
    if error:
        resp["error"] = error
    else:
        resp["result"] = result
    return resp

def main():
    engine = CorisEngine()

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
                        "name": "coris-engine-mcp",
                        "version": "1.0.0"
                    }
                }
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, result)) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                tools = [
                    {
                        "name": "coris_vital_pulse",
                        "description": "Rileva i parametri vitali omeostatici (Battito cardiaco bpm, Energia Libera di Friston F, Pressione di contesto e allarmi ischemia).",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "error_rate": {"type": "number", "description": "Tasso di errore corrente (0.0 - 1.0)"},
                                "latency_ms": {"type": "number", "description": "Latenza dell'ultima interazione in ms"},
                                "context_tokens_used": {"type": "integer", "description": "Numero di token attualmente allocati nel contesto"},
                                "context_tokens_max": {"type": "integer", "description": "Capacità massima della context window (default 128000)"}
                            },
                            "required": ["context_tokens_used"]
                        }
                    },
                    {
                        "name": "coris_hemodynamic_drain",
                        "description": "Applica vasocostrizione emodinamica: purga i log spuri, traceback e rami morti riducendo la fatica metabolica del contesto.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "context_items": {
                                    "type": "array",
                                    "description": "Lista di messaggi del contesto [{'role': '...', 'content': '...'}]"
                                }
                            },
                            "required": ["context_items"]
                        }
                    },
                    {
                        "name": "coris_synthesize_antibody",
                        "description": "Vaccina permanentemente l'organismo sintetizzando un anticorpo contro un'allucinazione o un comando tossico.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "pattern_signature": {"type": "string", "description": "Stringa o pattern tossico da neutralizzare"},
                                "source_layer": {"type": "string", "description": "Origine: ANIMA_DECOHERENCE o DEMON_BLAST_RADIUS"},
                                "neutralization_rule": {"type": "string", "description": "Regola di blocco o azione correttiva"}
                            },
                            "required": ["pattern_signature", "source_layer", "neutralization_rule"]
                        }
                    },
                    {
                        "name": "coris_immune_scan",
                        "description": "Scansione rapida del testo in input contro la memoria linfatica (neutralizzazione a monte a costo 0).",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "candidate_text": {"type": "string", "description": "Testo o comando da analizzare"}
                            },
                            "required": ["candidate_text"]
                        }
                    },
                    {
                        "name": "coris_cellular_repair",
                        "description": "Intervento di autolisi e rigenerazione tissutale su un modulo/file in avaria persistente.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "module_name": {"type": "string", "description": "Nome del file o componente degradato"}
                            },
                            "required": ["module_name"]
                        }
                    }
                ]
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"tools": tools})) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})

                if tool_name == "coris_vital_pulse":
                    err = float(tool_args.get("error_rate", 0.0))
                    lat = float(tool_args.get("latency_ms", 30.0))
                    used = int(tool_args.get("context_tokens_used", 1000))
                    c_max = int(tool_args.get("context_tokens_max", 128000))

                    vitals = engine.pulse(err, lat, used, c_max)
                    payload = vitals.__dict__
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps(payload, ensure_ascii=False, indent=2)
                    }]
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                    sys.stdout.flush()

                elif tool_name == "coris_hemodynamic_drain":
                    items = tool_args.get("context_items", [])
                    cleaned, purged = engine.drain_context_hemodynamics(items)
                    payload = {
                        "original_items": len(items),
                        "cleaned_items": len(cleaned),
                        "purged_metabolic_waste_count": purged,
                        "drained_context": cleaned
                    }
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps(payload, ensure_ascii=False, indent=2)
                    }]
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                    sys.stdout.flush()

                elif tool_name == "coris_synthesize_antibody":
                    pat = tool_args.get("pattern_signature", "")
                    src = tool_args.get("source_layer", "MANUAL")
                    rule = tool_args.get("neutralization_rule", "BLOCK")
                    ab = engine.synthesize_antibody(pat, src, rule)
                    payload = ab.__dict__
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps(payload, ensure_ascii=False, indent=2)
                    }]
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                    sys.stdout.flush()

                elif tool_name == "coris_immune_scan":
                    txt = tool_args.get("candidate_text", "")
                    ab_match = engine.check_antigen_binding(txt)
                    if ab_match:
                        payload = {
                            "is_antigen_detected": True,
                            "matched_antibody": ab_match.__dict__,
                            "action": "THREAT_NEUTRALIZED_BY_IMMUNE_SYSTEM"
                        }
                    else:
                        payload = {
                            "is_antigen_detected": False,
                            "action": "CLEAR_TO_PROCEED"
                        }
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps(payload, ensure_ascii=False, indent=2)
                    }]
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"content": tool_content})) + "\n")
                    sys.stdout.flush()

                elif tool_name == "coris_cellular_repair":
                    mod = tool_args.get("module_name", "")
                    report = engine.trigger_phagocytosis_and_healing(mod)
                    tool_content = [{
                        "type": "text",
                        "text": json.dumps(report, ensure_ascii=False, indent=2)
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
