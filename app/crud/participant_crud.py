from sqlalchemy.orm import Session
from typing import Optional
from app.models import Participant


class ParticipantCRUD:
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Participant]:
        return Participant.find_by_email(session=db, email=email)

    @staticmethod
    def get_by_alias(db: Session, alias: str) -> Optional[Participant]:
        return db.query(Participant).filter_by(alias=alias).first()

    @staticmethod
    def create(db: Session, email: str, alias: str) -> Participant:
        participant = Participant(email=email, alias=alias)
        db.add(participant)
        db.flush()
        db.refresh(participant)
        return participant
