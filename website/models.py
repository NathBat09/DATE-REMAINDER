# Import necessary modules and classes
from . import db  # Assuming you've defined the db instance in __init__.py
from flask_login import UserMixin
from sqlalchemy.sql import func

# Define the Note model
class Note(db.Model):
    # Define the columns of the Note table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    data = db.Column(db.String(10000))  # Column for note data
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # Column for creation date/time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to User table

# Define the User model with UserMixin for user authentication
class User(db.Model, UserMixin):
    # Define the columns of the User table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    email = db.Column(db.String(150), unique=True)  # Column for user email
    password = db.Column(db.String(150))  # Column for user password
    first_name = db.Column(db.String(150))  # Column for user's first name
    
    # Establish a relationship between User and Note (one-to-many)
    notes = db.relationship('Note')