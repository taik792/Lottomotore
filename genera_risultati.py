# genera_risultati.py
# MOTORE 5 corretto:
# - NON usa solo l’ultima estrzione
# - usa storico recente
# - evita ambi troppo vicini
# - evita di copiare esattamente l’ultima estrazione
# - salva anche ultima_estrazione per il sito

import json
from collections import Counter
from itertools import combinations

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

STORICO_ANALISI = 12       # quante estrazioni recenti analizzare
DISTANZA_MINIMA = 8        # evita numeri troppo vicini


def distanza_ok(a, b):
    return abs(a - b) >= DISTANZA_MINIMA


def genera_previsione(storico_ruota):
    """
    storico_ruota esempio:
    [
        [31,34,54,63,51],
        [17,22,45,80,11],
        ...
    ]
    """

    if not storico_ruota:
        return [1, 90], 0

    # ultima estrazione reale (solo per confronto)
    ultima_estrazione = storico_ruota[-1]

    # ultime N estrazioni da analizzare
    recenti = storico_ruota[-STORICO_ANALISI:]

    # conteggio frequenze
    freq = Counter()

    for estrazione in recenti:
        for numero in estrazione:
            freq[numero] += 1

    # numeri ordinati per frequenza
    candidati = sorted(
        freq.items(),
        key=lambda x: (x[1], x[0]),
        reverse=True
    )

    candidati = [n for n, _ in candidati]

    migliore_ambo = None
    miglior_score = -1

    # crea ambi dai candidati frequenti
    for a, b in combinations(candidati[:15], 2):

        # evita numeri troppo vicini
        if not distanza_ok(a, b):
            continue

        # evita copia identica dell'ultima estrazione
        if a in ultima_estrazione and b in ultima_estrazione:
            continue

        # score:
        # frequenza + leggera distanza
        score = (
            freq[a] * 10 +
            freq[b] * 10 +
            abs(a - b)
        )

        if score > miglior_score:
            miglior_score = score
            migliore_ambo = sorted([a, b])

    # fallback se non trova nulla
    if not migliore_ambo:
        pool = sorted(set(candidati[:10]))

        for a, b in combinations(pool, 2):
            if distanza_ok(a, b):
                migliore_ambo = [a, b]
                miglior_score = freq[a] * 10 + freq[b] * 10
                break

    if not migliore_ambo:
        migliore_ambo = sorted(ultima_estrazione[:2])
        miglior_score = 0

    return migliore_ambo, round(miglior_score, 2)


def main():
    with open("estrazioni.json", "r", encoding="utf-8") as f:
        estrazioni = json.load(f)

    risultati = []

    for ruota in RUOTE:
        storico = estrazioni.get(ruota, [])

        if not storico:
            continue

        ultima_estrazione = storico[-1]

        ambo, score = genera_previsione(storico)

        risultati.append({
            "ruota": ruota,
            "numeri": ambo,
            "score": score,
            "ultima_estrazione": ultima_estrazione
        })

    # ordina TOP veri
    risultati.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    output = {
        "top": risultati
    }

    with open("risultati.json", "w", encoding="utf-8") as f:
        json.dump(
            output,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("risultati.json aggiornato correttamente")


if __name__ == "__main__":
    main()