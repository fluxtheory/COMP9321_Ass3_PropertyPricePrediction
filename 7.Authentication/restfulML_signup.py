#-*-coding:utf8-*-
__author__ = 'Pengcheng Xie, Xavier Yan, Hanming Yin'

from mlAPI import PropertyPricePrediction
import json
import pymongo
import pandas as pd
import numpy as np
import requests

from flask import Flask, request
from flask_restplus import fields, inputs, reqparse, Resource, Api
from flask_bootstrap import Bootstrap
from forms import LoginForm,Register_Form

app = Flask(__name__)
api = Api(app,
          default="Property Price Prediction",  # Default namespace
          title="Property Features",  # Documentation Title
          description="This is the assignment 3 for Property Price Prediction.")  # Documentation Description
app.config['SECRET_KEY'] = 'any secret string'
bootstrap = Bootstrap(app)


# if we're going by url  i.e. http://localhost:12345/bedrooms=3&bathrooms=1&garage=0& .... etc
parser = reqparse.RequestParser()
parser.add_argument('bedrooms')
parser.add_argument('bathrooms')
parser.add_argument('garage')
parser.add_argument('council', required=True)
parser.add_argument('property_type', required=True)
parser.add_argument('distance', required=True)
parser.add_argument('landsize', required=True)

# otherwise, if we're accepting a json load.
request_model = api.model('Prediction',
    { "bedrooms" : fields.Integer,
      "bathrooms": fields.Integer,
      "garage"   : fields.Integer,
      "council"  : fields.String,
      "property_type": fields.String,
      "distance" : fields.Float,
      "landsize" : fields.Float
    })


@api.route('/predictionService')
class HousePrediction(Resource):
    # def __init__(self):
    #     self.env = []

    @api.response(400, 'Data invalid')
    @api.response(200, 'OK')
    @api.doc(description="Input some features of your property.")
    @api.expect(request_model, validate=True)
    def post(self):
        Rooms = request.json['bedrooms']
        Type = request.json['property_type']
        Distance = request.json['distance']
        Bathrooms = request.json['bathrooms']
        Car = request.json['garage']
        LandSize = request.json['landsize']
        CouncilArea = request.json['council']

        env = [Rooms, Type,'S','Nelson','2018', Distance,float(Bathrooms),float(Car),LandSize,CouncilArea]

        predict_price = PropertyPricePrediction()
        predict_price.setArgs(env)
        price, pic_name, info = predict_price.predict()
        response = dict()
        response["price"] = int(price)
        response['pic_name'] = pic_name
        for i in range(len(info)):
            for j in range(len(info[i])):
                info[i][j] = str(info[i][j])
            response["property" + str(i + 1)] = info[i]
        response = json.dumps(response)

        return response, 200



register_model = api.model('user_register',
    { "Username" : fields.String,
      "Password": fields.String,
    })


@api.route('/register')
class Register(Resource):
    @api.response(201, 'Created a user!')
    @api.response(200, 'this username exist...')
    @api.response(400, 'Validation Error')
    @api.doc(description="Input new username and password")
    @api.expect(register_model, validate=True)
    def post(self):
        Username = request.json['Username']
        Password = request.json['Password']

        df = read_db_from_mLab('user_info')
        #print(df)
        for tup in list(df['entries'][0]):
            if tup['username'] == Username:
                return {"message": "username '{}' has exist".format(Username)}, 200

        mLab_uri = 'mongodb://stevenqin:Scs120386@ds111562.mlab.com:11562/steven_qin'
        client = pymongo.MongoClient(mLab_uri)
        db = client.get_default_database()   
        db.drop_collection('user_info')
        client.close()

        entries = list(df['entries'][0])
        entries.append({'username': Username, 'password':Password})

        mLab_collections = []

        new_dic = {}
        new_dic['collection_id'] = 'user_info'
        new_dic['indicator'] = 'user_info'
        new_dic['entries'] = entries

        mLab_collections.append(new_dic)

        store_in_mLab(mLab_collections, 'user_info')


        return {"message": "username '{}' has been created!".format(Username)}, 201



def read_db_from_mLab(collection_name):
    mLab_uri = 'mongodb://stevenqin:Scs120386@ds111562.mlab.com:11562/steven_qin'

    client = pymongo.MongoClient(mLab_uri)
    db = client.get_default_database()     # db is the mLab db

    collection = db[collection_name]

    client.close()

    return pd.DataFrame(list(collection.find())) # convert to dataframe

def make_user_collection():
    """
     [ { 
          'collection_id' = 'user_info'
          'indicator' = 'user_info'
          'entries' = [ {'username': 'xxxxx', 'password': 'yyyyy'}
                        {'username': 'xxxxx', 'password': 'yyyyy'}
                        ......
                       ]

        } ]
    """
    mLab_uri = 'mongodb://stevenqin:Scs120386@ds111562.mlab.com:11562/steven_qin'

    client = pymongo.MongoClient(mLab_uri)
    db = client.get_default_database()     # db is the mLab db

    collection = db['user_info']

    client.close()

    df = pd.DataFrame(list(collection.find()))

    if not df.empty:
        return

    mLab_collections = []

    new_dic = {}
    new_dic['collection_id'] = 'user_info'
    new_dic['indicator'] = 'user_info'
    new_dic['entries'] = []
    username = 'admin'
    password = 'password'
    new_dic['entries'].append({'username': username, 'password':password})

    mLab_collections.append(new_dic)

    store_in_mLab(mLab_collections, 'user_info')
    print('make_user_collection ok!')
    return


    
def store_in_mLab(data_set, collection_name):
    mLab_uri = 'mongodb://stevenqin:Scs120386@ds111562.mlab.com:11562/steven_qin'

    client = pymongo.MongoClient(mLab_uri)
    db = client.get_default_database()     # db is the mLab db

    # setup a new collection call 'collection_name'
    collection = db[collection_name] 

    # insert the data into new collection
    # Note that the insert method can take either an array or a single dict.
    collection.insert_many(data_set)

    client.close()
    return


if __name__ == '__main__':
    make_user_collection()
    # df = read_db_from_mLab('user_info')
    # print(df['entries'])
    app.run(debug = True)
