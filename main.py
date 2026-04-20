from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "TU_API_KEY"

@app.get("/matches")
def get_matches():

    today = date.today().strftime("%Y-%m-%d")

    url = "https://v3.football.api-sports.io/fixtures?next=50"
    headers = {
        "x-apisports-key": API_KEY
    }

    res = requests.get(url, headers=headers).json()

    matches = []

    for m in res["response"][:6]:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        referee = m["fixture"]["referee"]
        stadium = m["fixture"]["venue"]["name"]
        date_match = m["fixture"]["date"]

        matches.append({
            "match": f"{home} vs {away}",
            "referee": referee,
            "stadium": stadium,
            "date": date_match,

            "markets": {
                "1X2": {"home": 33, "draw": 34, "away": 33},
                "over_2_5": {"over": 40, "under": 60},
                "btts": {"yes": 45, "no": 55}
            },

            "analysis": "Modelo en desarrollo: partido equilibrado."
        })

    return matches
    return matches
