from fastapi import FastAPI

app = FastAPI()

@app.get("/picks")
def picks():
    return {
        "match": "San Lorenzo vs Velez",
        "picks": [
            {
                "market": "Under 2.5",
                "prob": 73,
                "odds": 1.80,
                "value": 16
            },
            {
                "market": "Draw",
                "prob": 36,
                "odds": 3.20,
                "value": 5
            }
        ]
    }
