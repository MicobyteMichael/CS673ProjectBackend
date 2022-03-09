from .useraccounts import start as start_users

def start_api(flaskapp, db, api):
	start_users(flaskapp, db, api)