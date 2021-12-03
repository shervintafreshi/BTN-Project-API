import hashlib
import uuid
import os
import json
import jwt
from typing import List
from dotenv import load_dotenv
from managers.db_manager import *
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, Request, Depends, Response, Cookie
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

# Generate fast API object
app = FastAPI()

# Configure CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure CRSF protection
class CsrfSettings(BaseModel):
  secret_key: str = 'C1FEEF6FBA3CD5143BC080250CA9AD4591A227BE49E5E68B92F1E778F796CBFA'

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

# Load in environment variables
load_dotenv()

# Post Request Models
class Comment(BaseModel):
    content: str
    user_id: int
    story_id: int


class Credentials(BaseModel):
    email: str
    password: str

# Get Response Models
class Story(BaseModel):
    id: int
    title: str
    content: str
    comment: Comment


# Primary API Routes
@app.get("/")
async def read_root():
    return JSONResponse({"Name": "BTN Term Project API",
                         "Version": "1.5",
                         "Author": "Shervin Tafreshipour",
                         "Description": "backend API constructed to handle various requests"
                         })

# Request a single story object
@app.get("/stories/{item_id}", response_model=Story)
async def read_item(request: Request, item_id: int, q: Optional[str] = None, csrf_protect: CsrfProtect = Depends()):
    # CRSF protection
    csrf_protect.validate_csrf_in_cookies(request)
    # Get the story object
    story = get_story_by_id(item_id)
    # call for comments
    comments = get_all_comments()
    if len(comments) > 0:
        story["comments"] = []
        for comment in comments:
            if comment["story_id"] == story["story_id"]:
                # append comments to stories
                story["comments"].append(comment)
    return JSONResponse(content=jsonable_encoder(story))

# Request all user stories
@app.get("/stories", response_model=List[Story])
async def get_stories(request: Request, csrf_protect: CsrfProtect = Depends()):
    # CRSF protection
    csrf_protect.validate_csrf_in_cookies(request)
    # Get all stories
    stories = get_all_stories()
    # call for comments
    comments = get_all_comments()
    if len(comments) > 0:
        for story in stories:
            story["comments"] = []
            for comment in comments:
                if comment["story_id"] == story["story_id"]:
                    # append comments to stories
                    story["comments"].append(comment)
    return JSONResponse(content=jsonable_encoder(stories))

# Request to add comment to story
@app.post("/stories/add_comment")
async def add_story_comment(request: Request, comment: Comment, csrf_protect: CsrfProtect = Depends()):
    # CRSF protection
    csrf_protect.validate_csrf_in_cookies(request)
    # Add comment to story
    add_comment(comment.content, comment.user_id, comment.story_id)
    return JSONResponse({"Success": True})

"""
    Authentication:
    Return user object with JWT token
    store JWT token in cookie
    store user object in local storage
"""

# Request to add user login
@app.post("/account/login")
async def user_login(response: Response, credentials: Credentials):
    response_content = None
    user = get_user_by_email(credentials.email)
    if user['password'] == hashlib.sha512(credentials.password.encode()).hexdigest():
        response_content = {"authenticated": True,
                            "account_id": user["user_id"],
                            "account_name": user["username"],
                            "account_email": user["email"]} 

        jwt_token = jwt.encode({"exp": datetime.datetime.now(tz=datetime.timezone.utc) +
                               datetime.timedelta(minutes=10)}, os.environ["SECRET_KEY"], algorithm='HS256')
        response.set_cookie(key='token',
                            value=jwt_token,
                            httponly=True,
                            max_age=60 * 60 * 24,
                            secure=True,
                            samesite='None',
                            )
        #csrf_protect.set_csrf_cookie(response)                    
    else:
        response_content = {"authenticated": False }
    return response_content

# Request to authenticate JWT token
@app.get("/account/authenticate")
async def user_authentication(request: Request, response: Response, token: Optional[str] = Cookie(None), csrf_protect: CsrfProtect = Depends()):
    # CRSF protection
    csrf_protect.validate_csrf_in_cookies(request)
    response_content = None
    try:
        jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])
        response.set_cookie(key='token', value=token)
        response_content = {"authenticated": True}
    except jwt.exceptions.InvalidSignatureError:
        # invalid token passed in
        response_content = {"authenticated": False}
    except jwt.ExpiredSignatureError:
        # Signature has expired
        response_content = {"authenticated": False}
    except jwt.InvalidTokenError:
        # Invalid token
        response_content = {"authenticated": False}
    except jwt.exceptions.DecodeError:
        # Invalid token
        response_content = {"authenticated": False}
    return response_content

# Request to logout user
@app.get("/account/logout")
async def user_logout(request: Request, response: Response, token: Optional[str] = Cookie(None)):
    response.delete_cookie(key="token")
    return {"authenticated": False}

# Exception Handler for CSRF errors
@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
  return JSONResponse(status_code=exc.status_code, content={ 'detail':  exc.message })
