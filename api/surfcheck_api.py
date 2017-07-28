from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from pymongo import MongoClient
import datetime
import _strptime

app = Flask(__name__)
api = Api(app)

client = MongoClient()
db = client.surf_check
wave_data = db.wave_data

wave_fields = {
        "datetime": fields.DateTime(dt_format="iso8601"),
        "water_temperature": fields.String,
        "wave_direction": fields.String,
        "wave_height": fields.String,
        "wave_height_max": fields.String,
        "wave_period": fields.String,
        "wave_spreading": fields.String
}


class SurfCheck(Resource):
    @marshal_with(wave_fields, envelope='wave_data')
    def get(self, dt_value):
    if(dt_value == 'last'):
        return wave_data.find().sort([("datetime",0)]).limit(1)[0]
    dt_max = datetime.datetime.strptime(dt_value, '%Y%m%d%H%M')
    dt_min = dt_max - datetime.timedelta(minutes=30)
    doc = wave_data.find_one({"datetime": {"$lte":dt_max, "$gt": dt_min}},{"_id": 0})
    return doc

#    def put(self, datetime):
#    dt = datetime.strptime(datetime, '%Y%m%d%H%M')
#    surfchecks[datetime] = request.form['data']
#    return {datetime: surfchecks[datetime]}


class SurfCheckList(Resource):
    @marshal_with(wave_fields, envelope='wave_data')
    def get(self):
        dt_max = datetime.datetime.utcnow()
        dt_min = dt_max - datetime.timedelta(day=1)
        docs = wave_data.find({"datetime": {"$lte":dt_max, "$gt": dt_min}}).sort([("datetime",1)])
        return list(docs)

api.add_resource(SurfCheck, '/surfchecks/<string:dt_value>')
api.add_resource(SurfCheckList, '/surfchecks')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=5001)
