from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class RegistrationForm(FlaskForm):
	wp_username = StringField('Username', validators=[DataRequired()])
	wp_url = StringField('URL', validators=[DataRequired()])
	wp_password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Register')
