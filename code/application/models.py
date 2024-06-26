from application import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)


class UserModel(db.Model, UserMixin):

    __tablename__ = 'users'

    # can't change to user_id, it will crash the UserMixin
    id = db.Column(db.Integer, primary_key=True)
    given_name = db.Column(db.String(64))
    family_name = db.Column(db.String(64), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    identifier_system = db.Column(db.String(), nullable=True)
    identifier_value = db.Column(db.String(64), nullable=True)
    oauth_server = db.Column(db.String(64), default='smart',nullable=True)
    patient_id = db.Column(db.Integer,unique=True,nullable=True, index=True, name='idx_patient_id')
    email = db.Column(db.String(64), unique=True, nullable=True, index=True, name='idx_user_email')
    password_hash = db.Column(db.String(256), nullable=True)

    def __init__(self, given_name, family_name, date_of_birth, identifier_system, identifier_value, oauth_server, patient_id, email, password):
        self.given_name = given_name
        self.family_name = family_name
        self.date_of_birth = date_of_birth
        self.identifier_system = identifier_system
        self.identifier_value = identifier_value
        self.oauth_server = oauth_server
        self.patient_id = patient_id
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Email: {self.email}, given_name: {self.given_name}"

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    length = db.Column(db.Integer, nullable=False)
    hashtags = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, default=5, nullable=False)

class AudioRecord(db.Model):
    __tablename__ = 'audio_records'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_audio_record_user_id'), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id', name='fk_audio_record_news_id'), nullable=False)
    record_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    file_dir = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Float, nullable=True)
    score = db.Column(db.Integer)
    patient = db.relationship('UserModel', backref=db.backref('audio_records', lazy='dynamic'))
    news = db.relationship('News', backref=db.backref('audio_records', lazy='dynamic'))
