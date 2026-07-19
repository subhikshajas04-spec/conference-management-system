from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='draft')

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200), nullable=False)
    abstract = db.Column(db.Text)
    keywords = db.Column(db.String(300))
    file_path = db.Column(db.String(300))
    camera_ready_path = db.Column(db.String(300), nullable=True)
    status = db.Column(db.String(50), default='submitted')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviews = db.relationship('Review', backref='paper', lazy=True)
    schedule = db.relationship('PresentationSchedule', backref='paper', uselist=False)

class PaperAssignment(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'))
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'))
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)
    comments = db.Column(db.Text)
    recommendation = db.Column(db.String(20))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='registrations', lazy=True)

class PresentationSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'), nullable=False)
    session_title = db.Column(db.String(200))
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)