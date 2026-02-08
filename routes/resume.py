from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database.db import get_db
from services.resume_parser import parse_resume
from services.ats_scoring import calculate_ats_score
from services.ai_feedback import generate_ai_feedback
from models.report import ResumeReport
from utils.security import verify_token


router = APIRouter()


security = HTTPBearer()

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    payload = verify_token(credentials.credentials)

    if payload is None:
        return {"error": "Invalid token"}

    resume_text = await parse_resume(file)

    ats = calculate_ats_score(resume_text)
    feedback = generate_ai_feedback(resume_text)

    report = ResumeReport(
        user_email=payload["email"],
        filename=file.filename,
        ats_score=ats["score"],
        feedback="\n".join(feedback),
    )

    db.add(report)
    db.commit()

    return {
        "ats_score": ats["score"],
        "ai_feedback": feedback,
    }


@router.get("/history")
def get_history(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        return {"error": "Invalid token"}

    email = payload["email"]

    reports = db.query(ResumeReport).filter(
        ResumeReport.user_email == email
    ).all()

    return [
        {
            "filename": r.filename,
            "ats_score": r.ats_score,
            "feedback": r.feedback,
        }
        for r in reports
    ]
