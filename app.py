from flask import Flask, render_template, flash, url_for, redirect
from datetime import datetime
from forms import RegistrationForm, LoginForm, EventForm

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

'''
Event = [
    event {
        id
        title
        description
        date_posted
        content
        creator_id
        participant [
            {
                join_date
                user_id
            }
        ]
        polygon {
            [latitude, longitude],
            ...,
            ...
        }
    },
    ...
]
'''

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
        event = Event(title = form.title.data, date_posted = datetime.now, content = form.content.data, location = form.location.data)
        db.session.add(event)
        db.session.commit()
        flash(f'Event created, thanks for contributing!')
    return render_template('events.html', title = 'Events', form = form)

@app.route("/map")
def map():
    return render_template('map.html', title = 'Maps', data = '')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit:
        user = User(form.username.data, email = form.email.data, password = form.password.data, location = form.location.data)

        flash(f'Account created! Thanks for signing up, {form.username.data}!', 'success')
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Registration', form = form)


@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit:
        if form.username.data == "admin@blog.com" or "admin" and form.password.data == "password":
            flash(f'You have successfully logged in as admin!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Sorry, try again.', 'danger')
    return render_template('login.html', title = 'Log In', form = form)

if '__name__' == '__main__':
    app.run(debug=True)
    print("Running application. ")


