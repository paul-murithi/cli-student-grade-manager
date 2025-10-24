from enum import unique

from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref

from webapp.models import db

VALID_ROLES = ("student", "professor")

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)

    courses = db.relationship('Course', back_populates='professor', cascade='all, delete')
    enrollments = db.relationship('Enrollment', backref='user', lazy=True)

    def set_role(self, role):
        if role not in VALID_ROLES:
            raise ValueError(f"Invalid role {role}")
        self.role = role

class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), nullable=False, unique=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=True)  # TODO: make required later
    semester = db.Column(db.Integer, nullable=False)

    professor = db.relationship('User', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course', cascade='all, delete')
