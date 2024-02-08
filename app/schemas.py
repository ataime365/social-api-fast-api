# Pydantic models acts as Serializers
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

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

# class PostBase(BaseModel): #Dont inherit from the PostBase model, since it is only published field we want to update
#     published: bool
