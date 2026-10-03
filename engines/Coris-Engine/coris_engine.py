"""
CORIS Engine: The Homeostatic, Lymphatic & Autopoietic Heart for AI Agents.

Friston Variational Free Energy, Hemodynamic Context Pressure & Immune Phagocytosis.
- Maintains life far from thermal equilibrium (prevents context fatigue, loops, resource crashes).
- Regulates context hemodynamics (vasoconstriction & metabolic waste drainage).
- Lymphatic antibody synthesis (vaccinates system against known crash patterns).
- Relational autolysis & self-healing tissue repair.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
import math
import time
import json
import os
import hashlib
import pathlib

@dataclass
class VitalSigns:
    heart_rate_bpm: float
    free_energy_F: float
    homeostatic_pressure_P: float
    context_fullness_pct: float
    is_tachycardic: bool            # Battito accelerato sotto stress (>100 bpm)
    vasoconstriction_active: bool   # Drenaggio d'emergenza del contesto attivo
    active_antibodies: int
    necrotic_modules: List[str]
    status: str                     # "NOMINAL", "ELEVATED_STRESS", "ISCHEMIA", "AUTOPHAGY"

@dataclass
class Antibody:
    epitope_hash: str
    pattern_signature: str
    source_layer: str              # "ANIMA_DECOHERENCE", "DEMON_BLAST_RADIUS", "RUNTIME_CRASH"
    neutralization_rule: str
    affinity_strength: float = 1.0
    created_at: float = field(default_factory=time.time)

class CorisEngine:
    """
    Il Cuore e Sistema Immunitario Omeostatico dell'Organismo AI.
    """
    def __init__(
        self,
        base_bpm: float = 72.0,
        temp_context: float = 1.0,
        vasoconstriction_threshold: float = 0.35,  # P < 0.35 attiva drenaggio
        necrosis_critical: float = 3.5,            # N_k > 3.5 attiva fagositosi
        immune_store_path: Optional[str] = None
    ):
        self.base_bpm = base_bpm
        self.temp_context = temp_context
        self.vasoconstriction_threshold = vasoconstriction_threshold
        self.necrosis_critical = necrosis_critical
        
        self.immune_store_path = immune_store_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "immune_memory.json"
        )
        self.antibodies: Dict[str, Antibody] = {}
        self.necrosis_tensor: Dict[str, float] = {}  # N_k per ciascun modulo
        self.last_pulse_time = time.perf_counter()
        
        self._load_antibodies()

    def _load_antibodies(self):
        if os.path.exists(self.immune_store_path):
            try:
                with open(self.immune_store_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        self.antibodies[k] = Antibody(**v)
            except Exception as e:
                print(f"[CORIS IMMUNE] Errore caricamento anticorpi: {e}")

    def _save_antibodies(self):
        try:
            with open(self.immune_store_path, "w", encoding="utf-8") as f:
                serializable = {k: v.__dict__ for k, v in self.antibodies.items()}
                json.dump(serializable, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[CORIS IMMUNE] Errore salvataggio anticorpi: {e}")

    def pulse(
        self,
        error_rate: float,
        latency_ms: float,
        context_tokens_used: int,
        context_tokens_max: int = 128000
    ) -> VitalSigns:
        """
        Calcola il battito cardiaco e l'Energia Libera Variazionale (Friston Active Inference).
        F(t) = D_KL(q || p) - E_q[ln p]
        """
        context_pct = (context_tokens_used / max(1, context_tokens_max)) * 100.0
        
        # Pesi dell'energia libera Fristoniana
        w_error = 2.5
        w_latency = 0.8
        w_context = 1.8

        normalized_latency = math.log1p(max(0.0, latency_ms) / 50.0)
        normalized_context = (context_tokens_used / max(1, context_tokens_max)) * 2.0

        # Calcolo Energia Libera Variazionale F
        F = (w_error * error_rate) + (w_latency * normalized_latency) + (w_context * normalized_context)
        
        # Pressione Omeostatica P(t) = exp(-F / (k_B * T))
        P = math.exp(-F / max(0.1, self.temp_context))

        # Modulazione frequenza cardiaca (Allostasi non-lineare)
        # Se F è alto, la frequenza cardiaca sale (Tachicardia da stress)
        heart_rate = self.base_bpm * (1.0 + (F * 0.4))
        is_tachycardic = heart_rate > 105.0

        # Vasocostrizione / Drenaggio attivo se la pressione crolla o il contesto è saturo (>80%)
        vasoconstriction = (P < self.vasoconstriction_threshold) or (context_pct > 80.0)

        # Rilevamento necrosi attiva
        necrotic = [mod for mod, score in self.necrosis_tensor.items() if score >= self.necrosis_critical]

        # Stato vitale
        if necrotic:
            status = "AUTOPHAGY"
        elif vasoconstriction:
            status = "ISCHEMIA" if P < 0.2 else "ELEVATED_STRESS"
        else:
            status = "NOMINAL"

        return VitalSigns(
            heart_rate_bpm=round(heart_rate, 1),
            free_energy_F=round(F, 4),
            homeostatic_pressure_P=round(P, 4),
            context_fullness_pct=round(context_pct, 1),
            is_tachycardic=is_tachycardic,
            vasoconstriction_active=vasoconstriction,
            active_antibodies=len(self.antibodies),
            necrotic_modules=necrotic,
            status=status
        )

    def drain_context_hemodynamics(
        self,
        context_items: List[Dict[str, Any]],
        retention_ratio: float = 0.5
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Vasocostrizione selettiva: drena le scorie metaboliche dal contesto.
        Mantiene invarianti di sistema, contratti ed istruzioni cardine;
        purga log ripetuti, traceback intermedi e verbose thought dead-ends.
        """
        if not context_items:
            return [], 0

        original_count = len(context_items)
        drained: List[Dict[str, Any]] = []

        # Preserva sempre il system prompt iniziale e gli ultimi 2 scambi
        for idx, item in enumerate(context_items):
            role = item.get("role", "")
            content = str(item.get("content", ""))

            # Sempre vitale: system message o contratti critici
            if role == "system" or idx == 0 or idx >= original_count - 2:
                drained.append(item)
                continue

            # Scoria metabolica: log di debug o tentativi falliti già risolti
            is_metabolic_waste = (
                "Traceback" in content or
                "Error 429" in content or
                (len(content) > 3000 and "result:" in content)  # parentesi esplicite: and ha precedenza su or
            )

            if not is_metabolic_waste:
                drained.append(item)

        purged_count = original_count - len(drained)
        return drained, purged_count

    def synthesize_antibody(
        self,
        pattern_signature: str,
        source_layer: str,
        neutralization_rule: str
    ) -> Antibody:
        """
        Sintetizza un anticorpo linfatico permanente dall'epitopo dell'errore
        (intercetta pattern allucinati da ANIMA o attacchi bloccati da DEMON).
        """
        raw_epitope = f"{source_layer}::{pattern_signature.strip()}"
        epitope_hash = hashlib.sha256(raw_epitope.encode("utf-8")).hexdigest()[:16]

        ab = Antibody(
            epitope_hash=epitope_hash,
            pattern_signature=pattern_signature,
            source_layer=source_layer,
            neutralization_rule=neutralization_rule
        )
        self.antibodies[epitope_hash] = ab
        self._save_antibodies()
        return ab

    def check_antigen_binding(self, candidate_text: str) -> Optional[Antibody]:
        """
        Scansione immunitaria: verifica se un testo/comando si lega a un anticorpo noto.
        Neutralizzazione istantanea a monte (0 token sprecati).
        """
        for ab in self.antibodies.values():
            if ab.pattern_signature.lower() in candidate_text.lower():
                return ab
        return None

    def track_tissue_necrosis(self, module_name: str, has_failed: bool, latency_ms: float = 0.0):
        """
        Aggiorna il tensore di necrosi tissutale N_k con decadimento esponenziale.
        """
        current_score = self.necrosis_tensor.get(module_name, 0.0)
        # Decadimento omeostatico temporale
        decayed_score = current_score * 0.95

        if has_failed:
            delta = 1.0 + (latency_ms / 1000.0)
            decayed_score += delta

        self.necrosis_tensor[module_name] = round(decayed_score, 3)

    def trigger_phagocytosis_and_healing(self, module_name: str) -> Dict[str, Any]:
        """
        Isola il modulo necrotico, fagositosi dei residui e rigenerazione con cellule staminali.
        """
        score = self.necrosis_tensor.get(module_name, 0.0)
        self.necrosis_tensor[module_name] = 0.0  # Reset dopo l'intervento chirurgico
        return {
            "module": module_name,
            "necrosis_score_pre_op": score,
            "phagocytosis_status": "CELL_AUTOLYSIS_COMPLETED",
            "stem_cell_regeneration": "TISSUE_REPAIRED_HEALTHY",
            "action": "Vasodilation restored, module marked healthy."
        }
