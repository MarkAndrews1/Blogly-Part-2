"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)



class USER(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.Text,
                           nullable=False)

    last_name = db.Column(db.Text,
                           nullable=False)
    
    img_url = db.Column(
                        db.Text,
                        nullable=False,
                        default='https://pbs.twimg.com/media/E-wB_MRXMAczerU.jpg'
                        )
    
    post = db.relationship('Post', backref='user', cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f'{self.first_name}  {self.last_name}'
    

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.Text,
                      nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(
                        db.DateTime,
                        nullable=False,
                        default=datetime.datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_time(self):
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")