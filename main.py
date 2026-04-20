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

API_KEY = "66a3113b48bf7c011b1296c159af91c3"

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

    headers = {
        "x-apisports-key": API_KEY
    }

    all_matches = []

    for league_name, league_id in leagues.items():

        url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&next=2"

        try:
            res = requests.get(url, headers=headers).json()

            if "response" not in res:
                continue

            for m in res["response"]:

                all_matches.append({
                    "match": f"{m['teams']['home']['name']} vs {m['teams']['away']['name']}",
                    "league": league_name,

                    "home": m["teams"]["home"]["name"],
                    "away": m["teams"]["away"]["name"],
                    "home_logo": m["teams"]["home"]["logo"],
                    "away_logo": m["teams"]["away"]["logo"],

                    "markets": {
                        "1X2": {"home": 33, "draw": 34, "away": 33},
                        "over_2_5": {"over": 55, "under": 45},
                        "btts": {"yes": 50, "no": 50}
                    },

                    "analysis": "Modelo en desarrollo basado en forma reciente."
                })

        except Exception as e:
            print("ERROR:", e)
            continue

    # 🔥 fallback si la API falla
    if len(all_matches) == 0:
        return [
            {
                "match": "Manchester City vs Arsenal",
                "league": "Premier League",
                "home": "Manchester City",
                "away": "Arsenal",
                "home_logo": "https://media.api-sports.io/football/teams/50.png",
                "away_logo": "https://media.api-sports.io/football/teams/42.png",
                "markets": {
                    "1X2": {"home": 52, "draw": 25, "away": 23},
                    "over_2_5": {"over": 66, "under": 34},
                    "btts": {"yes": 68, "no": 32}
                },
                "analysis": "City dominante, Arsenal peligroso en transición."
            }
        ]

    return all_matches
