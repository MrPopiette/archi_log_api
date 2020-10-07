from flask import Flask, render_template, flash, request, redirect, url_for, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import haversine as hs
import requests
import json


# create the object of Flask
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'hardsecretkey'


# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flaskapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


# our model
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float(6))
    longitude = db.Column(db.Float(6))

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


# creating our routes
@app.route('/')
def index():
    return "<h1>API works</h1><p>Bon ça part de là</p>"


# home route test
@app.route('/home', methods=['GET', 'POST'])
def Home():
    return "<h1>Home page</h1><p>Direction les calculs</p>"


# distance route test
@app.route('/distance', methods=['GET', 'POST'])
def Distance():
    resp = requests.get('https://run.mocky.io/v3/eaf95a7c-3ff2-4d4b-ac6a-6e3341c1fee8')
    user = UserInfo(float(request.args.get('latitude')), float(request.args.get('longitude')))
    distance = {}
    truck = {}
    compteur = 0
    userLoc = (user.latitude, user.longitude)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET / {}'.format(resp.status_code))
    for todo_item in resp.json():
        print('{} {} {}'.format(todo_item['id'], todo_item['latitude'], todo_item['longitude']))
        loc=(todo_item['latitude'], todo_item['longitude'])
        truck = [{
            "id_truck" : todo_item['id'],
            "url": todo_item['url'],
            "distance": hs.haversine(loc,userLoc)
        }]
        distance[compteur] = truck
        compteur = compteur + 1

    return jsonify(distance)

# run flask app
if __name__ == "__main__":
    app.run(debug=True)
