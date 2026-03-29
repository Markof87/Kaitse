from fastapi import APIRouter

from app.api.v1 import competitions, player_stats, players, teams, seasons

api_router = APIRouter()

api_router.include_router(competitions.router)
api_router.include_router(seasons.router)
api_router.include_router(teams.router)
api_router.include_router(players.router)
api_router.include_router(player_stats.router)