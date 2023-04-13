from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
#ids unicos
from uuid import uuid4 as uuid



app=FastAPI()



posts=[]

#post model
class Post(BaseModel):
    id:Optional[str]
    title:str
    author:str
    content:Text
    created_at:datetime=datetime.now()
    published_at:Optional[datetime]
    published:bool=False


@app.get('/')
def read_root():
    return{"welcome":"welcome to my REST API"}

@app.get('/posts')
def get_posts():
    return posts

#aqui un parametro
@app.post('/posts')
def save_post(post:Post):
    post.id=str(uuid())
    posts.append(post.dict())
    return posts[-1]

@app.get('/posts/{post_id}')
def get_post(post_id:str):
    for post in posts:
        #si el id de cada publicacion es igual al parametro que me están pasando 
        #retorna el post
        if post["id"]==post_id:
            return post
    #exception
    raise HTTPException(status_code=404,detail="Post not found")

@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    #enumerate nos da la publicación y el índice
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post has been deleted succesfully"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.put('/posts/{post_id}')
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if posts["id"] == post_id:
            posts[index]["title"]= updatedPost.dict()["title"]
            posts[index]["author"]= updatedPost.dict()["author"]
            posts[index]["content"]= updatedPost.dict()["content"]
            return {"message": "Post has been updated succesfully"}
    raise HTTPException(status_code=404, detail="Item not found")
    