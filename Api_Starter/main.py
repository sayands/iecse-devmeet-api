# Standard Imports for a Flask Application
from flask import Flask, jsonify, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os

# Create a Flask App object
app = Flask(__name__)

# Configuration SQLAlchemy Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

# Create Database Object
db = SQLAlchemy(app)

# Declare the Model for the Database
class Music(db.Model):
	# Variable declarations
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(40), nullable = False)
	artist = db.Column(db.String(40))
	album = db.Column(db.String(40))
	yt_url = db.Column(db.String(200))

	# Inilialse the variables with values recieved in the API request
	def __init__(self, title, artist, album, yt_url):
		self.title = title
		self.artist = artist
		self.album = album
		self.yt_url = yt_url

	# Return a JSON object of the variables
	def serialize(self):
		return {
			'id' : self.id,
			'artist' : self.artist,
			'title' : self.title,
			'album' : self.album,
			'yt_url' : self.yt_url
		}

# Create the database and commit
db.create_all()
db.session.commit()

#
def format_string(str):
	return str.replace("_", " ").lower()


# Home route
# Method : GET
# This route is to test if Flask is working properly
@app.route("/")
def home():
	return "Hello Flask"


# Search All Music
# Method : GET
# This route should return a JSON Object with all the songs in the database
@app.route("/search/", methods = ["GET"])


# Search By Title
# Method : GET
# This route should return a JSON Object of the songs matching the title
@app.route("/search/title/<title_entered>/", methods = ["GET"])


# Search By Artist
# Method : GET
# This route should return a JSON Object of all the songs by a particular artist
@app.route("/search/artist/<artist_entered>/", methods = ["GET"])


# Search By Album
# Method : GET
# This route should return a JSON Object of all the songs from a particular album
@app.route("/search/album/<album_entered>/", methods = ["GET"])


# Add New Song To Database
# Method : GET , POST
# GET : This route should return a form to add a new song to the Database
# POST : This route should add the new song to the Database
@app.route("/add/", methods = ["GET", "POST"])



# Start App
if __name__ == "__main__":
	app.run()
