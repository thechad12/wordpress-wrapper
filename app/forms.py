from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class RegistrationForm(FlaskForm):
	wp_username = StringField('Username', validators=[DataRequired()])
	wp_url = StringField('URL', validators=[DataRequired()])
	wp_password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Register')

class EditForm(FlaskForm):
	wp_username = StringField('Username')
	wp_url = StringField('URL')
	wp_password = PasswordField('Password')
	submit = SubmitField('Edit')

class ImageUpload(FlaskForm):
	image = FileField('Image', validators=[FileRequired(),
		FileAllowed(['jpg', 'png', 'gif']),
		'Images Only'])
	submit = SubmitField('Upload')


class LoginForm(FlaskForm):
	wp_username = StringField('Username', validators=[DataRequired()])
	wp_password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')

