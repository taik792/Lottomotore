# genera_risultati.py
import json
from collections import Counter

FILE_INPUT = "estrazioni.json"
FILE_OUTPUT = "risultati.json"


def distanza(a, b):
    d = abs(a - b)
    return min(d, 90 - d)


def flatten(lista):
    out = []
    for estrazione in lista:
        out.extend(estrazione)
    return out


def genera_previsione(estrazioni_ruota):
    if not estrazioni_ruota:
        return {
            "numeri": [7, 29],
            "score": 0,
            "ultima_estrazione": []
        }

    ultima = estrazioni_ruota[-1]

    # storico senza ultima estrazione
    storico = estrazioni_ruota[:-1]

    if not storico:
        storico = estrazioni_ruota

    numeri_storici = flatten(storico)

    freq = Counter(numeri_storici)

    candidati = []

    numeri = list(freq.keys())

    for i in range(len(numeri)):
        for j in range(i + 1, len(numeri)):
            n1 = numeri[i]
            n2 = numeri[j]

            # evita numeri troppo vicini
            if abs(n1 - n2) < 8:
                continue

            # evita copia identica ultima estrazione
            if n1 in ultima and n2 in ultima:
                continue

            score = (
                freq[n1] * 3 +
                freq[n2] * 3 +
                distanza(n1, n2)
            )

            candidati.append({
                "numeri": sorted([n1, n2]),
                "score": score
            })

    if not candidati:
        return {
            "numeri": [7, 29],
            "score": 0,
            "ultima_estrazione": ultima
        }

    candidati.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    migliore = candidati[0]

    return {
        "numeri": migliore["numeri"],
        "score": migliore["score"],
        "ultima_estrazione": ultima
    }


def main():
    with open(FILE_INPUT, "r", encoding="utf-8") as f:
        estrazioni = json.load(f)

    risultati_completi = []

    # prende TUTTE le ruote presenti nel file
    for ruota in estrazioni:
        previsione = genera_previsione(estrazioni[ruota])

        risultati_completi.append({
            "ruota": ruota,
            "numeri": previsione["numeri"],
            "score": previsione["score"],
            "ultima_estrazione": previsione["ultima_estrazione"]
        })

    # ordina dal migliore al peggiore
    risultati_completi.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top3 = risultati_completi[:3]

    jolly = top3[0] if top3 else {}

    output = {
        "top": top3,
        "jolly": jolly,
        "ruote": risultati_completi
    }

    with open(FILE_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(
            output,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("risultati.json aggiornato con TUTTE le ruote")


if __name__ == "__main__":
    main()