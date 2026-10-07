"""
HEXAD Self-Awareness: risposte su se stesso ancorate alla Mappa della Verità.

Perché esiste (dal test di autoconsapevolezza, ottobre 2026):
- le domande su se stesso ricevevano testi preimpostati falsi invece della memoria;
- senza contesto il modello inventava scienziati, formule e meccanismi;
- confondeva le due cartelle (prototipo / progetto principale) perché i motori hanno lo stesso nome;
- riproponeva come novità funzioni che esistono già;
- "fai una ricerca per migliorarti" cercava l'intera frase sul web.

Questo modulo:
1. riconosce le domande su HEXAD (classify);
2. seleziona solo le schede pertinenti della mappa, etichettate per cartella (select_context);
3. fa rispondere il modello con regole rigide anti-invenzione (answer);
4. per l'automiglioramento: sceglie un punto debole, crea una query mirata, cerca sul web
   e propone citando le fonti, dichiarandole NON verificate (research log su file per la revisione).
"""

import json
import os
import re
import time
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

MAP_CATEGORY = "AUTOMAPPA_HEXAD"
SCI_CATEGORY = "SCIENZIATO_O_TECNOLOGIA"
SHARED_ENGINES = ["mneme", "coris", "anima", "demon", "peira", "oculus", "lunar", "daedalus"]

FOLDER_LABEL = {
    "prototipo": "PROTOTIPO, cartella SKILL DEMON/hexad_learner",
    "principale": "PROGETTO PRINCIPALE, cartella HEXAD/Hexad-Engine",
    "entrambe": "PANORAMICA, riguarda entrambe le cartelle",
}

# parola citata dall'utente -> schede della mappa
ALIASES: Dict[str, List[str]] = {
    "guardian": ["hexad guardian"], "guardiano del codice": ["hexad guardian"],
    "mcp": ["hexad mcp"], "strumenti": ["hexad mcp"],
    "action gate": ["demon action gate"], "filtro dei comandi": ["demon action gate"],
    "agent filter": ["demon agent filter"],
    "polypus": ["polypus"], "nemesis": ["nemesis"], "ariadne": ["ariadne"],
    "invarianza": ["invarianza ortogonale"], "ortogonal": ["invarianza ortogonale"],
    "corteccia": ["corteccia neurale", "qwen"], "qwen": ["corteccia neurale", "qwen"],
    "llm": ["corteccia neurale", "qwen"], "modello linguistico": ["corteccia neurale", "qwen"],
    "ollama": ["corteccia neurale"], "oracolo": ["oracolo sovrano"],
    "nous": ["nous"], "keryx": ["keryx"], "hermes": ["keryx"], "myia": ["myia"],
    "kalani": ["kalani"], "voce": ["kalani"],
    "hexad core": ["hexad principale"], "hexad_core": ["hexad principale"],
    "prototipo": ["hexad learner"], "hexad_learner": ["hexad learner"], "skill demon": ["hexad learner"],
    "progetto principale": ["hexad principale"], "hexad-engine": ["hexad principale"],
}
for _e in SHARED_ENGINES:
    ALIASES[_e] = [_e, f"{_e} prototipo", f"{_e} principale"]
ALIASES["lamarck"] = ["nemesis"]

# Nomi che sono anche parole comuni: valgono come "motore" solo in contesti espliciti
AMBIGUOUS = {"anima", "lunar", "nous", "voce", "strumenti", "prototipo", "lamarck", "oracolo", "corteccia"}

HARDWARE_RE = re.compile(r"\b(cpu|ram|gpu|vram|hardware|temperatur\w*|processore|scheda video|prestazioni del pc|disco)\b")
SECOND_PERSON_RE = re.compile(r"\b(tu|ti|tuo|tua|tuoi|tue|sei|hai|sai|puoi|riesci|funzioni|ricordi|usi|conosci|te stesso)\b")
SELF_TOPIC_RE = re.compile(
    r"(motor|struttur|architettur|costruit|\bfatto\b|formul|scienziat|teori|debol|limit|critic|miglior|cartell|"
    r"progett|codice|\bfile\b|capacit|ricord|errori|allucin|proteg|organi|component|algoritm|modul|automiglior|"
    r"funzion|ispirat|basat|\bmappa\b)"
)
RESEARCH_RE = re.compile(r"(ricerc|\bcerca|indag|studia|\btrova|informati)")
IMPROVE_RE = re.compile(r"(miglior|risolv|limit|debol|critic|correg|potenz|soluzion|aggiust|sistem)")
WEAKNESS_RE = re.compile(r"(debol|limit|critic|miglior|problem|difett|sbagli|errori|punti deboli|aggiung|manca|proteg)")


def _norm(text: str) -> str:
    return (text or "").lower().replace("’", "'").replace("`", "'")


class HexadSelfAwareness:
    def __init__(self, mneme=None, cortex=None, workspace_dir: str = ""):
        self.mneme = mneme
        self.cortex = cortex
        ws = workspace_dir or os.path.dirname(os.path.abspath(__file__))
        self.research_log = os.path.join(ws, "research_log.jsonl")

    # ------------------------------------------------------------------ routing
    def _engine_mentions(self, raw: str) -> List[str]:
        low = _norm(raw)
        hits = []
        for alias in ALIASES:
            if not re.search(r"\b" + re.escape(alias) + r"\b", low):
                continue
            if alias in AMBIGUOUS:
                upper_form = re.search(r"\b" + re.escape(alias.upper()) + r"\b", raw or "")
                explicit = re.search(r"(motore|tuo|tua|modulo|componente)\s+(?:\w+\s+)?" + re.escape(alias), low)
                if not (upper_form or explicit):
                    continue
            hits.append(alias)
        return hits

    def classify(self, raw_text: str) -> Optional[str]:
        low = _norm(raw_text)
        if not low.strip() or HARDWARE_RE.search(low):
            return None
        mentions = self._engine_mentions(raw_text)
        about_self = bool(mentions) or (SECOND_PERSON_RE.search(low) and SELF_TOPIC_RE.search(low))
        if re.search(r"\b(come sei (stato )?(fatto|costruito|nato|strutturato)|chi sei|cosa sei)\b", low):
            about_self = True
        if not about_self:
            return None
        if RESEARCH_RE.search(low) and IMPROVE_RE.search(low):
            return "SELF_IMPROVEMENT_RESEARCH"
        return "SELF_MAP_INQUIRY"

    # ------------------------------------------------------------------ contesto
    def _node(self, key: str) -> Optional[Dict[str, Any]]:
        n = self.mneme.nodes.get(key)
        if n is None:
            return None
        return n.to_dict() if hasattr(n, "to_dict") else n

    def _folder(self, nd: Dict[str, Any]) -> str:
        for p in nd.get("properties") or []:
            if isinstance(p, str) and p.startswith("cartella:"):
                return p.split(":", 1)[1]
        return "entrambe"

    def _format(self, key: str, compact: bool = False) -> str:
        nd = self._node(key)
        if not nd:
            return ""
        facts = (nd.get("verified_facts") or "").strip()
        if compact:
            facts = re.split(r"(?<=[.!?])\s+", facts)[0]
        if nd.get("category") == SCI_CATEGORY:
            label = f"RIFERIMENTO SCIENTIFICO: {key.upper()}"
        else:
            label = f"{key.upper()} ({FOLDER_LABEL.get(self._folder(nd), '')})"
        return f"[{label}]\n{facts}"

    def select_context(self, raw_text: str, improvement: bool = False, max_chars: int = 14000) -> Tuple[str, List[str]]:
        low = _norm(raw_text)
        keys: List[str] = []

        def add(*ks):
            for k in ks:
                if k in self.mneme.nodes and k not in keys:
                    keys.append(k)

        add("hexad")
        for alias in self._engine_mentions(raw_text):
            add(*ALIASES[alias])

        detail_engines = [f"{e} {v}" for e in SHARED_ENGINES for v in ("prototipo", "principale")]
        specific = len(keys) > 1

        if re.search(r"(scienziat|teori|ispirat|basat|fisic|matematic)", low):
            add(*[k for k, n in self.mneme.nodes.items() if self._node(k).get("category") == SCI_CATEGORY])
            add(*SHARED_ENGINES)
            specific = True
        if re.search(r"(formul|algoritm|calcol|equazion)", low):
            add(*detail_engines)
            specific = True
        if re.search(r"(cartell|progett|legger|analizz|scansion|\bfile\b)", low):
            add("hexad learner", "corteccia neurale", "oculus principale", "hexad guardian", "oculus prototipo")
            specific = True
        if re.search(r"(proteg|codice dell|sicurezz|modific)", low):
            add("hexad guardian", "demon action gate", "demon agent filter", "hexad mcp", "peira principale")
            specific = True
        if re.search(r"(ricord|errori|riavvi|dimentic)", low):
            add("nemesis", "mneme prototipo")
            specific = True
        if re.search(r"(allucin|invent|verific|controll)", low):
            add("demon prototipo", "demon agent filter", "corteccia neurale", "peira prototipo")
            specific = True
        if improvement or WEAKNESS_RE.search(low):
            add("punti deboli di hexad")
        add("cose già presenti in hexad")
        if not specific or re.search(r"(struttur|architettur|costruit|\bfatto\b|motor|organi|component|chi sei|cosa sei|modul)", low):
            add("hexad principale", "hexad learner", *SHARED_ENGINES, "corteccia neurale", "oracolo sovrano",
                "hexad guardian", "nemesis", "nous", "keryx", "myia")

        parts, used, total = [], [], 0
        for k in keys:
            block = self._format(k)
            if total + len(block) > max_chars:
                block = self._format(k, compact=True)
                if total + len(block) > max_chars:
                    continue
            parts.append(block)
            used.append(k)
            total += len(block) + 2
        return "\n\n".join(parts), used

    # ------------------------------------------------------------------ prompt
    @staticmethod
    def _system(creator_name: str, mappa: str) -> str:
        return (
            f"Sei HEXAD e stai parlando di TE STESSO con {creator_name}. Qui sotto c'è la tua MAPPA DELLA VERITÀ, "
            f"verificata sul tuo codice reale: è l'UNICA fonte valida su di te.\n\n"
            f"REGOLE OBBLIGATORIE:\n"
            f"1. Usa SOLO le informazioni della mappa. Se ciò che ti chiedono non c'è, dì chiaramente che non è nella tua mappa; non inventare.\n"
            f"2. Esistono DUE cartelle: il PROTOTIPO (SKILL DEMON/hexad_learner) e il PROGETTO PRINCIPALE (HEXAD/Hexad-Engine). "
            f"Molti motori hanno lo stesso nome nelle due cartelle ma fanno cose diverse: dì sempre di quale cartella parli e non "
            f"attribuire a una cartella ciò che la mappa assegna all'altra.\n"
            f"3. Distingui sempre ciò che è calcolato davvero da ciò che è solo un nome scientifico o una metafora, come dice la mappa.\n"
            f"4. Non inventare scienziati, formule, file, funzioni, numeri o esempi di codice. Non scrivere codice.\n"
            f"5. Prima di proporre un miglioramento controlla la scheda COSE GIÀ PRESENTI IN HEXAD: non proporre come novità ciò che esiste già; "
            f"se serve, proponi di potenziare il componente esistente citandolo per nome.\n"
            f"6. Rispondi in italiano, in prosa, al massimo tre paragrafi brevi, senza elenchi numerati e senza markdown: "
            f"il testo viene letto a voce. Chiudi sempre l'ultima frase.\n\n"
            f"MAPPA:\n{mappa}\n"
        )

    # ------------------------------------------------------------------ ricerca
    def _web_search(self, query: str, limit: int = 5) -> Tuple[List[Dict[str, str]], Optional[str]]:
        key = os.environ.get("FIRECRAWL_API_KEY")
        if not key:
            return [], "chiave Firecrawl assente"
        try:
            payload = json.dumps({"query": query, "limit": limit}).encode("utf-8")
            req = urllib.request.Request("https://api.firecrawl.dev/v1/search", data=payload, headers={
                "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            out = []
            for it in data.get("data", [])[:limit]:
                out.append({"title": (it.get("title") or "").strip()[:160],
                            "url": (it.get("url") or "").strip(),
                            "description": re.sub(r"\s+", " ", (it.get("description") or "")).strip()[:400]})
            return out, None if out else "nessun risultato"
        except Exception as e:
            return [], f"errore di rete: {e}"

    def _plan_research(self, raw_text: str) -> Dict[str, str]:
        weak = self._format("punti deboli di hexad")
        have = self._format("cose già presenti in hexad")
        system = (
            "Sei il pianificatore di ricerca di HEXAD. Dati i punti deboli verificati e le cose già presenti, "
            "scegli UN solo punto debole concreto, il più adatto alla richiesta dell'utente, e scrivi una query di ricerca web "
            "in inglese tecnico (da 4 a 8 parole) per trovare soluzioni pratiche già usate da altri sviluppatori. "
            "Non scegliere qualcosa che risulta già presente. Rispondi solo con JSON: "
            "{\"punto_debole\": \"descrizione breve in italiano\", \"query\": \"english search query\"}\n\n"
            f"{weak}\n\n{have}"
        )
        raw = self.cortex.generate_grounded(system, raw_text, num_predict=150, temperature=0.1, json_mode=True, timeout=60)
        plan = {"punto_debole": "", "query": ""}
        try:
            obj = json.loads(raw or "{}")
            plan["punto_debole"] = str(obj.get("punto_debole", "")).strip()
            plan["query"] = re.sub(r"\s+", " ", str(obj.get("query", ""))).strip()[:120]
        except Exception:
            pass
        if len(plan["query"].split()) < 3:
            plan["query"] = "LLM assistant prevent hallucination about own architecture grounding"
            plan["punto_debole"] = plan["punto_debole"] or "risposte su se stesso non ancorate ai dati reali"
        return plan

    def _log(self, entry: Dict[str, Any]) -> None:
        try:
            with open(self.research_log, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

    # ------------------------------------------------------------------ risposta
    def answer(self, raw_text: str, creator_name: str, history: Optional[List[Dict[str, str]]] = None,
               improvement: bool = False) -> Tuple[str, List[str], Dict[str, Any]]:
        mappa, used = self.select_context(raw_text, improvement=improvement)
        system = self._system(creator_name, mappa)
        meta: Dict[str, Any] = {"mode": "SELF_IMPROVEMENT_RESEARCH" if improvement else "SELF_MAP_INQUIRY",
                                "map_nodes": used, "map_chars": len(mappa)}

        if improvement:
            plan = self._plan_research(raw_text)
            results, err = self._web_search(plan["query"])
            meta.update({"plan": plan, "sources": results, "search_error": err})
            if results:
                lines = [f"{i}. {r['title']} — {r['url']} — {r['description']}" for i, r in enumerate(results, 1)]
                research_block = "\n".join(lines)
            else:
                research_block = f"RICERCA FALLITA ({err}). Non ci sono fonti."
            system += (
                f"\nRICERCA ESEGUITA ORA SUL WEB (risultati NON verificati: solo titolo, indirizzo e descrizione).\n"
                f"Punto debole scelto: {plan['punto_debole']}\nQuery usata: {plan['query']}\n{research_block}\n\n"
                f"REGOLE AGGIUNTIVE PER LA PROPOSTA:\n"
                f"7. Spiega quale punto debole hai scelto, che cosa hai cercato e che cosa hai trovato.\n"
                f"8. Basa la proposta SOLO su questi risultati e sulla mappa, citando il sito da cui prendi ogni idea. "
                f"Se i risultati non sono pertinenti o la ricerca è fallita, dillo e non inventare fonti.\n"
                f"9. Dichiara che i risultati non sono verificati e che la modifica va valutata e realizzata da Antigravity: tu non modifichi il codice.\n"
            )
            num_predict = 750
        else:
            num_predict = 600

        reply = self.cortex.generate_grounded(system, raw_text, conversation_history=(history or [])[-2:],
                                              num_predict=num_predict, temperature=0.15)
        if not reply:
            reply = ("In questo momento la mia corteccia neurale non risponde, quindi non posso descrivermi in modo affidabile. "
                     "Preferisco non improvvisare: riprova tra poco.")
        meta["reply_chars"] = len(reply)
        if improvement:
            self._log({"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "question": raw_text, "plan": meta.get("plan"),
                       "sources": meta.get("sources"), "search_error": meta.get("search_error"), "reply": reply})
        return reply, used, meta
