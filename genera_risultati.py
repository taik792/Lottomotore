# genera_risultati.py
# LOTTO ELITE PRO — MOTORE 5 DEFINITIVO
# compatibile con index nuovo + risultati.json

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

# =========================
# CONFIG
# =========================

TOP_COUNT = 3
NUMERI_PER_RUOTA = 2

# peso posizione estrazione
PESI_POSIZIONE = [1.35, 1.20, 1.10, 1.00, 0.90]

# bonus
BONUS_GEMELLA = 1.15
BONUS_VICINO_1 = 1.18
BONUS_VICINO_2 = 1.08


# =========================
# FUNZIONI
# =========================

def normalizza(n):
    while n < 1:
        n += 90
    while n > 90:
        n -= 90
    return n


def vicini(numero):
    return [
        normalizza(numero - 2),
        normalizza(numero - 1),
        numero,
        normalizza(numero + 1),
        normalizza(numero + 2)
    ]


def gemella(numero):
    if numero < 10:
        return numero + 9

    s = str(numero)

    if len(s) == 1:
        return numero

    g = int(s[::-1])

    if g < 1:
        g = numero

    if g > 90:
        g = numero

    return g


def analizza_ruota(lista_estrazioni):
    """
    esempio:
    [
      [12, 45, 67, 10, 90],
      [....]
    ]
    """

    punteggi = Counter()

    # ultime 8 estrazioni = parte calda
    ultime = lista_estrazioni[-8:]

    for estrazione in ultime:
        for idx, numero in enumerate(estrazione):

            peso = PESI_POSIZIONE[idx]

            # numero diretto
            punteggi[numero] += peso

            # gemella
            g = gemella(numero)
            punteggi[g] += peso * BONUS_GEMELLA

            # vicini ±1 ±2
            for v in vicini(numero):
                if v == numero:
                    continue

                diff = abs(v - numero)

                if diff == 1:
                    punteggi[v] += peso * BONUS_VICINO_1
                else:
                    punteggi[v] += peso * BONUS_VICINO_2

    migliori = [x[0] for x in punteggi.most_common(NUMERI_PER_RUOTA)]

    score = round(
        sum([x[1] for x in punteggi.most_common(5)]),
        2
    )

    return migliori, score


def scegli_jolly(previsioni, top_ruote):
    """
    jolly:
    prende migliore ruota FUORI TOP
    """

    candidate = []

    for ruota, dati in previsioni.items():
        if ruota in top_ruote:
            continue

        candidate.append(
            (
                ruota,
                dati["numeri"],
                dati["score"]
            )
        )

    candidate.sort(
        key=lambda x: x[2],
        reverse=True
    )

    if not candidate:
        return None

    ruota, numeri, _ = candidate[0]

    return {
        "ruota": ruota,
        "numeri": numeri,
        "label": f"{ruota} (jolly forte)"
    }


# =========================
# MAIN
# =========================

def main():
    with open(
        "estrazioni.json",
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

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

    # =========================
    # TOP
    # =========================

    top = sorted(
        previsioni.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )[:TOP_COUNT]

    top_ruote = [x[0] for x in top]

    # =========================
    # JOLLY
    # =========================

    jolly = scegli_jolly(
        previsioni,
        top_ruote
    )

    # =========================
    # JSON FINALE
    # =========================

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

    with open(
        "risultati.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            risultato_finale,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("🔥 risultati.json generato correttamente")


if __name__ == "__main__":
    main()