from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import bcrypt

from app.db.session import SessionLocal
from app.models.onboarding import OnboardingApplication
from app.models.user import User


router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.patch("/onboarding/{application_id}/approve")
def approve_application(application_id: str, db: Session = Depends(get_db)):

    application = db.query(OnboardingApplication).filter(
        OnboardingApplication.id == application_id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if application.status != "PENDING":
        raise HTTPException(status_code=400, detail="Already processed")

    # Generate temporary password
    temp_password = "Temp@123"
    hashed_password = bcrypt.hashpw(
        temp_password.encode(), bcrypt.gensalt()
    ).decode()

    # Create user
    new_user = User(
        name=application.name,
        email=application.email,
        phone=application.phone,
        role=["CONSULTANT"],
        password_hash=hashed_password,
        is_active=True,
        nda_signed=True,
        bank_details_submitted=True,
        onboarded_on=datetime.now(timezone.utc).date()
    )

    db.add(new_user)

    # Update application
    application.status = "APPROVED"
    application.reviewed_at = datetime.now(timezone.utc)

    db.commit()

    return {
        "message": "Application approved",
        "temporary_password": temp_password
    }