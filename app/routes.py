from flask import Flask, render_template, flash, url_for, redirect
from app import db, routes, bcrypt
from datetime import datetime
from forms import RegistrationForm, LoginForm, EventForm
from flask_login import login_user, current_user, logout_user, login_required, LoginManager



@routes.route("/")
@routes.route("/home")
def home():
    return render_template('home.html', title = 'Home')


@routes.route("/about")
def about():
    return render_template('about.html', title = 'About Page')

@routes.route("/events", methods = ['GET', 'POST'])
def events():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(form.title.data, date_posted = datetime.utcnow(), content = form.content.data, location = form.location.data, author = current_user)
        db.session.add(event)
        db.session.commit()
        flash(f'Event created, thanks for contributing!')
        flash(f'{Event.query.all()}')
        
    return render_template('events.html', title = 'Events', form = form)

@routes.route("/map")
def map():
    eventData = Event.query.all()
    return render_template('map.html', title = 'Maps', data = eventData)

# has hashing enabled
@routes.route("/register", methods=['GET', 'POST'])
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
@routes.route("/login", methods=['GET', 'POST'])
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

@routes.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@routes.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

if '__name__' == '__main__':
    routes.run(debug=True)
    print("Running application. ")


