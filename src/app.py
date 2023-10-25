"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# <------

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


# <======== Get All Data functions =========>


# Get a list of all users
@app.route('/user', methods=['GET'])
def all_users():

    user = User.query.all()
    user_serialize = list(map(lambda x: x.serialize(), user))

    return jsonify({'msg': 'ok', 'info': user_serialize})

# Get a list of all the people in the database


@app.route('/people', methods=['GET'])
def all_people():

    people = People.query.all()
    people_serialize = list(map(lambda x: x.serialize(), people))
    return jsonify({'msg': 'ok', 'info': people_serialize})

# Get a list of all the planets in the database


@app.route('/planets', methods=['GET'])
def all_planets():

    planets = Planets.query.all()
    planets_serialize = list(map(lambda x: x.serialize(), planets))
    return jsonify({'msg': 'ok', 'info': planets_serialize})


# <======== Get Single Data functions ==========>


# Get a one single people information
@app.route('/people/<int:people_id>', methods=['GET'])
def single_people(people_id):

    people = People.query.get(people_id)

    if people is None:
        return jsonify({'error': 'The person with id {} does not exist'.format(people_id)}), 400
    people_serialize = people.serialize()
    return jsonify({'msg': 'ok', 'info': people_serialize}), 200


# Get one single planet information
@app.route('/planets/<int:planet_id>', methods=['GET'])
def single_planet(planet_id):

    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({'error': 'The planet with id {} does not exist'.format(planet_id)}), 400
    planet_serialize = planet.serialize()
    return jsonify({'msg': 'ok', 'info': planet_serialize}), 200


# <======== Favorite functions ==========>

# Get all the favorites that belong to the current user
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def current_user_favorites(user_id):
    user = User.query.filter_by(id=user_id).first()
    user = user.serialize()
    favorites = {
        "favorite_planets": [],
        "favorite_people": []
    }
    for favorite_planet in user.favorite_planets:
        favorites.favorite_planets.append(favorite_planet)

    for favorite_people in user.favorite_people:
        favorites.favorite_people.append(favorite_people)

    return jsonify(favorites), 200


# Add a new favorite planet to the current user with the planet id = planet_id.
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_new_planet_favorite(planet_id):
    body = request.json
    user = User.query.filter_by(id=body["user_id"]).first()
    planet = Planets.query.filter_by(id=planet_id).first()

    if user is None:
        return "User not found", 404
    if planet is None:
        return "Planet not found", 404
    if user.favorite_planets is None:
        user.favorite_planets = []
    user.favorite_planets.append(planet)  # adds new favorite planet
    db.session.commit()
    payload = {
        "message": "Congrats, favorite planet has been saved!",
        "user": user.serialize()
    }

    return jsonify(payload)

# Add new favorite people to the current user with the people id = people_id.


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_new_people_favorite(people_id):
    body = request.json
    user = User.query.filter_by(id=body["user_id"]).first()
    people = People.query.filter_by(id=people_id).first()

    if user is None:
        return "User not found", 404
    if people is None:
        return "Person not found", 404
    if user.favorite_people is None:
        user.favorite_people = []
    user.favorite_people.append(people)  # adds new favorite person
    db.session.commit()

    payload = {
        "message": "Congrats, favorite person has been saved!",
        "user": user.serialize()
    }

    return jsonify(payload)


# <======== DELETE Data functions ==========>

# Delete favorite planet with the id = planet_id.
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    data = request.json
    user = User.query.filter_by(id=data["user_id"]).first()
    planet = Planets.query.filter_by(id=planet_id).first()
    if user is None:
        return "User not found", 404
    if planet is None:
        return "This planet does not exist", 404
    if planet not in user.favorite_planets:
        return "This planet is not in your favorite planets list", 404
    for x in user.favorite_planets:  # for any item in user.favorite_planets if the item is equal to planet provided then we remove it from user.favorite_planets
        if x == planet:
            user.favorite_planets.remove(planet)
    db.session.commit()

    payload = {
        "message": "Congrats, favorite planet has been deleted!",
        "user": user.serialize()
    }

    return jsonify(payload), 200

# Delete favorite people with the id = people_id.


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    data = request.json
    user = User.query.filter_by(id=data["user_id"]).first()
    people = People.query.filter_by(id=people_id).first()
    if user is None:
        return "User not found", 404
    if people is None:
        return "This person does not exist", 404
    if people not in user.favorite_people:
        return "This person is not in your favorite people list", 404
    for x in user.favorite_people:  # for any item in user.favorite_people if the item is equal to people provided then we remove it from user.favorite_people
        if x == people:
            user.favorite_people.remove(people)
    db.session.commit()

    payload = {
        "message": "Congrats, favorite person has been deleted!",
        "user": user.serialize()
    }

    return jsonify(payload), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
