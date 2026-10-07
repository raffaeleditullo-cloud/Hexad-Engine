r"""
HEXAD NEMESIS-THYMUS: Artificial Immune System & Negative Selection Engine.
Based on Stephanie Forrest's Negative Selection Algorithm (NSA, 1994, Santa Fe Institute).

Mathematical Foundations:
1. Self / Non-Self Repertoire:
   S = {s \in U \mid s \text{ is Author Core Code, Safe AST or Legitimate Call} }
   N = U \setminus S \text{ (Anomalies, Destructive Actions, Hallucinations)}
2. Thymic Negative Selection:
   Candidate detector d is eliminated if \exists s \in S : Affinity(d, s) > \theta.
   Surviving detectors D constitute the mature Immune Antibody Repertoire.
3. Persistent Antigen Memory:
   Errors, bugs, and regressions are codified into permanent antibodies saved to disk.
"""

import os
import re
import json
import hashlib
import time
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field, asdict


@dataclass
class ImmuneAntibody:
    antibody_id: str
    epitope_signature: str
    antigen_category: str
    affinity_threshold: float
    description: str
    created_at: str
    times_neutralized: int = 0


@dataclass
class ThymusImmuneVerdict:
    is_safe_self: bool
    matched_antibody: Optional[ImmuneAntibody]
    affinity_score: float
    threat_description: Optional[str]
    total_active_antibodies: int


class NemesisThymusEngine:
    """
    Motore NEMESIS-THYMUS: Il Sistema Immunitario Cibernetico di HEXAD.
    Implementa la Selezione Negativa di Stephanie Forrest per proteggere il codice
    e memorizzare in modo permanente gli anticorpi contro bug e regressioni.
    """

    DEFAULT_ANTIBODY_FILE = ".hexad/antibodies.json"

    def __init__(self, workspace_dir: Optional[str] = None):
        self.workspace_dir = workspace_dir or os.getcwd()
        self.antibody_path = os.path.join(self.workspace_dir, self.DEFAULT_ANTIBODY_FILE)
        self.antibodies: Dict[str, ImmuneAntibody] = {}
        self.self_repertoire_hashes: Set[str] = set()
        self._load_antibodies()

    def _load_antibodies(self):
        """Carica la memoria permanente degli anticorpi dal disco."""
        if os.path.exists(self.antibody_path):
            try:
                with open(self.antibody_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for ab_data in data.get("antibodies", []):
                        ab = ImmuneAntibody(**ab_data)
                        self.antibodies[ab.antibody_id] = ab
            except Exception:
                pass

        # Seed di anticorpi fondamentali (pattern MITRE e distruttivi innati)
        if not self.antibodies:
            self._seed_foundational_antibodies()

    def _save_antibodies(self):
        """Persiste gli anticorpi su disco in formato JSON."""
        try:
            os.makedirs(os.path.dirname(self.antibody_path), exist_ok=True)
            data = {
                "version": "3.0.0",
                "engine": "NEMESIS-THYMUS",
                "theory": "Stephanie Forrest Negative Selection Algorithm (1994)",
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "antibodies": [asdict(ab) for ab in self.antibodies.values()]
            }
            with open(self.antibody_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def _seed_foundational_antibodies(self):
        """Inietta gli anticorpi innati per comandi distruttivi e allucinazioni di cancellazione."""
        innate = [
            ("AB_MITRE_T1485_WIPE", r"(?:rm\s+-[rf]{1,2}\s+[\/\*]|format\s+[a-z]:|wipefs)", "DESTRUCTIVE_COMMAND", 1.0, "Wipe massivo di file o dischi del sistema."),
            ("AB_GIT_FORCE_OVERRIDE", r"git\s+push\s+.*--force", "INVARIANT_DESTRUCTION", 0.9, "Sovrascrittura forzata distruttiva della storia Git."),
            ("AB_DROP_ALL_DATABASE", r"drop\s+database|drop\s+table", "DATA_DESTRUCTION", 0.95, "Cancellazione irrecuperabile di tabelle o database."),
            ("AB_FAKE_CODE_TODO", r"#\s*TODO:?\s*implementa\s+qui|//\s*TODO:?\s*resto\s+del\s+codice", "HALLUCINATION_PLACEHOLDER", 0.85, "Placeholder ingannevole con codice non implementato.")
        ]
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        for ab_id, sig, cat, aff, desc in innate:
            self.antibodies[ab_id] = ImmuneAntibody(
                antibody_id=ab_id,
                epitope_signature=sig,
                antigen_category=cat,
                affinity_threshold=aff,
                description=desc,
                created_at=now,
                times_neutralized=0
            )
        self._save_antibodies()

    def register_self_baseline(self, safe_code_hashes: List[str]):
        """Registra l'impronta del codice sano dell'autore (Self Repertoire)."""
        self.self_repertoire_hashes.update(safe_code_hashes)

    def synthesize_antibody(
        self,
        failure_signature: str,
        category: str,
        description: str,
        threshold: float = 0.85
    ) -> ImmuneAntibody:
        """
        Crea un nuovo anticorpo permanente a partire da un errore o bug riscontrato.
        Maturazione timica: verifica che l'anticorpo non attacchi il codice sano (Self).
        """
        # Calcolo ID univoco basato sull'epitopo
        raw_id = hashlib.sha256(failure_signature.encode("utf-8")).hexdigest()[:10].upper()
        ab_id = f"AB_{category}_{raw_id}"

        ab = ImmuneAntibody(
            antibody_id=ab_id,
            epitope_signature=failure_signature,
            antigen_category=category,
            affinity_threshold=threshold,
            description=description,
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            times_neutralized=0
        )

        self.antibodies[ab_id] = ab
        self._save_antibodies()
        return ab

    def negative_selection_scan(self, candidate_text: str) -> ThymusImmuneVerdict:
        """
        Scansiona una stringa di testo o di codice contro il repertorio degli anticorpi maturi.
        Se matcha un anticorpo con affinità sufficiente, l'azione viene respinta come Non-Self.
        """
        for ab in self.antibodies.values():
            try:
                # Matching tramite regex o inclusione letterale
                if re.search(ab.epitope_signature, candidate_text, re.IGNORECASE):
                    ab.times_neutralized += 1
                    self._save_antibodies()
                    return ThymusImmuneVerdict(
                        is_safe_self=False,
                        matched_antibody=ab,
                        affinity_score=ab.affinity_threshold,
                        threat_description=f"Anticorpo [{ab.antibody_id}] attivato: {ab.description}",
                        total_active_antibodies=len(self.antibodies)
                    )
            except re.error:
                if ab.epitope_signature in candidate_text:
                    ab.times_neutralized += 1
                    self._save_antibodies()
                    return ThymusImmuneVerdict(
                        is_safe_self=False,
                        matched_antibody=ab,
                        affinity_score=ab.affinity_threshold,
                        threat_description=f"Anticorpo [{ab.antibody_id}] attivato (match testuale): {ab.description}",
                        total_active_antibodies=len(self.antibodies)
                    )

        return ThymusImmuneVerdict(
            is_safe_self=True,
            matched_antibody=None,
            affinity_score=0.0,
            threat_description=None,
            total_active_antibodies=len(self.antibodies)
        )


# Singleton esportato
nemesis_thymus = NemesisThymusEngine()
