from fastapi import APIRouter
from app.api.v1.endpoints import rfps, projects, users, auth, rfp_analysis

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(rfps.router, prefix="/rfps", tags=["rfps"])
api_router.include_router(rfp_analysis.router, prefix="/rfps", tags=["rfp-analysis"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"]) 