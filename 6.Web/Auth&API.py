import json
from functools import wraps
from time import time

import pandas as pd
from flask import Flask
from flask import request
from flask_restplus import Resource, Api, abort
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature


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

        token = request.headers.get('AUTH-TOKEN')
        if not token:
            abort(401, 'Authentication token is missing')

        try:
            user = auth.validate_token(token)
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
parser.add_argument('order', choices=list(column for column in property_model.keys()))
parser.add_argument('ascending', type=inputs.boolean)

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

        return {"message": "authorization has been refused for those credentials."}, 401


@api.route('/Property')
class BooksList(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Get all property")
    @requires_auth
    def get(self):

        args = parser.parse_args()

        order_by = args.get('order')
        ascending = args.get('ascending', True)

        if order_by:
            df.sort_values(by=order_by, inplace=True, ascending=ascending)

        json_str = df.to_json(orient='index')

        ds = json.loads(json_str)
        ret = []

        for idx in ds:
            property = ds[idx]
            property['Identifier'] = int(idx)
            ret.append(property)

        return ret

    @api.response(201, 'Property Created Successfully')
    @api.response(400, 'Validation Error')
    @api.doc(description="Add a new property")
    @api.expect(property_model, validate=True)
    @requires_auth
    def post(self):
        property = request.json

        if 'Identifier' not in property:
            return {"message": "Missing Identifier"}, 400

        id = property['Identifier']


        if id in df.index:
            return {"message": "A property with Identifier={} is already in the dataset".format(id)}, 400


        for key in property:
            if key not in property_model.keys():

                return {"message": "Property {} is invalid".format(key)}, 400
            df.loc[id, key] = property[key]


        return {"message": "Property {} is created".format(id)}, 201


@api.route('/property/<int:id>')
@api.param('id', 'The Property identifier')
class Books(Resource):
    @api.response(404, 'Property was not found')
    @api.response(200, 'Successful')
    @api.doc(description="Get a property by its ID")
    @requires_auth
    def get(self, id):
        if id not in df.index:
            api.abort(404, "Property {} doesn't exist".format(id))

        property = dict(df.loc[id])
        return property

    @api.response(404, 'Property was not found')
    @api.response(200, 'Successful')
    @api.doc(description="Delete a property by its ID")
    @requires_auth
    def delete(self, id):
        if id not in df.index:
            api.abort(404, "Property {} doesn't exist".format(id))

        df.drop(id, inplace=True)
        return {"message": "Property {} is removed.".format(id)}, 200

    @api.response(404, 'Property was not found')
    @api.response(400, 'Validation Error')
    @api.response(200, 'Successful')
    @api.expect(property_model, validate=True)
    @api.doc(description="Update a property by its ID")
    @requires_auth
    def put(self, id):

        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))

        # get the payload and convert it to a JSON
        property = request.json


        if 'Identifier' in property and id != property['Identifier']:
            return {"message": "Identifier cannot be changed".format(id)}, 400

        # Update the values
        for key in property:
            if key not in property_model.keys():
                # unexpected column
                return {"message": "Property {} is invalid".format(key)}, 400
            df.loc[id, key] = property[key]

        df.append(property, ignore_index=True)
        return {"message": "Book {} has been successfully updated".format(id)}, 200


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
