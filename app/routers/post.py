from fastapi import FastAPI,Response ,status, HTTPException, Depends ,APIRouter 
from .. import models, schemas ,oauth2
from ..database import get_dp
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts" ,
    tags=["Posts"]
)



@router.get("/" , response_model=list[schemas.PostOut])
def get_posts(dp : Session = Depends(get_dp) , current_user : int = Depends(oauth2.get_current_user) , limit : int = 10 , skip :int = 0 ,search : str|None = ""):
    # posts = dp.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = dp.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote ,models.Post.id == models.Vote.post_id , isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return [
    {"post": post, "votes": votes}
    for post, votes in results
]


@router.post("/", status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def create_posts(post: schemas.CreatePost , dp : Session = Depends(get_dp) , current_user : int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    dp.add(new_post)
    dp.commit()
    dp.refresh(new_post)
    return new_post
   
    # cursor.execute("""INSERT INTO posts (title , content , published) VALUES (%s ,%s ,%s) RETURNING *""",(post.title , post.content ,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"Data" :  new_post}
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    # return {"data": post_dict}


@router.get("/{id}" ,response_model=schemas.PostOut)
def get_post(id: int, response: Response , dp :Session = Depends(get_dp) , current_user : int = Depends(oauth2.get_current_user)):
    # post = dp.query(models.Post).filter(models.Post.id == id).first()

    post = dp.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote ,models.Post.id == models.Vote.post_id , isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} was not found ",
            )
    post, votes = post

    return {
    "post": post,
    "votes": votes
}

        
    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int , dp :Session = Depends(get_dp) , current_user : int = Depends(oauth2.get_current_user)):
    deleted_post = dp.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("""DELETE FROM POSTS WHERE id = %s RETURNING * """,(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    if not deleted_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} is not found"
        )
    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    deleted_post.delete(synchronize_session = False)
    dp.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_posts(id: int, post: schemas.CreatePost ,dp : Session = Depends(get_dp) , current_user : int = Depends(oauth2.get_current_user)):
    updated_post_query = dp.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("""UPDATE posts SET (title , content ,published) =(%s,%s,%s) WHERE ID = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    if not updated_post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    if updated_post_query.first().owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    updated_post_query.update(post.model_dump() , synchronize_session = False)
    dp.commit()
    return updated_post_query.first()
