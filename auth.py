from passlib.context import CryptContext
import jwt, models
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.orm import Session
SECRET_KEY = "fastchat_super_secret_key_sifat"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_password_hash(password: str):
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
def get_current_user(token: str = Depends(oauth2_scheme), db: Session= Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload =jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username =payload.get("sub")
        if username is None:
            raise credentials_exception
        user_found= db.query(models.User).filter(models.User.username == username).first()
        if not user_found:
            raise credentials_exception
        return user_found
    except Exception:
        raise credentials_exception