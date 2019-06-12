from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo


roles = ['Student', 'Teacher', 'Admin']

class EmailRegistrationForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()]) 
	submit = SubmitField('Register')

class RegistrationForm(FlaskForm):
	firstname = StringField('First Name', validators=[DataRequired()])
	secondname = StringField('Second Name')
	username = StringField('Username', validators=[DataRequired()])
	school_id = StringField('School ID', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	identification = StringField('Email or Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class OTPForm(FlaskForm):
	OTP = StringField('OTP', validators=[DataRequired(), Length(min=6, max=6)])
	submit = SubmitField('Verify')


class ForgotForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Send verification email')
		

class ResetForm(FlaskForm):
	code = StringField('Code', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset password')

class AddSchoolForm(FlaskForm):
	schoolname = StringField('School Name', validators=[DataRequired()])
	city = StringField('City', validators=[DataRequired()])
	state = StringField('State', validators=[DataRequired()])
	pincode = StringField('Pin Code', validators=[DataRequired()])
	addresslineone = StringField('Address Line 1', validators=[DataRequired()])
	addresslinetwo = StringField('Address Line 2')
	board = StringField('Board', validators=[DataRequired()])
	numberofstudent = StringField('Number of Student', validators=[DataRequired()])
	priciplename = StringField('Principle Name', validators=[DataRequired()])
	ownername = StringField('Owner Name', validators=[DataRequired()])
	website = StringField('School Website', validators=[DataRequired()])
	additionalcomment = StringField('Additional Comment')
	submit = SubmitField('Add School')

# class SessionForm(FlaskForm):
# 	session = StringField('Session Name', validators=[DataRequired()])
# 	starttime = DateField('Start at (Year-month-date)', format='%Y-%m-%d')
# 	endtime = DateField('End at (Year-month-date)', format='%Y-%m-%d')
# 	submit = SubmitField('Create Session')



	


















