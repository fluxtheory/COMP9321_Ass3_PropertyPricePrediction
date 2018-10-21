#-*-coding:utf8-*-
__author__ = 'Pengcheng Xie, Xavier Yan'

#from mlAPI import PropertyPricePrediction

from flask import Flask, request
from flask_restplus import fields, inputs, reqparse, Resource, Api

app = Flask(__name__)
api = Api(app,
          default="Property Price Prediction",  # Default namespace
          title="Property Features",  # Documentation Title
          description="This is the assignment 3 for Property Price Prediction.")  # Documentation Description

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

    env = []

    @api.response(400, 'Data invalid')
    @api.response(200, 'OK')
    @api.doc(description="Input some features of your property.")
    @api.expect(request_model)
    def post(self):

        Rooms = request.json['bedrooms']
        Type = request.json['property_type']
        Distance = request.json['distance']
        Bathrooms = request.json['bathrooms']
        Car = request.json['garage']
        LandSize = request.json['landsize']
        CouncilArea = request.json['council']

        self.env = [Rooms, Type,'S','Nelson','2018', Distance,float(Bathrooms),float(Car),LandSize,CouncilArea]

        return {
            "bedrooms" : str(Rooms),
            "bathrooms" : str(Bathrooms),
            "garage"   : str(Car),
            "property_type"     : str(Type),
            "landsize" : str(LandSize),
            "distance" : str(Distance),
            "council"  : CouncilArea
        }, 200
        
        # if not check:
        #     api.abort(400, "Input information invalid")

    @api.doc(description="Retrieves the price information")
    def get(self):
        
        predict_price = PropertyPricePrediction()
        predict_price.setArgs(env)
        price, pic_name, info = predict_price.predict()
        response = dict()
        response['price'] = price
        response['pic_name'] = pic_name
        response['similar_property'] = info
        return response, 200
            

    #def get(self)
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

if __name__ == '__main__':
    app.run(debug=True)
