from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import User
from backend.app.utils.hashing import hash_password, verify_password
#from pydantic import BaseModel
from backend.app.auth.jwt_handler import create_access_token
from backend.app.auth.schemas import UserCreate

router = APIRouter(prefix="/chat", tags=["chat"])


    
@router.post("/register")
def register(user: UserCreate, db: Session=Depends(get_db)):
    existing = db.query(User).filter(User.username==user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username Already Exists")
    db_user = User(username=user.username, password_hash=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token = create_access_token({
        "user_id": db_user.id,
        "username": db_user.username
    })
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user":{
            "id": db_user.id,
            "username": user.username
            }
    }

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({
        "user_id": db_user.id,
        "username": db_user.username
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "username": db_user.username
        }
    }