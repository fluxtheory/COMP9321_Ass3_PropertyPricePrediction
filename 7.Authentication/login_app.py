

from forms import LoginForm
from models import User

import json
from functools import wraps
from time import time

import pandas as pd
from flask import Flask, render_template, request
from flask_restplus import Resource, Api, abort
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
import os
from flask_wtf.csrf import CsrfProtect
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user


app = Flask(__name__)
api = Api(app,
          default="Login",  # Default namespace
          title="Login",  # Documentation Title
          description="Login")




app.secret_key = os.urandom(24)

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)


# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# csrf protection
# csrf = CsrfProtect()
# csrf.init_app(app)

@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = User(user_name)
        if user.verify_password(password):
            login_user(user, remember=remember_me)
            return redirect(request.args.get('next') or url_for('main'))
    return render_template('login.html', title="Sign In", form=form)



@app.route('/')
@app.route('/main')
@login_required
def main():
    return render_template(
        'main.html', username=current_user.username)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    
    columns_to_drop = ['SellerG',
                       'Propertycount',
                       'Address'
                       ]
    csv_file = "data.csv"
    df = pd.read_csv(csv_file)
    df.drop(columns_to_drop, inplace=True, axis=1)


    new_date = df['Date'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    new_date = new_date.fillna(0)
    df['Date'] = new_date


    df.columns = [c.replace(' ', '_') for c in df.columns]


    df.set_index('Price', inplace=True)

    app.run(debug=True)















