from . import startup

if __name__ == "__main__":
	flaskapp = startup()
	flaskapp.run(threaded = True)