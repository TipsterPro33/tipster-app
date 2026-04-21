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

API_KEY = "66a3113b48bf7c011b1296c159af91c3"

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

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/matches")
def get_matches():

    headers = {"x-apisports-key": API_KEY}
    url = "https://v3.football.api-sports.io/fixtures?next=10"

    matches = []

    try:
        res = requests.get(url, headers=headers, timeout=10).json()

        if "response" in res and len(res["response"]) > 0:

            for m in res["response"]:

                home = m["teams"]["home"]
                away = m["teams"]["away"]

                home_xg = 1.6
                away_xg = 1.3

                hw, dr, aw = calc_probs(home_xg, away_xg)

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
        print("ERROR API:", e)

    # 🔥 FALLBACK (SIEMPRE FUNCIONA)
    if len(matches) == 0:

        teams = [
            ("Manchester City",50),
            ("Arsenal",42),
            ("Real Madrid",541),
            ("Barcelona",529),
            ("Bayern",157),
            ("PSG",85)
        ]

        for i in range(10):

            h = random.choice(teams)
            a = random.choice(teams)

            if h == a:
                continue

            matches.append({
                "league": "Demo",
                "home": h[0],
                "away": a[0],
                "home_logo": f"https://media.api-sports.io/football/teams/{h[1]}.png",
                "away_logo": f"https://media.api-sports.io/football/teams/{a[1]}.png",

                "prob": {"home":50,"draw":25,"away":25},
                "odds": {"home":2.0,"draw":3.2,"away":3.5},
                "analysis": "Modo fallback activo (API limitada)."
            })

    return matches
