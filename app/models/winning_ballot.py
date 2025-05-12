import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime, date


class WinningBallot(Base):
    __tablename__ = "winning_ballot"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    ballot_id = Column(
        UUID(as_uuid=True),
        ForeignKey("ballot.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # Setting unique True for ballot since a ballot can only win once
    )

    ballot = relationship("Ballot", back_populates="winning_entry")

    @property
    def lottery_draw_date(self) -> date:
        return self.ballot.lottery.draw_date

    @property
    def ballot_created_at(self) -> datetime:
        return self.ballot.created_at

    @property
    def participant_alias(self) -> str:
        return self.ballot.participant.alias 