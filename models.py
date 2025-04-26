# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    """Stores client/patient information"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    enrollments = db.relationship(
        'Enrollment', 
        backref='client', 
        lazy=True,
        cascade='all, delete-orphan'
    )

class Program(db.Model):
    """Stores health programs (e.g., TB, Malaria)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    enrollments = db.relationship(
        'Enrollment', 
        backref='program', 
        lazy=True,
        cascade='all, delete-orphan'
    )

class Enrollment(db.Model):
    """Tracks which clients are in which programs"""
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    enrollment_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)