from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

from init_db import db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

base = declarative_base()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Position(base, db.Model):
    __tablename__ = 'position'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    details = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"Position('{self.name}')"


class Department(base, db.Model):
    __tablename__ = 'department'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    manager = db.relationship('Employee', foreign_keys=[manager_id], backref=backref('managing_department'), lazy=True)

    def __repr__(self):
        return f"Department('{self.name}')"


class State(base, db.Model):

    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"State('{self.name}')"


class Employee(base, db.Model):
    __tablename__ = 'employee'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    position = db.relationship('Position', backref=backref('employees'), lazy=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    department = db.relationship('Department', foreign_keys=[department_id], backref=backref('employees'), lazy=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    state = db.relationship('State', backref=backref('employees'), lazy=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Employee('{self.name}', '{self.position.name}', '{self.department.name}')"
