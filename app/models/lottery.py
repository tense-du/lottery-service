import uuid
from datetime import datetime
from sqlalchemy import Column, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from zoneinfo import ZoneInfo
from app.models.base import Base


class Lottery(Base):
    __tablename__ = "lottery"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    draw_date = Column(Date, nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Europe/Amsterdam")),
    )
    ballots = relationship(
        "Ballot",
        back_populates="lottery",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Lottery draw_date={self.draw_date.strftime('%d/%m/%Y')}>"
