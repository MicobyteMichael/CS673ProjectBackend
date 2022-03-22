from .authentication  import start as start_authen
from .accountsettings import start as start_settings
from .foodanddrink    import start as start_food
from .sleeptracking   import start as start_sleep
from .bodycomposition import start as start_bodycomp
from .steptracking    import start as start_steps
from .exercise        import start as start_exercise
from .goalsystem      import start as start_goals

def start_api(flaskapp, db, api):
	class UserAccount(db.Model):
		id		= db.Column(db.Integer, primary_key = True)
		username= db.Column(db.String, unique = True, nullable = False)
		email	= db.Column(db.String, unique = True, nullable = False)
		phone	= db.Column(db.String, unique = True, nullable = False)
		passhash= db.Column(db.String, nullable = False)
		salt	= db.Column(db.String, nullable = False)
	
	start_authen  (flaskapp, db, api, UserAccount)
	start_settings(flaskapp, db, api, UserAccount)
	start_food    (flaskapp, db, api)
	start_sleep   (flaskapp, db, api)
	start_bodycomp(flaskapp, db, api)
	start_steps   (flaskapp, db, api)
	start_exercise(flaskapp, db, api)
	start_goals   (flaskapp, db, api)