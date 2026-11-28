# from pydantic import BaseModel
# from datetime import datetime

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True


# class PostBase(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class PostCreate(PostBase):
#     pass


# class Post(BaseModel):
#     title:str
#     content:str
#     published:bool
#     class Config:
#         orm_mode=True
from pydantic import BaseModel, ConfigDict, EmailStr, Field
import datetime
from typing import Optional

from typing import Annotated
from pydantic import Field



class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    owner: UserResponse

    model_config = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    model_config = ConfigDict(from_attributes=True)



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    id: Optional[int] = None
    


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]
 

    