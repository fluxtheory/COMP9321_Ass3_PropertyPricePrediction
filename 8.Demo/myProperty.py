#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_bootstrap import Bootstrap
from flask_restplus import reqparse
#from mlAPI import PropertyPricePrediction
from wtforms import *
from flask_wtf import FlaskForm
from wtforms.validators import *
import requests
import json
import unicodedata
import re
import os.path

app = Flask(__name__)
app.config['SECRET_KEY'] = '3141592653589793238462643383279502884197169399'    # for CSRF
bootstrap = Bootstrap(app)

#ppp = PropertyPricePrediction()

parser = reqparse.RequestParser()
#parser.add_argument('address',required=True)
parser.add_argument('landsize', required=True)
parser.add_argument('distance', required=True)
parser.add_argument('council')
parser.add_argument('type', required=True)
parser.add_argument('bedrooms')
parser.add_argument('bathrooms')
parser.add_argument('garage')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max =50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

melb_councils = [("Alpine Shire","Alpine Shire"),
("Ararat Rural City","Ararat Rural City"),
("Ballarat City","Ballarat City"),
("Banyule City","Banyule City"),
("Bass Coast Shire","Bass Coast Shire"),
("Baw Baw Shire","Baw Baw Shire"),
("Bayside City","Bayside City"),
("Benalla Rural City","Benalla Rural City"),
("Boroondara City","Boroondara City"),
("Brimbank City","Brimbank City"),
("Buloke Shire","Buloke Shire"),
("Campaspe Shire","Campaspe Shire"),
("Cardinia Shire","Cardinia Shire"),
("Casey City","Casey City"),
("Central Goldfields Shire","Central Goldfields Shire"),
("Colac Otway Shire","Colac Otway Shire"),
("Corangamite Shire","Corangamite Shire"),
("Darebin City","Darebin City"),
("East Gippsland Shire","East Gippsland Shire"),
("Frankston City","Frankston City"),
("Gannawarra Shire","Gannawarra Shire"),
("Glen Eira City","Glen Eira City"),
("Glenelg Shire","Glenelg Shire"),
("Golden Plains Shire","Golden Plains Shire"),
("Greater Bendigo City","Greater Bendigo City"),
("Greater Dandenong City","Greater Dandenong City"),
("Greater Geelong City","Greater Geelong City"),
("Greater Shepparton City","Greater Shepparton City"),
("Hepburn Shire","Hepburn Shire"),
("Hindmarsh Shire","Hindmarsh Shire"),
("Hobsons Bay City","Hobsons Bay City"),
("Horsham Rural City","Horsham Rural City"),
("Hume City","Hume City"),
("Indigo Shire","Indigo Shire"),
("Kingston City","Kingston City"),
("Knox City","Knox City"),
("Latrobe City","Latrobe City"),
("Loddon Shire","Loddon Shire"),
("Macedon Ranges Shire","Macedon Ranges Shire"),
("Manningham City","Manningham City"),
("Mansfield Shire","Mansfield Shire"),
("Maribyrnong City","Maribyrnong City"),
("Maroondah City","Maroondah City"),
("Melbourne City","Melbourne City"),
("Melton City","Melton City"),
("Mildura Rural City","Mildura Rural City"),
("Mitchell Shire","Mitchell Shire"),
("Moira Shire","Moira Shire"),
("Monash City","Monash City"),
("Moonee Valley City","Moonee Valley City"),
("Moorabool Shire","Moorabool Shire"),
("Moreland City","Moreland City"),
("Mornington Peninsula Shire","Mornington Peninsula Shire"),
("Mount Alexander Shire","Mount Alexander Shire"),
("Moyne Shire","Moyne Shire"),
("Murrindindi Shire","Murrindindi Shire"),
("Nillumbik Shire","Nillumbik Shire"),
("Northern Grampians Shire","Northern Grampians Shire"),
("Port Phillip City","Port Phillip City"),
("Pyrenees Shire","Pyrenees Shire"),
("Borough of Queenscliffe","Borough of Queenscliffe"),
("South Gippsland Shire","South Gippsland Shire"),
("Southern Grampians Shire","Southern Grampians Shire"),
("Stonnington City","Stonnington City"),
("Strathbogie Shire","Strathbogie Shire"),
("Surf Coast Shire","Surf Coast Shire"),
("Swan Hill Rural City","Swan Hill Rural City"),
("Towong Shire","Towong Shire"),
("Wangaratta Rural City","Wangaratta Rural City"),
("Warrnambool City","Warrnambool City"),
("Wellington Shire","Wellington Shire"),
("West Wimmera Shire","West Wimmera Shire"),
("Whitehorse City","Whitehorse City"),
("Whittlesea City","Whittlesea City"),
("Wodonga City","Wodonga City"),
("Wyndham City","Wyndham City"),
("Yarra City","Yarra City"),
("Yarra Ranges Shire","Yarra Ranges Shire"),
("Yarriambiack Shire","Yarriambiack Shire")]

class SearchForm(FlaskForm):
    #address = StringField('Address', validators=[DataRequired()])
    distance = IntegerField('Distance to CBD', validators=[DataRequired()])
    council = SelectField('Council', validators=[Optional()], choices=melb_councils, default="")
    landsize = IntegerField('Landsize', validators=[InputRequired(), NumberRange(min=1, max=9999, message="Please provide a valid number")])
    property_type = SelectField('Type', validators=[DataRequired()], choices=[('House','House'), ('Unit','Unit'), ('Other','Other')])
    num_bedroom = SelectField('Bedrooms', validators=[Optional()], choices=[("",""),('1','1'),('2','2'),('3','3'),('4','4')], default="")
    num_bathroom = SelectField('Bathrooms', validators=[Optional()], choices=[("",""),('1','1'),('2','2'),('3','3')], default="")
    num_garage = SelectField('Garage Spaces', validators=[Optional()], choices=[("",""),('0','0'),('1','1'),('2','2')], default="")
    submit = SubmitField('Predict')


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['username'] == 'admin' and \
               request.form['password'] == 'password':
                #flash('Login requested for user {}, remember_me={}'.format(
                #form.username.data, form.remember_me.data))
                session.clear()
                return redirect(url_for('searchpage', name=form.username.data))
            else :
                flash('Incorrect username or password')
 
    return render_template('login.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def searchpage():
    form = SearchForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Retrieving prediction for Council={} Landsize={} Type={} Bedrooms={} Bathrooms={} \
                Garage={}'.format(
                form.council.data, form.landsize.data, form.property_type.data, \
                form.num_bedroom.data, form.num_bathroom.data, form.num_garage.data)) # form.address.data
            session.clear()
            return redirect(url_for('resultpage', landsize=form.landsize.data, council=form.council.data, \
            type=form.property_type.data, bedrooms=form.num_bedroom.data, bathrooms=form.num_bathroom.data, garage=form.num_garage.data, distance=form.distance.data))   #address=form.address.data,
        else:
            flash('Retrieving prediction for Council={} Landsize={} Type={} Bedrooms={} Bathrooms={} \
                Garage={}'.format(
                form.council.data, form.landsize.data, form.property_type.data, \
                form.num_bedroom.data, form.num_bathroom.data, form.num_garage.data))
            flash('errors={}'.format(form.errors.items()))

    return render_template('search.html', form=form)

# search property / return results
@app.route('/property')
def resultpage():
    args = parser.parse_args()

    #address = args['address']
    landsize = float(args['landsize'])
    distance = float(args['distance'])

    council = args['council']  
    council = re.sub(r"Shire", "Shire Council", council)
    council = re.sub(r"City", "City Council", council)

    if args['bedrooms']:
        bedrooms = int(args['bedrooms']) 
    else:
        bedrooms = None

    if args['bathrooms']:
        bathrooms = int(args['bathrooms'])
    else:
        bathrooms = None

    if args['garage']:
        garage = int(args['garage'])
    else :
        garage = None

    property_type = args['type']
    
    
    # method, seller and sold year will be none.

    env = [bedrooms,property_type,None,None,None,distance, bathrooms, garage, landsize, council]
    #ppp.setArgs(env)
    #price = ppp.predict()

    pic1 = os.path.join("images","avg.png")
    pic2 = os.path.join("images","greg.png")

    return render_template('show.html', pic1=pic1, pic2=pic2)
    #return os.path.abspath(pic1)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=12345)