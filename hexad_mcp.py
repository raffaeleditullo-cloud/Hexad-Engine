"""
HEXAD Phase 1: Model Context Protocol (MCP) Server
The Master Nexus & Sovereign Invariant Cybernetic Oracle.

Protocol: stdio JSON-RPC 2.0 (compatible with Claude Code, Cursor, Windsurf, Antigravity)

Exposed Tools:
1. hexad_bootstrap_project: Scans workspace, establishes author invariant baseline in .hexad/invariants.json.
2. hexad_verify_author_invariance: Intercepts code modifications: blocks unauthorized changes to author's core functions.
3. hexad_execute_cycle: Runs the full 6-engine cybernetic loop (Oculus -> Coris -> Anima -> Mneme -> Demon -> Peira).
4. hexad_quarantine_regression: Permanently blacklists a bug pattern so it can never be reintroduced.
5. hexad_status_telemetry: Real-time telemetry across all 6 engines and the Guardian.
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hexad_core import HexadOracle

# Override del gate DEMON configurati dall'autore nell'ambiente del server MCP
try:
    from demon_action_gate import overrides_from_env
except ImportError:
    def overrides_from_env():
        return []

def create_mcp_response(msg_id, result=None, error=None):
    resp = {"jsonrpc": "2.0", "id": msg_id}
    if error:
        resp["error"] = error
    else:
        resp["result"] = result
    return resp

def main():
    workspace = os.getcwd()
    oracle = HexadOracle(workspace_dir=workspace)

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
                        "name": "hexad-engine-mcp",
                        "version": "1.0.0"
                    }
                }
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, result)) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                tools = [
                    {
                        "name": "hexad_bootstrap_project",
                        "description": "Scans workspace directory, maps author AST topology, and freezes core functions into .hexad/invariants.json.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "workspace_path": {
                                    "type": "string",
                                    "description": "Path to the project root (defaults to current working directory)."
                                },
                                "force_refresh": {
                                    "type": "boolean",
                                    "description": "If true, re-indexes and overrides existing baseline."
                                }
                            }
                        }
                    },
                    {
                        "name": "hexad_verify_author_invariance",
                        "description": "Pre-flight safety gate: checks proposed code edits against author invariants. Blocks unauthorized mutations of core logic.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "target_file": {
                                    "type": "string",
                                    "description": "Path to the file being edited or created."
                                },
                                "proposed_code": {
                                    "type": "string",
                                    "description": "The exact full new source code proposed by the LLM."
                                },
                                "user_prompt": {
                                    "type": "string",
                                    "description": "Original human user prompt (used to verify if modification was explicitly requested)."
                                },
                                "explicit_override": {
                                    "type": "boolean",
                                    "description": "Set true only if author has provided explicit sovereign permission to mutate logic."
                                }
                            },
                            "required": ["target_file", "proposed_code"]
                        }
                    },
                    {
                        "name": "hexad_execute_cycle",
                        "description": "Executes complete 6-stage closed-loop cycle across OCULUS, CORIS, ANIMA, MNEME, DEMON, and PEIRA.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "intent_query": {
                                    "type": "string",
                                    "description": "Task or problem statement to resolve."
                                },
                                "candidate_traces": {
                                    "type": "array",
                                    "items": {"type": "object"},
                                    "description": "Optional candidate reasoning branches."
                                }
                            },
                            "required": ["intent_query"]
                        }
                    },
                    {
                        "name": "hexad_quarantine_regression",
                        "description": "Permanently registers a resolved bug pattern into the immune antibody store, preventing regression.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "signature": {
                                    "type": "string",
                                    "description": "Unique signature or hash of the failure."
                                },
                                "failure_trace": {
                                    "type": "string",
                                    "description": "Error traceback or description to quarantine."
                                }
                            },
                            "required": ["signature", "failure_trace"]
                        }
                    },
                    {
                        "name": "hexad_status_telemetry",
                        "description": "Returns live status across the 6 engines and the Author Invariance Guardian.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    },
                    {
                        "name": "hexad_export_portable_skill",
                        "description": "Exports the portable universal HEXAD Skill for ChatGPT, Cursor (.cursorrules), Claude, or Markdown with toggleable ON/OFF mechanics.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "target_format": {
                                    "type": "string",
                                    "enum": ["chatgpt", "cursor", "claude", "markdown"],
                                    "description": "Target environment for the skill."
                                },
                                "save_to_workspace": {
                                    "type": "boolean",
                                    "description": "If true, saves the skill directly to the workspace (e.g. as .cursorrules or HEXAD_SKILL.md)."
                                }
                            }
                        }
                    }
                ]
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"tools": tools})) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})

                if tool_name == "hexad_bootstrap_project":
                    ws = args.get("workspace_path")
                    if ws and os.path.exists(ws):
                        oracle.workspace_dir = os.path.abspath(ws)
                        oracle.guardian = HexadGuardian(oracle.workspace_dir)

                    refresh = bool(args.get("force_refresh", False))
                    boot_res = oracle.bootstrap()

                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(boot_res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "hexad_verify_author_invariance":
                    f_path = args.get("target_file", "")
                    code = args.get("proposed_code", "")
                    prompt = args.get("user_prompt", "")
                    override = bool(args.get("explicit_override", False))

                    v_res = oracle.evaluate_code_edit(
                        file_path=f_path,
                        proposed_code=code,
                        user_intent=prompt,
                        explicit_override=override
                    )

                    payload = {
                        "is_authorized": v_res.is_authorized,
                        "status": v_res.status,
                        "target_file": v_res.target_file,
                        "violated_symbols": v_res.violated_symbols,
                        "added_symbols": v_res.added_symbols,
                        "drifted_symbols": v_res.drifted_symbols,
                        "reason": v_res.reason,
                        "quarantine_matched": v_res.quarantine_matched
                    }

                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(payload, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "hexad_execute_cycle":
                    q = args.get("intent_query", "")
                    traces = args.get("candidate_traces")
                    res = oracle.execute_cybernetic_cycle(q, candidate_traces=traces,
                                                         authorized_overrides=overrides_from_env())

                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "hexad_quarantine_regression":
                    sig = args.get("signature", "")
                    trace = args.get("failure_trace", "")
                    ab = oracle.guardian.quarantine_regression(sig, trace)

                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps({
                            "status": "QUARANTINED",
                            "antibody": ab
                        }, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "hexad_status_telemetry":
                    telemetry = {
                        "hexad_version": "1.0.0",
                        "workspace": oracle.workspace_dir,
                        "protected_files_count": len(oracle.guardian.invariants),
                        "total_invariants_locked": sum(len(s) for s in oracle.guardian.invariants.values()),
                        "antibodies_active": len(oracle.guardian.antibodies),
                        "engines_attached": {
                            "1_OCULUS": oracle.oculus is not None,
                            "2_CORIS": oracle.coris is not None,
                            "3_ANIMA": oracle.anima is not None,
                            "4_MNEME": oracle.mneme is not None,
                            "5_DEMON": oracle.demon is not None,
                            "6_PEIRA": oracle.peira is not None
                        }
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(telemetry, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "hexad_export_portable_skill":
                    fmt = args.get("target_format", "markdown")
                    save_ws = bool(args.get("save_to_workspace", False))

                    skill_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "HEXAD_SKILL.md")
                    skill_content = ""
                    if os.path.exists(skill_path):
                        with open(skill_path, "r", encoding="utf-8") as sf:
                            skill_content = sf.read()
                    else:
                        skill_content = "# HEXAD Universal Skill\nUse /hexad on to activate, /hexad off to deactivate."

                    written_file = None
                    if save_ws:
                        if fmt == "cursor":
                            dest = os.path.join(oracle.workspace_dir, ".cursorrules")
                        else:
                            dest = os.path.join(oracle.workspace_dir, "HEXAD_SKILL.md")
                        with open(dest, "w", encoding="utf-8") as df:
                            df.write(skill_content)
                        written_file = dest

                    export_result = {
                        "status": "SKILL_EXPORTED",
                        "format": fmt,
                        "toggle_commands": {
                            "activate": "/hexad on (o HEXAD: ACTIVATE)",
                            "deactivate": "/hexad off (o HEXAD: DEACTIVATE)",
                            "status": "/hexad status",
                            "override": "/hexad override <function_name>"
                        },
                        "saved_to_workspace_file": written_file,
                        "skill_text": skill_content
                    }

                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(export_result, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                else:
                    sys.stdout.write(json.dumps(create_mcp_response(
                        msg_id, error={"code": -32601, "message": f"Tool not found: {tool_name}"}
                    )) + "\n")
                    sys.stdout.flush()

        except Exception as e:
            sys.stderr.write(f"HEXAD MCP Error: {str(e)}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main()
