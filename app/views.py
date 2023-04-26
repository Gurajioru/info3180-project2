"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, g
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
from functools import wraps
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



def generate_token(username, password, id):
    timestamp = datetime.utcnow()
    payload = {
        "user_id":id,
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
    if request.method=='POST' and form.validate_on_submit():
        username=form.username.data
        password=form.password.data

        user = db.session.execute(db.select(User).filter_by(username=username)).scalar()

        if user is not None and check_password_hash(user.password, password):

                login_user(user)
                token = generate_token(username,password, user.id)
                response=[{"token": token, "message": "User successfully logged in"}]



                return jsonify(response=response), 200
        else:
            failure={"Error": "Could not validate user"}
            return jsonify(failure=failure)
            
    error=form_errors(form)
    return jsonify(error=error)

    

@app.route("/api/v1/images/<filename>")
def getImage(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)



@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
@requires_auth
def add_post(user_id):
    form = PostForm()
    if request.method=='POST' and form.validate_on_submit():
        photo=form.picture.data
        caption = form.caption.data

        file = photo 
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            post=Posts(caption,filename, user_id)
            db.session.add(post)
            db.session.commit()
        except:
            traceback.print_exc()
            error={"message":"Failed to add to database"}
            return jsonify(error=error)

        user={"message": "Successfully created a new post"}
        return jsonify(user=user)

    else:
        error=form_errors(form)
        return jsonify(error=error)




