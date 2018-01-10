from flask import Flask, jsonify, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)

class Music(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(40), nullable = False)
	artist = db.Column(db.String(40))
	album = db.Column(db.String(40))
	yt_url = db.Column(db.String(200))

	def __init__(self, title, artist, album, yt_url):
		self.title = title
		self.artist = artist
		self.album = album
		self.yt_url = yt_url

	def serialize(self):
		return {
			'id' : self.id,
			'title' : self.title,
			'artist' : self.artist,
			'album' : self.album,
			'yt_url' : self.yt_url
		}

db.create_all()
db.session.commit()

def format_string(str):
	return str.replace("_", " ").lower()

@app.route("/")
def home():
	return "hello flask"

@app.route("/search/", methods = ["GET"])
def search():
	all_music = db.session.query(Music).all()
	
	response = []
	for music in all_music:
		response.append(music.serialize())

	return jsonify(response)

@app.route("/search/title/<title_entered>/", methods = ["GET"])
def search_by_title(title_entered):

	title_entered = format_string(title_entered)

	all_music = db.session.query(Music).filter_by(title = title_entered).all()
	
	response = []
	for music in all_music:
		response.append(music.serialize())

	return jsonify(response)


@app.route("/search/artist/<artist_entered>/", methods = ["GET"])
def search_by_artist(artist_entered):

	artist_entered = format_string(artist_entered)

	all_music = db.session.query(Music).filter_by(artist = artist_entered).all()
	
	response = []
	for music in all_music:
		response.append(music.serialize())

	return jsonify(response)

@app.route("/search/album/<album_entered>/", methods = ["GET"])
def search_by_album(album_entered):

	album_entered = format_string(album_entered)

	all_music = db.session.query(Music).filter_by(album = album_entered).all()
	
	response = []
	for music in all_music:
		response.append(music.serialize())

	return jsonify(response)

@app.route("/add/", methods = ["GET", "POST"])
def add():
	if request.method == "POST":
		new_music = Music(request.form["title"], request.form["artist"], request.form["album"], request.form["yt_url"])
		db.session.add(new_music)
		db.session.commit()
		return redirect(url_for("search"))
	
	return ('<form action="/add/" method="POST"><label>Title </label><input name="title"><br><label>Artist </label><input name="artist"><br><label>Album </label><input name="album"><br><label>Youtube URL </label><input name="yt_url"><br><input type="submit" value="Add"></form>')



if __name__ == "__main__":
	app.run(debug = True)