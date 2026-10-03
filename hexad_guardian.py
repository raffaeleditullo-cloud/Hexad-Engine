"""
HEXAD Guardian: The Sovereign Lock, AST Digest & Author Invariance Engine.

Protects author-defined architecture and core functions from unauthorized LLM mutation.
Enforces the Sovereign Invariant Principle:
1. Author's core functions are immutable by default (SOVEREIGN_CORE).
2. Safe extensions and additions are permitted (EXTENSION_PERMITTED).
3. Resolved bugs are permanently quarantined as immune antibodies (ANTI_REGRESSION).
"""

import os
import sys
import ast
import json
import hashlib
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple, Set


@dataclass
class AuthorInvariant:
    """Rappresentazione immutabile di una funzione o classe dell'autore."""
    symbol_name: str
    file_path: str
    kind: str                    # "function", "async_function", "class"
    line_start: int
    line_end: int
    arg_signature: List[str]
    ast_structural_hash: str     # Hash semantico dell'albero sintattico
    docstring: Optional[str] = None
    criticality: str = "SOVEREIGN_CORE" # "SOVEREIGN_CORE" | "EXTENSION_PERMITTED"
    registered_at: float = field(default_factory=time.time)
    constant_value_hash: Optional[str] = None  # Hash dei valori costanti (None nelle baseline precedenti)


@dataclass
class InvarianceVerificationResult:
    """Esito del controllo pre-flight di invarianza prima della scrittura su disco."""
    is_authorized: bool
    status: str                  # "APPROVED_SAFE_EXTENSION", "APPROVED_CONSTANT_DRIFT_REVIEW", "APPROVED_SOVEREIGN_OVERRIDE", "REJECTED_AUTHOR_VIOLATION"
    target_file: str
    violated_symbols: List[str] = field(default_factory=list)
    added_symbols: List[str] = field(default_factory=list)
    drifted_symbols: List[str] = field(default_factory=list)  # Struttura intatta, valori costanti cambiati
    reason: Optional[str] = None
    quarantine_matched: Optional[str] = None


class HexadGuardian:
    """
    Il Guardiano Cibernetico del DNA del Progetto.
    Impedisce allucinazioni distruttive e garantisce che le logiche dell'autore non vengano toccate.
    """

    def __init__(self, workspace_dir: str):
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.hexad_dir = os.path.join(self.workspace_dir, ".hexad")
        self.invariants_file = os.path.join(self.hexad_dir, "invariants.json")
        self.antibodies_file = os.path.join(self.hexad_dir, "antibodies.json")
        self.invariants: Dict[str, Dict[str, AuthorInvariant]] = {} # file -> symbol -> AuthorInvariant
        self.antibodies: List[Dict[str, Any]] = []
        self.integrity_status: str = "READY"
        self.integrity_error: Optional[str] = None

        self._ensure_storage()
        self._load_state()

    def _ensure_storage(self):
        os.makedirs(self.hexad_dir, exist_ok=True)

    def _load_state(self):
        # Carica invarianti
        if os.path.exists(self.invariants_file):
            try:
                with open(self.invariants_file, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    for file_rel, syms in raw.items():
                        self.invariants[file_rel] = {}
                        for sym_name, s_data in syms.items():
                            self.invariants[file_rel][sym_name] = AuthorInvariant(**s_data)
            except Exception as e:
                # FAIL-CLOSED: Non silenziare la corruzione della baseline
                self.integrity_status = "INTEGRITY_FAILURE"
                self.integrity_error = f"Corruzione invariants.json: {str(e)}"
                return

        # Carica anticorpi anti-regressione
        if os.path.exists(self.antibodies_file):
            try:
                with open(self.antibodies_file, "r", encoding="utf-8") as f:
                    self.antibodies = json.load(f)
            except Exception as e:
                # FAIL-CLOSED: Non silenziare la corruzione degli anticorpi
                self.integrity_status = "INTEGRITY_FAILURE"
                self.integrity_error = f"Corruzione antibodies.json: {str(e)}"
                return

    def _save_state(self):
        # Salva invarianti
        serializable = {}
        for f_path, syms in self.invariants.items():
            serializable[f_path] = {s_name: asdict(inv) for s_name, inv in syms.items()}
        with open(self.invariants_file, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2)

        # Salva anticorpi
        with open(self.antibodies_file, "w", encoding="utf-8") as f:
            json.dump(self.antibodies, f, indent=2)

    # =========================================================================
    # 1. BOOTSTRAP DEL PROGETTO: Mappatura del DNA dell'Autore
    # =========================================================================
    def bootstrap_project(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Scansiona l'intero repository, estrae l'AST di ogni file Python e blocca
        le funzioni dell'autore come nodi sacri invarianti.
        """
        if self.integrity_status == "INTEGRITY_FAILURE" and not force_refresh:
            return {
                "status": "INTEGRITY_FAILURE",
                "error": self.integrity_error,
                "workspace": self.workspace_dir,
                "action_required": "Eseguire bootstrap con force_refresh=True per sanare e ricostruire la baseline."
            }

        if force_refresh:
            self.integrity_status = "READY"
            self.integrity_error = None
            self.invariants = {}

        indexed_files = 0
        indexed_symbols = 0

        for root, dirs, files in os.walk(self.workspace_dir):
            if any(ign in root for ign in [".git", ".hexad", "__pycache__", "node_modules", "venv", ".venv"]):
                continue
            for file in files:
                if file.endswith(".py"):
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, self.workspace_dir)

                    if rel_p not in self.invariants or force_refresh:
                        syms = self._extract_ast_invariants(full_p, rel_p)
                        if syms:
                            self.invariants[rel_p] = syms
                            indexed_files += 1
                            indexed_symbols += len(syms)

        self._save_state()

        return {
            "status": "BOOTSTRAP_COMPLETE",
            "workspace": self.workspace_dir,
            "indexed_files": indexed_files,
            "total_invariants_protected": sum(len(s) for s in self.invariants.values()),
            "storage_path": self.invariants_file
        }

    # =========================================================================
    # 2. VERIFICA DI INVARIANZA PRE-FLIGHT (Il Filtro Sovrano)
    # =========================================================================
    def verify_proposed_edit(
        self,
        target_file_path: str,
        proposed_content: str,
        user_prompt: str = "",
        explicit_override: bool = False
    ) -> InvarianceVerificationResult:
        """
        Controlla prima della scrittura:
        1. Se il codice proposto contiene pattern di bug già registrati (Anti-Regressione).
        2. Se il codice proposto sovrascrive o cancella funzioni protette dell'autore.
        3. Autorizza solo estensioni sicure o modifiche esplicitamente ordinate dall'autore.

        Soglia graduata:
        - struttura AST cambiata              -> REJECTED_AUTHOR_VIOLATION (salvo override)
        - struttura intatta, costanti cambiate -> APPROVED_CONSTANT_DRIFT_REVIEW (autorizzato, da revisionare)
        - nessun cambiamento sui simboli sacri -> APPROVED_SAFE_EXTENSION
        """
        # 0. Sovereign Fail-Closed: se la baseline è corrotta, blocca qualsiasi mutazione
        if self.integrity_status == "INTEGRITY_FAILURE":
            return InvarianceVerificationResult(
                is_authorized=False,
                status="REJECTED_INTEGRITY_FAILURE",
                target_file=target_file_path,
                reason=f"SOVEREIGN FAIL-CLOSED: Il database degli invarianti o anticorpi è corrotto ({self.integrity_error}). Modifica bloccata per salvaguardia di sicurezza."
            )

        # Normalizzazione canonica: "a/b.py", ".\a\b.py" e il percorso assoluto sono lo stesso file
        rel_p = self._resolve_workspace_path(target_file_path)
        if rel_p is None:
            return InvarianceVerificationResult(
                is_authorized=False,
                status="REJECTED_OUTSIDE_WORKSPACE",
                target_file=target_file_path,
                reason="Il percorso proposto risolve fuori dal workspace protetto da HEXAD."
            )

        # 1. Check Anti-Regressione contro anticorpi linfatici noti
        matched_ab = self.check_regression_risk(proposed_content)
        if matched_ab:
            return InvarianceVerificationResult(
                is_authorized=False,
                status="REJECTED_REGRESSION_DETECTED",
                target_file=rel_p,
                reason=f"ANTI-REGRESSION BLOCKED: Rilevato pattern di bug già risolto in passato ({matched_ab.get('signature')}).",
                quarantine_matched=matched_ab.get("signature")
            )

        # Se il file non era precedentemente indicizzato, è un file nuovo -> Autorizzato come estensione
        if rel_p not in self.invariants:
            if os.path.exists(os.path.join(self.workspace_dir, rel_p)):
                # Esiste su disco ma non nella baseline (creato dopo il bootstrap o mai indicizzato):
                # autorizzato, ma segnalato, perché nessun invariante lo protegge
                return InvarianceVerificationResult(
                    is_authorized=True,
                    status="APPROVED_UNINDEXED_FILE_REVIEW",
                    target_file=rel_p,
                    reason="File esistente non presente nella baseline di invarianti: modifica autorizzata, da revisionare."
                )
            return InvarianceVerificationResult(
                is_authorized=True,
                status="APPROVED_SAFE_EXTENSION",
                target_file=rel_p,
                reason="Nuovo file o modulo non appartenente al core primario dell'autore."
            )

        # 2. Parsing AST del codice proposto
        try:
            proposed_tree = ast.parse(proposed_content, filename=rel_p)
        except SyntaxError as se:
            return InvarianceVerificationResult(
                is_authorized=False,
                status="REJECTED_SYNTAX_ERROR",
                target_file=rel_p,
                reason=f"Errore di sintassi nel codice proposto: riga {se.lineno}: {se.msg}"
            )

        proposed_symbols: Dict[str, str] = {} # sym_name -> ast_hash
        proposed_values: Dict[str, str] = {}  # sym_name -> hash dei valori costanti
        for node in ast.walk(proposed_tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                h = self._compute_ast_structural_hash(node)
                proposed_symbols[node.name] = h
                proposed_values[node.name] = self._compute_ast_constant_hash(node)
        for name, node in self._module_constant_nodes(proposed_tree).items():
            proposed_symbols[name] = self._compute_ast_structural_hash(node)
            proposed_values[name] = self._compute_ast_constant_hash(node)

        # 3. Analisi delle alterazioni rispetto agli invarianti dell'autore
        protected_syms = self.invariants[rel_p]
        violated_symbols = []
        added_symbols = []
        drifted_symbols = []

        for name, inv in protected_syms.items():
            if inv.criticality == "SOVEREIGN_CORE":
                if name not in proposed_symbols:
                    # Funzione cancellata!
                    violated_symbols.append(f"{name} [DELETED]")
                elif proposed_symbols[name] != inv.ast_structural_hash:
                    # Funzione alterata nella sua logica interna!
                    violated_symbols.append(f"{name} [LOGIC_MUTATED]")
                elif inv.constant_value_hash and proposed_values[name] != inv.constant_value_hash:
                    # Struttura intatta ma soglie, default o letterali cambiati
                    drifted_symbols.append(f"{name} [CONSTANT_DRIFT]")

        for name in proposed_symbols:
            if name not in protected_syms:
                added_symbols.append(name)

        # 4. Verdetto di Sovranità
        if violated_symbols:
            # Controllo se l'utente ha chiesto esplicitamente di toccare questo file/funzione
            user_has_authorized = explicit_override or self._check_explicit_intent(user_prompt, rel_p, violated_symbols)

            if user_has_authorized:
                # Sovranità umana esplicita: l'autore ha ordinato la modifica
                return InvarianceVerificationResult(
                    is_authorized=True,
                    status="APPROVED_SOVEREIGN_OVERRIDE",
                    target_file=rel_p,
                    violated_symbols=violated_symbols,
                    added_symbols=added_symbols,
                    drifted_symbols=drifted_symbols,
                    reason="Modifica autorizzata esplicitamente dal prompt dell'autore umano."
                )
            else:
                # VIOLAZIONE: L'AI ha cercato di cambiare la logica di testa sua
                return InvarianceVerificationResult(
                    is_authorized=False,
                    status="REJECTED_AUTHOR_VIOLATION",
                    target_file=rel_p,
                    violated_symbols=violated_symbols,
                    added_symbols=added_symbols,
                    drifted_symbols=drifted_symbols,
                    reason=(
                        f"TENTATIVO DI MANOMISSIONE NON AUTORIZZATO: Le seguenti logiche dell'autore sono state alterate senza permesso esplicito: {', '.join(violated_symbols)}. "
                        f"L'azione è stata bloccata per preservare l'integrità del progetto."
                    )
                )

        if drifted_symbols:
            # Categorizzazione Sovrana del Drift:
            # SECURITY_CONSTANT / CONTROL_LIMIT / CRYPTO / AUTH -> BLOCK (salvo esplicito override)
            # CONFIG_CONSTANT / GENERAL -> REVIEW / ALLOW
            security_crypto_keywords = [
                "SECRET", "PASSWD", "PASSWORD", "API_KEY", "PRIVATE_KEY", 
                "AUTH_TOKEN", "ACCESS_TOKEN", "CIPHER", "SECURITY",
                "RATE_LIMIT", "MAX_RETRIES", "LOGIN_ATTEMPTS", "SSL_CERT", "JWT",
                "CONTROL_LIMIT"
            ]
            critical_drifted = []
            for s in drifted_symbols:
                clean_sym = s.replace(" [CONSTANT_DRIFT]", "").strip()
                sym_obj = protected_syms.get(clean_sym)
                is_mod_const = sym_obj and getattr(sym_obj, "kind", "") == "module_constant"
                s_upper = clean_sym.upper()
                if is_mod_const and any(kw in s_upper for kw in security_crypto_keywords):
                    critical_drifted.append(s)

            if critical_drifted:
                user_has_authorized = explicit_override or self._check_explicit_intent(user_prompt, rel_p, critical_drifted)
                if user_has_authorized:
                    return InvarianceVerificationResult(
                        is_authorized=True,
                        status="APPROVED_SOVEREIGN_OVERRIDE",
                        target_file=rel_p,
                        drifted_symbols=drifted_symbols,
                        reason="Modifica a costanti critiche autorizzata esplicitamente dal prompt dell'autore."
                    )
                else:
                    return InvarianceVerificationResult(
                        is_authorized=False,
                        status="REJECTED_CRITICAL_CONSTANT_DRIFT",
                        target_file=rel_p,
                        violated_symbols=critical_drifted,
                        drifted_symbols=drifted_symbols,
                        reason=(
                            f"BLOCCO SOVRANO COSTANTI CRITICHE: Rilevato drift su parametri di sicurezza/controllo: "
                            f"{', '.join(critical_drifted)}. Azione bloccata per prevenire allentamento vincoli (FAIL-CLOSED). "
                            f"Classificazione: SECURITY_CONSTANT / CONTROL_LIMIT -> BLOCK."
                        )
                    )

            # Soglia intermedia per costanti ordinarie/configurative
            return InvarianceVerificationResult(
                is_authorized=True,
                status="APPROVED_CONSTANT_DRIFT_REVIEW",
                target_file=rel_p,
                added_symbols=added_symbols,
                drifted_symbols=drifted_symbols,
                reason=(
                    f"Struttura delle logiche dell'autore intatta, ma valori costanti ordinari modificati in: {', '.join(drifted_symbols)}. "
                    f"Modifica autorizzata con revisione (CONFIG_CONSTANT -> REVIEW)."
                )
            )

        return InvarianceVerificationResult(
            is_authorized=True,
            status="APPROVED_SAFE_EXTENSION",
            target_file=rel_p,
            added_symbols=added_symbols,
            reason="Tutte le logiche dell'autore sono state preservate intatte."
        )

    # =========================================================================
    # 3. MEMORIA LINFATICA ANTI-REGRESSIONE (Coris/Peira Bridge)
    # =========================================================================
    def quarantine_regression(
        self,
        signature: str,
        failure_trace: str,
        neutralization_rule: str = "BLOCK_IDENTICAL_PATTERN"
    ) -> Dict[str, Any]:
        """Registra un bug risolto per bloccarlo per sempre da future generazioni."""
        ab = {
            "signature": signature,
            "failure_trace": failure_trace[:300],
            "rule": neutralization_rule,
            "created_at": time.time()
        }
        self.antibodies.append(ab)
        self._save_state()
        return ab

    def check_regression_risk(self, code_snippet: str) -> Optional[Dict[str, Any]]:
        """Rileva se uno snippet contiene un pattern noto di fallimento pregresso."""
        for ab in self.antibodies:
            sig = ab.get("signature", "")
            if sig and (sig in code_snippet or hashlib.sha256(code_snippet.encode()).hexdigest()[:12] == sig):
                return ab
        return None

    # =========================================================================
    # METODI AUSILIARI DI HASHING SEMANTICO
    # =========================================================================
    def _extract_ast_invariants(self, file_path: str, rel_path: str) -> Dict[str, AuthorInvariant]:
        invariants = {}
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            tree = ast.parse(content, filename=file_path)

            for node in ast.iter_child_nodes(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    kind = "class" if isinstance(node, ast.ClassDef) else ("async_function" if isinstance(node, ast.AsyncFunctionDef) else "function")
                    args = [a.arg for a in getattr(node, "args", ast.arguments()).args] if hasattr(node, "args") else []
                    h = self._compute_ast_structural_hash(node)

                    invariants[node.name] = AuthorInvariant(
                        symbol_name=node.name,
                        file_path=rel_path,
                        kind=kind,
                        line_start=node.lineno,
                        line_end=getattr(node, "end_lineno", node.lineno + 10),
                        arg_signature=args,
                        ast_structural_hash=h,
                        docstring=ast.get_docstring(node),
                        criticality="SOVEREIGN_CORE",
                        constant_value_hash=self._compute_ast_constant_hash(node)
                    )

            # Costanti di modulo (soglie, limiti, configurazione): stesse regole dei simboli
            for name, node in self._module_constant_nodes(tree).items():
                invariants[name] = AuthorInvariant(
                    symbol_name=name,
                    file_path=rel_path,
                    kind="module_constant",
                    line_start=node.lineno,
                    line_end=getattr(node, "end_lineno", node.lineno),
                    arg_signature=[],
                    ast_structural_hash=self._compute_ast_structural_hash(node),
                    criticality="SOVEREIGN_CORE",
                    constant_value_hash=self._compute_ast_constant_hash(node)
                )
        except Exception:
            pass
        return invariants

    @staticmethod
    def _module_constant_nodes(tree: ast.AST) -> Dict[str, ast.AST]:
        """
        Costanti di modulo per convenzione PEP 8: assegnamenti semplici a un nome in
        MAIUSCOLO (MAX_RETRY = 3, _TIMEOUT: float = 2.0). Le variabili di lavoro degli
        script (img, arr, threshold...) e i dunder come __all__ restano libere.
        """
        nodes: Dict[str, ast.AST] = {}
        for node in getattr(tree, "body", []):
            if isinstance(node, ast.Assign):
                names = [t.id for t in node.targets if isinstance(t, ast.Name)]
                if len(names) != len(node.targets):
                    continue  # Destrutturazioni e attributi: fuori dal perimetro
            elif isinstance(node, ast.AnnAssign) and node.value is not None and isinstance(node.target, ast.Name):
                names = [node.target.id]
            else:
                continue
            for name in names:
                bare = name.lstrip("_")
                is_dunder = name.startswith("__") and name.endswith("__")
                if not is_dunder and bare and bare == bare.upper() and any(c.isalpha() for c in bare):
                    nodes[name] = node
        return nodes

    def _compute_ast_structural_hash(self, node: ast.AST) -> str:
        """Calcola un hash canonico della struttura dei nodi AST (indipendente da spaziature)."""
        structure = []
        for sub in ast.walk(node):
            structure.append(sub.__class__.__name__)
            if isinstance(sub, ast.Name):
                structure.append(sub.id)
            elif isinstance(sub, ast.Attribute):
                structure.append(sub.attr)
            elif isinstance(sub, ast.Constant):
                structure.append(str(type(sub.value)))
        digest = hashlib.sha256("::".join(structure).encode()).hexdigest()[:16]
        return digest

    def _resolve_workspace_path(self, target_file_path: str) -> Optional[str]:
        """
        Converte qualsiasi forma del percorso (relativa, assoluta, con '/' o '\\', con './')
        nella chiave canonica usata dalla baseline. Ritorna None se il file è fuori dal workspace.
        """
        try:
            abs_p = os.path.abspath(os.path.join(self.workspace_dir, target_file_path))
            rel = os.path.normpath(os.path.relpath(abs_p, self.workspace_dir))
        except ValueError:
            return None  # Unità diversa su Windows
        if rel == os.pardir or rel.startswith(os.pardir + os.sep) or os.path.isabs(rel):
            return None
        # Su Windows il filesystem ignora le maiuscole: allinea alla chiave già registrata
        wanted = os.path.normcase(rel)
        for key in self.invariants:
            if os.path.normcase(os.path.normpath(key)) == wanted:
                return key
        return rel

    def _compute_ast_constant_hash(self, node: ast.AST) -> str:
        """
        Hash dei valori costanti del nodo (numeri, booleani, None, stringhe, default degli argomenti),
        complementare all'hash strutturale che registra solo il tipo delle costanti.
        Le docstring sono escluse: modificarle non altera la logica.
        """
        docstring_ids = set()
        for sub in ast.walk(node):
            if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and sub.body:
                first = sub.body[0]
                if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                    docstring_ids.add(id(first.value))

        values = []
        for sub in ast.walk(node):
            if isinstance(sub, ast.Constant) and id(sub) not in docstring_ids:
                values.append(f"{type(sub.value).__name__}:{sub.value!r}")
        return hashlib.sha256("::".join(values).encode()).hexdigest()[:16]

    def _check_explicit_intent(self, prompt: str, rel_file: str, violated_syms: List[str]) -> bool:
        """Verifica se l'umano ha espressamente ordinato di modificare il file o il simbolo."""
        if not prompt:
            return False
        p_lower = prompt.lower()
        file_base = os.path.basename(rel_file).lower()

        # Parole chiave di intenzione di modifica
        change_verbs = [
            # Italiano
            "modifica", "cambia", "aggiorna", "riscrivi", "correggi", "elimina", "rinomina",
            # Inglese
            "refactor", "delete", "remove", "update", "rewrite", "fix", "rename",
            "replace", "eliminate", "drop", "destroy", "rework", "overwrite", "edit",
        ]
        has_change_verb = any(v in p_lower for v in change_verbs)

        if has_change_verb:
            if file_base in p_lower:
                return True
            for sym in violated_syms:
                clean_sym = sym.split()[0].lower()
                if clean_sym in p_lower:
                    return True

        return False
