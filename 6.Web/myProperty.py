#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_bootstrap import Bootstrap
from flask_restplus import reqparse
from wtforms import *
from flask_wtf import FlaskForm
from wtforms.validators import *
import requests
import json
import unicodedata

app = Flask(__name__)
app.config['SECRET_KEY'] = '3141592653589793238462643383279502884197169399'    # for CSRF
bootstrap = Bootstrap(app)

parser = reqparse.RequestParser()
parser.add_argument('address',required=True)
parser.add_argument('landsize', required=True)
parser.add_argument('council')
parser.add_argument('type')
parser.add_argument('bedrooms')
parser.add_argument('bathrooms')
parser.add_argument('garage')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max =50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

melb_councils = []

class SearchForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    council = SelectField('Council', validators=[Optional()], choices=[("",""),('City of Council1','City of Council1'),('Council2','Council2')], default="")
    #region = StringField()
    landsize = IntegerField('Landsize', validators=[InputRequired(), NumberRange(min=1, max=9999, message="Please provide a valid number")])
    property_type = SelectField('Type', validators=[DataRequired()], choices=[('House','House'), ('Flat','Flat'),('Unit','Unit')])
    num_bedroom = SelectField('Bedrooms', validators=[Optional()], choices=[("",""),('1','1'),('2','2'),('3','3'),('4','4')], default="")
    num_bathroom = SelectField('Bathrooms', validators=[Optional()], choices=[("",""),('1','1'),('2','2'),('3','3')], default="")
    num_garage = SelectField('Garage Spaces', validators=[Optional()], choices=[("",""),('0','0'),('1','1'),('2','2')], default="")
    # last_sale_date = DateField()      # OPTIONAL FIELDS?
    # last_sale_price = FloatField()    #OPTIONAL FIELDS?
    submit = SubmitField('Predict')


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['username'] == 'admin' and \
               request.form['password'] == 'password':
                flash('Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
                session.clear()
                return redirect(url_for('searchpage', name=form.username.data))
            else :
                flash('Incorrect username or password')

    #elif request.method == 'GET':        
    return render_template('login.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def searchpage():
    form = SearchForm()
    flash("Welcome Guest!")
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Retrieving prediction for address={} Council={} Landsize={} Type={} Bedrooms={} Bathrooms={} \
                Garage={}'.format(
                form.address.data, form.council.data, form.landsize.data, form.property_type.data, \
                form.num_bedroom.data, form.num_bathroom.data, form.num_garage.data))
            session.clear()
            return redirect(url_for('resultpage', address=form.address.data, landsize=form.landsize.data, council=form.council.data, \
            type=form.property_type.data, bedrooms=form.num_bedroom.data, bathrooms=form.num_bathroom.data, garage=form.num_garage.data))
        else:
            flash('Retrieving prediction for address={} Council={} Landsize={} Type={} Bedrooms={} Bathrooms={} \
                Garage={}'.format(
                form.address.data, form.council.data, form.landsize.data, form.property_type.data, \
                form.num_bedroom.data, form.num_bathroom.data, form.num_garage.data))
            flash('errors={}'.format(form.errors.items()))

    #elif request.method == 'GET': 
    return render_template('show.html', form=form)

# search property / return results
@app.route('/property')
def resultpage():
    args = parser.parse_args()
    return "Address " + args['address'] + "<br/>" \
    "Landsize " + args['landsize'] + "<br/>" \
    "Council " + args['council'] + "<br/>" \
    "Bedrooms " + args['bedrooms'] + "<br/>" \
    "Bathrooms " + args['bathrooms'] + "<br/>" \
    "Garage " + args['garage'] + "<br/>" \

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
