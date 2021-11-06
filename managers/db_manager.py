import json
import sqlite3
import hashlib
import datetime

# Initialize the database connection
db_connection = sqlite3.connect('./database/btn_database.db')

"""

Primary Table Definitions:
     User: Table for managing accounts.
     Project: Table for managing the various stories.
     Comment: Table for managing the various comments.

Table User:
    user_id = Integer(primary_key=True)
    username = Varchar(unique=True)
    email = Varchar(unique=True)
    password = Varchar()

Table Story:
    story_id = Integer(primary_key=True)
    title = Varchar(unique=True)
    content =  Varchar()

Table Comment:
    comment_id = Integer(primary_key=True)
    content = Varchar()
    date_posted = Date(default=datetime.datetime.now)
    story_id = ForeignKey(Story, backref='comments') 
    user_id = ForeignKey(User, backref='comments')

"""

# Story Table Transactions
def get_story_by_id(story_id: int) -> dict:
    db_connection.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Story WHERE story_id = ?", (story_id,))
    story = cursor.fetchone()
    return dict(story)

def get_all_stories() -> str:
    db_connection.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Story")
    stories = cursor.fetchall()
    return [dict(ix) for ix in stories]

def add_story(title: str, content: str) -> None:
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO Story (title, content) VALUES (?, ?)", (title, content))
    db_connection.commit()

# User Table Transactions
def get_user_by_username(username: str) -> dict:
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
    user = cursor.fetchone()
    return user

def get_user_by_id(user_id: int) -> dict:
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM User WHERE user_id = ? ", (user_id,))
    user = cursor.fetchone()
    return user

def get_user_by_email(email: str) -> dict:
    db_connection.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM User WHERE email = ?", (email,))
    user = cursor.fetchone()
    return dict(user)

def add_user(username: str, email: str, password: str) -> None:
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO User (username, email, password) VALUES (?, ?, ?)", (username, email, hashlib.sha512(password).hexdigest()))
    db_connection.commit()

# Comment Table Transactions
def add_comment(content: str, user_id: int, story_id: int) -> None:
    cursor = db_connection.cursor()
    date_posted = datetime.datetime.now()
    cursor.execute("INSERT INTO Comment (content, user_id, story_id, date_posted) VALUES (?, ?, ?, ?)", (content, user_id, story_id, date_posted))
    db_connection.commit()

def get_comment_by_id(comment_id: str) -> dict:
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM Comment WHERE comment_id = ?", (comment_id,))
    comment = cursor.fetchone()
    return comment

def get_all_comments() -> str:
    db_connection.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Comment")
    comments = cursor.fetchall()
    return [dict(ix) for ix in comments]

