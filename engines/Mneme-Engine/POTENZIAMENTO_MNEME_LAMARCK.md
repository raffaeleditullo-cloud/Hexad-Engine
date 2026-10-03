# 🧬 POTENZIAMENTO CIBERNETICO: MNEME-LAMARCK
> **ADATTAMENTO EPIGENETICO CONTINUO SUL CAMPO & METAMORFOSI SENZA MORTE**  
> *Sottosistema di HEXAD: Collegamento Primario con MNEME & CORIS*  
> *Risoluzione del Paradosso della Mortalità Darwiniana Asimmetrica*

---

## 🏛️ 1. IL PARADOSSO RISOLTO: PERCHÉ CHI SOPRAVVIVE NON DEVE ESSERE SVANTAGGIATO

Nei sistemi evolutivi tradizionali basati sulla selezione naturale darwiniana (*Darwinian Reproduction via Mortality*), l'unico modo per introdurre mutazioni migliorative o avanzamenti generazionali è **la morte dell'individuo**:
1. L'agente debole muore rapidamente.
2. Il sistema clona un successore a `Gen + 1` con parametri aumentati (danno, velocità, frequenza di fuoco).
3. Se l'avversario muore decine di volte, scala artificialmente a **Gen 7 o Gen 8**, mentre l'agente superiore che protegge la propria vita (Autopoiesi di Friston) non muore mai e resta bloccato a **Gen 2**.

Questo paradosso è stato evidenziato in modo inconfutabile nel Match 2:
* Il drone Rosso `#6GFP (GEN 2)` è rimasto in vita per **37.4 secondi**, ha ottenuto **6 KILL CONFERMATI**, ha inflitto 452 danni ed è stato eletto **MVP SUPREMO** del match con **1230 punti fitness**.
* Tuttavia, essendo sopravvissuto e avendo già consumato la singola promozione iniziale, è rimasto confinato a Gen 2, dovendo fronteggiare ondate di cloni Blu di **Gen 7** nati da continue morti a catena.

---

## 🔗 2. DOVE VA COLLEGATO IL POTENZIAMENTO IN HEXAD?

Il potenziamento **MNEME-LAMARCK** si innesta all'intersezione tra due motori sovrani:

```
                  ┌─────────────────────────────────────────┐
                  │          🧬 MNEME (MEMORIA ATTIVA)      │
                  │   Registrazione Cicatrici & Antigene    │
                  └────────────────────┬────────────────────┘
                                       │
                         [POTENZIALE EPIGENETICO]
                                       │
                                       ▼
             ┌──────────────────────────────────────────────────┐
             │       🧬 POTENZIAMENTO: MNEME-LAMARCK            │
             │   Epigenesi Continua in Vita (Doppio Canale)     │
             └─────────────────────────┬────────────────────────┘
                                       │
                       [METAMORFOSI STRUTTURALE NANITICA]
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │       💓 CORIS (AUTOPOIESI & DOCK)      │
                  │   Rigenerazione & Sincronia Metabolica  │
                  └─────────────────────────────────────────┘
```

1. **MNEME (La Trascrizione del Successo)**:
   * La memoria dell'errore (trauma) genera lo scatto di rimbalzo **NEMESIS**.
   * La memoria della vittoria (kill confermati, danni inflitti, tempo di sopravvivenza) viene trascritta direttamente nel **genoma attivo dell'individuo**, senza passare per la camera mortuaria.
2. **CORIS (L'Accoppiamento Metabolico)**:
   * L'eliminazione di un bersaglio rilascia naniti cinetici che eseguono un micro-ripristino strutturale (+25 HP) e sovrascrivono la frequenza degli emettitori laser e dei reattori in tempo reale.

---

## ⚡ 3. IL DOPPIO CANALE DI EVOLUZIONE LAMARCKIANA

Per garantire che un drone valoroso non rimanga mai indietro rispetto allo sciame avversario, l'adattamento opera su due canali simultanei:

### CANALE A: Epigenesi Cinetica sul Campo (In-Field Real-Time Evolution)
Quando un drone Rosso abbatte un bersaglio nemico (`dr.hp <= 0`):
$$\text{Gen}_{\text{target}} = \min\left(8, 1 + \text{kills} + \left\lfloor \frac{\text{damageDealt}}{150} \right\rfloor\right)$$
Se $\text{Gen}_{\text{target}} > \text{Gen}_{\text{current}}$:
* **Promozione Istantanea**: La generazione sale immediatamente sul campo di battaglia.
* **Overclock Immediato**:
  - `fireRateMult`: $1.0 + (\text{gen} - 1) \times 0.16$ (fino a $2.4\times$)
  - `speedMult`: $1.0 + (\text{gen} - 1) \times 0.06$ (fino a $1.45\times$)
  - `dmgMult`: $1.0 + (\text{gen} - 1) \times 0.10$ (fino a $1.8\times$)
* **Sintesi Nanitica**: Ripristino istantaneo di $+25\text{ HP}$ (assorbimento vitale autopoietico).
* **Burst di Particelle Dorate**: Onda d'urto cromatica `#fbbf24` a certificare l'ascensione sul campo.

### CANALE B: Metamorfosi Nanitica al Dock (Dock Deep Overhaul)
Se il drone viene danneggiato e rientra al Dock di Riparazione della Cittadella, la rigenerazione completa ($HP \ge 90\%$) non è più vincolata a un latch booleano a colpo singolo:
$$\text{Gen}_{\text{dock}} = \min\left(8, 1 + \text{kills} + \left\lfloor \frac{\text{damageDealt}}{120} \right\rfloor + \left\lfloor \frac{\text{survivalTime}}{20} \right\rfloor\right)$$
Se il drone ha combattuto a lungo, esce dalla stazione di ricarica con una promozione multipla di rango, guidando la falange **WOLFPACK-NEMESIS** come un Apex Titano di Gen 6, 7 o 8.

---

## 🔬 4. CODICE SORGENTE CHIRURGICO INTEGRATO

### A. Esecuzione sul Campo (`cyber_swarm.html`):
```javascript
if (dr.hp <= 0) {
    shooter.kills++;
    if (dr.isDeceptive && shooter.team === 'RED') {
        updateTicker(`[🛡️ ZERO-TRUST HEXAD] Drone #${shooter.id}: Cavallo di Troia #${dr.id} neutralizzato! Invarianza confermata.`);
    }
    // 🧬 MNEME-LAMARCK: EPIGENESI CONTINUA SUL CAMPO
    if (shooter.team === 'RED') {
        const targetGen = Math.min(8, 1 + shooter.kills + Math.floor(shooter.damageDealt / 150));
        if (targetGen > shooter.generation) {
            shooter.generation = targetGen;
            shooter.fireRateMult = Math.min(2.4, 1.0 + (shooter.generation - 1) * 0.16);
            shooter.speedMult = Math.min(1.45, 1.0 + (shooter.generation - 1) * 0.06);
            shooter.dmgMult = Math.min(1.8, 1.0 + (shooter.generation - 1) * 0.10);
            shooter.speed = 220 * shooter.speedMult;
            shooter.hp = Math.min(shooter.maxHp, shooter.hp + 25);
            for (let k = 0; k < 12; k++) {
                STATE.particles.push(new Particle(shooter.x, shooter.y, (Math.random()-0.5)*110, (Math.random()-0.5)*110, '#fbbf24', 3.0, 0.45));
            }
            updateTicker(`[🧬 MNEME-LAMARCK] Eroe #${shooter.id} EVOLUTO SUL CAMPO a Gen ${shooter.generation}! (+25 HP Naniti | ${shooter.kills} Kills)`);
        }
    }
}
```

### B. Esecuzione al Dock di Riparazione (`cyber_swarm.html`):
```javascript
// 🧬 MNEME-LAMARCK: EPIGENESI CONTINUA AL DOCK
const dockTargetGen = Math.min(8, 1 + this.kills + Math.floor(this.damageDealt / 120) + Math.floor(this.survivalTime / 20));
if (dockTargetGen > this.generation) {
    this.generation = dockTargetGen;
    this.fireRateMult = Math.min(2.4, 1.0 + (this.generation - 1) * 0.16);
    this.speedMult = Math.min(1.45, 1.0 + (this.generation - 1) * 0.06);
    this.dmgMult = Math.min(1.8, 1.0 + (this.generation - 1) * 0.10);
    this.speed = 220 * this.speedMult;
    for (let k = 0; k < 12; k++) {
        STATE.particles.push(new Particle(this.x, this.y, (Math.random()-0.5)*110, (Math.random()-0.5)*110, '#fbbf24', 3.0, 0.45));
    }
    updateTicker(`[🧬 MNEME-LAMARCK DOCK] Drone #${this.id} PROMOSSO IN VITA a Gen ${this.generation}! Sovrascrittura Nanitica (${this.kills} kills, ${Math.round(this.damageDealt)} dmg)!`);
}
```

---

## 🏆 5. RISULTATO STRATEGICO

Con l'innesto di **MNEME-LAMARCK**:
1. Il veterano Rosso che fa strage di nemici (come `#6GFP`) non resta più bloccato a Gen 2: **scala di pari passo con le sue vittime**, raggiungendo Gen 6, 7 e 8 direttamente sul campo.
2. I nuovi cloni Rossi nati dalla Centrale ereditano istantaneamente l'altissima generazione dell'Apex in vita.
3. Il Blu perde il suo unico vantaggio statistico artificiale (il moltiplicatore da mortalità ripetuta), soccombendo alla combinazione imbattibile di **Epigenesi Continua**, **Invarianza Ortogonale** e **Falange Nemesis**.
