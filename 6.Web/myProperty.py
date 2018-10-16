#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from wtforms import *
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
import requests
import json
import unicodedata

app = Flask(__name__)
app.config['SECRET_KEY'] = '3141592653589793238462643383279502884197169399'    # for CSRF
bootstrap = Bootstrap(app)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max =50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

melb_councils = []

class SearchForm(FlaskForm):
    address = StringField()
    council = SelectField('Council', choices = [])
    #region = StringField()
    landsize = IntegerField()
    property_type = SelectField('Type', validators=[DataRequired()], choices = ['House', 'Flat', 'Apartment'])
    num_bedroom = SelectField('Bedrooms', validators=[DataRequired()], choices = ['1','2','3','4'])
    num_bathroom = SelectField('Bathrooms', validators=[DataRequired()], choices = ['1','2','3'])
    num_garage = SelectField('Garage Spaces', validators=[DataRequired()], choices = ['0','1','2'])
    # last_sale_date = DateField()      # OPTIONAL FIELDS?
    # last_sale_price = FloatField()    #OPTIONAL FIELDS?
    submit = SubmitField('Predict')


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        if request.form['username'] == 'admin' and \
           request.form['password'] == 'password':
            flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
            return redirect(url_for('searchpage', name=form.username.data))
        else :
            flash('Incorrect username or password')
        
    return render_template('login.html', form=form)


@app.route('/login/<name>')
def searchpage(name):
    form = SearchForm()
    if form.validate_on_submit():
        flash("testing")
        return redirect(url_for('resultpage',))
    return render_template('show.html', form=form)

# search property / return results
@app.route('/property')
def results():
    return

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port= 12345)
