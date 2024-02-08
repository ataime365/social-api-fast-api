from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import models, schemas, utils, oauth2  #going two steps up
# from app.database import get_db #Also works
from ..database import get_db #going two steps up

import bcrypt

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token) #output data serializing
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
                 db: Session = Depends(get_db)): #user_credentials: schemas.UserLogin
    """Because we are using OAuth2PasswordRequestForm, user_credentials will only contain {"username": "us", "password": "p"} , No email
      but username string is email here """
    user_exists = db.query(models.User).filter(models.User.email==user_credentials.username).first() #user_credentials.email
    if not user_exists: #Email check
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials") #Makes it harder for hackers to guess
    
    user_s = utils.verify(user_credentials.password, user_exists.password)
    if not user_s: #password check
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials") 
    
    # if user has both Email and password
    # create a token and return the created token
    access_token = oauth2.create_access_token(data={"user_id": user_exists.id})

    return {"access_token": access_token, "token_type": "bearer"}

    

