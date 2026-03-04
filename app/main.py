from fastapi import FastAPI
from app.api import auth, invite, onboarding
from app.db.base import Base
from app.db.session import engine
from app.api import admin

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(invite.router)
app.include_router(onboarding.router)