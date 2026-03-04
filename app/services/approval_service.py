from app.models.user import User
from app.models.onboarding import OnboardingApplication
from datetime import date

def approve_application(db, application_id, admin_id):

    app = db.query(OnboardingApplication).filter_by(id=application_id).first()

    new_user = User(
        name=app.name,
        email=app.email,
        phone=app.phone,
        role=["CONSULTANT"],
        nda_signed=True,
        bank_details_submitted=True,
        onboarded_on=date.today(),
        password_hash="TEMP_HASH"
    )

    db.add(new_user)
    app.status = "APPROVED"
    app.reviewed_by = admin_id

    db.commit()