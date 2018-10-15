import json
from functools import wraps
from time import time,sleep

import pandas as pd
from flask import Flask
from flask import request
from flask_restplus import Resource, Api, abort
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature

try_name = 'Tom'
name_list = ['Tom', 'Jerry']
set = {}


class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, username):
        info = {
            'username': username,
            'creation_time': time()
        }

        token = self.serializer.dumps(info)
        return token.decode()

    def validate_token(self, token):
        info = self.serializer.loads(token.encode())

        if time() - info['creation_time'] > self.expires_in:
            raise SignatureExpired("The Token has been expired; get a new token")

        return info['username']


SECRET_KEY = "A SECRET KEY; USUALLY A VERY LONG RANDOM STRING"
expires_in = 600
auth = AuthenticationToken(SECRET_KEY, expires_in)

app = Flask(__name__)
api = Api(app, authorizations={
                'API-KEY': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'AUTH-TOKEN'
                }
            },
          security='API-KEY',
          default="Property",
          title="Property Prediction",
          description="This is just a simple example to show how publish data as a service.")


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        #token = request.headers.get('AUTH-TOKEN')
        token = try_name
        if not token:
            abort(401, 'Authentication token is missing')
        if token not in set:
            abort(401, 'Authentication is missing for matching')

        try:
            user = auth.validate_token(set[token])
        except SignatureExpired as e:
            abort(401, e.message)
        except BadSignature as e:
            abort(401, e.message)

        return f(*args, **kwargs)

    return decorated



property_model = api.model('Property', {
    'Flickr_URL': fields.String,
    'Constructor': fields.String,
    'Agent': fields.String,
    'Title': fields.String,
    'Date_of_Construction': fields.Integer,
    'Price': fields.Integer,
    'Position': fields.String,
    'Identifier': fields.String
})

parser = reqparse.RequestParser()


credential_model = api.model('credential', {
    'username': fields.String,
    'password': fields.String
})

credential_parser = reqparse.RequestParser()
credential_parser.add_argument('username', type=str)
credential_parser.add_argument('password', type=str)


@api.route('/token')
class Token(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Generates a authentication token")
    @api.expect(credential_parser, validate=True)
    def get(self):
        args = credential_parser.parse_args()

        username = args.get('username')
        password = args.get('password')

        if username == 'property' and password == 'property':
            return {"token": auth.generate_token(username)}

        if usename in name_list:
            a = auth.generate_token(username)
            set[username] = a




        return {"message": "authorization has been refused for those credentials."}, 401




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
