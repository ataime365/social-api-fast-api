from passlib.context import CryptContext


#Here we are just defining the library we wuld be using for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

def hash_p(password: str):
    """Our logic for hashing password"""
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    """This function would help us hash the plain password that is to be verified
    and then compare it with the hashed pasword from the database
    pwd_context.verify(a, b) does both the hashing and comparison for us"""
    return pwd_context.verify(plain_password, hashed_password)
