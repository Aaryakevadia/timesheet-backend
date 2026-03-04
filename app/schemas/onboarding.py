from pydantic import BaseModel, EmailStr
from typing import List, Optional


class OnboardingSubmitRequest(BaseModel):
    token: str
    name: str
    email: EmailStr
    phone: str

    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None

    experience_summary: Optional[str] = None
    primary_skills: List[str]
    secondary_skills: Optional[List[str]] = []

    aadhar_card_url: Optional[str] = None
    pan_card_url: Optional[str] = None
    education_doc_url: Optional[str] = None

    bank_account_holder: str
    bank_name: str
    bank_account_number: str
    bank_ifsc_code: str

    nda_text: str
    nda_signature_url: str