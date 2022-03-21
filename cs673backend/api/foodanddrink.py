from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

def start(flaskapp, db, api):
	class Waters(db.Model):
		userid  = db.Column(db.Integer, primary_key = True)
		year    = db.Column(db.Integer, primary_key = True)
		day     = db.Column(db.Integer, primary_key = True)
		glasses = db.Column(db.Integer, nullable = False)
	
	class Meals(db.Model):
		userid   = db.Column(db.Integer, primary_key = True)
		year     = db.Column(db.Integer, primary_key = True)
		day      = db.Column(db.Integer, primary_key = True)
		meal     = db.Column(db.String,  primary_key = True)
		calories = db.Column(db.Integer, nullable = False)
	
	class WaterGlasses(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("year", type = int, required = True)
			self.parser.add_argument("day",  type = int, required = True)
			
			self.parser2 = RequestParser()
			self.parser2.add_argument("glasses", type = int, required = True)
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			
			if "userid" in session:
				water = Waters.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"]).first()
				glasses = 0
				
				if water is not None:
					glasses = water.glasses
				
				return { "glasses": glasses }
			else:
				return { "error": "Not signed in" }
		
		def put(self):
			args = self.parser.parse_args() | self.parser2.parse_args()
			
			if "userid" in session:
				water = Waters.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"]).first()
				if water is None:
					water = Waters(userid = session["userid"], year = args["year"], day = args["day"], glasses = 0)
					db.session.add(water)
				
				water.glasses = args["glasses"]
				db.session.commit()
				
				return { "updated": True }
			else:
				return { "error": "Not signed in" }
	
	class MealsEaten(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("year", type = int, required = True)
			self.parser.add_argument("day",  type = int, required = True)
			
			self.parser2 = RequestParser()
			self.parser2.add_argument("mealname", type = str, required = True)
			self.parser2.add_argument("calories", type = int, required = True)
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			
			if "userid" in session:
				meals = (Meals.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"]).all()) or []
				meals_data = [ { "meal": meal.meal, "calories": meal.calories } for meal in meals ]
				
				return { "meals": meals_data }
			else:
				return { "error": "Not signed in" }
		
		def put(self):
			args = self.parser.parse_args() | self.parser2.parse_args()
			
			if "userid" in session:
				existing_meal = Meals.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"], meal = args["mealname"]).first()
				if existing_meal is not None:
					return { "error": "A meal with that name is already added" }
				
				db.session.add(Meals(userid = session["userid"], year = args["year"], day = args["day"], meal = args["mealname"], calories = args["calories"]))
				db.session.commit()
				
				return { "added": True }
			else:
				return { "error": "Not signed in" }
	
	api.add_resource(WaterGlasses, "/waterintake")
	api.add_resource(MealsEaten,   "/mealintake")