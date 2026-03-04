from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.db.session import SessionLocal
from app.models.invite import Invite
from app.models.onboarding import OnboardingApplication
from app.schemas.onboarding import OnboardingSubmitRequest


router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/submit")
def submit_onboarding(request: OnboardingSubmitRequest, db: Session = Depends(get_db)):

    invite = db.query(Invite).filter(Invite.token == request.token).first()

    if not invite:
        raise HTTPException(status_code=404, detail="Invalid invite token")

    if invite.status != "PENDING":
        raise HTTPException(status_code=400, detail="Invite already used")

    new_application = OnboardingApplication(
        invite_id=invite.id,
        name=request.name,
        email=request.email,
        phone=request.phone,
        street=request.street,
        city=request.city,
        state=request.state,
        zip=request.zip,
        country=request.country,
        experience_summary=request.experience_summary,
        primary_skills=request.primary_skills,
        secondary_skills=request.secondary_skills,
        aadhar_card_url=request.aadhar_card_url,
        pan_card_url=request.pan_card_url,
        education_doc_url=request.education_doc_url,
        bank_account_holder=request.bank_account_holder,
        bank_name=request.bank_name,
        bank_account_number=request.bank_account_number,
        bank_ifsc_code=request.bank_ifsc_code,
        nda_text=request.nda_text,
        nda_signature_url=request.nda_signature_url,
        nda_signed_at=datetime.now(timezone.utc),
        is_submitted=True,
        status="PENDING",
        submitted_at=datetime.now(timezone.utc)
    )

    db.add(new_application)

    invite.status = "ACCEPTED"

    db.commit()

    return {"message": "Application submitted successfully"}