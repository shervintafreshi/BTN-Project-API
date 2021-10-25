import sqlite3
import datetime
from peewee import *

# Initialize the database connection
db = SqliteDatabase('btn_database.db')

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
    username = charField(unique=True)
    email = charField(unique=True)
    password = charField()

class Story(BaseModel):
    story_id = AutoField(primary_key=True)
    title = charField(unique=True)
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

# Primary database transactions methods:

# Story Table Transactions
def add_story(title: str, content: str):
    return Story.create(title=title, content=content)

def get_all_stories():
    return Story.select()

# User Table Transactions
def get_user_by_username(username: str):
    return User.get(User.username == username)

def get_user_by_id(user_id: int):
    return User.get(User.user_id == user_id)

def add_user(username: str, email: str, password: str):
    return User.create(username=username, email=email, password=password)

# Comment Table Transactions
def add_comment(content: str, user_id: int):
    return Comment.create(content=content, user_id=user_id)

def get_comment_by(comment_id: str):
    return Comment.create(Comment.comment_id == comment_id)