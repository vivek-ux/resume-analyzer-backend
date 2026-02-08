from fastapi import FastAPI
from database.db import engine, Base
from models.user import User
from models.report import ResumeReport

from routes import auth, resume, admin

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
app.include_router(resume.router, prefix="/resume")
app.include_router(admin.router, prefix="/admin")


@app.get("/")
def root():
    return {"message": "Resume Analyzer API running"}
