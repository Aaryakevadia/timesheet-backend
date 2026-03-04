from sqlalchemy import Column, String, Boolean, Date, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    role = Column(ARRAY(String))
    profile_status = Column(String, default="COMPLETE")
    rate = Column(String, default="0")
    is_active = Column(Boolean, default=True)
    nda_signed = Column(Boolean, default=False)
    bank_details_submitted = Column(Boolean, default=False)
    onboarded_on = Column(Date)
    password_hash = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())