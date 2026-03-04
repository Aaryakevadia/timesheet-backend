import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from uuid import UUID
from datetime import datetime, date


def seed_users():
    db: Session = SessionLocal()

    existing = db.query(User).filter(User.email == "superadmin@timesheet.com").first()

    if existing:
        print("Super admin already exists.")
        return

    super_admin = User(
        id=UUID("3094bc63-b48f-4e56-b3a8-4b86fa3d3f5f"),
        name="Super Admin",
        email="superadmin@timesheet.com",
        phone="9999999999",
        role=["SUPER_ADMIN"],
        profile_status="COMPLETE",
        rate=0.00,
        is_active=True,
        nda_signed=True,
        bank_details_submitted=True,
        onboarded_on=date(2026, 3, 3),
        password_hash="$2b$12$QaQAnsO8emSU/1PrSJiNPOBJB/C2i7tNkx8Mm2kmCzwb3X4lMc8EG",
        created_at=datetime.fromisoformat("2026-03-03T17:22:54.085031+05:30")
    )

    db.add(super_admin)
    db.commit()

    print("Super Admin seeded successfully.")


if __name__ == "__main__":
    seed_users()