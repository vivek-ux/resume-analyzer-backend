from sqlalchemy import Column, Integer, String
from database.db import Base

class ResumeReport(Base):
    __tablename__ = "resume_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    filename = Column(String)
    ats_score = Column(Integer)
    feedback = Column(String)
