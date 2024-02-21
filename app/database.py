from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# SQLALCHEMY_DATABASE_URL = f"""postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}/{settings.db_name}"""

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.postgres_user}:"
    f"{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/"
    f"{settings.postgres_db}"
)

# postgres_user
# postgres_password
# postgres_host
# postgres_port
# postgres_db

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    """This functions creates a db sesssion each time we make a request, 
    then closes the db session after we are done"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
