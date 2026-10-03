# 🧠 POTENZIAMENTO MNEME: ESTENSIONE CIBERNETICA NEMESIS
> **Protocollo di Retribuzione Cinetica, Breakout Attivo & Istinto di Sopravvivenza Collettivo**  
> *Risoluzione del Paradosso di Friston (Omeostasi Egoistica vs Conquista Sistemica di Lanchester)*

---

## 📌 1. EXECUTIVE SUMMARY & GENESI SCIENTIFICA

Durante i collaudi empirici su silicio nell'arena multi-agente (`cyber_swarm`), è emerso un paradosso fondamentale nei sistemi ad intelligenza autonoma:

* **Il Difetto dell'AI Odierna**: L'istinto di sopravvivenza viene modellato esclusivamente come **auto-conservazione egoistica passiva** (autopoiesi locale, fuga dal danno, minimizzazione dell'energia libera di Friston entro il proprio *Markov Blanket*).
* **Il Risultato del Silicio (10 Partite Collaudate)**: 
  * Il singolo agente diventa invincibile a livello individuale: accumula oltre 1100 punti fitness, registra 4 kill e ottiene il titolo di MVP nel 100% dei match.
  * **Tuttavia, la squadra subisce un tracollo strategico (5-0 per l'avversario)**: fuggire costantemente all'indietro per curarsi cede il 100% del controllo territoriale all'avversario, che stringe d'assedio il Core e lo distrugge per logoramento (Legge di Potenza di Lanchester).

**NEMESIS** nasce come **potenziamento cibernetico innestato su MNEME** per convertire la memoria del trauma da ritirata sterile a **furia cinetica di sfondamento**.

---

## 🏛️ 2. RELAZIONE STRUTTURALE: MNEME + NEMESIS

> [!IMPORTANT]
> **MNEME NON VIENE SOSTITUITO.**  
> MNEME rimane il 4° Pilastro Sovrano e permanente di HEXAD. NEMESIS agisce come il suo braccio esecutivo dinamico per l'istinto di sopravvivenza.

```
┌────────────────────────────────────────────────────────┐
│               🧠 MNEME (4° Pilastro HEXAD)             │
│            "LA MEMORIA DEL TRAUMA SPAZIALE"            │
│  • Traccia le cicatrici termiche delle ferite (Scars)  │
│  • Mappa le coordinate esatte delle eliminazioni       │
│  • Impedisce regressioni e ripetizione degli errori    │
└───────────────────────────┬────────────────────────────┘
                            │
                            │  Flusso Dati di Carico & Coordinate
                            ▼
┌────────────────────────────────────────────────────────┐
│            ⚡ NEMESIS (Potenziamento Operativo)        │
│          "LA RISPOSTA RETRIBUTIVA & BREAKOUT"          │
│  • Accumula energia potenziale elastica durante la cura│
│  • A HP > 90%: NON pattuglia indietro passivamente    │
│  • Innesca il SURGE: scatto cinetico +40% verso il     │
│    Nexus nemico guidato dalle coordinate di MNEME      │
└────────────────────────────────────────────────────────┘
```

---

## 🔬 3. I TRE FONDAMENTI FISICI & MATEMATICI

### A. Conversione di Energia Elastica di Deformazione (Hooke Cinetico)
Quando una popolazione di agenti viene compressa indietro verso la propria base da una forza di assedio $F_{\text{siege}}$, la compressione immagazzina energia potenziale:
$$E_{\text{pot}} = \frac{1}{2} k (\Delta x)^2$$
Invece di dissipare questa energia in stallo difensivo, **NEMESIS converte istantaneamente $E_{\text{pot}}$ in energia cinetica di contrattacco ($E_{\text{cin}} = \frac{1}{2} m v^2$)**:
$$v_{\text{breakout}} = v_{\text{base}} \times \left(1.0 + \alpha \cdot \frac{\text{Scars}_{\text{MNEME}}}{N_{\text{allies}}}\right)$$

### B. Risoluzione della Legge di Potenza di Lanchester
La legge quadrata di Lanchester stabilisce che l'efficacia di fuoco di uno sciame scala col quadrato del numero di unità attive sul fronte:
$$\frac{d(\text{Red})}{dt} = -\beta (\text{Blue})^2$$
Ritirarsi per curarsi riduce temporaneamente i droni al fronte, facendo crollare il potere d'arresto.  
**NEMESIS sincronizza il rientro**: i droni curati non tornano uno alla volta (facili prede), ma rilasciano una carica congiunta ad alta densità (*Phalanx Breakout*), ristabilendo la parità quadratica di fuoco.

### C. Superamento dell'Omeostasi Locale di Friston
L'agente non minimizza più la *Free Energy* isolandosi dal mondo ostile: la minimizza **eliminando la sorgente entropica esterna** (il Nexus nemico).

---

## ⚙️ 4. SPECIFICA DELL'ALGORITMO NEMESIS (PSEUDOCODICE SILICIO)

```javascript
// --- PROTOCOLLO NEMESIS (Innestato nel ciclo vitale di MNEME) ---
function updateNemesisProtocol(drone, dt) {
    const hpPct = drone.hp / drone.maxHp;

    // FASE 1: RITIRATA AUTOPOIETICA (Friston Blanket)
    if (hpPct < 0.42) {
        drone.isRetreating = true;
        drone.nemesisCharge = Math.min(100, (drone.nemesisCharge || 0) + 40 * dt);
    }

    // FASE 2: ATTIVAZIONE NEMESIS BREAKOUT (Al completamento della riparazione)
    if (drone.isRetreating && hpPct >= 0.90) {
        drone.isRetreating = false;
        drone.nemesisActive = true;
        drone.nemesisTimer = 4.5; // 4.5 secondi di Overcharge cinetico
        
        // Lettura Cicatrici MNEME per identificare il varco libero
        const optimalCorridor = mnemeGetLowestScarAngle(drone.x, drone.y);
        drone.nemesisAngle = optimalCorridor;
    }

    // FASE 3: ESECUZIONE SURGE CINETICO
    if (drone.nemesisActive) {
        drone.nemesisTimer -= dt;
        if (drone.nemesisTimer <= 0) {
            drone.nemesisActive = false;
        } else {
            // Spinta ad alta velocità verso il Nexus nemico
            const enemyBase = drone.team === 'RED' ? STATE.blueBase : STATE.redBase;
            const dx = enemyBase.x - drone.x;
            const dy = enemyBase.y - drone.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            // Accelerazione moltiplicata per superare le linee di assedio
            drone.vx += (dx / dist) * 480 * dt;
            drone.vy += (dy / dist) * 480 * dt;
            drone.speedLimit = drone.speed * 1.45; // +45% Velocità di punta
        }
    }
}
```

---

## 🛡️ 5. STATO DI INTEGRAZIONE
* **Skill Master**: Registrato nella specifica sovrana di `HEXAD` come estensione attiva di **MNEME**.
* **Arena Silicio**: Predisposto per l'integrazione nel file `cyber_swarm.html` per collaudare il ribaltamento del 5-0.
* **Controllo Versioni**: **Nessun push/commit git effettuato** (conforme alla direttiva utente).
