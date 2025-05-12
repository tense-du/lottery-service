from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.lottery import (
    UpcomingLotteriesResponse,
)
from app.services.lottery_service import LotteryService

router = APIRouter()


# Lottery Management Endpoints
@router.get("/upcoming", response_model=UpcomingLotteriesResponse)
def get_upcoming(
    db: Session = Depends(get_db),
):
    """Get all upcoming lotteries with their ballot counts."""
    return LotteryService.get_upcoming(db=db)
