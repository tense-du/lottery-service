from datetime import date, timedelta, datetime
from uuid import UUID
from zoneinfo import ZoneInfo
from pydantic import BaseModel, field_validator

class WinningBallotByDrawDateQuery(BaseModel):
    draw_date: date = datetime.now(ZoneInfo("Europe/Amsterdam")).date() - timedelta(days=1)  # Default to yesterday

    @field_validator("draw_date")
    @classmethod
    def draw_date_not_in_future(cls, v: date) -> date:
        """Validate that the draw date is not in the future."""
        if v > datetime.now(ZoneInfo("Europe/Amsterdam")).date():
            raise ValueError("Draw date cannot be in the future")
        return v


class WinningBallotResponse(BaseModel):
    ballot_id: UUID
    lottery_draw_date: date
    ballot_created_at: datetime
    participant_alias: str

    class Config:
        from_attributes = True


class ParticipantWinningBallot(BaseModel):
    ballot_id: UUID
    ballot_created_at: datetime
    lottery_draw_date: date

    class Config:
        from_attributes = True


class ParticipantWinningBallotsResponse(BaseModel):
    winning_ballots: list[ParticipantWinningBallot]