#-*-coding:utf8-*-

__author__ = 'Pengcheng Xie, Xavier Yan, Hanming Yin'

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
<<<<<<< HEAD

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
        predict_price.setArgs(self.env)
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
    app.run(debug = True)

