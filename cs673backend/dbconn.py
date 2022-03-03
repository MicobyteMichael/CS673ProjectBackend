import os

import psycopg2
import psycopg2.extras

con = None

def connect():
	global con
	con = psycopg2.connect(os.environ["DATABASE_URL"], sslmode = "require")

def query(query, *args, as_dict = False):
	cur_params = {}
	
	if as_dict:
		cur_params["cursor_factory"] = psycopg2.extras.RealDictCursor
	
	cur = con.cursor(**cur_params)
	cur.execute(query, *args)
	
	try:
		res = cur.fetchall()
	except psycopg2.ProgrammingError:
		res = None
	
	if as_dict and res is not None:
		res = [dict(r) for r in res]
	
	cur.close()
	return res

def commit():
	con.commit()