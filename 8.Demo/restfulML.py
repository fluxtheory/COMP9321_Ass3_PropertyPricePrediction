#-*-coding:utf8-*-
__author__ = 'Pengcheng Xie'

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

@api.route('/pengcheng9321/<int:Rooms>/<string:Type>/<float:Distance>/<int:Bathrooms>/<int:Car>/<float:LandSize>/<string:CouncilArea>')
@api.param('Rooms', 'Number of rooms.')
@api.param('Type', 'br - bedroom(s); h - house,cottage,villa, semi,terrace; u - unit, duplex; t - townhouse; dev site - development site; o res - other residential.')
@api.param('Distance', 'Distance from CBD in Kilometres.')
@api.param('Bathrooms', 'Number of bathrooms.')
@api.param('Car', 'Number of car spots.')
@api.param('LandSize', 'Land Size in Metres squared.')
@api.param('CouncilArea', 'Governing council for the area.')
class HousePrediction(Resource):
    @api.response(400, 'Data invalid')
    @api.response(200, 'OK')
    @api.doc(description="Input some features of your property and you will get its price.")
    def get(self, Rooms, Type, Distance, Bathrooms, Car, LandSize, CouncilArea):
        env = [Rooms,Type,'S','Nelson','2018', Distance,float(Bathrooms),float(Car),LandSize,CouncilArea]
        predict_price = PropertyPricePrediction()
        predict_price.setArgs(env)
        price = predict_price.predict()
        price = round(price[0])
        return {"message": "The price of this property is: AUD$ {} ".format(price)}, 200

        # if not check:
        #     api.abort(400, "Input information invalid")

# @api.route('/pengcheng9321/<int:Rooms>/<string:Type>')
# @api.param('Rooms', 'Number of rooms.')
# @api.param('Type', 'br - bedroom(s); h - house,cottage,villa, semi,terrace; u - unit, duplex; t - townhouse; dev site - development site; o res - other residential.')
# # @api.param('Distance', 'Distance from CBD in Kilometres.')
# class HousePrediction(Resource):
#     @api.response(400, 'Data invalid')
#     @api.response(200, 'OK')
#     # @api.doc(description="Q5: Get an economic indicator value for given country and a year")
#     def get(self, Rooms, Type):
#         # env = [Rooms,Type,'None','None','None', Distance,Bathrooms,Car,LandSize,CouncilArea]
#         predict_price = PropertyPricePrediction()
#         # predict_price.setArgs(env)
#         # price = predict_price.predict()
#         return {"message": "The price is {} ".format(Type)}, 200

# run the application
app.run(debug=True)