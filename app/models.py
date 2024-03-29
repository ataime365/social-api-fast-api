from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts" #Name used to create the table for us, if the table doesnt exists

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()') , nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) #nullable=False also makes sure there is 'no' NULL on the users side, after a LEFT JOIN
    owner = relationship("User") #This automatically grabs all user info for us


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()') , nullable=False)
    phone_number = Column(String)


class Vote(Base):
    """This is the intermediate table that resolves 
    the 1 'many-to-many' relationship into two(2) 'one-to-many' relationships ,
    using 2 foreign keys from each table"""
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)



# reverse relationships(backref or back_populates) is for when we want to query the 2 tables from both directions,
# For now we are only querying the models from the Post table, so no need for reverse relationships yet