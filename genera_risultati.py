# genera_risultati.py
# MOTORE 5 - versione corretta con logica reale
# Fix bug:
# - evita di usare l'ultima estrazione come previsione diretta
# - ordina per score dal più alto al più basso
# - TOP = migliori 3 ruote
# - JOLLY = miglior TOP assoluto
# - RUOTE = tutte ordinate per score

import json
from collections import Counter

FILE_INPUT = "estrazioni.json"
FILE_OUTPUT = "risultati.json"


def carica_estrazioni():
    with open(FILE_INPUT, "r", encoding="utf-8") as f:
        return json.load(f)


def distanza(n1, n2):
    """Distanza circolare sul lotto 1-90"""
    d = abs(n1 - n2)
    return min(d, 90 - d)


def genera_coppie_forti(numeri_storici):
    """
    Cerca le coppie più forti evitando:
    - coppie identiche all'ultima estrazione
    - numeri troppo vicini (tipo 41-42)
    """

    frequenze = Counter(numeri_storici)

    numeri_frequenti = [
        n for n, _ in frequenze.most_common(20)
    ]

    migliori = []
    ultima = set(numeri_storici[-5:]) if len(numeri_storici) >= 5 else set()

    for i in range(len(numeri_frequenti)):
        for j in range(i + 1, len(numeri_frequenti)):
            a = numeri_frequenti[i]
            b = numeri_frequenti[j]

            # evita numeri troppo vicini
            if abs(a - b) < 8:
                continue

            # evita copia ultima estrazione
            if a in ultima and b in ultima:
                continue

            # score con distanza + frequenza
            score = (
                frequenze[a]
                + frequenze[b]
                + distanza(a, b)
            )

            migliori.append({
                "numeri": sorted([a, b]),
                "score": score
            })

    migliori.sort(key=lambda x: x["score"], reverse=True)

    if migliori:
        return migliori[0]

    # fallback sicurezza
    return {
        "numeri": [7, 29],
        "score": 0
    }


def main():
    dati = carica_estrazioni()

    risultati_ruote = []

    for ruota, estrazioni in dati.items():
        if not estrazioni or len(estrazioni) < 2:
            continue

        # ultima estrazione reale
        ultima_estrazione = estrazioni[-1]

        # storico senza ultima estrazione
        storico = estrazioni[:-1]

        # flatten storico
        numeri_storici = []
        for estrazione in storico:
            numeri_storici.extend(estrazione)

        migliore = genera_coppie_forti(numeri_storici)

        risultati_ruote.append({
            "ruota": ruota,
            "numeri": migliore["numeri"],
            "score": migliore["score"],
            "ultima_estrazione": ultima_estrazione
        })

    # ordine corretto: score alto -> basso
    risultati_ruote.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top3 = risultati_ruote[:3]

    jolly = top3[0] if top3 else {}

    output = {
        "top": top3,
        "jolly": jolly,
        "ruote": risultati_ruote
    }

    with open(FILE_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print("risultati.json aggiornato correttamente")


if __name__ == "__main__":
    main()