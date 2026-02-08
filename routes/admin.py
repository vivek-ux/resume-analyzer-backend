from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from models.user import User
from utils.dependencies import require_admin

router = APIRouter()

@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    users = db.query(User).all()

    return [
        {
            "email": u.email,
            "role": u.role
        }
        for u in users
    ]
