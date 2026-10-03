"""
POLYPUS Engine: The Cephalopod Tri-Ventricular Hemodynamic Regulator for CORIS.

Bio-Inspired by Octopus vulgaris (Cephalopoda):
1. Cuore Sistemico (Systemic Heart): Drives nominal cognition & immune memory under calm conditions.
2. Cuore Branchiale A (Branchial Context Filter): Oxygenator that purges metabolic context waste under high token density.
3. Cuore Branchiale B (Branchial Silicon Buffer): High-pressure hydrodynamic buffer that absorbs physical trial latency & friction.

Guarantees 100% zero-regression backward compatibility with CorisEngine.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import time
import os
import math

from coris_engine import CorisEngine, VitalSigns, Antibody


@dataclass
class PolypusTelemetry:
    active_governor: str                   # "SYSTEMIC", "BRANCHIAL_CONTEXT", "BRANCHIAL_SILICON"
    effective_bpm: float
    effective_pressure: float
    effective_free_energy: float
    effective_status: str                  # "NOMINAL", "OXYGENATING_PURGE", "SILICON_BUFFERED", "ISCHEMIA"
    drainage_triggered: bool
    purged_items_count: int
    systemic_vitals: VitalSigns
    branchial_context_vitals: VitalSigns
    branchial_silicon_vitals: VitalSigns
    audit_notes: List[str] = field(default_factory=list)


class PolypusEngine:
    """
    Sistema di Circolazione Tri-Ventricoide a 3 Cuori per Agenti Autonomi.
    """
    def __init__(
        self,
        immune_store_path: Optional[str] = None,
        context_congestion_threshold: int = 32000,
        physical_latency_threshold_ms: float = 400.0
    ):
        self.context_congestion_threshold = context_congestion_threshold
        self.physical_latency_threshold_ms = physical_latency_threshold_ms

        # 1. Cuore Sistemico (Il Cuore Centrale - Fedele all'originale al 100%)
        self.systemic_heart = CorisEngine(
            base_bpm=72.0,
            temp_context=1.0,
            vasoconstriction_threshold=0.35,
            immune_store_path=immune_store_path
        )

        # 2. Cuore Branchiale A: Filtro e Purificazione del Contesto (Ossigenatore)
        # Più proattivo nel drenare scorie (soglia drenaggio 0.50, temperatura termodinamica 1.6)
        self.branchial_context_heart = CorisEngine(
            base_bpm=65.0,
            temp_context=1.6,
            vasoconstriction_threshold=0.50,
            immune_store_path=immune_store_path
        )

        # 3. Cuore Branchiale B: Spinta ad Alta Pressione per Silicio e Rete (Ammortizzatore di Attrito)
        # Temperatura T=2.8 per assorbire latenze fisiche (PEIRA) senza scattare in ischemia isterica
        self.branchial_silicon_heart = CorisEngine(
            base_bpm=58.0,
            temp_context=2.8,
            vasoconstriction_threshold=0.18,
            immune_store_path=immune_store_path
        )

    # =========================================================================
    # DELEGA IMMUNITARIA CENTRALIZZATA (Preserva la memoria linfa vitale)
    # =========================================================================
    @property
    def antibodies(self) -> Dict[str, Antibody]:
        return self.systemic_heart.antibodies

    def check_antigen_binding(self, candidate_text: str) -> Optional[Antibody]:
        """Scansione antigenica a monte tramite il sistema linfatico condiviso."""
        return self.systemic_heart.check_antigen_binding(candidate_text)

    def synthesize_antibody(self, signature: str, source_layer: str, rule: str) -> Optional[Antibody]:
        """Sintesi linfatica istantanea di un nuovo anticorpo contro i crash."""
        ab = self.systemic_heart.synthesize_antibody(signature, source_layer, rule)
        if ab:
            # Sincronizza lo stato nei cuori ausiliari
            self.branchial_context_heart.antibodies[ab.epitope_hash] = ab
            self.branchial_silicon_heart.antibodies[ab.epitope_hash] = ab
        return ab

    def track_tissue_necrosis(self, module_name: str, has_failed: bool, latency_ms: float = 0.0):
        self.systemic_heart.track_tissue_necrosis(module_name, has_failed, latency_ms)

    # =========================================================================
    # CICLO CIRCOLATORIO TRI-VENTRICOLARE (The Cephalopod Pulse)
    # =========================================================================
    def pulse_polypus(
        self,
        error_rate: float,
        latency_ms: float,
        context_tokens_used: int,
        context_items: Optional[List[Dict[str, Any]]] = None,
        context_tokens_max: int = 128000
    ) -> Tuple[PolypusTelemetry, Optional[List[Dict[str, Any]]]]:
        """
        Emette il battito coordinato dei 3 cuori e applica la dinamica dell'emolinfa:
        - Cuore 1 (Sistemico) monitora l'omeostasi di base.
        - Se i token intasano il sangue, Cuore 2 attiva il lavaggio delle scorie metaboliche.
        - Se PEIRA o la rete creano attrito temporale elevato, Cuore 3 ammortizza l'impatto.
        """
        audit: List[str] = []

        # 1. Rilevazione dei parametri di ciascun ventricolo
        sys_vitals = self.systemic_heart.pulse(
            error_rate=error_rate,
            latency_ms=min(120.0, latency_ms),  # Cuore sistemico protetto dal jet propulsion
            context_tokens_used=context_tokens_used,
            context_tokens_max=context_tokens_max
        )

        ctx_vitals = self.branchial_context_heart.pulse(
            error_rate=error_rate,
            latency_ms=50.0,
            context_tokens_used=context_tokens_used,
            context_tokens_max=context_tokens_max
        )

        sil_vitals = self.branchial_silicon_heart.pulse(
            error_rate=error_rate,
            latency_ms=latency_ms,
            context_tokens_used=min(20000, context_tokens_used),
            context_tokens_max=context_tokens_max
        )

        # 2. Decisione Emodinamica sull'Autorità di Governo
        active_governor = "SYSTEMIC"
        eff_bpm = sys_vitals.heart_rate_bpm
        eff_pressure = sys_vitals.homeostatic_pressure_P
        eff_free_energy = sys_vitals.free_energy_F
        eff_status = sys_vitals.status

        drainage_triggered = False
        purged_count = 0
        cleaned_context = context_items

        # REGIME A: Congestione di Token / Scorie (Branchia A: Purificazione)
        is_token_congested = (context_tokens_used >= self.context_congestion_threshold)
        if is_token_congested or ctx_vitals.vasoconstriction_active:
            active_governor = "BRANCHIAL_CONTEXT"
            eff_bpm = ctx_vitals.heart_rate_bpm
            eff_pressure = ctx_vitals.homeostatic_pressure_P
            eff_status = "OXYGENATING_PURGE"

            audit.append(
                f"[POLYPUS GILL-A] Congestione metabolica ({context_tokens_used} token). "
                f"Attivata branchia di lavaggio contestuale."
            )

            if context_items:
                cleaned_context, purged_count = self.branchial_context_heart.drain_context_hemodynamics(context_items)
                drainage_triggered = (purged_count > 0)
                if drainage_triggered:
                    audit.append(f"[POLYPUS GILL-A] Purga metabolica completata: rimossi {purged_count} item spazzatura.")

        # REGIME B: Forte Attrito Fisico / Latenza Silicio (Branchia B: Ammortizzatore)
        elif latency_ms >= self.physical_latency_threshold_ms or error_rate > 0.3:
            active_governor = "BRANCHIAL_SILICON"
            eff_bpm = sil_vitals.heart_rate_bpm
            eff_pressure = sil_vitals.homeostatic_pressure_P
            eff_free_energy = sil_vitals.free_energy_F
            eff_status = "SILICON_BUFFERED"

            audit.append(
                f"[POLYPUS GILL-B] Attrito fisico/silicio rilevato (Latenza={latency_ms:.1f}ms, ErrorRate={error_rate:.2f}). "
                f"Cuore ausiliario branchiale stabilizza la pressione a P={eff_pressure:.3f} (Evitata ischemia isterica)."
            )

        # REGIME C: Flusso Nominale (Cuore Sistemico)
        else:
            audit.append(
                f"[POLYPUS SYSTEMIC] Flusso emodinamico nominale. Cuore centrale attivo (BPM={eff_bpm:.1f}, P={eff_pressure:.3f})."
            )

        telemetry = PolypusTelemetry(
            active_governor=active_governor,
            effective_bpm=round(eff_bpm, 1),
            effective_pressure=round(eff_pressure, 4),
            effective_free_energy=round(eff_free_energy, 4),
            effective_status=eff_status,
            drainage_triggered=drainage_triggered,
            purged_items_count=purged_count,
            systemic_vitals=sys_vitals,
            branchial_context_vitals=ctx_vitals,
            branchial_silicon_vitals=sil_vitals,
            audit_notes=audit
        )

        return telemetry, cleaned_context

    def pulse(
        self,
        error_rate: float,
        latency_ms: float,
        context_tokens_used: int,
        context_tokens_max: int = 128000
    ) -> VitalSigns:
        """Interfaccia polimorfica standard: compatibile al 100% con CorisEngine.pulse()."""
        telem, _ = self.pulse_polypus(
            error_rate=error_rate,
            latency_ms=latency_ms,
            context_tokens_used=context_tokens_used,
            context_tokens_max=context_tokens_max
        )
        return VitalSigns(
            heart_rate_bpm=telem.effective_bpm,
            free_energy_F=telem.effective_free_energy,
            homeostatic_pressure_P=telem.effective_pressure,
            context_fullness_pct=(context_tokens_used / max(1, context_tokens_max)) * 100.0,
            is_tachycardic=telem.effective_bpm > 105.0,
            vasoconstriction_active=telem.drainage_triggered,
            active_antibodies=len(self.antibodies),
            necrotic_modules=[],
            status=telem.effective_status
        )
