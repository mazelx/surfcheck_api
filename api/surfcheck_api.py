from api import custom_fields
from api.data_provider import WeatherProvider, WavesProvider
from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with
import datetime
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
cors = CORS(app)


wave_fields = {"datetime": custom_fields.DateTimeIsoZ,
               "water_temperature": fields.String,
               "wave_direction": fields.String,
               "wave_height": fields.String,
               "wave_height_max": fields.String,
               "wave_period": fields.String,
               "wave_spreading": fields.String
               }

weather_fields = {"datetime": custom_fields.DateTimeIsoZ,
                  "name": fields.String,
                  "wind": fields.String,
                  }



class WaveDoc(Resource):
    @marshal_with(wave_fields)
    def get(self, dt_value):
        provider = WavesProvider()
        if dt_value == 'last':
            doc = provider.latest_one()
        else:
            doc = provider.latest_one(dt_value)
        if not doc:
            print("wave doc ko")
            return "error", 404
        print("wave doc dt :" + str(doc.get("datetime")))
        return doc

#    def put(self, datetime):
#    dt = datetime.strptime(datetime, '%Y%m%d%H%M')
#    surfchecks[datetime] = request.form['data']
#    return {datetime: surfchecks[datetime]}


class WaveList(Resource):
    @marshal_with(wave_fields)
    def get(self):
        dt_max = datetime.datetime.utcnow()
        docs = WavesProvider().latest_list(dt_max)
        return list(docs)


class WeatherDoc(Resource):
    @marshal_with(weather_fields)
    def get(self, dt_value):
        provider = WeatherProvider()
        if dt_value == 'last':
            doc = provider.latest_one()
        else:
            doc = provider.latest_one(dt_value)
        if not doc:
            print("wave doc ko")
            return "error", 404
        print("wave doc dt :" + str(doc.get("datetime")))
        return doc


class WeatherList(Resource):
    @marshal_with(weather_fields)
    def get(self):
        dt_max = datetime.datetime.utcnow()
        docs = WeatherProvider().latest_list(dt_max)
        return list(docs)


api.add_resource(WaveDoc, '/surfchecks/wavereports/<string:dt_value>')
api.add_resource(WaveList, '/surfchecks/wavereports')
api.add_resource(WeatherDoc, '/surfchecks/weatherreports/<string:dt_value>')
api.add_resource(WeatherList, '/surfchecks/weatherreports')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
