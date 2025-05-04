from typing import List, Optional
from fastapi import HTTPException, Response, status, Depends, APIRouter
# from psycopg.rows import dict_row
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
     prefix="/posts",
     tags=["Posts"]
)

@router.get("", response_model= List[schemas.PostOut])
def get_Posts(db: Session = Depends(get_db),
              user :models.User = Depends(oauth2.get_current_user),
              limit : int = 10,
              skip :int = 0, 
              search : Optional[str] = ""):
     # old method to get data from sql
     # cursor.execute("""SELECT * FROM Posts""")
     # posts = cursor.fetchall()
     # posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
     results = (
        db.query(models.Posts, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True)
        .filter(models.Posts.title.contains(search))
        .group_by(models.Posts.id)
        .limit(limit)
        .offset(skip)
        .all()
     )
     return [{"post": post, "votes": votes} for post, votes in results]

@router.post("", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_Post(post: schemas.PostCreate, db:Session = Depends(get_db), user :models.User = Depends(oauth2.get_current_user)):
     # cursor.execute("""INSERT INTO posts (title,  content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
     # new_posts = cursor.fetchone()
     # conn.commit()
     new_posts = models.Posts(who_created_user = user.id, **post.dict())
     db.add(new_posts)
     db.commit()
     db.refresh(new_posts)
     return new_posts

# @app.get("/posts/latest")
# def get_latest_post():
#      latest_post = my_posts[len(my_posts) - 1]
#      return{"Latest_Post": latest_post}

@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id:int, db:Session = Depends(get_db),user :models.User = Depends(oauth2.get_current_user)):
     # print(type(id))
     # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
     # get_posts = cursor.fetchone()
     # print(user.email)
     # post = db.query(models.Posts).filter(models.Posts.id == id).first()
     post_data = (
        db.query(models.Posts, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True)
        .filter(models.Posts.id == id)
        .group_by(models.Posts.id)
        .first()
     )
     # conn.commit()
     # post = find_post(id)
     if not post_data:
          # response.status_code = status.HTTP_404_NOT_FOUND
          # return {"Message": f"Post with id: {id} was not found"}
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")
     
     post, votes = post_data
     return {"post": post, "votes": votes}


@router.delete("/{id}")
def delete_post(id:int, db:Session = Depends(get_db), user :models.User = Depends(oauth2.get_current_user)):

     # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
     # deleted_posts = cursor.fetchone()
     # conn.commit()
     # index = find_index_post(id)

     post_query = db.query(models.Posts).filter(models.Posts.id == id)
     post = post_query.first()

     if post == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exits")
     
     if post.who_created_user != user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
     
     post_query.delete(synchronize_session=False)
     db.commit()
     # my_posts.pop(index)
     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model= schemas.Post)
def update_post(id:int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), user :models.User = Depends(oauth2.get_current_user)):
     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id),))
     # updated_posts = cursor.fetchone()
     # conn.commit()

     post_query = db.query(models.Posts).filter(models.Posts.id == id)
     post = post_query.first()
     # post = post_query.first()
     if post == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exits")
     # post_dict = post.model_dump()
     # post_dict['id'] = id
     # my_posts[index] = post_dict

     if post.who_created_user != user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
     
     post_query.update(updated_post.dict(),synchronize_session=False)
     db.commit()
     return post

