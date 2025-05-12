from datetime import date
from uuid import UUID
from pydantic import BaseModel


# Lottery Management Schemas
class UpcomingLottery(BaseModel):
    lottery_id: UUID
    draw_date: date
    ballot_count: int

    class Config:
        from_attributes = True


class UpcomingLotteriesResponse(BaseModel):
    lotteries: list[UpcomingLottery]

    class Config:
        from_attributes = True

