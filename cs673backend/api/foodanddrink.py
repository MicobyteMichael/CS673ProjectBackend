from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

def start(flaskapp, db, api):
	class Waters(db.Model):
		userid  = db.Column(db.Integer, primary_key = True)
		year    = db.Column(db.Integer, primary_key = True)
		day     = db.Column(db.Integer, primary_key = True)
		glasses = db.Column(db.Integer, nullable = False)
	
	class WaterGlasses(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("year", type = int)
			self.parser.add_argument("day", type = int)
			
			self.parser2 = RequestParser()
			self.parser2.add_argument("glasses", type = int)
		
		def post():
			args = self.parser.parse_args(strict = True)
			
			if "userid" in session:
				water = Waters.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"]).first()
				glasses = 0
				
				if water is not None:
					glasses = water.glasses
				
				return { "glasses": glasses }
			else:
				return { "error": "Not signed in" }
	
	api.add_resource(WaterGlasses, "/waterintake")