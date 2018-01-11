# Standard Imports for a Flask Application
from flask import Flask, jsonify

# Create a Flask App object
app = Flask(__name__)

# Home route
# Method : GET
# This route is to test if Flask is working properly
@app.route("/")
def home():
	return "Hello Flask"

# Simple get request using flask
@app.route("/print/<string>", methods = ["GET"])
def printer(string):
	response ={}
	response['string'] = string
	return jsonify(response)
	


# Start App
if __name__ == "__main__":
	app.run()
