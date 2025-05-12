from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from uuid import UUID
from pydantic import EmailStr
from app.database.session import get_db
from app.schemas.winning_ballot import (
    WinningBallotByDrawDateQuery,
    WinningBallotResponse,
    ParticipantWinningBallotsResponse,
)
from app.services.winning_ballot_service import WinningBallotService

router = APIRouter()

@router.get("/lottery-draw-date", response_model=WinningBallotResponse)
def get_by_lottery_draw_date(
    query: WinningBallotByDrawDateQuery = Depends(),
    db: Session = Depends(get_db),
):
    """Get the single winning ballot for a specific lottery draw date.
    
    By default, returns yesterday's winning ballot if no date is provided.
    Cannot query future dates.
    
    Raises:
        404: If no winning ballot exists for the specified draw date
    """
    winning_ballot = WinningBallotService.get_by_lottery_draw_date(
        db=db,
        draw_date=query.draw_date,
    )
    if not winning_ballot:
        raise HTTPException(
            status_code=404,
            detail=f"No winning ballot found for lottery draw date {query.draw_date}.",
        )
    
    return winning_ballot


@router.get("/participant-id", response_model=ParticipantWinningBallotsResponse)
def get_by_participant_id(
    participant_id: UUID = Query(
        ...,
        description="UUID of the participant to look up their winning ballots"
    ),
    db: Session = Depends(get_db),
):
    """Get winning ballots for a participant."""
    return WinningBallotService.get_by_participant_id(
        db=db, participant_id=participant_id
    )


@router.get("/participant-email", response_model=ParticipantWinningBallotsResponse)
def get_by_participant_email(
    email: EmailStr = Query(
        ...,
        description="Email of the participant to look up their winning ballots"
    ),
    db: Session = Depends(get_db),
):
    """Get winning ballots for a participant by their email.
    If no participant is found with provided email, returns an empty list."""
    return WinningBallotService.get_by_participant_email(
        db=db, email=email
    )
