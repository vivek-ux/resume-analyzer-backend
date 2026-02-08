from jose import jwt, JWTError
from datetime import datetime, timedelta
from argon2 import PasswordHasher

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

ph = PasswordHasher()


def hash_password(password: str):
    return ph.hash(password)


def verify_password(password: str, hashed: str):
    return ph.verify(hashed, password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
