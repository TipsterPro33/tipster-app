from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/matches")
def get_matches():
    return [
        {
            "match": "Real Madrid vs Barcelona",
            "league": "La Liga",
            "referee": "Antonio Mateu",
            "stadium": "Santiago Bernabéu",
            "date": "Hoy 21:00",
            "markets": {
                "1X2": {"home": 45, "draw": 28, "away": 27},
                "over_2_5": {"over": 62, "under": 38},
                "btts": {"yes": 70, "no": 30}
            },
            "analysis": "Partido de alto ritmo, tendencia a goles."
        },
        {
            "match": "Manchester City vs Arsenal",
            "league": "Premier League",
            "referee": "Michael Oliver",
            "stadium": "Etihad Stadium",
            "date": "Hoy 18:30",
            "markets": {
                "1X2": {"home": 52, "draw": 25, "away": 23},
                "over_2_5": {"over": 66, "under": 34},
                "btts": {"yes": 68, "no": 32}
            },
            "analysis": "City dominante, Arsenal peligroso en transición."
        }
    ]
