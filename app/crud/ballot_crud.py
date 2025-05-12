from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from app.models import Ballot


class BallotCRUD:
    @staticmethod
    def create(db: Session, participant_id: UUID, lottery_id: UUID) -> Ballot:
        ballot = Ballot(participant_id=participant_id, lottery_id=lottery_id)
        db.add(ballot)
        db.flush()
        db.refresh(ballot)
        return ballot

    @staticmethod
    def get_by_lottery_id(db: Session, lottery_id: UUID) -> list[Ballot]:
        return db.query(Ballot).filter_by(lottery_id=lottery_id).all()
