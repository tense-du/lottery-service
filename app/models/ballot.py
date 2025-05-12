import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from zoneinfo import ZoneInfo
from app.models.base import Base


class Ballot(Base):
    __tablename__ = "ballot"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Europe/Amsterdam")),
    )

    participant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("participant.id", ondelete="CASCADE"),
        nullable=False,
    )
    lottery_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lottery.id", ondelete="CASCADE"),
        nullable=False,
    )

    participant = relationship("Participant", back_populates="ballots")
    lottery = relationship("Lottery", back_populates="ballots")
    # Since ballot can't win more than once we set uselist to False
    winning_entry = relationship(
        "WinningBallot",
        back_populates="ballot",
        uselist=False,
        cascade="all, delete-orphan",
    )
