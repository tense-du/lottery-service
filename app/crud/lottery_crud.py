from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime
from typing import Optional
from app.models import Lottery, Ballot
from zoneinfo import ZoneInfo


class LotteryCRUD:
    @staticmethod
    def get_by_draw_date(db: Session, draw_date: date) -> Optional[Lottery]:
        return db.query(Lottery).filter_by(draw_date=draw_date).first()

    @staticmethod
    def get_by_id(db: Session, lottery_id: int) -> Optional[Lottery]:
        return db.query(Lottery).filter_by(id=lottery_id).first()

    @staticmethod
    def create(db: Session, draw_date: date) -> Lottery:
        lottery = Lottery(draw_date=draw_date)
        db.add(lottery)
        db.flush()
        db.refresh(lottery)
        return lottery

    @staticmethod
    def get_upcoming(db: Session) -> list[tuple[Lottery, int]]:
        today = datetime.now(ZoneInfo("Europe/Amsterdam")).date()
        return (
            db.query(
                Lottery,
                func.count(Ballot.id).label('ballot_count')
            )
            .outerjoin(Ballot)
            .filter(Lottery.draw_date >= today)
            .group_by(Lottery.id)
            .order_by(Lottery.draw_date)
            .all()
        )
