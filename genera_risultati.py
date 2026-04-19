# genera_risultati.py

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


def distanza_ok(a, b):
    """
    Evita numeri troppo vicini:
    differenza minima >= 8
    """
    return abs(a - b) >= 8


def scegli_ambo(estrazione):
    """
    Sceglie il miglior ambo evitando numeri troppo vicini
    """
    numeri = sorted(estrazione)

    migliori = None
    score = -1

    for i in range(len(numeri)):
        for j in range(i + 1, len(numeri)):
            a = numeri[i]
            b = numeri[j]

            if not distanza_ok(a, b):
                continue

            # score semplice ma stabile
            s = a + b

            if s > score:
                score = s
                migliori = [a, b]

    # fallback se tutti troppo vicini
    if not migliori:
        migliori = sorted(estrazione[:2])
        score = sum(migliori)

    return migliori, score


def main():
    with open("estrazioni.json", "r", encoding="utf-8") as f:
        estrazioni = json.load(f)

    risultati = []

    for ruota in RUOTE:
        storico = estrazioni.get(ruota, [])

        if not storico:
            continue

        # ultima estrazione = ultima lista
        ultima_estrazione = storico[-1]

        ambo, score = scegli_ambo(ultima_estrazione)

        risultati.append({
            "ruota": ruota,
            "numeri": ambo,
            "score": round(score, 2),
            "ultima_estrazione": ultima_estrazione
        })

    # ordina TOP
    risultati.sort(key=lambda x: x["score"], reverse=True)

    output = {
        "top": risultati[:10]
    }

    with open("risultati.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print("risultati.json aggiornato correttamente")


if __name__ == "__main__":
    main()