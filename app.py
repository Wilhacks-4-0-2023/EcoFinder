from flask import Flask, render_template, flash, url_for, redirect
import bcrypt
from datetime import datetime
from forms import RegistrationForm, LoginForm, EventForm
from flask_login import login_user, current_user, logout_user, login_required

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = 'ab9c32a070313d1343395f1cc4d5a669'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False )
    password = db.Column(db.String, nullable = False)
    events = db.relationship('Event', backref = 'author', lazy = True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    content = db.Column(db.Text, nullable = False)
    location = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title = 'Home')


@app.route("/about")
def about():
    return render_template('about.html', title = 'About Page')

@app.route("/events")
def events():
    form = EventForm()
    if form.validate_on_submit:
        event = Event(form.title.data, date_posted = datetime.utcnow(), content = form.content.data, location = form.location.data)
        db.session.add(event)
        db.session.commit()
        flash(f'Event created, thanks for contributing!')
    return render_template('events.html', title = 'Events', form = form)

@app.route("/map")
def map():
    eventData = Event.query.all()
    return render_template('map.html', title = 'Maps', data = eventData)

# has hashing enabled
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# has hashing enabled
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

if '__name__' == '__main__':
    app.run(debug=True)
    print("Running application. ")


