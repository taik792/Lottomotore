# genera_risultati.py
# MOTORE DEFINITIVO PRO V2
# anti-ambi vicini + penalità speculari + top + jolly

import json

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

DISTANZA_MINIMA = 3


def carica_estrazioni():
    with open("estrazioni.json", "r", encoding="utf-8") as f:
        return json.load(f)


def somma_cifre(n):
    return sum(int(c) for c in str(n))


def score_coppia(n1, n2, ultima):
    score = 0
    distanza = abs(n1 - n2)

    # blocco ambi troppo vicini
    if distanza < DISTANZA_MINIMA:
        return -999

    # presenza in ultima estrazione
    if n1 in ultima:
        score += 15
    if n2 in ultima:
        score += 15

    # premio distanza ottimale
    if 6 <= distanza <= 15:
        score += 14
    elif 3 <= distanza <= 5:
        score += 8
    elif 16 <= distanza <= 24:
        score += 9
    else:
        score += 4

    # bonus finali uguali
    if str(n1)[-1] == str(n2)[-1]:
        score += 4

    # bonus somma cifre uguale
    if somma_cifre(n1) == somma_cifre(n2):
        score += 3

    # penalità schemi troppo speculari
    if abs((n1 // 10) - (n2 // 10)) == 1 and str(n1)[-1] == str(n2)[-1]:
        score -= 6

    # penalità numeri consecutivi forti
    if distanza <= 2:
        score -= 20

    return round(score, 2)


def migliore_coppia(estrazioni_ruota):
    ultima = estrazioni_ruota[-1]
    migliori = []

    for i in range(len(ultima)):
        for j in range(i + 1, len(ultima)):
            n1 = ultima[i]
            n2 = ultima[j]

            score = score_coppia(n1, n2, ultima)

            if score > 0:
                migliori.append({
                    "numeri": sorted([n1, n2]),
                    "score": score
                })

    if not migliori:
        fallback = sorted([ultima[0], ultima[1]])
        return {
            "numeri": fallback,
            "score": 10
        }

    migliori.sort(key=lambda x: x["score"], reverse=True)
    return migliori[0]


def genera_top(previsioni):
    top = sorted(
        previsioni,
        key=lambda x: x["score"],
        reverse=True
    )[:3]

    return top


def genera_jolly(top):
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