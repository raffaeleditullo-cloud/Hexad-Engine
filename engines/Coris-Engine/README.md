# CORIS ENGINE // The Homeostatic, Lymphatic & Autopoietic Heart

<p align="center">
  <img src="logos/coris_core.png" width="240" height="240" alt="CORIS Engine Logo" />
</p>

<p align="center">
  <strong>The First Self-Healing, Homeostatic Living Heart for AI Agents.</strong><br>
  <em>Active Inference, Dynamic Context Hemodynamics, and Lymphatic Immune Memory.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Free_Energy-Friston_Active_Inference-FF2A55?style=flat-square" alt="Friston"/>
  <img src="https://img.shields.io/badge/Immune_System-Lymphatic_Antibodies-FF7700?style=flat-square" alt="Immune"/>
  <img src="https://img.shields.io/badge/Protocol-MCP%20JSON--RPC-00F0FF?style=flat-square" alt="Protocol"/>
  <img src="https://img.shields.io/badge/License-MIT-00FF88?style=flat-square" alt="License"/>
</p>

---

## 🫀 The Third Pillar: Why AI Needs Homeostasis

In cybernetics and biology, an intelligence cannot survive with just a **Mind** and a **Muscle**:
* **ANIMA (The Mind)** computes continuous intent, path integrals, and phase collapse in Hilbert space.
* **DEMON (The Muscle)** executes deterministic actions, enforces MITRE blast-radius gates, and manages reflex caches.

Without a **Heart**, this system suffocates: context windows fill with metabolic waste (repetitive logs, debug traces), rate limits cause panic loops, and repeated errors drain resources.

**CORIS is the non-linear self-tuning homeostatic oscillator that keeps the organism far from thermal equilibrium.**

---

## 🔬 Mathematical Foundations

```
                  ┌───────────────────────────────┐
                  │          ANIMA (Mente)        │
                  │   Fase e Principio di Azione  │
                  └──────────────┬────────────────┘
                                 │ Flusso di Intento & Segnali di Decoerenza
                                 ▼
┌───────────────────────────────────────────────────────────────┐
│                          CORIS (Cuore)                        │
│                                                               │
│  Pressione Omeostatica: P(t) = exp(-F / k_B T_context)       │
│  Tensione Immunitaria:  Γ(t) = dF/dt + ∫ Auto-Antigeni dt    │
│  Emodinamica Contesto: Vasocostrizione & Drenaggio Scorie     │
│  Autolisi e Fagositosi: N_k(t) > Θ -> Rigenerazione Tissutale │
└────────────────────────────────┬──────────────────────────────┘
                                 │ Ritmo di Clock & Allostasi
                                 ▼
                  ┌───────────────────────────────┐
                  │          DEMON (Muscolo)      │
                  │  Attuazione OS e Blast-Radius │
                  └───────────────────────────────┘
```

### 1. Friston Variational Free Energy $\mathcal{F}(t)$
Measures total systemic stress as the divergence between the internal model and environmental reality:

$$\mathcal{F}(t) = \text{D}_{KL}\Big(q(\text{Internal State}) \;\big\Vert{}\; p(\text{External Environment})\Big) - \mathbb{E}_q\big[\ln p(\text{Execution}, \text{Context})\big]$$

$$\mathcal{F} \approx w_e \cdot \text{ErrorRate} + w_l \cdot \ln\left(1 + \frac{\text{Latency}}{50}\right) + w_c \cdot \frac{\text{ContextUsed}}{\text{ContextMax}}$$

### 2. Homeostatic Context Pressure $P(t)$
$$P(t) = \exp\left(-\frac{\mathcal{F}}{k_B \cdot T_{context}}\right)$$

* **$P > 0.60$ (Nominal)**: Laminare flow, normal heart rate (70-80 bpm).
* **$P < 0.35$ (Vasoconstriction)**: Triggers hemodynamic drainage: purges dead thought loops, old tracebacks, and verbose logs while preserving vital system contracts.

### 3. Lymphatic Immune System & Antibody Synthesis
When ANIMA prunes an erratic branch or DEMON blocks a malicious command, CORIS extracts the **molecular epitope**:

$$\text{Epitope} = \text{SHA256}\Big(\text{SourceLayer} \oplus \text{PatternSignature}\Big)_{[:16]}$$

Stores permanent antibodies in `immune_memory.json`. Future candidate prompts/commands that bind to this antigen are **neutralized instantly at 0 token cost**.

### 4. Necrosis Tensor $N_k$ & Cellular Healing (Autophagy)
Tracks degradation per module:
$$N_k(t) = \int_0^t \Big(\alpha \cdot \text{Fails}(k) + \beta \cdot \text{Latency}(k)\Big) e^{-\frac{t-\tau}{\tau_{rec}}} d\tau$$
When $N_k > 3.5$, CORIS initiates cellular autolysis, resection of necrotic code, and stem-cell self-repair.

---

## ⚡ The Living Organism Triad

| Organ | Engine | Domain | Core Superpower |
| :--- | :--- | :--- | :--- |
| 🧠 **Mente** | **ANIMA** | Hilbert Space $\mathbb{C}$ | Path integral action phase $\phi = \int (H - \lambda C) dt$, streaming mid-sentence killswitch. |
| 🫀 **Cuore** | **CORIS** | Statistical Thermodynamics | Free energy homeostasis, context hemodynamics, lymphatic antibodies & autopoiesis. |
| 🦾 **Muscolo** | **DEMON** | Deterministic OS Gates | MITRE ATT&CK T1485 blast-radius sandbox, 0-token reflex cache (`knowledge_base.json`). |

---

## 🤖 Model Context Protocol (MCP) Server

CORIS exposes a high-speed stdio JSON-RPC 2.0 server (`coris_mcp.py`).

### Exposed Tools:
* **`coris_vital_pulse`**: Ingests error rate, latency, and context tokens; returns heart rate bpm, Free Energy $\mathcal{F}$, pressure $P$, and ischemia alerts.
* **`coris_hemodynamic_drain`**: Purges metabolic waste from context window (removes tracebacks, redundant logs) while keeping vital instructions intact.
* **`coris_synthesize_antibody`**: Creates permanent immune memory against dangerous patterns or hallucinatory loops.
* **`coris_immune_scan`**: Pre-flight threat neutralization against known antigens.
* **`coris_cellular_repair`**: Triggers self-healing on necrotic modules.

### Claude Code CLI Setup
```bash
claude mcp add coris-engine python c:/Users/stree/Desktop/Coris-Engine/coris_mcp.py
```

### Full Triad MCP Configuration (`mcp.json` for Cursor / Windsurf)
```json
{
  "mcpServers": {
    "anima-engine": {
      "command": "python",
      "args": ["c:/Users/stree/Desktop/Anima-Engine/anima_mcp.py"]
    },
    "coris-engine": {
      "command": "python",
      "args": ["c:/Users/stree/Desktop/Coris-Engine/coris_mcp.py"]
    },
    "demon-engine": {
      "command": "python",
      "args": ["c:/Users/stree/Desktop/Demon-Engine/demon_mcp.py"]
    }
  }
}
```

---

## 🧪 Benchmark Verification

Run the full validation suite:
```bash
python test_coris_engine.py
```

* **4/4 Tests Passed in 0.003s**: Homeostatic pulse, hemodynamic context drain, antibody synthesis/binding, necrosis autolysis & healing.

---

## 📄 License
MIT License. Developed by Raffaele Di Tullo.
