from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Union

from .. import models, schemas, utils  #going two steps up
# from app.database import get_db #Also works
from ..database import get_db #going two steps up

router = APIRouter(prefix="/users", tags=["Users"])

## User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Union[schemas.UserOut, dict]) #output data serializing
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(models.User).filter(models.User.email==user.email).first()
    if user_exists: #If user exist in the database
        return {'message': f"User with Email: {user_exists.email} already exist"}

    # hash the password - user.password
    hashed_password = utils.hash_p(user.password)
    user.password = hashed_password #updating the user.password

    new_user = models.User(**user.model_dump()) # **user.dict() #key-word unpacking
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}" , response_model=schemas.UserOut) #output data serializing
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user