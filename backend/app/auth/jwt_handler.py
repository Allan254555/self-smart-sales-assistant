from datetime import datetime, timedelta
from jose import jwt, JWTError
from backend.app.core import config
from backend.app.auth.schemas import TokenData

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM if hasattr(config, 'ALGORITHM') else "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = config.ACCESS_TOKEN_EXPIRE_HOURS

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        username: str = payload.get("username")
        return TokenData(user_id=user_id, username=username)
    except JWTError:
        return TokenData()