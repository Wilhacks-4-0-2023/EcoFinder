from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):

    # uses validators (required data and max and min username length) to check whether a username is valid or not.
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min = 2, max = 20)]) 

    # same things with email and password sfields
    email = StringField('Email', validators=[DataRequired(), Email()]) # if datarequired is used, it marks the field as required.
    password = PasswordField('Password', 
                           validators=[DataRequired(), Length(min = 5, max = 32)])
    
    confirm_password = PasswordField('Confirm Password', 
                           validators=[DataRequired(), EqualTo('password')]) # checks if confirm's value = password's value
    
    submit = SubmitField('Sign Up!')

class LoginForm(FlaskForm):

    username = StringField('Username', 
                           validators=[DataRequired(), Length(min = 2, max = 20)]) 

    password = PasswordField('Password', 
                           validators=[DataRequired(), Length(min = 5, max = 32)])
    
    # checkbox bool for remembering account
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Log In')

    
