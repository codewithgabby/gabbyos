from fastapi import APIRouter
from app.api.v1 import auth, categories, routines, weekly_planner, dashboard, daily_logs, streaks, reflections, goals, inbox, knowledge, projects, analytics

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(categories.router)
api_router.include_router(routines.router)
api_router.include_router(weekly_planner.router)
api_router.include_router(dashboard.router)
api_router.include_router(daily_logs.router)
api_router.include_router(streaks.router)
api_router.include_router(reflections.router)
api_router.include_router(goals.router)
api_router.include_router(inbox.router)
api_router.include_router(knowledge.router)
api_router.include_router(projects.router)
api_router.include_router(analytics.router)