import json,jwt
from typing import Optional
from fastapi import FastAPI
from managers.db_manager import *

# Generate fast API object
app = FastAPI()

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
    return {}

@app.get("/stories/all")
async def get_stories():
    return {}

@app.post("/stories/add_comment")
async def add_story_comment():
    return {}

@app.post("/user/login")
async def user_login():
    return {}

@app.post("/account/authenticate")
async def user_authentication():
    return {}

@app.post("/account/logout")
async def user_logout():
    return {}

# Temporary route to call populate database
@app.post("/database/populate")
async def populate_database():
    return {}