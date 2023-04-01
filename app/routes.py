from flask import render_template, flash, url_for, redirect, request, jsonify
from app import app, db, bcrypt
from datetime import datetime
from app.forms import RegistrationForm, LoginForm, EventForm
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Event

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title = 'Home')


@app.route("/about")
def about():
    return render_template('about.html', title = 'About Page')

@app.route("/events", methods = ['GET', 'POST'])
@login_required
def events():
    getEventRows()

    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, date_posted=datetime.utcnow(), content=form.content.data, author=current_user)
        db.session.add(event)
        db.session.commit()
        flash(f'Event created, thanks for contributing!')
        flash(f'{Event.query.all()}')

        
    return render_template('events.html', title='Events', form=form)

@app.route("/map", methods = ['GET', 'POST'])
def map():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, date_posted=datetime.utcnow(), content=form.content.data, author=current_user)
        db.session.add(event)
        db.session.commit()
        flash(f'Event created, thanks for contributing!')
        flash(f'{Event.query.all()}')
    eventData = Event.query.all()
    return render_template('map.html', title='Maps', data=eventData, form=form) 

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
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
    return render_template('login.html', title = 'Log In', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account Details')

def getEventRows():
    rows = Event.query.all()
    column_keys = Event.__table__.columns.keys()
    rows_dic_temp = {}
    rows_dic = []
    for row in rows:
        for col in column_keys:
            rows_dic_temp[col] = getattr(row, col)
        rows_dic.append(rows_dic_temp)
        rows_dic_temp= {}
    return jsonify(rows_dic)