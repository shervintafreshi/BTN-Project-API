import sqlite3
import hashlib
import datetime
from peewee import *

# Initialize the database connection
db = SqliteDatabase('./database/btn_database.db')

# Define Meta Table 
class BaseModel(Model):
    class Meta:
        database = db      

"""
Primary Table Definitions:
     User: Table for managing accounts.
     Project: Table for managing the various stories.
     Comment: Table for managing the various comments.
"""

class User(BaseModel):
    user_id = AutoField(primary_key=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

class Story(BaseModel):
    story_id = AutoField(primary_key=True)
    title = CharField(unique=True)
    content =  TextField()

class Comment(BaseModel):
    comment_id = AutoField(primary_key=True)
    content = TextField()
    date_posted = DateTimeField(default=datetime.datetime.now)
    story_id = ForeignKeyField(Story, backref='comments') 
    user_id = ForeignKeyField(User, backref='comments')


# Initalize connection to database
db.connect()
# Create the required tables
db.create_tables([User, Story, Comment]) 


# Story Table Transactions
def add_story(title: str, content: str) -> Story:
    return Story.create(title=title, content=content)

def get_story_by_id(story_id: int) -> Story:
    return Story.get(Story.story_id == story_id)

def get_all_stories() -> list[Story]:
    return Story.select()

# User Table Transactions
def get_user_by_username(username: str) -> User:
    return User.get(User.username == username)

def get_user_by_id(user_id: int) -> User:
    return User.get(User.user_id == user_id)

def add_user(username: str, email: str, password: str) -> User:
    return User.create(username=username, email=email, password=hashlib.sha512(password).hexdigest())

# Comment Table Transactions
def add_comment(content: str, user_id: int, story_id: int) -> Comment:
    return Comment.create(content=content, user_id=user_id, story_id=story_id)

def get_comment_by(comment_id: str) -> Comment:
    return Comment.create(Comment.comment_id == comment_id)