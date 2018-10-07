from flask import Flask, render_template, redirect, url_for, flash
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
import requests
import json
import unicodedata

app = Flask(__name__)
app.config['SECRET_KEY'] = '3141592653589793238462643383279502884197169399'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max =50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('login', name=form.username.data))
    return render_template('login.html', form=form)

# search property
@app.route('/search/<name>')
def search(name):
    info = requests.get('http://localhost:5000/search/'+name)
    info = unicodedata.normalize('NFKD', info.text).encode('ascii','ignore')
    info = json.loads(info)
    return render_template('show.html', info=info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
