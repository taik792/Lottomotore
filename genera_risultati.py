# genera_risultati.py
# MOTORE DEFINITIVO PRO
# genera risultati.json nel formato corretto per index.html

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


def somma_cifre(n):
    return sum(int(x) for x in str(n))


def numero_specchio(n):
    if n < 10:
        return int(f"{n}{n}")
    s = str(n)
    return int(s[::-1])


def distanza(a, b):
    d = abs(a - b)
    return min(d, 90 - d)


def scegli_ambo(lista):
    """
    prende gli ultimi 5 numeri della ruota
    e costruisce un ambo forte semplice e stabile
    """
    base = lista[-1]

    candidati = []

    for n in lista:
        if n == base:
            continue

        score = 0

        # vicinanza
        score += (20 - min(distanza(base, n), 20))

        # somma cifre simile
        score += 10 - abs(somma_cifre(base) - somma_cifre(n))

        # specchio
        if numero_specchio(base) == n:
            score += 20

        candidati.append((score, n))

    candidati.sort(reverse=True)

    if not candidati:
        return [base, (base + 9) % 90 or 90], 0

    secondo = candidati[0][1]
    score_finale = round(candidati[0][0], 2)

    return [base, secondo], score_finale


def scegli_top(previsioni_ruote):
    """
    prende le 3 ruote con score migliore
    """
    ordinati = sorted(
        previsioni_ruote,
        key=lambda x: x["score"],
        reverse=True
    )

    return ordinati[:3]


def scegli_jolly(top):
    """
    Jolly forte:
    prende il miglior top
    e usa il suo ambo invertito
    """
    migliore = top[0]

    n1 = migliore["numeri"][0]
    n2 = migliore["numeri"][1]

    return {
        "ruota": migliore["ruota"],
        "numeri": [n2, n1]
    }


def main():
    try:
        with open("estrazioni.json", "r", encoding="utf-8") as f:
            estrazioni = json.load(f)

        ruote_output = []

        for ruota in RUOTE:
            if ruota not in estrazioni:
                continue

            storico = estrazioni[ruota]

            if not storico or len(storico) == 0:
                continue

            ultima = storico[-1]

            ambo, score = scegli_ambo(ultima)

            ruote_output.append({
                "ruota": ruota,
                "numeri": ambo,
                "score": score,
                "ultima_estrazione": ultima
            })

        top = scegli_top(ruote_output)
        jolly = scegli_jolly(top)

        risultato_finale = {
            "top": top,
            "jolly": jolly,
            "ruote": ruote_output
        }

        with open("risultati.json", "w", encoding="utf-8") as f:
            json.dump(
                risultato_finale,
                f,
                indent=2,
                ensure_ascii=False
            )

        print("risultati.json generato correttamente")

    except Exception as e:
        print("ERRORE:", str(e))


if __name__ == "__main__":
    main()