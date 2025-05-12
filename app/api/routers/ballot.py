from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.ballot import (
    SubmitBallotByLotteryDrawDateRequest,
    SubmitBallotResponse,
)
from app.services.ballot_service import BallotService
from app.exceptions.ballot import BallotSubmissionException

router = APIRouter()


@router.post("/submit-by-lottery-draw-date", response_model=SubmitBallotResponse)
def submit_by_lottery_draw_date(
    ballot: SubmitBallotByLotteryDrawDateRequest, db: Session = Depends(get_db)
):
    """Submit a ballot for a lottery.
    
    If the participant doesn't exist, they will be created with a random alias.
    If no lottery exists for the given draw date, a new lottery will be created for that date.
    The draw date must be in the future and within the configured maximum days ahead.
    
    Raises:
        HTTPException: If there's an error during submission
    """
    try:
        db_ballot = BallotService.submit_by_lottery_draw_date(
            db=db, email=ballot.email, draw_date=ballot.draw_date
        )
        return db_ballot
    except BallotSubmissionException as e:
        raise HTTPException(status_code=500, detail=str(e))
