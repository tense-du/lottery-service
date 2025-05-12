from sqlalchemy.orm import Session
from app.models import Participant
from app.utils.random_utils import generate_random_alphanumeric
from app.crud.participant_crud import ParticipantCRUD


class ParticipantService:
    @staticmethod
    def get_or_create_participant(db: Session, email: str) -> Participant:
        """Check if participant exists with email. If not, create one with unique alias.

        """
        participant = ParticipantCRUD.get_by_email(db=db, email=email)

        if not participant:
            # Generate a unique alias if the participant doesn't exist
            alias = generate_random_alphanumeric()
            while ParticipantCRUD.get_by_alias(db=db, alias=alias):
                alias = generate_random_alphanumeric()
            participant = ParticipantCRUD.create(db=db, email=email, alias=alias)

        return participant
