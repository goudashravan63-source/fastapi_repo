from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response, status,APIRouter
import fastapi
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import database,models,schemas,utils,oauth2
router=APIRouter(
tags=["Authentication"])
@router.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  
  #username
  #password
  
   user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
   if not user:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
   if not utils.verify_password(user_credentials.password, user.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")


   access_token = oauth2.create_access_token(data={"user_id": user.id})


#    create a token and return it

   return {"access_token": access_token, "token_type": "bearer"}