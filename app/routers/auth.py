from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import session
from ..database import get_db
from .. import schemas, utils, models, oauth2

router = APIRouter(tags= ['Authentication'])

@router.post('/login', response_model = schemas.Token)
def login(user_creaditials: OAuth2PasswordRequestForm = Depends() , db:session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_creaditials.username).first()

    error = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Creditails')
    if not user:
        raise error
    
    if not utils.verify(user_creaditials.password, user.password):
        raise error
    
    access_token = oauth2.create_access_token(data={"user_id" :user.id})
    return {"access_token" : access_token, "token_type" :"Bearer"}
