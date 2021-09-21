from flask import Flask, render_template, flash, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required
import os

app = Flask(__name__)


# Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', default='jhsdjfhfvhnskdjamkhcdsfakdfm')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

from models import User
from forms import LoginForm, RegistrationForm, UploadFile


@app.route('/')
def index():
    form = UploadFile()
    if form.validate_on_submit():
        json_file = form.certificate_image.data
        filename = secure_filename(json_file.filename)
        mimetype = json_file.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400
    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            if next_page is None or not next_page[0] == '/':
                next_page = url_for('index')

            return redirect(next_page)
        else:
            flash('Invalid username / password', 'error')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = str(form.email.data).split('@')[0]
        check_exist = User.query.filter_by(email=form.email.data).first()
        if check_exist:
            flash('User already exist', 'error')
            return redirect(url_for('login'))

        user = User(email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=username,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
