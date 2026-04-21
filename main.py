from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "66a3113b48bf7c011b1296c159af91c3"
ODDS_KEY = "TU_ODDS_API_KEY"

leagues = [39,140,135,78,61,128,71,253]

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
    matches = []

    for league in leagues:

        url = f"https://v3.football.api-sports.io/fixtures?league={league}&next=5"

        try:
            res = requests.get(url, headers=headers).json()

            for m in res.get("response", []):

                home = m["teams"]["home"]
                away = m["teams"]["away"]

                # xG estimado simple (luego mejoramos)
                home_xg = 1.5
                away_xg = 1.2

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

                    "analysis": "Modelo Poisson basado en xG estimado."
                })

        except:
            continue

    return matches[:40]
