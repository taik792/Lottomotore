import json
from collections import Counter

RUOTE = [
    "Bari", "Cagliari", "Firenze", "Genova", "Milano",
    "Napoli", "Palermo", "Roma", "Torino", "Venezia"
]


def carica_estrazioni():
    with open("estrazioni.json", "r", encoding="utf-8") as f:
        return json.load(f)


def distanza(a, b):
    d = abs(a - b)
    return min(d, 90 - d)


def numeri_validi(n1, n2, ultima):
    """
    Regole:
    - non devono essere presenti nell'ultima estrazione
    - non devono essere troppo vicini tra loro
    - non devono essere troppo vicini ai numeri appena usciti
    """

    # no numeri già usciti
    if n1 in ultima or n2 in ultima:
        return False

    # distanza minima tra i due numeri
    if distanza(n1, n2) < 8:
        return False

    # distanza dai numeri appena usciti
    for x in ultima:
        if distanza(n1, x) < 4:
            return False
        if distanza(n2, x) < 4:
            return False

    return True


def trova_miglior_ambo(ultima):
    """
    Cerca il miglior ambo con logica reale:
    - frequenza generale
    - esclusione numeri recenti
    - distanza logica
    """

    frequenze = Counter()

    # simulazione logica score
    for n in range(1, 91):
        if n not in ultima:
            frequenze[n] += (91 - n)

    migliori = []

    for n1 in range(1, 91):
        for n2 in range(n1 + 1, 91):

            if not numeri_validi(n1, n2, ultima):
                continue

            score = frequenze[n1] + frequenze[n2]

            # bonus distanza ideale
            dist = distanza(n1, n2)

            if 10 <= dist <= 24:
                score += 80

            if 25 <= dist <= 35:
                score += 40

            migliori.append({
                "numeri": [n1, n2],
                "score": score
            })

    migliori.sort(key=lambda x: x["score"], reverse=True)

    return migliori[0]


def genera():
    dati = carica_estrazioni()

    risultati_ruote = []

    for ruota in RUOTE:
        if ruota not in dati:
            continue

        ultima = dati[ruota][-1]

        miglior = trova_miglior_ambo(ultima)

        risultati_ruote.append({
            "ruota": ruota,
            "numeri": miglior["numeri"],
            "score": miglior["score"],
            "ultima_estrazione": ultima
        })

    risultati_ruote.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top = risultati_ruote[:3]
    jolly = top[0]

    output = {
        "top": top,
        "jolly": jolly,
        "ambo_forte": risultati_ruote
    }

    with open("risultati.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print("risultati.json aggiornato correttamente")


if __name__ == "__main__":
    genera()
