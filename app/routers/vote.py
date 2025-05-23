from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2   
from ..database import get_db

router = APIRouter(
     prefix="/vote",
     tags=["vote"]
)

@router.post("/", status_code=status.HTTP_200_OK)
def vote(vote: schemas.Vote, db:Session = Depends(get_db),user: schemas.Users = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {vote.post_id} does not exists ')
    
    if post.who_created_user == user.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'user {user.id} can not vote own on post')
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'user {user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id = vote.post_id, user_id = user.id)
        db.add(new_vote)
        db.commit()
        return {"message" : "sucessfully added a vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exists")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message" : "successfully deleted vote"}

