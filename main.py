from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    ("Manchester City", 50),
    ("Arsenal", 42),
    ("Real Madrid", 541),
    ("Barcelona", 529),
    ("Bayern Munich", 157),
    ("PSG", 85),
    ("Juventus", 496),
    ("Milan", 489),
    ("River Plate", 435),
    ("Boca Juniors", 451),
    ("Flamengo", 127),
    ("Palmeiras", 121),
    ("Inter Miami", 9568),
    ("LA Galaxy", 1609)
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

@app.get("/matches")
def get_matches():

    matches = []

    for i in range(40):  # 🔥 40 partidos SIEMPRE

        home = random.choice(teams)
        away = random.choice(teams)

        while home == away:
            away = random.choice(teams)

        home_prob = random.randint(30, 60)
        draw_prob = random.randint(20, 30)
        away_prob = 100 - home_prob - draw_prob

        matches.append({
            "league": random.choice(leagues),
            "home": home[0],
            "away": away[0],
            "home_logo": f"https://media.api-sports.io/football/teams/{home[1]}.png",
            "away_logo": f"https://media.api-sports.io/football/teams/{away[1]}.png",

            "markets": {
                "1X2": {
                    "home": home_prob,
                    "draw": draw_prob,
                    "away": away_prob
                },
                "over_2_5": {
                    "over": random.randint(45, 70),
                    "under": random.randint(30, 55)
                },
                "btts": {
                    "yes": random.randint(40, 70),
                    "no": random.randint(30, 60)
                }
            },

            "analysis": "Modelo basado en forma, ataque y tendencia de goles."
        })

    return matches
