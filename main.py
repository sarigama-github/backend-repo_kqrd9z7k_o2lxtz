import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel

from database import create_document, get_documents
from schemas import Game, Player, Team, Tournament, Match, export_schemas

app = FastAPI(title="Esports & Gaming Tournament API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"service": "Esports API", "status": "ok"}

# --- Schema discovery for viewers ---
@app.get("/schema")
def schema():
    return {"schemas": [s.model_dump() for s in export_schemas()]}

# --- Utility list endpoints (basic read) ---
@app.get("/games")
def list_games(limit: Optional[int] = 50):
    return {"items": get_documents("game", {}, limit)}

@app.get("/players")
def list_players(limit: Optional[int] = 50):
    return {"items": get_documents("player", {}, limit)}

@app.get("/teams")
def list_teams(limit: Optional[int] = 50):
    return {"items": get_documents("team", {}, limit)}

@app.get("/tournaments")
def list_tournaments(limit: Optional[int] = 50):
    return {"items": get_documents("tournament", {}, limit)}

@app.get("/matches")
def list_matches(limit: Optional[int] = 50):
    return {"items": get_documents("match", {}, limit)}

# --- Create endpoints ---
@app.post("/games")
def add_game(payload: Game):
    doc_id = create_document("game", payload)
    return {"inserted_id": doc_id}

@app.post("/players")
def add_player(payload: Player):
    doc_id = create_document("player", payload)
    return {"inserted_id": doc_id}

@app.post("/teams")
def add_team(payload: Team):
    doc_id = create_document("team", payload)
    return {"inserted_id": doc_id}

@app.post("/tournaments")
def create_tournament(payload: Tournament):
    doc_id = create_document("tournament", payload)
    return {"inserted_id": doc_id}

@app.post("/matches")
def create_match(payload: Match):
    doc_id = create_document("match", payload)
    return {"inserted_id": doc_id}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
