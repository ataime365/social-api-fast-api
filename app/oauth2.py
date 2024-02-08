
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, database, models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # /login


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes #change it to 60 minutes later


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #expiry date in 30 mins from now
    to_encode.update({"exp": expire}) #Adding the expiry time to the payload

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #jwt.encode
    return encoded_jwt



def verify_access_token(token: str, credentials_exception):
    """This is where the user id is extracted/generated"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # The id cones in as int, we need to convert it to string
        id: str = str(payload.get("user_id")) # Extracting the id from the decoded token

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id) #using pydating to validate the data type gotten
        # Pydantic generates a constructor (__init__) for your class, 
        # which accepts keyword arguments corresponding to the fields you've defined in your class. 
        # This means you don't have to write your own __init__ 
        return token_data #Token is only the user id, for now
    except JWTError:
        raise credentials_exception
    
    # return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """This is sometimes used to get the user from the database, using the user id""" 
    #The token for the current user depends on the OAuth2PasswordBearer("login_url") from security
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
        )
    token = verify_access_token(token, credentials_exception) # #id='19' #returns the user id in a class format, or dict format
    # print(token, "tokentokentokentokentokentokentokentokentoken") #id='19'
    # Using the current user id, to get the full user details
    current_user = db.query(models.User).filter(models.User.id==token.id).first()
    return current_user #Not just the id

