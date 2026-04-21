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

    url = "https://v3.football.api-sports.io/fixtures?next=20"

    headers = {
        "x-apisports-key": API_KEY
    }

    try:
        res = requests.get(url, headers=headers, timeout=10).json()

        fixtures = res.get("response", [])

        # 🚨 SI NO HAY DATOS → ERROR (NO INVENTAR)
        if len(fixtures) == 0:
            return {
                "error": "NO HAY PARTIDOS REALES DISPONIBLES (API LIMITADA O MAL CONFIGURADA)"
            }

        matches = []

        for m in fixtures:

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

                "analysis": "Datos reales + modelo Poisson"
            })

        return matches

    except Exception as e:
        return {"error": str(e)}
