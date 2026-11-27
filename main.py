# from urllib import response

# from fastapi import Depends, FastAPI, HTTPException, Response,status
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange
# import psycopg
# from psycopg.rows import dict_row
# import time
# import models
# from sqlalchemy.orm import Session
# from database import engine, SessionLocal

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()



# class Post(BaseModel):
#     title:str
#     content:str
#     published:bool = True
    
# try:
#     conn = psycopg.connect(host='localhost', dbname='my_database', user='postgres', password='db@123', row_factory=dict_row)
#     cursor = conn.cursor()
#     print("Database connection was successful")
# except Exception as error:
#     print("Connecting to database failed")
#     print("Error:", error)

# my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favorite foods","content":"i like pizza","id":2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


# @app.get("/")
# def root():
#     return {"welcome to my api,hello hii"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data":posts}


# @app.get("/posts")
# def get_posts():
#     cursor.execute("SELECT * FROM posts")
#     my_posts = cursor.fetchall()
#     conn.commit()
#     return{"data":my_posts}


# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post):
#     cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return{"data":new_post}


# @app.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
#     post = cursor.fetchone()
#     conn.commit()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#     return{"post_detail":post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if not deleted_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


         
  


# @app.put("/posts/{id}")
# def update_post(id:int,post:Post):
#     cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#     return{"data":updated_post}


from typing import List, Optional
# from pydantic import Basesettings
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from sqlalchemy.orm import Session
from sqlalchemy import func
import oauth2
import oauth2 as oauth2
import models,schemas,utils,auth,vote,user
from database import SessionLocal, engine,get_db
from fastapi.middleware.cors import CORSMiddleware
# class Settings(BaseSettings):
#     database_hostname: str
#     database_port: str
#     database_password: str
#     database_name: str
#     database_username: str
#     secret_key: str
#     algorithm: str
#     access_token_expire_minutes: int

#     model_config = SettingsConfigDict(env_file=".env")


# settings = Settings()



# print(settings.database_hostname)



# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(vote.router)




class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # owner_id: int
    # owner: schemas.UserResponse


class User(BaseModel):
    email: str
    password: str


def get_post_or_404(db: Session, id: int):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post


@app.get("/")
def root():
    return {"message": "welcome to my api, hello hii"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .all()
    )
    return results


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return result


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    post = get_post_or_404(db, id)
    


    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post:Post, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    existing = get_post_or_404(db, id)
    if existing.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    existing.title = post.title
    existing.content = post.content
    existing.published = post.published
    db.commit()
    db.refresh(existing)
    return {"data": existing}


@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
   
   
   #hash the password - user.password
   
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )
    return user

