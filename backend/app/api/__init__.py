from fastapi import APIRouter
from .endpoints import users, team_members

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(team_members.router, prefix="/team-members", tags=["team-members"])
