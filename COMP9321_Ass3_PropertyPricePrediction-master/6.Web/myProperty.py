#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for, flash
from wtforms import *
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
import requests
import json
import unicodedata

app = Flask(__name__)

app.config['SECRET_KEY'] = '3141592653589793238462643383279502884197169399'    # for CSRF

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max =50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class SearchForm(FlaskForm):
    address = StringField()
    #council = StringField()
    #region = StringField()
    landsize = IntegerField()
    property_type = SelectField('Type', validators=[DataRequired()], choices = ['House', 'Flat', 'Apartment'])
    num_bedroom = SelectField('Bedrooms', validators=[DataRequired()], choices = ['1','2','3','4'])
    num_bathroom = SelectField('Bathrooms', validators=[DataRequired()], choices = ['1','2','3'])
    # last_sale_date = DateField()      # OPTIONAL FIELDS?
    # last_sale_price = FloatField()    #OPTIONAL FIELDS?

@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('welcome', name=form.username.data))
    return render_template('login.html', form=form)

@app.route('/login')
def welcome():
    return redirect(url_for('search'))     # code breaks here

# search property
@app.route('/property')
def search(name):
    form = SearchForm()
    return render_template('show.html', info=info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
