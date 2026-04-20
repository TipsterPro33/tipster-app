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
def matches():
    return [
        {
            "match": "San Lorenzo vs Velez",
            "markets": {
                "1X2": {"home": 34, "draw": 36, "away": 30},
                "over_2_5": {"over": 26, "under": 74},
                "btts": {"yes": 46, "no": 54}
            },
            "analysis": "Partido cerrado, tendencia a pocos goles y empate probable."
        },
        {
            "match": "Tigre vs Huracan",
            "markets": {
                "1X2": {"home": 22, "draw": 33, "away": 45},
                "over_2_5": {"over": 34, "under": 66},
                "btts": {"yes": 36, "no": 64}
            },
            "analysis": "Huracán llega mejor, Tigre con bajo poder ofensivo."
        }
    ]
