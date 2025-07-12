from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                         validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                           validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                           validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    username = StringField('Username',
                         validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                      validators=[DataRequired(), Email()])
    location = StringField('Location')
    profile_photo = FileField('Profile Photo')
    availability = SelectField('Availability',
                             choices=[('weekends', 'Weekends'),
                                     ('evenings', 'Evenings'),
                                     ('flexible', 'Flexible')])
    is_public = BooleanField('Make my profile public')
    skills_offered = StringField('Skills Offered (comma separated)',
                               validators=[DataRequired()])
    skills_wanted = StringField('Skills Wanted (comma separated)',
                              validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class SwapRequestForm(FlaskForm):
    offered_skill = StringField('Skill You Will Offer',
                              validators=[DataRequired()])
    requested_skill = StringField('Skill You Want in Return',
                                validators=[DataRequired()])
    submit = SubmitField('Request Swap')

class RatingForm(FlaskForm):
    rating = IntegerField('Rating (1-5)',
                        validators=[DataRequired()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit Rating')