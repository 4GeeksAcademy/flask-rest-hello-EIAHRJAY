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
from models import db, User,Planet, People,Favorites_Planet,Favorites_People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

def get_current_user_id():
    return 1  # ID del usuario para pruebas

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def user():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    return jsonify(planet.serialize()), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        raise APIException('Person not found', status_code=404)
    return jsonify(person.serialize()), 200

@app.route('/users/favorites', methods=["GET"])
def get_list_favorites():
    user_id = get_current_user_id()
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"info": "Not found"}), 404
    response = user.serialize()
    response["favorites"] = list(
        map(lambda planet: planet.serialize(), user.favorites_planets)) + list(
        map(lambda people: people.serialize(), user.favorites_people))
    return jsonify(response), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    people = People.query.get(people_id)
    if people is None:
        return jsonify({"message": "People not found"}), 404
    user_id = get_current_user_id()
    favorites = Favorites_People(user_id=user_id, people_id=people_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify({"message": "People added to favorite"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404
    user_id = get_current_user_id()
    favorites = Favorites_Planet(user_id=user_id, planet_id=planet_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify({"message": "Planet added to favorite"}), 200

@app.route('/favorite/people/<int:id>', methods=['DELETE'])
def delete_favorite_people(id):
    favorite_people = Favorites_People.query.get(id)
    if favorite_people is None:
        return jsonify({"message": "Favorite People not found"}), 404
    favorite = Favorites_People.query.filter_by(user_id=get_current_user_id(), id=id).first()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite People deleted from favorites"}), 200

@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_favorite_planet(id):
    favorite_planet = Favorites_Planet.query.get(id)
    if favorite_planet is None:
        return jsonify({"message": "Favorite Planet not found"}), 404
    favorite = Favorites_Planet.query.filter_by(user_id=get_current_user_id(), id=id).first()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite Planet deleted from favorites"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)