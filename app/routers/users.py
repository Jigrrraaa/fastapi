from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from psycopg.rows import dict_row
from sqlalchemy.orm import Session
from .. import models, schemas, utils   
from ..database import get_db

router = APIRouter(
     prefix="/User",
     tags=["User"]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model= schemas.Users)
def create_user(user: schemas.UserCreate , db:Session = Depends(get_db)):
     #hased(encrpt) the password
     user.password = utils.hash(user.password) 
     new_user = models.User(**user.dict())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user

@router.get("/{id}", response_model= schemas.Users)
def get_user(id:int, db:Session = Depends(get_db)):
     get_user = db.query(models.User).filter(models.User.id == id).first()

     if not get_user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} was not found")
     
     return get_user