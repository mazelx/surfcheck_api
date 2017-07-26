from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

surfchecks = {
    "201707261600": {'yo': 'yooooo'},
    "201707261530": {'he': 'heeeee'},
}

class SurfCheck(Resource):
    def get(self, datetime):
	return {datetime: surfchecks[datetime]}

    def put(self, datetime):
	print("data : " + request.form['data'])
	surfchecks[datetime] = request.form['data']
	return {datetime: surfchecks[datetime]}


class SurfCheckList(Resource):
    def get(self):
        return surfchecks

api.add_resource(SurfCheck, '/surfcheck/<string:datetime>')
api.add_resource(SurfCheckList, '/surfchecks')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
