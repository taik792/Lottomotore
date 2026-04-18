import json
import random
from collections import defaultdict

# ===== CONFIG =====
NUM_ESTRAZIONI = 120

RUOTE_GEMELLE = {
    "Bari": "Napoli",
    "Napoli": "Bari",
    "Cagliari": "Roma",
    "Roma": "Cagliari",
    "Firenze": "Genova",
    "Genova": "Firenze",
    "Milano": "Torino",
    "Torino": "Milano",
    "Palermo": "Venezia",
    "Venezia": "Palermo"
}

# ===== CARICA DATI =====
with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

risultati = {"ruote": {}}

# ===== FUNZIONI =====

def calcola_frequenze(estrazioni):
    freq = defaultdict(int)
    for estr in estrazioni:
        for n in estr:
            freq[n] += 1
    return freq

def calcola_ritardi(estrazioni):
    ritardi = {n: 0 for n in range(1, 91)}

    for n in range(1, 91):
        for i in range(len(estrazioni)-1, -1, -1):
            if n in estrazioni[i]:
                ritardi[n] = len(estrazioni) - i
                break
    return ritardi

def distanza_ok(n1, n2):
    return abs(n1 - n2) <= 60  # evita ambi troppo distanti

# ===== CALCOLO =====
for ruota, estrazioni_ruota in estrazioni.items():

    ultime = estrazioni_ruota[-NUM_ESTRAZIONI:]
    ultima_estrazione = estrazioni_ruota[-1]

    freq = calcola_frequenze(ultime)
    ritardi = calcola_ritardi(ultime)

    score_numeri = {}

    for n in range(1, 91):
        f = freq[n]
        r = ritardi[n]

        # 🔥 formula equilibrata
        score = (f * 2.2) + (r * 0.4)

        # penalità leggera
        if n in ultima_estrazione:
            score -= 5

        score_numeri[n] = score

    ordinati = sorted(score_numeri.items(), key=lambda x: x[1], reverse=True)

    top_numeri = [n for n,_ in ordinati[:15]]

    # ===== CREA AMBI =====
    migliori_ambi = []

    for i in range(len(top_numeri)):
        for j in range(i+1, len(top_numeri)):
            n1 = top_numeri[i]
            n2 = top_numeri[j]

            if not distanza_ok(n1, n2):
                continue

            score = score_numeri[n1] + score_numeri[n2]
            migliori_ambi.append(((n1, n2), score))

    migliori_ambi.sort(key=lambda x: x[1], reverse=True)

    ambo = list(migliori_ambi[0][0])
    score_finale = round(migliori_ambi[0][1], 2)

    risultati["ruote"][ruota] = {
        "ambo": ambo,
        "score": score_finale
    }

# ===== TOP =====
top = sorted(
    [(r, risultati["ruote"][r]["score"]) for r in risultati["ruote"]],
    key=lambda x: x[1],
    reverse=True
)[:3]

risultati["top"] = [r[0] for r in top]

# ===== JOLLY PRO =====
jolly_ruota = random.choice(risultati["top"])
ambo_top = risultati["ruote"][jolly_ruota]["ambo"]

usa_gemella = random.random() < 0.35

if usa_gemella:
    gemella = RUOTE_GEMELLE.get(jolly_ruota, jolly_ruota)

    ultime = estrazioni[gemella][-80:]
    freq = calcola_frequenze(ultime)
    ritardi = calcola_ritardi(ultime)

    score_numeri = {}

    for n in range(1,91):
        score_numeri[n] = (freq[n]*2) + (ritardi[n]*0.5)

    ordinati = sorted(score_numeri.items(), key=lambda x: x[1], reverse=True)

    candidati = [n for n,_ in ordinati[:15]]

    jolly_ambo = random.sample(candidati, 2)

    risultati["jolly"] = {
        "ruota": gemella + " (gemella)",
        "ambo": jolly_ambo
    }

else:
    ultime = estrazioni[jolly_ruota][-80:]
    freq = calcola_frequenze(ultime)
    ritardi = calcola_ritardi(ultime)

    score_numeri = {}

    for n in range(1,91):
        score_numeri[n] = (freq[n]*2) + (ritardi[n]*0.5)

    ordinati = sorted(score_numeri.items(), key=lambda x: x[1], reverse=True)

    candidati = [n for n,_ in ordinati if n not in ambo_top][:15]

    jolly_ambo = random.sample(candidati, 2)

    risultati["jolly"] = {
        "ruota": jolly_ruota,
        "ambo": jolly_ambo
    }

# ===== SALVA =====
with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=2)

print("🔥 MOTORE 4 DEFINITIVO ATTIVO")