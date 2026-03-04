import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.invite import Invite
from app.schemas.invite import InviteRequest


router = APIRouter(prefix="/invite", tags=["Invite"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
def send_invite(request: InviteRequest, db: Session = Depends(get_db)):

    # Check if invite already exists
    existing = db.query(Invite).filter(Invite.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invite already exists for this email"
        )

    token = str(uuid.uuid4())

    new_invite = Invite(
        email=request.email,
        token=token,
        required_documents=request.required_documents,
        status="PENDING",
        expires_at=datetime.utcnow() + timedelta(days=3)
    )

    db.add(new_invite)
    db.commit()
    db.refresh(new_invite)

    return {
        "message": "Invite sent",
        "token": token
    }

@router.get("/validate")
def validate_invite(token: str, db: Session = Depends(get_db)):

    invite = db.query(Invite).filter(Invite.token == token).first()

    if not invite:
        raise HTTPException(status_code=404, detail="Invalid invite token")

    if invite.status != "PENDING":
        raise HTTPException(status_code=400, detail="Invite already used")

    if invite.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invite expired")

    return {
        "valid": True,
        "email": invite.email,
        "required_documents": invite.required_documents
    }