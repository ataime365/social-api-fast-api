from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Union

from .. import models, schemas, utils, oauth2  #going two steps up
from ..database import get_db #going two steps up

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED) #output data serializing
async def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #if post does not exists
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} was not found")
    # main
    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, 
                                              models.Vote.user_id == current_user.id) # (post_id, user_id) i.e (15, 2)
    found_vote = vote_query.first()
    if vote.vote_dir == 1: #Add vote/create a vote
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        # else Create vote, since it doesnt exist yet
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "successfully added vote"}
    else: #delete vote 
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}


        
