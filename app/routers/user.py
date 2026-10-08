from fastapi import FastAPI, status, HTTPException, Depends ,APIRouter 
from .. import models, schemas, utils
from ..database import get_dp
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users" ,
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, dp: Session = Depends(get_dp)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    dp.add(new_user)
    dp.commit()
    dp.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, dp: Session = Depends(get_dp)):
    user = dp.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found"
        )

    return user
