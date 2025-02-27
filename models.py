from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    qualification = db.Column(db.String(120))
    dob = db.Column(db.Date)
    role = db.Column(db.String(10), default="user")  # 'admin' or 'user'

class Subject(db.Model):
    __tablename__ = 'subjects'
    subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)

class Chapter(db.Model):
    __tablename__ = 'chapters'
    chapter_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'))
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    subject = db.relationship("Subject", backref="chapters")

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    quiz_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.chapter_id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)  # minutes
    chapter = db.relationship("Chapter", backref="quizzes")

class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'))
    question_text = db.Column(db.Text, nullable=False)
    option_1 = db.Column(db.Text)
    option_2 = db.Column(db.Text)
    option_3 = db.Column(db.Text)
    option_4 = db.Column(db.Text)
    correct_option = db.Column(db.Integer)  # 1, 2, 3, or 4
    quiz = db.relationship("Quiz", backref="questions")

class Score(db.Model):
    __tablename__ = 'scores'
    score_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'))
    total_questions = db.Column(db.Integer)
    correct_answers = db.Column(db.Integer)
    score = db.Column(db.Integer)
    attempt_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref="user_scores")
    quiz = db.relationship("Quiz", backref="quiz_scores")