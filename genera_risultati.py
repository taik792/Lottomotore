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


def calcola_frequenze_reali(estrazioni_ruota):
    """
    Usa le ultime 30 estrazioni vere della ruota
    per calcolare frequenze reali
    """
    freq = Counter()

    ultime = estrazioni_ruota[-30:] if len(estrazioni_ruota) >= 30 else estrazioni_ruota

    for estrazione in ultime:
        for numero in estrazione:
            freq[numero] += 1

    return freq


def calcola_ritardo(numero, estrazioni_ruota):
    """
    Quante estrazioni fa è uscito
    """
    ritardo = 0

    for estrazione in reversed(estrazioni_ruota):
        if numero in estrazione:
            return ritardo
        ritardo += 1

    return ritardo


def numeri_validi(n1, n2, ultima):
    """
    Regole vere:
    - non usciti nell'ultima
    - non troppo vicini tra loro
    - non troppo vicini ai numeri appena usciti
    """

    if n1 in ultima or n2 in ultima:
        return False

    if distanza(n1, n2) < 8:
        return False

    for x in ultima:
        if distanza(n1, x) < 4:
            return False
        if distanza(n2, x) < 4:
            return False

    return True


def trova_miglior_ambo(estrazioni_ruota):
    ultima = estrazioni_ruota[-1]

    freq = calcola_frequenze_reali(estrazioni_ruota)

    migliori = []

    for n1 in range(1, 91):
        for n2 in range(n1 + 1, 91):

            if not numeri_validi(n1, n2, ultima):
                continue

            freq_score = freq[n1] + freq[n2]

            rit1 = calcola_ritardo(n1, estrazioni_ruota)
            rit2 = calcola_ritardo(n2, estrazioni_ruota)

            ritardo_score = rit1 + rit2

            dist = distanza(n1, n2)

            bonus = 0

            if 10 <= dist <= 24:
                bonus += 40

            if 25 <= dist <= 35:
                bonus += 20

            score = (
                freq_score * 20 +
                ritardo_score * 8 +
                bonus
            )

            migliori.append({
                "numeri": [n1, n2],
                "score": score
            })

    migliori.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return migliori[0]


def genera():
    dati = carica_estrazioni()

    risultati_ruote = []

    for ruota in RUOTE:
        if ruota not in dati:
            continue

        estrazioni_ruota = dati[ruota]

        miglior = trova_miglior_ambo(estrazioni_ruota)

        risultati_ruote.append({
            "ruota": ruota,
            "numeri": miglior["numeri"],
            "score": miglior["score"],
            "ultima_estrazione": estrazioni_ruota[-1]
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
        json.dump(
            output,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("risultati.json aggiornato correttamente")


if __name__ == "__main__":
    genera()