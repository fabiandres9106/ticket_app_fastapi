from fastapi import APIRouter
from app.api.endpoints import user, role, stage, event, event_dates, survey, tickets, auth


api_router = APIRouter()
api_router.include_router(user.router, prefix="/users/", tags=["users"])
api_router.include_router(role.router, prefix="/roles", tags=["roles"])
api_router.include_router(stage.router, prefix="/stage", tags=["stages"])
api_router.include_router(event.router, prefix="/event", tags=["events"])
api_router.include_router(event_dates.router, prefix="/event_date", tags=["event_dates"])
api_router.include_router(survey.router, prefix="/survey", tags=["surveys"])
api_router.include_router(tickets.router, prefix="/ticket", tags=["tickets"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])