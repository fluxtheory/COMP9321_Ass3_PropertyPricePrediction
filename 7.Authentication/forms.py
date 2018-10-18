from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)

class Register_Form(FlaskForm):
    username=StringField('User Name',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('register')
