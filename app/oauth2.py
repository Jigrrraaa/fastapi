from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from . import schemas,database, models
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .config import setting


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
#secret_key
#Algorithm
#Expiration_time

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, creditals_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        id :str = payload.get("user_id")
        if id is None:
            print(False)
            raise creditals_exception
        
        token_data = schemas.TokenData(id = id)
    
    except JWTError:
        raise creditals_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    creditials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail=f" Could not validate the creditials", headers={"WWW-Authenticate" : "Bearer"})

    token = verify_access_token(token, creditials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
    