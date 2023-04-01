from flask import Flask, render_template, flash, url_for, redirect
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = 'ab9c32a070313d1343395f1cc4d5a669'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(24), unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False )
    password = db.Column(db.String(32), nullable = False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    content = db.Column(db.Text, nullable = False)
    location = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

@app.route("/home")
def home():
    return render_template('home.html', title = 'Home')

@app.route("/about")
def about():
    return render_template('about.html', title = 'About Page')

@app.route("/events")
def events():
    return render_template('events.html', title = 'Events')

@app.route("/mapping")
def mapping():
    return render_template('mapping.html', title = 'Mapping')


