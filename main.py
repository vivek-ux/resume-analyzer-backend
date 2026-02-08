from fastapi import FastAPI
from database.db import engine, Base
from models.user import User
from models.report import ResumeReport
from fastapi.middleware.cors import CORSMiddleware


from routes import auth, resume, admin

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
app.include_router(resume.router, prefix="/resume")
app.include_router(admin.router, prefix="/admin")


@app.get("/")
def root():
    return {"message": "Resume Analyzer API running"}
