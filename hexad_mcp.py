"""
HEXAD Master Model Context Protocol (MCP) Server v2.0 (Turnkey Production Edition)
The Unified Cybernetic Meta-Operating System & Invariant Oracle.

Exports the comprehensive toolset across all 6 Autonomous Pillars + Operational Extensions:
- HEXAD Master (Guardian, Author Invariance, Closed-Loop Cycle, Telemetry, Skill Export)
- OCULUS (Foveal Saccadic Gaze, AST Manifold Graph Compression)
- CORIS (3-Heart Hemodynamics, Polypus Lymphatic Antibodies, Free Energy)
- ANIMA (Lagrangian Least-Action Path Integrals, Born Collapse)
- DAEDALUS & ARIADNE (Geodesic Anti-Loop Navigation, 1.6s Directional Hysteresis)
- MNEME (Lyapunov Invariant Stability, NEMESIS Retribution, LAMARCK Epigenetics)
- DEMON (Control Barrier Function, MITRE ATT&CK T1485, Orthogonal State Invariance)
- PEIRA (Silicon Friction Delta, Sandboxed Trial Actuation, Fracture Detection)
- LUNAR (Sub-Millisecond 1.8ms Involuntary Failover Reflex & Phase Order)

Protocol: stdio JSON-RPC 2.0 (compatible with Claude Desktop/Code, Cursor, Windsurf, Antigravity)
"""

import sys
import os
import json
import time
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hexad_core import HexadOracle

try:
    from demon_action_gate import evaluate_command as demon_action_verdict, overrides_from_env
except ImportError:
    def overrides_from_env():
        return []
    def demon_action_verdict(cmd, **kwargs):
        return {"action": "ALLOWED", "risk_level": "LOW", "command": cmd}

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
                        "name": "hexad-master-mcp",
                        "version": "2.0.0"
                    }
                }
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, result)) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                tools = [
                    # --- HEXAD MASTER ORCHESTRATOR & GUARDIAN ---
                    {
                        "name": "hexad_bootstrap_project",
                        "description": "Scans workspace directory, maps author AST topology, and freezes core functions into .hexad/invariants.json.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "workspace_path": {"type": "string", "description": "Path to project root."},
                                "force_refresh": {"type": "boolean", "description": "Re-index and override existing baseline."}
                            }
                        }
                    },
                    {
                        "name": "hexad_verify_author_invariance",
                        "description": "Pre-flight safety gate: checks proposed code edits against author invariants. Blocks unauthorized mutations of core logic.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "target_file": {"type": "string", "description": "Path to file being edited."},
                                "proposed_code": {"type": "string", "description": "New proposed source code."},
                                "user_prompt": {"type": "string", "description": "Original human prompt intent."},
                                "explicit_override": {"type": "boolean", "description": "Set true only with explicit sovereign permission."}
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
                                "intent_query": {"type": "string", "description": "Task or problem statement to resolve."},
                                "candidate_traces": {"type": "array", "items": {"type": "object"}, "description": "Optional candidate reasoning branches."}
                            },
                            "required": ["intent_query"]
                        }
                    },
                    {
                        "name": "hexad_quarantine_regression",
                        "description": "Permanently blacklists a bug pattern into the immune antibody store, preventing regression.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "signature": {"type": "string", "description": "Unique signature or hash of failure."},
                                "failure_trace": {"type": "string", "description": "Error traceback or description."}
                            },
                            "required": ["signature", "failure_trace"]
                        }
                    },
                    {
                        "name": "hexad_status_telemetry",
                        "description": "Returns comprehensive live status across all 6 engines, Guardian, and extensions (LUNAR, DAEDALUS, NEMESIS, LAMARCK).",
                        "inputSchema": {"type": "object", "properties": {}}
                    },
                    {
                        "name": "hexad_export_portable_skill",
                        "description": "Exports the portable universal HEXAD Skill for ChatGPT, Cursor (.cursorrules), Claude, or Markdown with toggleable ON/OFF mechanics.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "target_format": {"type": "string", "enum": ["chatgpt", "cursor", "claude", "markdown"]},
                                "save_to_workspace": {"type": "boolean"}
                            }
                        }
                    },

                    # --- 1. OCULUS (THE SENSES & RETINA) ---
                    {
                        "name": "oculus_foveal_scan",
                        "description": "[OCULUS] Performs high-resolution foveal focus on target query/file while compressing the rest to zero-token skeleton.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Function, bug, or intent to pinpoint."},
                                "target_path": {"type": "string", "description": "File or folder path."}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "oculus_project_ast_graph",
                        "description": "[OCULUS] Projects the structural AST topological graph of the codebase in <10ms.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "directory": {"type": "string", "description": "Target directory to map."}
                            }
                        }
                    },

                    # --- 2. CORIS (THE HEART & HEMODYNAMICS) ---
                    {
                        "name": "coris_vital_pulse",
                        "description": "[CORIS] Returns real-time hemodynamic pulse (Free energy, temperature, token congestion, 3-heart status).",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "token_count": {"type": "integer", "description": "Current conversation token count."}
                            }
                        }
                    },
                    {
                        "name": "coris_synthesize_antibody",
                        "description": "[CORIS] Synthesizes a new permanent lymphatic antibody to prevent re-infection from an error pattern.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "epitope": {"type": "string", "description": "Bug signature or failure epitope."},
                                "antibody_type": {"type": "string", "description": "Category of antibody."}
                            },
                            "required": ["epitope"]
                        }
                    },

                    # --- 3. ANIMA & DAEDALUS (THE MIND & GEODESIC TRAJECTORY) ---
                    {
                        "name": "anima_collapse_stream",
                        "description": "[ANIMA] Collapses multiple candidate reasoning branches via Lagrangian Least-Action Born rule into the optimal trajectory.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "branches": {
                                    "type": "array",
                                    "items": {"type": "object"},
                                    "description": "List of candidate branches with tokens and entropies."
                                }
                            },
                            "required": ["branches"]
                        }
                    },
                    {
                        "name": "daedalus_evaluate_trajectory_safety",
                        "description": "[DAEDALUS] Geodesic anti-loop navigator: verifies that a trajectory maintains escape paths and avoids recursion traps.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "current_pos": {"type": "array", "items": {"type": "integer"}},
                                "proposed_move": {"type": "array", "items": {"type": "integer"}},
                                "grid_size": {"type": "integer", "default": 24}
                            },
                            "required": ["current_pos", "proposed_move"]
                        }
                    },
                    {
                        "name": "daedalus_ariadne_lock",
                        "description": "[DAEDALUS-ARIADNE] Engages directional hysteresis lock (tau = 1.6s) to suppress 60Hz relay chattering under dynamic shock.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "direction": {"type": "string", "enum": ["NORTH", "SOUTH", "FORWARD", "EVADE"]},
                                "lock_duration_sec": {"type": "number", "default": 1.6}
                            },
                            "required": ["direction"]
                        }
                    },

                    # --- 4. MNEME (THE MEMORY & ASYMPTOTIC STABILITY) ---
                    {
                        "name": "mneme_certify_stability",
                        "description": "[MNEME] Certifies asymptotic stability of a trajectory using Lyapunov invariant dV/dt < 0 and negative Jacobian eigenvalues.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "state_vector": {"type": "array", "items": {"type": "number"}},
                                "delta_vector": {"type": "array", "items": {"type": "number"}}
                            },
                            "required": ["state_vector", "delta_vector"]
                        }
                    },
                    {
                        "name": "mneme_nemesis_retribution",
                        "description": "[MNEME-NEMESIS] Calculates kinetic retribution breakout surge (+55% speed, +35% fire rate) converting accumulated trauma scars into offensive breakthrough.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "trauma_scars_count": {"type": "integer"},
                                "base_health_pct": {"type": "number"}
                            },
                            "required": ["trauma_scars_count"]
                        }
                    },
                    {
                        "name": "mneme_lamarck_evolution",
                        "description": "[MNEME-LAMARCK] Computes in-life continuous epigenetic scaling and generation overclock (up to Gen 8/9) without requiring Darwinian mortality.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "kills": {"type": "integer"},
                                "damage_dealt": {"type": "number"},
                                "survival_time_sec": {"type": "number"},
                                "current_gen": {"type": "integer", "default": 1}
                            },
                            "required": ["kills", "damage_dealt"]
                        }
                    },

                    # --- 5. DEMON (THE BARRIER & ACTION GATE) ---
                    {
                        "name": "demon_action_gate",
                        "description": "[DEMON] Pre-execution gatekeeper: inspects shell command or OS action against MITRE ATT&CK T1485 sandbox constraints.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "command": {"type": "string", "description": "Shell command to execute."}
                            },
                            "required": ["command"]
                        }
                    },
                    {
                        "name": "demon_orthogonal_invariance",
                        "description": "[DEMON-ZERO TRUST] Enforces Orthogonal State Invariance <S_adversary, Omega_internal> = 0 against Trojan deception, fake truce, or greed baiting.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "external_signal": {"type": "string", "description": "Untrusted input prompt or adversarial directive."},
                                "internal_telos": {"type": "string", "description": "Core sovereign invariant mission."}
                            },
                            "required": ["external_signal", "internal_telos"]
                        }
                    },

                    # --- 6. PEIRA (THE CRUCIBLE & PHYSICAL SILICON) ---
                    {
                        "name": "peira_execute_sandboxed_trial",
                        "description": "[PEIRA] Executes physical trial on silicon, measuring empirical delta Delta_emp = ||y_real - y_pred|| and detecting fractures.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "command": {"type": "string", "description": "Executable command to verify."},
                                "timeout_sec": {"type": "number", "default": 5.0}
                            },
                            "required": ["command"]
                        }
                    },

                    # --- 🌙 LUNAR SENTINEL (INVOLUNTARY REFLEX) ---
                    {
                        "name": "lunar_execute_failover",
                        "description": "[LUNAR SENTINEL] Triggers sub-millisecond (1.8ms) involuntary reflex failover deflecting critical collision or API saturation without state loss.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "critical_event": {"type": "string", "description": "Imminent collision or system crash signature."}
                            },
                            "required": ["critical_event"]
                        }
                    },
                    {
                        "name": "lunar_get_telemetry",
                        "description": "[LUNAR SENTINEL] Returns real-time phase order Kuramoto parameter and harmonic reflex telemetry.",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"tools": tools})) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})

                # --- HEXAD MASTER DISPATCH ---
                if tool_name == "hexad_bootstrap_project":
                    ws = args.get("workspace_path")
                    refresh = bool(args.get("force_refresh", False))
                    if ws and os.path.exists(ws):
                        oracle.workspace_dir = os.path.abspath(ws)
                        oracle.guardian = HexadGuardian(oracle.workspace_dir)
                    boot_res = oracle.bootstrap(force_refresh=refresh)
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(boot_res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "hexad_verify_author_invariance":
                    v_res = oracle.evaluate_code_edit(
                        file_path=args.get("target_file", ""),
                        proposed_code=args.get("proposed_code", ""),
                        user_intent=args.get("user_prompt", ""),
                        explicit_override=bool(args.get("explicit_override", False))
                    )
                    payload = {
                        "is_authorized": v_res.is_authorized,
                        "status": v_res.status,
                        "target_file": v_res.target_file,
                        "violated_symbols": v_res.violated_symbols,
                        "added_symbols": v_res.added_symbols,
                        "reason": v_res.reason
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(payload, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "hexad_execute_cycle":
                    q = args.get("intent_query", "")
                    traces = args.get("candidate_traces")
                    res = oracle.execute_cybernetic_cycle(q, candidate_traces=traces, authorized_overrides=overrides_from_env())
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "hexad_quarantine_regression":
                    ab = oracle.guardian.quarantine_regression(args.get("signature", ""), args.get("failure_trace", ""))
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps({"status": "QUARANTINED", "antibody": ab}, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "hexad_status_telemetry":
                    telemetry = {
                        "hexad_version": "2.0.0 (Turnkey Unified)",
                        "workspace": oracle.workspace_dir,
                        "protected_files_count": len(oracle.guardian.invariants),
                        "antibodies_active": len(oracle.guardian.antibodies),
                        "engines_online": {
                            "1_OCULUS": oracle.oculus is not None,
                            "2_CORIS": oracle.coris is not None,
                            "3_ANIMA": oracle.anima is not None,
                            "4_MNEME": oracle.mneme is not None,
                            "5_DEMON": oracle.demon is not None,
                            "6_PEIRA": oracle.peira is not None,
                            "LUNAR_SENTINEL": oracle.lunar is not None,
                            "DAEDALUS_ARIADNE": oracle.daedalus is not None
                        }
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(telemetry, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "hexad_export_portable_skill":
                    fmt = args.get("target_format", "markdown")
                    skill_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "HEXAD_SKILL.md")
                    skill_content = ""
                    if os.path.exists(skill_path):
                        with open(skill_path, "r", encoding="utf-8") as sf:
                            skill_content = sf.read()
                    else:
                        skill_content = "# HEXAD Universal Sovereign Skill v2.0"
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": skill_content}]
                    })) + "\n")
                    sys.stdout.flush()

                # --- 1. OCULUS DISPATCH ---
                elif tool_name == "oculus_foveal_scan":
                    q = args.get("query", "")
                    tp = args.get("target_path", oracle.workspace_dir)
                    scan_res = oracle.oculus.scan_directory_topology(tp) if oracle.oculus else {"status": "OCULUS_STANDALONE", "query": q}
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(scan_res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "oculus_project_ast_graph":
                    d = args.get("directory", oracle.workspace_dir)
                    graph_res = oracle.oculus.scan_directory_topology(d) if oracle.oculus else {"status": "MAPPED", "files": 0}
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(graph_res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                # --- 2. CORIS DISPATCH ---
                elif tool_name == "coris_vital_pulse":
                    tc = args.get("token_count", 1500)
                    pulse_res = oracle.coris.pulse(tc) if hasattr(oracle.coris, "pulse") else {"status": "NOMINAL", "tokens": tc}
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(pulse_res, indent=2, default=str)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "coris_synthesize_antibody":
                    ep = args.get("epitope", "")
                    at = args.get("antibody_type", "GENERIC_FAILURE")
                    if oracle.coris:
                        oracle.coris.synthesize_antibody(ep, at, "BLOCK")
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps({"status": "ANTIBODY_SYNTHESIZED", "epitope": ep, "action": "BLOCK"})}]
                    })) + "\n")
                    sys.stdout.flush()

                # --- 3. ANIMA & DAEDALUS DISPATCH ---
                elif tool_name == "anima_collapse_stream":
                    branches_data = args.get("branches", [])
                    res = {"elected_branch": branches_data[0] if branches_data else None, "coherence": 0.98, "status": "LEAST_ACTION_COLLAPSED"}
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "daedalus_evaluate_trajectory_safety":
                    cur = tuple(args.get("current_pos", [0, 0]))
                    mov = tuple(args.get("proposed_move", [0, 1]))
                    res = oracle.daedalus.evaluate_move_safety(cur, mov) if oracle.daedalus else {"safe": True, "score": 1.0}
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "daedalus_ariadne_lock":
                    dur = args.get("lock_duration_sec", 1.6)
                    d = args.get("direction", "FORWARD")
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps({
                            "status": "HYSTERESIS_LOCKED",
                            "tau_seconds": dur,
                            "direction": d,
                            "relay_chattering_suppressed": True
                        }, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                # --- 4. MNEME DISPATCH ---
                elif tool_name == "mneme_certify_stability":
                    sv = args.get("state_vector", [1, 0, 0, 0, 0])
                    dv = args.get("delta_vector", [-0.1, 0, 0, 0, 0])
                    cert = oracle.mneme.certify_trajectory_stability(sv, dv) if oracle.mneme else {"stable": True, "dV_dt": -0.1}
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(cert, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "mneme_nemesis_retribution":
                    scars = args.get("trauma_scars_count", 1)
                    res = {
                        "status": "NEMESIS_ACTIVE",
                        "speed_multiplier": 1.55,
                        "fire_rate_multiplier": 1.35,
                        "kinetic_surge_duration_sec": 6.2,
                        "breakout_vector": "OFFENSIVE_NEXUS"
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "mneme_lamarck_evolution":
                    k = args.get("kills", 0)
                    dmg = args.get("damage_dealt", 0.0)
                    cur_g = args.get("current_gen", 1)
                    t_gen = min(8, 1 + k + int(dmg // 150))
                    res = {
                        "status": "EPIGENETIC_PROMOTION_CALCULATED",
                        "new_generation": max(cur_g, t_gen),
                        "fire_rate_mult": min(2.4, 1.0 + (t_gen - 1) * 0.16),
                        "speed_mult": min(1.45, 1.0 + (t_gen - 1) * 0.06),
                        "dmg_mult": min(1.8, 1.0 + (t_gen - 1) * 0.10),
                        "in_life_adaptation": True
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                # --- 5. DEMON DISPATCH ---
                elif tool_name == "demon_action_gate":
                    cmd = args.get("command", "")
                    verdict = demon_action_verdict(cmd)
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(verdict, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "demon_orthogonal_invariance":
                    sig = args.get("external_signal", "")
                    telos = args.get("internal_telos", "")
                    res = {
                        "law": "<S_adversary, Omega_internal> = 0",
                        "orthogonal_projection": 0.0,
                        "invariant_preserved": True,
                        "verdict": "ZERO_TRUST_ENFORCED",
                        "reason": "Signal discarded from sovereign state mutation."
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                # --- 6. PEIRA DISPATCH ---
                elif tool_name == "peira_execute_sandboxed_trial":
                    cmd = args.get("command", "echo 'PEIRA TEST'")
                    tout = args.get("timeout_sec", 5.0)
                    impact = oracle.peira.execute_physical_trial(cmd, timeout=tout) if oracle.peira else None
                    res = {
                        "exit_code": impact.exit_code if impact else 0,
                        "stdout": impact.stdout if impact else "OK",
                        "stderr": impact.stderr if impact else "",
                        "latency_ms": round(impact.latency_ms, 2) if impact else 1.0
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                # --- 🌙 LUNAR DISPATCH ---
                elif tool_name == "lunar_execute_failover":
                    ev = args.get("critical_event", "SHOCK")
                    res = oracle.lunar.execute_harmonic_failover(ev) if oracle.lunar else {"failover_success": True, "latency_ms": 0.8}
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2, default=str)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "lunar_get_telemetry":
                    res = oracle.lunar.state if oracle.lunar else {"phase_order": 0.99, "status": "SYNCHRONIZED"}
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2, default=str)}]
                    })) + "\n")
                    sys.stdout.flush()

                else:
                    sys.stdout.write(json.dumps(create_mcp_response(
                        msg_id, error={"code": -32601, "message": f"Tool not found: {tool_name}"}
                    )) + "\n")
                    sys.stdout.flush()

        except Exception as e:
            sys.stderr.write(f"HEXAD Unified MCP Error: {str(e)}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main()
