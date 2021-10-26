import hashlib, uuid
import json, jwt
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, Response, Cookie
from managers.db_manager import *

# Generate fast API object
app = FastAPI()

# Post Request Models
class Comment(BaseModel):
    content: str
    user_id: int
    story_id: int

class Credientials(BaseModel):
    username: str
    password: str

# Primary API Routes
@app.get("/")
async def read_root():
    return {"Name": "BTN Term Project API"
            "Version": "1.0", 
            "Author": "Shervin Tafreshipour",
            "Description": """backend API constructed to handle the various requests
                              types emitted from the frontend React Application
                           """
            }

@app.get("/stories/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return get_story_by_id(item_id) 

@app.get("/stories/all")
async def get_stories():
    return get_all_stories()

@app.post("/stories/add_comment")
async def add_story_comment(comment: Comment):
    return add_story_comment(comment['content'], comment['user_id'], comment['story_id'])
    
@app.post("/user/login")
async def user_login(response: Response, credentials: Credentials):
    response_content = None
    user = get_user_by_username(credentials.username)
    if user and user.password == hashlib.sha512(credentials['password']).hexdigest():
        response_content = {"authenticated": True}
        jwt_token = jwt.encode({"exp": datetime.now(tz=timezone.utc)} + datetime.timedelta(minutes=10), "SECRET_KEY", algorithm='HS256')
        response.set_cookie(key='token', value=jwt_token)
    else:
        response_content = {"authenticated": False}
    return response_content

@app.post("/account/authenticate")
async def user_authentication(token: Optional[str] = Cookie(None)):
    response_content = None
    try:
        jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        response.set_cookie(key='token', value=token)
        response_content = {"authenticated": True}
    except jwt.ExpiredSignatureError:
        # Signature has expired
        response_content = {"authenticated": False}
    return response_content

@app.get("/account/logout")
async def user_logout(token: Optional[str] = Cookie(None)):
    jwt_token = jwt.encode({"exp": datetime.now(tz=timezone.utc)}, "SECRET_KEY", algorithm='HS256')
    response.set_cookie(key='token', value=jwt_token)
    return {"authenticated": False}

# Temporary route to call populate database
@app.post("/database/populate")
async def populate_database():
    return {}
