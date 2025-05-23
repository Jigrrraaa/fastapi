from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key= True, nullable= False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default = 'TRUE', nullable= False)
    created_at = Column(TIMESTAMP(timezone = True), server_default=text('now()'))
    who_created_user = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable = False)

    created_user = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, nullable= False)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), server_default=text('now()'))
    phone_number = Column(String, nullable= True)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable = False, primary_key= True)
    post_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"), nullable = False, primary_key= True)