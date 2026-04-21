from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
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

API_KEY = "TU_API_KEY"

def poisson(lmbda, k):
    return (lmbda**k * math.exp(-lmbda)) / math.factorial(k)

def calc_probs(home_xg, away_xg):
    hw = dr = aw = 0
    for i in range(6):
        for j in range(6):
            p = poisson(home_xg,i)*poisson(away_xg,j)
            if i>j: hw+=p
            elif i==j: dr+=p
            else: aw+=p
    return hw*100, dr*100, aw*100

@app.get("/matches")
def get_matches():

    headers = {"x-apisports-key": API_KEY}
    url = "https://v3.football.api-sports.io/fixtures?next=10"

    matches = []

    try:
        res = requests.get(url, headers=headers, timeout=10).json()

        if "response" in res:
            for m in res["response"]:

                home = m["teams"]["home"]
                away = m["teams"]["away"]

                hw, dr, aw = calc_probs(1.6, 1.3)

                matches.append({
                    "league": m["league"]["name"],
                    "home": home["name"],
                    "away": away["name"],
                    "home_logo": home["logo"],
                    "away_logo": away["logo"],

                    "prob": {
                        "home": round(hw),
                        "draw": round(dr),
                        "away": round(aw)
                    },

                    "odds": {
                        "home": round(100/hw,2),
                        "draw": round(100/dr,2),
                        "away": round(100/aw,2)
                    },

                    "analysis": "Datos reales + modelo Poisson."
                })

    except Exception as e:
        print("ERROR:", e)

    # 🔥 CLAVE: fallback SIEMPRE si no hay datos
    if len(matches) < 5:

        matches = []  # reset

        teams = [
            ("Manchester City",50),
            ("Arsenal",42),
            ("Real Madrid",541),
            ("Barcelona",529),
            ("Bayern",157),
            ("PSG",85),
            ("Juventus",496),
            ("Milan",489),
            ("River Plate",435),
            ("Boca Juniors",451)
        ]

        for i in range(15):

            h = random.choice(teams)
            a = random.choice(teams)

            if h == a:
                continue

            hw, dr, aw = calc_probs(1.7, 1.3)

            matches.append({
                "league": "Demo (API limitada)",
                "home": h[0],
                "away": a[0],
                "home_logo": f"https://media.api-sports.io/football/teams/{h[1]}.png",
                "away_logo": f"https://media.api-sports.io/football/teams/{a[1]}.png",

                "prob": {
                    "home": round(hw),
                    "draw": round(dr),
                    "away": round(aw)
                },

                "odds": {
                    "home": round(100/hw,2),
                    "draw": round(100/dr,2),
                    "away": round(100/aw,2)
                },

                "analysis": "Modo fallback activo."
            })

    return matches
