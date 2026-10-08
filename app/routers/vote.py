from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_dp
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    dp: Session = Depends(get_dp),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = dp.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} not found"
        )

    vote_query = dp.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        dp.add(new_vote)
        dp.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        dp.commit()

        return {"message": "successfully deleted vote"}
