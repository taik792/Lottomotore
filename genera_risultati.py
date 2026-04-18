# genera_risultati.py
# MOTORE DEFINITIVO PRO
# filtro anti-ambi troppo vicini + top + jolly + ruote ambi forti

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

DISTANZA_MINIMA = 3  # evita ambi troppo vicini (es: 41-42)


def carica_estrazioni():
    with open("estrazioni.json", "r", encoding="utf-8") as f:
        return json.load(f)


def score_coppia(n1, n2, ultima):
    """
    Score semplice ma stabile:
    - presenza nell'ultima estrazione
    - distanza numerica
    - preferenza per numeri presenti davvero nel ciclo recente
    """

    score = 0

    if n1 in ultima:
        score += 15
    if n2 in ultima:
        score += 15

    distanza = abs(n1 - n2)

    # penalità se troppo vicini
    if distanza <= 2:
        return -999

    # premio distanza equilibrata
    if 3 <= distanza <= 12:
        score += 10
    elif 13 <= distanza <= 25:
        score += 7
    else:
        score += 3

    # bonus coppie speculari / finali simili
    if str(n1)[-1] == str(n2)[-1]:
        score += 5

    if sum(map(int, str(n1))) == sum(map(int, str(n2))):
        score += 4

    return round(score, 2)


def migliore_coppia(numeri_ruota):
    """
    prende ultima estrazione e cerca la miglior coppia
    evitando coppie troppo vicine
    """

    ultima = numeri_ruota[-1]

    migliori = []

    for i in range(len(ultima)):
        for j in range(i + 1, len(ultima)):
            n1 = ultima[i]
            n2 = ultima[j]

            if abs(n1 - n2) < DISTANZA_MINIMA:
                continue

            score = score_coppia(n1, n2, ultima)

            if score > 0:
                migliori.append({
                    "numeri": sorted([n1, n2]),
                    "score": score
                })

    if not migliori:
        # fallback sicurezza
        nums = sorted(ultima[:2])
        return {
            "numeri": nums,
            "score": 10
        }

    migliori.sort(key=lambda x: x["score"], reverse=True)
    return migliori[0]


def genera_top(previsioni_ruote):
    top = sorted(
        previsioni_ruote,
        key=lambda x: x["score"],
        reverse=True
    )[:3]

    return [
        {
            "ruota": x["ruota"],
            "numeri": x["numeri"],
            "score": x["score"]
        }
        for x in top
    ]


def genera_jolly(top):
    """
    prende il TOP migliore e lo usa come JOLLY
    """
    migliore = top[0]

    return {
        "ruota": migliore["ruota"],
        "numeri": migliore["numeri"]
    }


def main():
    dati = carica_estrazioni()

    ruote_output = []

    for ruota in RUOTE:
        if ruota not in dati:
            continue

        miglior = migliore_coppia(dati[ruota])

        ruote_output.append({
            "ruota": ruota,
            "numeri": miglior["numeri"],
            "score": miglior["score"]
        })

    top = genera_top(ruote_output)
    jolly = genera_jolly(top)

    risultati = {
        "top": top,
        "jolly": jolly,
        "ruote": ruote_output
    }

    with open("risultati.json", "w", encoding="utf-8") as f:
        json.dump(
            risultati,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("risultati.json aggiornato correttamente")


if __name__ == "__main__":
    main()