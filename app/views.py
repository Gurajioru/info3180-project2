"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file
import os
from .forms import LoginForm, RegistrationForm, PostForm
from wtforms.validators import DataRequired
from.models import User, Likes, Follows, Posts
from werkzeug.utils import secure_filename
import traceback
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, request, jsonify, send_file, send_from_directory
import jwt
from datetime import datetime, timedelta
from time import time

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated



def generate_token(username, password):
    timestamp = datetime.utcnow()
    payload = {
        "username": username,
        "password": password,
        "exp": timestamp + timedelta(minutes=180)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return token



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/register', methods=['POST'])
def register():
    form=RegistrationForm()

    if request.method=='POST' and form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        firstname=form.firstname.data
        lastname=form.lastname.data
        email=form.email.data
        location=form.location.data
        biography=form.biography.data
        photo=form.profile_pic.data

        file = photo 
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            user=User(username, password, firstname, lastname, email, location, biography,filename)
            db.session.add(user)
            db.session.commit()
        except:
            traceback.print_exc()
            error=form_errors(form)
            return jsonify(error=error)

        user=[{ "message": "User successfully registered", "firstname":firstname,"lastname":lastname,"username":username, "password":password, "email":email, "location":location, "biography":biography, "profile_photo":filename  }]
        return jsonify(user=user)

    else:
        error=form_errors(form)
        return jsonify(error=error)


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit:
        username=form.username.data
        password=form.password.data

        user = db.session.execute(db.select(User).filter_by(username=username)).scalar()

        if user is not None and check_password_hash(user.password, password):

                login_user(user)
                token = generate_token(username,password)
                response=[{"token": token, "message": "User successfully logged in"}]



                return jsonify(response=response)
        else:
            failure={"Error": "Could not validate user"}
            return jsonify(failure=failure)
            
    error=form_errors(form)
    return jsonify(error=error)

# Get all posts for all users
@app.route('/api/v1/posts', methods=['GET'])
def get_all_posts():
    posts = Posts.query.all()
    return jsonify([post.serialize() for post in posts])
# Get a user's posts
@app.route('/api/v1/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    posts = Posts.query.filter_by(user_id=user_id).all()
    return jsonify([post.serialize() for post in posts])

@app.route('/api/v1/users/<int:user_id>/follow', methods=['POST'])
def follow_user(user_id):
    target_user = User.query.filter_by(id=user_id).first()
    if not target_user:
        return jsonify({'error': 'User not found.'}), 404

    current_user_id = db.session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'You must be logged in to follow a user.'}), 401

    if current_user_id == user_id:
        return jsonify({'error': 'You cannot follow yourself.'}), 400

    follow_relationship = Follows.query.filter_by(user_id=user_id, follower_id=current_user_id).first()
    if follow_relationship:
        return jsonify({'error': 'Already following this user.'}), 400

    follow = Follows(user_id=user_id, follower_id=current_user_id)
    db.session.add(follow)
    db.session.commit()

    return jsonify(follow), 201


@app.route("/api/v1/images/<path:filename>")
def getImage(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)