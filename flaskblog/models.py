from datetime import datetime
from hashlib import md5

from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship('Tag', secondary='post_tags', backref='post')

    def append_tags(self, tags):
        for tag_name in tags:
            tag_to_add = Tag.query.filter(Tag.name == tag_name).one_or_none()
            if tag_to_add is None:
                new_tag = Tag(name=tag_name)
                self.tags.append(new_tag)
            else:
                self.tags.append(tag_to_add)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    site_url = db.Column(db.String(50), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def author_avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    posts = db.relationship('Post', secondary='post_tags', backref='tag')


post_tags = db.Table('post_tags',
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                     )
