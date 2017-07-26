from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from pymongo import MongoClient
import datetime
import _strptime

app = Flask(__name__)
api = Api(app)

surfchecks = {
    "201707261600": {'yo': 'yooooo'},
    "201707261530": {'he': 'heeeee'},
}


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
	dt_max = datetime.datetime.strptime(dt_value, '%Y%m%d%H%M')
	dt_min = dt_max - datetime.timedelta(minutes=30)
	doc = wave_data.find_one({"datetime": {"$lte":dt_max, "$gt": dt_min}},{"_id": 0})
	return doc

#    def put(self, datetime):
#	dt = datetime.strptime(datetime, '%Y%m%d%H%M')
#	surfchecks[datetime] = request.form['data']
#	return {datetime: surfchecks[datetime]}


class SurfCheckList(Resource):
    @marshal_with(wave_fields, envelope='wave_data')
    def get(self):
 	return list(wave_data.find().sort([("datetime",0)]).limit(100))

api.add_resource(SurfCheck, '/surfcheck/<string:dt_value>')
api.add_resource(SurfCheckList, '/surfchecks')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
