from flask import Flask, render_template, flash, url_for, redirect
from datetime import datetime

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
    return render_template('events.html', title = 'Events', data = '')

@app.route("/map")
def map():
    return render_template('map.html', title = 'Maps', data = '')

@app.route("/login")
def login():
    return render_template('login.html', title = 'Login')

@app.route("/register")
def register():
    return render_template('register.html', title = 'Register')

if '__name__' == '__main__':
    app.run(debug=True)
    print("Running application. ")


