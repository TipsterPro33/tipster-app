from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 PEGÁ TU API KEY ACÁ
API_KEY = 66a3113b48bf7c011b1296c159af91c3

@app.get("/matches")
def get_matches():

    url = "https://v3.football.api-sports.io/fixtures?league=128&season=2024"

    headers = {
        "x-apisports-key": API_KEY
    }

    res = requests.get(url, headers=headers).json()

    matches = []

    for m in res["response"][:5]:
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        matches.append({
            "match": f"{home} vs {away}",
            "markets": {
                "1X2": {"home": 33, "draw": 34, "away": 33},
                "over_2_5": {"over": 40, "under": 60},
                "btts": {"yes": 45, "no": 55}
            },
            "analysis": "Datos en construcción (modelo en desarrollo)"
        })

    return matches
