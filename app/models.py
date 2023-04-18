# Add any model classes for Flask-SQLAlchemy here
from . import db
import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy import func



class User(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(255))
    firstname = db.column(db.String(80))
    lastname= db.column(db.String(80))
    email= db.column(db.String(100))
    location= db.column(db.String(150))
    biography= db.column(db.String(255))
    profile_photo=db.column(db.String(255))
    joined_on = db.Column(db.DateTime, server_default=func.now())

    def __init__(self, username, password, firstname, lastname, email, location, biography):
        now=datetime.datetime.now()
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email= email
        self.location= location
        self.biography = biography
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
    

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

class Posts(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    caption = db.Column(db.String(100))
    photo = db.Column(db.String(255))
    user_id = db.column(db.Integer)
    db.Column(db.DateTime, server_default=func.now())

    def __init__(self, caption, photo, user_id):
        self.caption = caption
        self.photo=photo
        self.user_id=user_id


class Likes(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id=db.column(db.Integer)
    user_id=db.column(db.Integer)

    def __init__(self, post_id, user_id):
        self.post_id=post_id
        self.user_id=user_id


class Follows(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id=db.column(db.Integer)
    user_id=db.column(db.Integer)

    def __init__(self, post_id, user_id):
        self.user_id=post_id
        self.follower_id=user_id