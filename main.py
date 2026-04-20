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

API_KEY = "TU_API_KEY"

# ligas importantes
leagues = {
    "Premier League": 39,
    "La Liga": 140,
    "Serie A": 135,
    "Bundesliga": 78,
    "Ligue 1": 61,
    "Argentina": 128,
    "Brasil": 71,
    "MLS": 253
}

@app.get("/matches")
def get_matches():

    all_matches = []

    headers = {
        "x-apisports-key": API_KEY
    }

    for league_name, league_id in leagues.items():

        url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&next=3"

        try:
            res = requests.get(url, headers=headers).json()

            for m in res.get("response", []):

                all_matches.append({
                    "match": f"{m['teams']['home']['name']} vs {m['teams']['away']['name']}",
                    "league": league_name,
                    "date": m["fixture"]["date"],
                    "stadium": m["fixture"]["venue"]["name"],
                    "referee": m["fixture"]["referee"],

                    "markets": {
                        "1X2": {"home": 33, "draw": 34, "away": 33},
                        "over_2_5": {"over": 55, "under": 45},
                        "btts": {"yes": 50, "no": 50}
                    },

                    "analysis": "Modelo en desarrollo basado en contexto y forma."
                })

        except:
            continue

    return all_matches
