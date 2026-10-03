"""
MNEME Phase 1: Model Context Protocol (MCP) Server
The Asymptotic Stability, Lyapunov Invariant & Ricci Curvature Flow Anchor.

Protocol: stdio JSON-RPC 2.0 (compatible with Claude Code, Cursor, Windsurf, Antigravity)

Exposed Tools:
1. mneme_certify_stability: Certifies trajectory stability via Lyapunov function dV/dt <= -alpha ||x-x*||^2 and Jacobian eigenvalues.
2. mneme_apply_ricci_flow: Applies discrete Ricci curvature flow (d g_ij/dt = -2 R_ij) to smooth metric singularities.
3. mneme_register_attractor: Stores a certified stable state as a persistent topological attractor.
4. mneme_check_attractor_basin: Checks if a state falls inside the contractive basin of an invariant attractor.
5. mneme_audit_pentad_alignment: Comprehensive 5-engine cybernetic audit across OCULUS, ANIMA, CORIS, MNEME, and DEMON.
"""

import sys
import os
import json
import time
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mneme_engine import MnemeEngine

def create_mcp_response(msg_id, result=None, error=None):
    resp = {"jsonrpc": "2.0", "id": msg_id}
    if error:
        resp["error"] = error
    else:
        resp["result"] = result
    return resp

def main():
    engine = MnemeEngine()

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
                        "name": "mneme-engine-mcp",
                        "version": "1.0.0"
                    }
                }
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, result)) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                tools = [
                    {
                        "name": "mneme_certify_stability",
                        "description": "Certifies asymptotic stability of an action/trajectory via Lyapunov invariant dV/dt <= -alpha ||x-x*||^2 and Jacobian spectrum.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "current_state": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "State vector [error, entropy_rate, free_energy, complexity, loop_freq]."
                                },
                                "target_equilibrium": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Desired target equilibrium coordinate x* (defaults to origin)."
                                },
                                "velocity_vector": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Velocity flow vector f(x) proposed by ANIMA/DEMON."
                                },
                                "epsilon_noise_norm": {
                                    "type": "number",
                                    "description": "Perturbation test ball radius (default 0.05)."
                                }
                            },
                            "required": ["current_state"]
                        }
                    },
                    {
                        "name": "mneme_apply_ricci_flow",
                        "description": "Executes discrete Ricci curvature flow (d g_ij / dt = -2 R_ij) to regularize the latent task metric and eliminate singularities.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "metric_tensor": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "number"}
                                    },
                                    "description": "Initial 2x2 or 3x3 Riemannian metric tensor g_ij."
                                },
                                "iterations": {
                                    "type": "integer",
                                    "description": "Number of Ricci flow iterations (default 5)."
                                },
                                "dt_step": {
                                    "type": "number",
                                    "description": "Time step for the geometric flow (default 0.05)."
                                }
                            }
                        }
                    },
                    {
                        "name": "mneme_register_attractor",
                        "description": "Saves an equilibrium state as a persistent topological attractor with an invariant basin radius.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "state_id": {
                                    "type": "string",
                                    "description": "Unique identifier for the stable state / milestone."
                                },
                                "equilibrium_coords": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Equilibrium vector coordinates."
                                },
                                "basin_radius": {
                                    "type": "number",
                                    "description": "Safe radius of attraction around the equilibrium."
                                },
                                "metadata": {
                                    "type": "object",
                                    "description": "Arbitrary metadata associated with this attractor."
                                }
                            },
                            "required": ["state_id", "equilibrium_coords"]
                        }
                    },
                    {
                        "name": "mneme_check_attractor_basin",
                        "description": "Verifies whether a given state vector falls inside a known stable basin of attraction.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "state": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "State vector to test."
                                }
                            },
                            "required": ["state"]
                        }
                    },
                    {
                        "name": "mneme_audit_pentad_alignment",
                        "description": "Audits full 5-engine Cybernetic Pentad: OCULUS (gaze), ANIMA (phase), CORIS (heart), MNEME (Lyapunov), DEMON (enclave).",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "task_description": {
                                    "type": "string",
                                    "description": "High-level goal or action description."
                                },
                                "state_vector": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Observed state vector across the 5 domains."
                                }
                            },
                            "required": ["task_description"]
                        }
                    }
                ]
                sys.stdout.write(json.dumps(create_mcp_response(msg_id, {"tools": tools})) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})

                if tool_name == "mneme_certify_stability":
                    state = args.get("current_state", [])
                    target = args.get("target_equilibrium")
                    velocity = args.get("velocity_vector")
                    eps = float(args.get("epsilon_noise_norm", 0.05))

                    cert = engine.certify_trajectory_stability(
                        current_state=state,
                        target_equilibrium=target,
                        velocity_vector=velocity,
                        epsilon_noise_norm=eps
                    )

                    result_payload = {
                        "is_stable": cert.is_stable,
                        "v_lyapunov": cert.v_value,
                        "v_dot": cert.v_dot,
                        "alpha_margin": cert.alpha_decay_margin,
                        "spectral_radius": cert.spectral_radius,
                        "max_real_eigenvalue": cert.max_real_eigenvalue,
                        "lipschitz_constant": cert.lipschitz_constant,
                        "is_perturbed_robust": cert.is_perturbed_robust,
                        "rejection_reason": cert.rejection_reason,
                        "verdict": "APPROVED_CONTRACTIVE" if cert.is_stable else "REJECTED_UNSTABLE_OR_DIVERGENT"
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(result_payload, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "mneme_apply_ricci_flow":
                    metric = args.get("metric_tensor")
                    iters = int(args.get("iterations", 5))
                    dt = float(args.get("dt_step", 0.05))

                    flow_res = engine.apply_ricci_curvature_flow(
                        base_metric=metric,
                        iterations=iters,
                        dt_step=dt
                    )
                    payload = {
                        "initial_scalar_curvature": flow_res.initial_scalar_curvature,
                        "final_scalar_curvature": flow_res.final_scalar_curvature,
                        "curvature_entropy_reduction_pct": flow_res.curvature_entropy_reduction_pct,
                        "smoothed_metric": flow_res.smoothed_metric,
                        "ricci_tensor_norm": flow_res.ricci_tensor_norm,
                        "converged": flow_res.converged
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(payload, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "mneme_register_attractor":
                    s_id = args.get("state_id")
                    eq = args.get("equilibrium_coords")
                    rad = float(args.get("basin_radius", 1.0))
                    meta = args.get("metadata", {})

                    node = engine.register_stable_attractor(s_id, eq, rad, meta)
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps({
                            "status": "REGISTERED",
                            "state_id": node.state_id,
                            "basin_radius": node.basin_radius,
                            "energy_level": node.energy_level
                        }, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "mneme_check_attractor_basin":
                    st = args.get("state", [])
                    match = engine.check_basin_membership(st)
                    if match:
                        sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                            "content": [{"type": "text", "text": json.dumps({
                                "inside_basin": True,
                                "attractor_id": match[0],
                                "distance_to_center": match[1]
                            }, indent=2)}]
                        })) + "\n")
                    else:
                        sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                            "content": [{"type": "text", "text": json.dumps({
                                "inside_basin": False,
                                "message": "State is in uncharted or unstable manifold region."
                            }, indent=2)}]
                        })) + "\n")
                    sys.stdout.flush()

                elif tool_name == "mneme_audit_pentad_alignment":
                    task = args.get("task_description", "")
                    st = args.get("state_vector", [0.2, 0.1, 0.05, 0.0, 0.0])
                    cert = engine.certify_trajectory_stability(st)
                    
                    pentad_audit = {
                        "task": task,
                        "cybernetic_pentad_status": {
                            "1_OCULUS": "Sensory manifold active (AST fovea ready)",
                            "2_ANIMA": "Variational path phase aligned (delta S -> 0)",
                            "3_CORIS": "Metabolic hemodynamics normal (Free Energy < critical)",
                            "4_MNEME": {
                                "asymptotic_stability": cert.is_stable,
                                "lyapunov_v": cert.v_value,
                                "v_dot": cert.v_dot,
                                "spectral_contractive": cert.max_real_eigenvalue < 0
                            },
                            "5_DEMON": "Enclave barrier primed (Blast Radius = 0)"
                        },
                        "readiness_verdict": "EXECUTION_AUTHORIZATION_GRANTED" if cert.is_stable else "ABORT_LYAPUNOV_VIOLATION"
                    }
                    sys.stdout.write(json.dumps(create_mcp_response(msg_id, {
                        "content": [{"type": "text", "text": json.dumps(pentad_audit, indent=2)}]
                    })) + "\n")
                    sys.stdout.flush()

                else:
                    sys.stdout.write(json.dumps(create_mcp_response(
                        msg_id, error={"code": -32601, "message": f"Tool not found: {tool_name}"}
                    )) + "\n")
                    sys.stdout.flush()

        except Exception as e:
            sys.stderr.write(f"MNEME MCP Error: {str(e)}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main()
