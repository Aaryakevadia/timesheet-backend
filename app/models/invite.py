# app/models/invite.py

import uuid
from sqlalchemy import Column, String, DateTime, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class Invite(Base):
    __tablename__ = "invites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String, nullable=False, unique=True)
    token = Column(String, nullable=False, unique=True)

    required_documents = Column(ARRAY(String))

    status = Column(String, default="PENDING")  # PENDING, ACCEPTED, EXPIRED

    expires_at = Column(DateTime(timezone=True), nullable=False)

    accepted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())