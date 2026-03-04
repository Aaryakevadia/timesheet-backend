# app/models/onboarding.py

import uuid
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import ARRAY
from app.db.base import Base


class OnboardingApplication(Base):
    __tablename__ = "onboarding_applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    invite_id = Column(UUID(as_uuid=True), ForeignKey("invites.id"), nullable=True)

    # ========================
    # PERSONAL DETAILS
    # ========================
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    street = Column(Text)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    country = Column(String)

    # ========================
    # PROFESSIONAL PROFILE
    # ========================
    experience_summary = Column(Text)
    primary_skills = Column(ARRAY(String))
    secondary_skills = Column(ARRAY(String))

    # ========================
    # DOCUMENTS
    # ========================
    aadhar_card_url = Column(Text)
    pan_card_url = Column(Text)
    education_doc_url = Column(Text)

    # ========================
    # BANK DETAILS
    # ========================
    bank_account_holder = Column(String)
    bank_name = Column(String)
    bank_account_number = Column(String)
    bank_ifsc_code = Column(String)

    # ========================
    # NDA
    # ========================
    nda_text = Column(Text)
    nda_signature_url = Column(Text)
    nda_signed_at = Column(DateTime(timezone=True))

    # ========================
    # APPLICATION STATE
    # ========================
    is_submitted = Column(Boolean, default=False)

    status = Column(String, default="PENDING")  # PENDING, APPROVED, REJECTED

    admin_notes = Column(Text)

    submitted_at = Column(DateTime(timezone=True))
    reviewed_at = Column(DateTime(timezone=True))
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())