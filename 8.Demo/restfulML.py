#-*-coding:utf8-*-
__author__ = 'Pengcheng Xie and Hanming Yin'

import json
from mlAPI import PropertyPricePrediction
from flask_restplus import Resource, Api
from flask import request
from flask import Flask
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse

app = Flask(__name__)
api = Api(app,
          default="Property Price Prediction",  # Default namespace
          title="Property Features",  # Documentation Title
          description="This is the assignment 3 for Property Price Prediction.")  # Documentation Description

@api.route('/predict/<Rooms>/<Type>/<Distance>/<Bathrooms>/<Car>/<LandSize>/<CouncilArea>')
@api.param('Rooms', 'Number of rooms.')
@api.param('Type', 'h - house,cottage,villa, semi,terrace; u - unit, duplex; t - townhouse; dev site - development site; o res - other residential.')
@api.param('Distance', 'Distance from CBD in Kilometres.')
@api.param('Bathrooms', 'Number of bathrooms.')
@api.param('Car', 'Number of car spots.')
@api.param('LandSize', 'Land Size in Metres.')
@api.param('CouncilArea', 'Governing council for the area.')
class HousePrediction(Resource):
    @api.response(400, 'Data invalid')
    @api.response(200, 'OK')
    @api.doc(description="Input some features of your property and you will get its price.")
    def get(self, Rooms, Type, Distance, Bathrooms, Car, LandSize, CouncilArea):
        env = [int(Rooms), Type,'S','Nelson','2018', int(Distance),float(Bathrooms),float(Car),int(LandSize),CouncilArea]
        print(env)
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

if __name__ == '__main__':
    app.run(debug=True)
