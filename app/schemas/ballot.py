from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, timedelta, datetime
from uuid import UUID
from zoneinfo import ZoneInfo
from app.core.settings import settings


class SubmitBallotByLotteryDrawDateRequest(BaseModel):
    email: EmailStr
    draw_date: date

    @field_validator("draw_date")
    @classmethod
    def validate_draw_date(cls, v: date) -> date:
        today = datetime.now(ZoneInfo("Europe/Amsterdam")).date()

        if v < today:
            raise ValueError("Draw date cannot be in the past")
        if v > today + timedelta(days=settings.LOTTERY_DRAW_DATE_MAX_DAYS_AHEAD):
            raise ValueError(
                f"Draw date cannot be more than {settings.LOTTERY_DRAW_DATE_MAX_DAYS_AHEAD} days in the future"
            )

        return v


class SubmitBallotResponse(BaseModel):
    id: UUID
    class Config:
        from_attributes = True

