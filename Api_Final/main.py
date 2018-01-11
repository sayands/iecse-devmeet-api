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
# This route returns a JSON Object with all the songs in the database
@app.route("/search/", methods = ["GET"])
def search():
	all_music = db.session.query(Music).all()

	# Response is a Python dictionary ( Key - Value Pair)
	response = {}
	# response_data is an array. This will
	# contain the JSON objects for every song that matches our database query
	response_data = []

	for music in all_music:
		# append is a python function that adds a new element
		# to the end of an array
		response_data.append(music.serialize())

	# len(response_data) returns the length of the response_data array
	# if this length is zero, there were no matches found in the database
	if len(response_data) == 0:
		response['success'] = False
		response['message'] = "No Songs Found"
	else:
		response['success'] = True
		response['data'] = response_data

	# jsonify function creates a JSON object from the dictionary before returning the data to the browser
	return jsonify(response)

# Search By Title
# Method : GET
# Returns a JSON Object of the songs matching the title
@app.route("/search/title/<title_entered>/", methods = ["GET"])
def search_by_title(title_entered):

	title_entered = format_string(title_entered)

	all_music = db.session.query(Music).filter_by(title = title_entered).all()

	response = {}
	response_data = []

	for music in all_music:
		response_data.append(music.serialize())

	if len(response_data) == 0:
		response['success'] = False
		response['message'] = "No Songs Found"
	else:
		response['success'] = True
		response['data'] = response_data

	return jsonify(response)

# Search By Artist
# Method : GET
# Returns a JSON Object of all the songs by a particular artist
@app.route("/search/artist/<artist_entered>/", methods = ["GET"])
def search_by_artist(artist_entered):

	artist_entered = format_string(artist_entered)

	all_music = db.session.query(Music).filter_by(artist = artist_entered).all()

	response = {}
	response_data = []

	for music in all_music:
		response_data.append(music.serialize())

	if len(response_data) == 0:
		response['success'] = False
		response['message'] = "No Songs Found"
	else:
		response['success'] = True
		response['data'] = response_data

	return jsonify(response)

# Search By Album
# Method : GET
# Returns a JSON Object of all the songs from a particular album
@app.route("/search/album/<album_entered>/", methods = ["GET"])
def search_by_album(album_entered):

	album_entered = format_string(album_entered)

	all_music = db.session.query(Music).filter_by(album = album_entered).all()

	response = {}
	response_data = []

	for music in all_music:
		response_data.append(music.serialize())

	if len(response_data) == 0:
		response['success'] = False
		response['message'] = "No Songs Found"
	else:
		response['success'] = True
		response['data'] = response_data

	return jsonify(response)

# Add New Song To Database
# Method : GET , POST
# GET : Returns a form to add a new song to the Database
# POST : Adds the new song to the Database
@app.route("/add/", methods = ["GET", "POST"])
def add():
	# request.method contains a string to indicate the type of request that was sent
	if request.method == "POST":
		new_music = Music(request.form["title"], request.form["artist"], request.form["album"], request.form["yt_url"])
		db.session.add(new_music)
		db.session.commit()
		return redirect(url_for("search"))

	return ('<form action="/add/" method="POST"><label>Title </label><input name="title"><br><label>Artist </label><input name="artist"><br><label>Album </label><input name="album"><br><label>Youtube URL </label><input name="yt_url"><br><input type="submit" value="Add"></form>')

# Start App
if __name__ == "__main__":
	app.run()
