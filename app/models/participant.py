from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
import uuid
from app.models.base import Base
from app.core.security import create_encrypted_and_hashed_versions_of_data, decrypt_data, hash_for_search
from typing import Optional


class Participant(Base):
    """Each participant must have a unique email and alias.
    Email addresses are stored in encrypted form with a searchable hash.

    """
    __tablename__ = "participant"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    email = Column(String(512), nullable=False)  # Encrypted email
    email_hash = Column(String(64), nullable=False, unique=True)  # For searching
    alias = Column(String(255), nullable=False, unique=True) 

    ballots = relationship(
        "Ballot",
        back_populates="participant",
        cascade="all, delete-orphan",
    )

    def __init__(self, **kwargs):
        """Initialize a participant with encrypted email and hash.

        """
        if 'email' in kwargs:
            encrypted_email, email_hash = create_encrypted_and_hashed_versions_of_data(kwargs['email'])
            kwargs['email'] = encrypted_email
            kwargs['email_hash'] = email_hash
        super().__init__(**kwargs)

    @property
    def decrypted_email(self) -> str:
        """Get the decrypted email address.

        Returns:
            The decrypted email address

        Raises:
            ValueError: If the email cannot be decrypted
        """
        return decrypt_data(self.email)

    @classmethod
    def find_by_email(cls, session, email: str) -> Optional['Participant']:
        email_hash = hash_for_search(email)
        return session.query(cls).filter(cls.email_hash == email_hash).first()

    def __repr__(self):
        return f"<Participant(alias={self.alias})>"
