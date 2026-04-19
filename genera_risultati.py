# genera_risultati.py
import json
from collections import Counter

FILE_INPUT = "estrazioni.json"
FILE_OUTPUT = "risultati.json"


def distanza(a, b):
    d = abs(a - b)
    return min(d, 90 - d)


def genera_previsione(lista_estrazioni):
    """
    lista_estrazioni esempio:
    [
        [12, 45, 67, 8, 90],
        [4, 17, 33, 51, 72]
    ]
    """

    if not lista_estrazioni:
        return {
            "numeri": [7, 29],
            "score": 0,
            "ultima_estrazione": []
        }

    ultima_estrazione = lista_estrazioni[-1]

    storico = []
    for estrazione in lista_estrazioni[:-1]:
        storico.extend(estrazione)

    if len(storico) < 2:
        storico = []
        for estrazione in lista_estrazioni:
            storico.extend(estrazione)

    freq = Counter(storico)

    candidati = []

    numeri = list(freq.keys())

    if len(numeri) < 2:
        return {
            "numeri": [7, 29],
            "score": 0,
            "ultima_estrazione": ultima_estrazione
        }

    for i in range(len(numeri)):
        for j in range(i + 1, len(numeri)):
            n1 = numeri[i]
            n2 = numeri[j]

            # evita numeri troppo vicini
            if abs(n1 - n2) < 8:
                continue

            # evita copia identica ultima estrazione
            if n1 in ultima_estrazione and n2 in ultima_estrazione:
                continue

            score = (
                freq[n1] * 2
                + freq[n2] * 2
                + distanza(n1, n2)
            )

            candidati.append({
                "numeri": sorted([n1, n2]),
                "score": score
            })

    if not candidati:
        return {
            "numeri": [7, 29],
            "score": 0,
            "ultima_estrazione": ultima_estrazione
        }

    candidati.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    migliore = candidati[0]

    return {
        "numeri": migliore["numeri"],
        "score": migliore["score"],
        "ultima_estrazione": ultima_estrazione
    }


def main():
    with open(FILE_INPUT, "r", encoding="utf-8") as f:
        estrazioni = json.load(f)

    risultati = []

    for ruota, lista in estrazioni.items():
        previsione = genera_previsione(lista)

        risultati.append({
            "ruota": ruota,
            "numeri": previsione["numeri"],
            "score": previsione["score"],
            "ultima_estrazione": previsione["ultima_estrazione"]
        })

    risultati.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top = risultati[:3]
    jolly = top[0] if top else {}

    output = {
        "top": top,
        "jolly": jolly,
        "ruote": risultati
    }

    with open(FILE_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print("risultati.json aggiornato con tutte le ruote")


if __name__ == "__main__":
    main()