# =============================================================================
# IMPORT STATEMENTS

from flask import Flask, redirect, request, url_for
from flask import Response

import requests
import secrets
import re

import flask
from flask import request
from flask import Flask, render_template

from jinja2 import Template

from flask import session

from werkzeug.utils import secure_filename

from logging.config import dictConfig

import os

app = Flask(__name__)

app.secret_key = secrets.token_hex()


# =============================================================================

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    },
     'file.handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'photoportal.log',
            'maxBytes': 10000000,
            'backupCount': 5,
            'level': 'DEBUG',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file.handler']
    }
})


# =============================================================================
# PHOTOS

PHOTO_FOLDER = "static/images/photos"

# In-memory photo storage.
photos = []


class Photo:
	def __init__(self, photo_name='', date_taken='', tags=''):
		self.name = photo_name
		self.date_taken = date_taken
		self.tags = tags

# Requirement 5
# 5.1 Define the method that will handle the search_form submission
# 5.3 Implement search of photos based the input criteria and the provided data
# 5.4 Create the matching photos list and set the appropriate status message when rendering
#     the photo-portal.html
# 5.5 Set empty photo list and appropriate status message when rendering the photo-portal.html
# Pass the username by extracting it from flask's session dictionary.

@app.route("/upload", methods=["POST"])
def upload_photo():
    app.logger.info("Inside upload_photo")

    username = ""
    if "username" in session:
        username = session['username']

    date_taken = request.form["date_taken"].strip()
    tags = request.form["tags"].strip()
    file = request.files['photo_name']
    filename = secure_filename(file.filename)
    filename = filename.strip()
    app.logger.info("File Name:%s\n", filename)

    if not os.path.exists(PHOTO_FOLDER):
        os.makedirs(PHOTO_FOLDER)

    file.save(PHOTO_FOLDER + "/" + filename)

    photo = Photo(photo_name=filename, date_taken=date_taken, tags=tags)
    photos.append(photo)

    app.logger.info("Date taken:" + date_taken)
    app.logger.info("Tags:" + tags)

    # Requirement 3
    # 3.1 - Set the status and pass that in to photo_upload_status parameter.

    return render_template("photo-portal.html", username=username, photo_list=photos)


# =============================================================================
# FUNCTION -- Logging Out

@app.route("/logout",methods=['POST'])
def logout():
    app.logger.info("Logout called.")
    app.logger.info("Before returning...")
    user = flask.session["username"]
    flask.session.pop('username', None)

    # ASSIGNMENT 2 (R2.1, R2.2) 
    pattern = r'[a-zA-Z0-9]+@gmail\.com' # Regular expression to match Gmail
    if re.match(pattern, user):
        return flask.redirect("/")
    else:
        return flask.redirect("/admin")


# =============================================================================
# FUNCTION -- Logging In 

# Admin Login 
@app.route("/adminlogin", methods=['POST'])
def adminlogin():
    username = ""
    password = ""
    gmail = ""
    user = ""
    upload_form_display = ""
    status = ""
    if 'username' in request.form:
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        user = username
        app.logger.info("Username:%s", username)
        app.logger.info("Password:%s", password)
        upload_form_display = "display:block;"
    app.logger.info("User photos:")
    app.logger.info(photos)
    app.logger.info("---")

    flask.session["username"] = user

    return render_template('photo-portal.html',
    						upload_form_display=upload_form_display,
    						username=user,
    						photo_upload_status=status,
    						photo_list=photos)


'''
ASSIGNMENT 2 (R1.2, R1.3, R1.4)
    1.2 Add method that handles the general user login form submission
    1.3 Set the status & upload_form_display status appropriately 
    1.4 Save the logged in user's name in flask session and pass that in the render_template for username parameter.
'''

# General Login
@app.route("/genlogin", methods=['POST'])
def genlogin():
    gmail = ""
    user = ""
    upload_form_display = ""
    status = "TODO: Implement slide-show functionality"
    if 'gmail' in request.form:
        gmail = request.form['gmail'].strip()
        user = gmail
        app.logger.info("Gmail:%s", gmail)
        upload_form_display = "display:none;"
        
    app.logger.info("User photos:")
    app.logger.info(photos)
    app.logger.info("---")

    flask.session["username"] = user

    return render_template('photo-portal.html',
    						upload_form_display=upload_form_display,
    						username=user,
    						photo_upload_status=status,
    						photo_list=photos)

# =============================================================================
# FUNCTION -- Rendering 

# Admin Landing Page
@app.route("/admin")
def adminindex():
    return render_template('adminindex.html')

# ASSIGNEMNT 1 (R1.1) -- General User Landing Page
@app.route("/")
def index():
    return render_template('index.html')
 
if __name__ == "__main__":

    app.debug = True
    app.logger.info('Portal started...')
    app.run(host='0.0.0.0', port=5009)
