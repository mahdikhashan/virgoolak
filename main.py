from flask_login import login_user, login_required, logout_user
from flask_login import UserMixin
from flask_login import LoginManager

login_manager = LoginManager()

import io

from flask import Flask
from flask import request
from flask import render_template, send_file

from flask import abort
from jinja2 import TemplateNotFound

from flask import redirect
from flask import url_for

from werkzeug.security import (generate_password_hash,
                                check_password_hash)

from virgool import Virgool
from virgoolak import Type1

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

sentry_sdk.init(
    dsn="https://e17333e06f6747e9b3d0eb6aed5b6aee@o330581.ingest.sentry.io/5321573",
    integrations=[FlaskIntegration()]
)


db = SQLAlchemy()

login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0


@app.route('/')
@app.endpoint('index')
# @login_manager.request_loader
def index():
    return render_template('index.html')


@app.route('/dashboard')
@app.endpoint('dashboard')
# @login_manager.request_loader
# @login_required
def dashboard():
    return "dashboard"


@app.route('/auth/signin', methods=['POST', 'GET'])
@app.endpoint('auth.signin')
# @login_manager.request_loader
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else FlaskIntegration

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return redirect(url_for('auth.signup'))

        login_user(user, remember=remember)
        return redirect (url_for('dashboard'))
    else:
        try:
            return render_template('signin.html')
        except TemplateNotFound:
            abort(404)


@app.route('/auth/signup')
@app.endpoint('auth.signup')
@login_manager.request_loader
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            return redirect(url_for(signup))

        naw_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('signin'))
    else:
        try:
            return render_template('signup.html')
        except TemplateNotFound:
            abort(404)


@app.route('/auth/logout')
@app.endpoint('auth.logout')
@login_manager.request_loader
@login_required
def logout():
    login_user()
    return redirect(url_for('index'))


@app.route('/api/v1/tag/virgool', methods=['GET'])
def tag_virgool():
    if request.method == 'GET':
        v = Virgool(request.args.get('url'))
        virgoolak1 = Type1(avatar=v.get_avatar(), 
                           name=v.get_name(), 
                           bio=v.get_bio(), 
                           title=v.get_title(), 
                           poster=v.get_poster())
        return send_file(
            io.BytesIO(virgoolak1.byte_array()),
            mimetype='image/png',
            as_attachment=True,
            attachment_filename='virgoolak.png')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
