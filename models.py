"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import *

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    profile_pic = db.Column(db.String, 
                            nullable=True, 
                            default='https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png?w=640')
    
    posts = db.relationship('Post', backref='users', cascade='all, delete-orphan')

    def __repr__(self):
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name}>"


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String, nullable=False)

    content = db.Column(db.String, nullable=False)

    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        p = self
        return f"<Post {p.id} {p.title} {p.content} {p.posted_by} {p.posted_at}>"



class PostTags(db.Model):

    __tablename__ = 'posttags'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        pt = self
        return f"<Post {pt.id} {pt.post_id} {pt.tag_id}>"



class Tags(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='posttags', backref='tags', cascade='all, delete')

    def __repr__(self):
        t = self
        return f"<Tag {t.id} {t.name}>"
