from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date
from app.crud.winning_ballot_crud import WinningBallotCRUD
from app.schemas.winning_ballot import WinningBallotResponse, ParticipantWinningBallotsResponse
from app.crud.participant_crud import ParticipantCRUD


class WinningBallotService:
    @staticmethod
    def get_by_lottery_draw_date(
        db: Session,
        draw_date: date,
    ) -> WinningBallotResponse | None:
        """Get the winning ballot for a specific lottery draw date.

        The winning ballot is found by joining through the ballot to get the lottery's draw date.
        This maintains the domain model where a winning ballot is a marker on a ballot,
        and the ballot connects to the lottery.

        Args:
            db (Session): Database session
            draw_date (date): The draw date to look up

        Returns:
            WinningBallotResponse | None: The winning ballot if found, None otherwise
        """
        return WinningBallotCRUD.get_by_lottery_draw_date(
            db=db, draw_date=draw_date
        )

    @staticmethod
    def get_by_participant_id(
        db: Session, participant_id: UUID
    ) -> ParticipantWinningBallotsResponse:
        winning_ballots = WinningBallotCRUD.get_by_participant_id(db=db, participant_id=participant_id)
        return ParticipantWinningBallotsResponse(winning_ballots=winning_ballots)

    @staticmethod
    def get_by_participant_email(
        db: Session, email: str
    ) -> ParticipantWinningBallotsResponse:
        participant = ParticipantCRUD.get_by_email(db=db, email=email)
        if not participant:
            return ParticipantWinningBallotsResponse(winning_ballots=[])
        return WinningBallotService.get_by_participant_id(db=db, participant_id=participant.id)
