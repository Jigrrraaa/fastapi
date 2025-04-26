from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class PostBase(BaseModel):
     title: str
     content: str
     published: bool = True

class PostCreate(PostBase):
    pass

class Users(BaseModel):
     id : int
     email : EmailStr
     created_at : datetime

class Post(PostBase):
     id : int
     created_at: datetime
     who_created_user : int
     created_user : Users
     
     class Config:
          orm_mode = True

class PostOut(BaseModel):
     post : Post
     votes: int

     class Config:
        orm_mode = True


class UserCreate(BaseModel):
     email : EmailStr
     password : str



     # class Config:
     #      orm_mode = True
class UserLogin(BaseModel):
     email: EmailStr
     password : str
     
class Token(BaseModel):
     access_token : str
     token_type :str

class TokenData(BaseModel):
     id:Optional[int] = None


class Vote(BaseModel):
     post_id : int
     dir : conint(le=1) # type: ignore