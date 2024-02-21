# Pydantic models acts as Serializers
from pydantic import BaseModel, EmailStr, validator, field_validator
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #Default value is True
    # rating: Optional[int] = None


class PostCreate(PostBase): #Pydantic models acts as data serializers #In
    """Will serve for both create and update, we dont want the user to pass the owner id, by them self,
    It will be automatic"""
    pass  #Already inherited all from PostBase


class UserCreate(BaseModel):
    email : EmailStr #for email validator
    password : str


class UserOut(BaseModel):
    """Serializing output data, removed the password field"""
    id: int
    email : EmailStr 
    created_at: datetime

class PostResponse(PostBase): #Returning to the frontend #Out
    """For Sending data back"""
    id: int  #I removed id and created_at #before
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        # orm_mode = True #* 'orm_mode' has been renamed to 'from_attributes'
        from_attributes = True

class PostResponseNoOwnerDetails(PostBase): #Returning to the frontend #Out
    """For Sending data back, didnt later use this"""
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        # orm_mode = True #* 'orm_mode' has been renamed to 'from_attributes'
        from_attributes = True

class PostWithVoteCount(BaseModel):
    """This is for the Post with count, complex sql query output result, different"""
    post: PostResponse
    votes_count: int


class UserLogin(BaseModel):
    email : EmailStr #for email validator
    password : str

class Token(BaseModel):
    """This is the structure of the data we expect out of the login verification process"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Output token verification"""
    # user_id: Optional[str] = None
    id: Optional[str] = None
    # exp: datetime

class Vote(BaseModel):
    post_id: int
    vote_dir: int    # conint(le=1) # 0,1  #or Annotated[int, range(0, 2)]

    @field_validator('vote_dir')
    def check_vote_dir(cls, v):
        if v not in (0, 1):
            raise ValueError('vote_dir must be 0 or 1')
        return v
    

# class PostBase(BaseModel): #Dont inherit from the PostBase model, since it is only published field we want to update
#     published: bool
