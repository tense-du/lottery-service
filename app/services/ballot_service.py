from sqlalchemy.orm import Session
from datetime import date
from app.models import Ballot
from app.services.participant_service import ParticipantService
from app.services.lottery_service import LotteryService
from app.crud.ballot_crud import BallotCRUD
from app.exceptions.ballot import BallotSubmissionException
from app.core.logging import logger


class BallotService:
    """Service handling ballot submission and management.

    This service manages the process of submitting ballots for lotteries,
    including participant creation/lookup and lottery creation/lookup.
    """

    @staticmethod
    def submit_by_lottery_draw_date(db: Session, email: str, draw_date: date) -> Ballot:
        """Submit a ballot for a lottery on a specific draw date.

        This method handles the complete ballot submission process:
        1. Gets or creates a participant for the given email
        2. Gets or creates a lottery for the given draw date
        3. Creates a ballot linking the participant and lottery

        Raises:
            BallotSubmissionException: If there's an error during submission
        """
        try:
            with db.begin():
                # Get or create participant with email
                participant = ParticipantService.get_or_create_participant(
                    db=db, email=email
                )

                # Get or create lottery with draw date
                lottery = LotteryService.get_or_create_lottery_by_draw_date(
                    db=db, draw_date=draw_date
                )

                # Create ballot
                ballot = BallotCRUD.create(
                    db=db, participant_id=participant.id, lottery_id=lottery.id
                )
                return ballot
        except Exception as e:
            logger.error(f"Error submitting ballot: {str(e)}", exc_info=True)
            raise BallotSubmissionException("Error submitting ballot.") from e
