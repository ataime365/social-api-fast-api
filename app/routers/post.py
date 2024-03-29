from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from .. import models, schemas, oauth2
# from app.database import get_db #Also works
from ..database import get_db #going two steps up


router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[schemas.PostWithVoteCount]) #output data serializing
# @router.get("/", response_model=List[schemas.PostResponse]) #output data serializing
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
                    limit: int= 10, skip: int = 0, search: Optional[str] = ""): #limit and skip are a query parameters
    # print(search)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)). \
    #             order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()

    posts_votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")) \
                        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
                        .group_by(models.Post.id) \
                        .filter(models.Post.title.contains(search)) \
                        .order_by(models.Post.created_at.desc()).offset(skip).limit(limit) \
                            .all() #outerjoin is Left outer join by default
    # print(posts_votes)
    result = []
    for post_obj, votes_count in posts_votes:
        # Filter out SQLAlchemy-specific keys and append a new dictionary with post data and count
        filtered_post_owner = {key: value for key, value in post_obj.owner.__dict__.items() if not key.startswith('_')}
        schemas.PostResponse.owner = filtered_post_owner # I Had to add the owner by myself
        # main
        filtered_post_data = {key: value for key, value in post_obj.__dict__.items() if not key.startswith('_')} #_sa_instance_state
        result.append({'post': filtered_post_data, 'votes_count': votes_count})
    return result 


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) #output data serializing
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                      current_user: int = Depends(oauth2.get_current_user)): #Adding an extra dependency for the jwt authentication
    # print(current_user.email)
    # print(current_user.id)
    new_post = models.Post(**post.model_dump()) #title=post.title, content=post.content, published=post.published # **post.dict()
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}" , response_model=schemas.PostWithVoteCount) #output data serializing
async def get_post(id: int, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)): #int is wrong, but it doesnt affect the outcome
    
    post =  db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")) \
                        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
                        .group_by(models.Post.id) \
                            .filter(models.Post.id==id).first()
        
    # post = db.query(models.Post).filter_by(id=id).first() #This also works, but it is less flexible
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    # dictionary comprehension
    filtered_post_owner = {key: value for key, value in post[0].owner.__dict__.items() if not key.startswith('_')}
    schemas.PostResponse.owner = filtered_post_owner # I Had to add the owner by myself
    #main
    filtered_post_data = {key: value for key, value in post[0].__dict__.items() if not key.startswith('_')} #_sa_instance_state
    
    s_post = {'post': filtered_post_data, 'votes_count': post[1] }
    return s_post # FastApi automatically serializes the data to json format


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), 
                      current_user: int = Depends(oauth2.get_current_user)): #Authenticated user id
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # To be sure I can only delete a post that I 'own' and not another persons post
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized: You can't delete a post that is not yours")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  #{"msg": "Post was deleted successfully"}


@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail=f"post with id: {id} was not found")
    # To be sure I can only update a post that I 'own' and not another persons post
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized: You can't update a post that is not yours")
    post_query.update(updated_post.model_dump(), synchronize_session=False) #As a dict, no need for unpacking here
    db.commit()
    db.refresh(post)
    return post