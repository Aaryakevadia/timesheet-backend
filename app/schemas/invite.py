from pydantic import BaseModel, EmailStr
from typing import List


class InviteRequest(BaseModel):
    email: EmailStr
    required_documents: List[str]