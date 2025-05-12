from fastapi import FastAPI
from app.api.routers import ballot, lottery, winning_ballot


def include_routers(app: FastAPI):
    """Include all API routers with their prefixes and tags."""
    app.include_router(ballot.router, prefix="/ballot", tags=["ballot"])
    app.include_router(lottery.router, prefix="/lottery", tags=["lottery"])
    app.include_router(winning_ballot.router, prefix="/winning-ballot", tags=["winning-ballot"])