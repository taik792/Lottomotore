# genera_risultati.py
# LOTTO ELITE PRO — MOTORE 5 (chirurgico)
# versione pronta da testare:
# - top ruote forti
# - jolly separato (mai uguale ai top)
# - controllo ±1 / ±2
# - scelta numero più forte
# - filtro finale precisione

import json
from collections import Counter

RUOTE = [
    "Bari",
    "Cagliari",
    "Firenze",
    "Genova",
    "Milano",
    "Napoli",
    "Palermo",
    "Roma",
    "Torino",
    "Venezia"
]

# -------------------------
# CONFIG
# -------------------------

TOP_COUNT = 3
NUMERI_PER_RUOTA = 2

# peso posizione estrazione
PESI_POSIZIONE = [1.35, 1.20, 1.10, 1.00, 0.90]

# bonus ritardo breve / ritorno rapido
BONUS_RIPETIZIONE = 1.25

# bonus gemella
BONUS_GEMELLA = 1.15

# bonus numero vicino ±1 ±2
BONUS_VICINO_1 = 1.18
BONUS_VICINO_2 = 1.08


# -------------------------
# FUNZIONI BASE
# -------------------------

def gemella(n):
    if n < 10:
        return n + 9
    s = str(n)
    if len(s) == 1:
        return n
    return int(s[::-1])


def normalizza(n):
    while n > 90:
        n -= 90
    while n < 1:
        n += 90
    return n


def vicini(n):
    return [
        normalizza(n - 2),
        normalizza(n - 1),
        n,
        normalizza(n + 1),
        normalizza(n + 2)
    ]


def carica_json(nome_file):
    with open(nome_file, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------
# ANALISI RUOTA
# -------------------------

def analizza_ruota(estrazioni):
    """
    usa ultime estrazioni:
    [
      [12, 45, 67, 10, 90],
      [....]
    ]
    """

    punteggi = Counter()

    for estrazione in estrazioni[-8:]:
        for idx, numero in enumerate(estrazione):
            base = PESI_POSIZIONE[idx]

            # numero diretto
            punteggi[numero] += base

            # gemella
            g = gemella(numero)
            punteggi[g] += base * BONUS_GEMELLA

            # vicini ±1 ±2
            for v in vicini(numero):
                if v == numero:
                    continue

                if abs(v - numero) == 1:
                    punteggi[v] += base * BONUS_VICINO_1
                else:
                    punteggi[v] += base * BONUS_VICINO_2

    migliori = [x[0] for x in punteggi.most_common(NUMERI_PER_RUOTA)]

    score_totale = round(sum([x[1] for x in punteggi.most_common(5)]), 2)

    return migliori, score_totale


# -------------------------
# JOLLY
# -------------------------

def scegli_jolly(previsioni, top_ruote):
    """
    jolly diverso dai top
    prende la migliore ruota fuori top
    oppure gemella forte
    """

    escluse = set(top_ruote)

    candidate = []

    for ruota, dati in previsioni.items():
        if ruota in escluse:
            continue

        numeri = dati["numeri"]
        score = dati["score"]

        candidate.append((ruota, numeri, score))

    candidate.sort(key=lambda x: x[2], reverse=True)

    if not candidate:
        return None

    ruota, numeri, _ = candidate[0]

    return {
        "ruota": ruota,
        "numeri": numeri,
        "label": f"{ruota} (jolly forte)"
    }


# -------------------------
# MAIN
# -------------------------

def main():
    """
    struttura richiesta:

    estrazioni.json

    {
      "Bari": [
        [12,14,29,85,76],
        [17,71,26,6,73],
        ...
      ],
      ...
    }
    """

    data = carica_json("estrazioni.json")

    previsioni = {}

    for ruota in RUOTE:
        estrazioni = data.get(ruota, [])

        if not estrazioni:
            continue

        numeri, score = analizza_ruota(estrazioni)

        previsioni[ruota] = {
            "numeri": numeri,
            "score": score
        }

    # top ruote
    top = sorted(
        previsioni.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )[:TOP_COUNT]

    top_ruote = [x[0] for x in top]

    # jolly separato
    jolly = scegli_jolly(previsioni, top_ruote)

    risultato_finale = {
        "top": [],
        "jolly": jolly,
        "ruote": previsioni
    }

    for ruota, dati in top:
        risultato_finale["top"].append({
            "ruota": ruota,
            "numeri": dati["numeri"],
            "score": dati["score"]
        })

    with open("previsioni.json", "w", encoding="utf-8") as f:
        json.dump(risultato_finale, f, indent=2, ensure_ascii=False)

    print("PREVISIONI GENERATE → previsioni.json")


if __name__ == "__main__":
    main()