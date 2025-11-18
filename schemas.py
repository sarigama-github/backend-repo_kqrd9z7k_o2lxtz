"""
Database Schemas for Esports & Gaming Tournament Management

Each Pydantic model maps to a MongoDB collection using the lowercase of the class name.
- Game      -> "game"
- Player    -> "player"
- Team      -> "team"
- Tournament-> "tournament"
- Match     -> "match"
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any

# Games
class Game(BaseModel):
    name: str = Field(..., description="Game name")
    logo: Optional[str] = Field(None, description="Logo URL")
    genre: Optional[str] = Field(None, description="Game genre")
    platform: Optional[str] = Field(None, description="Primary platform")
    release_year: Optional[int] = Field(None, description="Release year")

# Players
class PlayerStatistics(BaseModel):
    kda: Optional[float] = None
    winrate: Optional[float] = None
    matches_played: Optional[int] = None
    notes: Optional[str] = None

class Player(BaseModel):
    player_name: str
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    country: Optional[str] = None
    team_id: Optional[str] = Field(None, description="Team ObjectId as string")
    rank: Optional[str] = None
    statistics: Optional[PlayerStatistics] = None

# Teams
class TeamStatistics(BaseModel):
    winrate: Optional[float] = None
    matches_played: Optional[int] = None
    trophies: Optional[int] = None

class Team(BaseModel):
    team_name: str
    logo: Optional[str] = None
    country: Optional[str] = None
    members: Optional[List[str]] = Field(default_factory=list, description="List of player ids")
    coach: Optional[str] = None
    team_statistics: Optional[TeamStatistics] = None

# Tournaments
class Tournament(BaseModel):
    tournament_name: str
    game: Optional[str] = Field(None, description="Game id or name")
    format: Optional[str] = Field(None, description="Format e.g. BO3, Swiss, Groups+Playoffs")
    start_date: Optional[str] = Field(None, description="ISO date string")
    end_date: Optional[str] = Field(None, description="ISO date string")
    prize_pool: Optional[float] = Field(None, ge=0)
    teams_limit: Optional[int] = Field(None, ge=2)
    status: Optional[str] = Field(None, description="planned|ongoing|completed")

# Matches
class MatchStatistics(BaseModel):
    duration_minutes: Optional[int] = None
    highlights: Optional[str] = None

class Match(BaseModel):
    match_id: str
    tournament_id: Optional[str] = None
    team_a: Optional[str] = None
    team_b: Optional[str] = None
    schedule_time: Optional[str] = Field(None, description="ISO datetime string")
    score: Optional[str] = Field(None, description="e.g. 2-1")
    winner: Optional[str] = None
    match_statistics: Optional[MatchStatistics] = None

# Minimal schema export for viewer tools
class SchemaExport(BaseModel):
    name: str
    fields: Dict[str, Any]


def export_schemas() -> List[SchemaExport]:
    def fields_of(model: BaseModel):
        return {k: str(v.annotation) for k, v in model.model_fields.items()}

    return [
        SchemaExport(name="game", fields=fields_of(Game)),
        SchemaExport(name="player", fields=fields_of(Player)),
        SchemaExport(name="team", fields=fields_of(Team)),
        SchemaExport(name="tournament", fields=fields_of(Tournament)),
        SchemaExport(name="match", fields=fields_of(Match)),
    ]
