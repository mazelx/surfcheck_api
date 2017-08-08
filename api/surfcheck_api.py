from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with
from pymongo import MongoClient
import datetime
import os
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
cors = CORS(app)


client = MongoClient(os.environ['MONGODB_URI'])
db = client.surf_check
wave_data = db.wave_data
weather_data = db.weather_data

wave_fields = {"datetime": fields.DateTime(dt_format="iso8601"),
               "water_temperature": fields.String,
               "wave_direction": fields.String,
               "wave_height": fields.String,
               "wave_height_max": fields.String,
               "wave_period": fields.String,
               "wave_spreading": fields.String
               }


class SurfCheck(Resource):
    @marshal_with(wave_fields)
    def get(self, dt_value):
        if(dt_value == 'last'):
            return wave_data.find({}).sort("datetime", 1).limit(1)[0]
        wave_dt_max = datetime.datetime.strptime(dt_value, '%Y%m%d%H%M')
        wave_dt_min = wave_dt_max - datetime.timedelta(minutes=30)
        wave_doc = wave_data.find_one({"datetime": {"$lte": wave_dt_max, "$gt": wave_dt_min}}, {"_id": 0})
        if(not wave_doc):
            print("wave doc ko")
            return "error", 404
        print("wave doc dt :" + str(wave_doc.get("datetime")))
        weather_dt_max = wave_doc.get("datetime") + datetime.timedelta(minutes=15)
        weather_dt_min = wave_doc.get("datetime") - datetime.timedelta(minutes=15)
        weather_doc = weather_data.find_one({"datetime":
                                            {"$lte": weather_dt_max, "$gt": weather_dt_min}},
                                            {"datetime": 0})
        if(not weather_doc):
            print("weather doc ko")
            return "error", 404
        print("wearther doc : " + str(weather_doc))
        doc = wave_doc.copy()
        doc.update(weather_doc)
        doc = wave_doc
        return doc

#    def put(self, datetime):
#    dt = datetime.strptime(datetime, '%Y%m%d%H%M')
#    surfchecks[datetime] = request.form['data']
#    return {datetime: surfchecks[datetime]}


class SurfCheckList(Resource):
    @marshal_with(wave_fields)
    def get(self):
        dt_max = datetime.datetime.utcnow()
        dt_min = dt_max - datetime.timedelta(hours=49)
        wave_docs = wave_data.find({"datetime": {"$lte": dt_max, "$gt": dt_min}}).sort([("datetime", 1)])
        # weather_docs = wave
        return list(wave_docs)


api.add_resource(SurfCheck, '/surfchecks/<string:dt_value>')
api.add_resource(SurfCheckList, '/surfchecks')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
