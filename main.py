from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import math
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

teams = [
    ("Manchester City", 2.5),
    ("Arsenal", 2.0),
    ("Real Madrid", 2.3),
    ("Barcelona", 2.1),
    ("Bayern", 2.6),
    ("PSG", 2.4),
    ("Juventus", 1.8),
    ("Milan", 1.7),
    ("River", 1.9),
    ("Boca", 1.8),
    ("Flamengo", 2.2),
    ("Palmeiras", 2.1),
    ("Inter Miami", 1.6),
    ("LA Galaxy", 1.7)
]

leagues = [
    "Premier League",
    "La Liga",
    "Serie A",
    "Bundesliga",
    "Ligue 1",
    "Argentina",
    "Brasil",
    "MLS"
]

def poisson(lmbda, k):
    return (lmbda**k * math.exp(-lmbda)) / math.factorial(k)

def match_prob(home_xg, away_xg):

    home_win = 0
    draw = 0
    away_win = 0

    for i in range(6):
        for j in range(6):
            p = poisson(home_xg, i) * poisson(away_xg, j)

            if i > j:
                home_win += p
            elif i == j:
                draw += p
            else:
                away_win += p

    return home_win, draw, away_win

@app.get("/matches")
def get_matches():

    matches = []

    for i in range(25):

        home = random.choice(teams)
        away = random.choice(teams)

        while home == away:
            away = random.choice(teams)

        home_xg = home[1]
        away_xg = away[1]

        hw, dr, aw = match_prob(home_xg, away_xg)

        # convertir a %
        hw *= 100
        dr *= 100
        aw *= 100

        # cuotas tipo casa
        odd_home = round(100 / hw, 2)
        odd_draw = round(100 / dr, 2)
        odd_away = round(100 / aw, 2)

        value = max(hw, dr, aw)

        matches.append({
            "league": random.choice(leagues),
            "home": home[0],
            "away": away[0],

            "markets": {
                "1X2": {
                    "home": round(hw),
                    "draw": round(dr),
                    "away": round(aw)
                },
                "odds": {
                    "home": odd_home,
                    "draw": odd_draw,
                    "away": odd_away
                }
            },

            "pick": "HOME" if hw > aw else "AWAY",
            "confidence": round(value),

            "analysis": "Modelo Poisson basado en expectativa de gol (xG)."
        })

    # 🔥 ordenar por mejor pick
    matches = sorted(matches, key=lambda x: x["confidence"], reverse=True)

    return matches
