from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from datetime import date
from app.models import WinningBallot, Lottery, Ballot


class WinningBallotCRUD:
    @staticmethod
    def get_by_lottery_draw_date(
        db: Session, draw_date: date
    ) -> WinningBallot | None:
        """Get winning ballot for a specific lottery draw date by joining through ballot to lottery."""
        return (
            db.query(WinningBallot)
            .join(WinningBallot.ballot)  # Join to ballot
            .join(Ballot.lottery)  # Join ballot to lottery
            .options(
                joinedload(WinningBallot.ballot).joinedload(Ballot.participant)  # Eager load participant
            )
            .filter(Lottery.draw_date == draw_date)
            .first()
        )

    @staticmethod
    def get_by_participant_id(
        db: Session, participant_id: UUID
    ) -> list[WinningBallot]:
        """Get all winning ballots for a participant by joining through ballot."""
        return (
            db.query(WinningBallot)
            .join(WinningBallot.ballot)  # Join to ballot
            .options(
                joinedload(WinningBallot.ballot).joinedload(Ballot.participant)
            )
            .filter(Ballot.participant_id == participant_id)
            .all()
        )

    @staticmethod
    def create(db: Session, ballot_id: UUID) -> WinningBallot:
        winning_ballot = WinningBallot(ballot_id=ballot_id)
        db.add(winning_ballot)
        db.flush()
        db.refresh(winning_ballot)
        return winning_ballot
