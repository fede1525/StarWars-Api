
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, People, Planets, Users, Favorites

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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people/', methods=['GET'])
def get_characters():
    people = People.query.all
    people_data = [person.serialize() for person in people]
    response_body = {
        "people": people_data
    }
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_character(people_id):
    character = People.query.get(people_id)
    if character is None:
        raise APIException("Character not found", status_code=404)
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets_data = [planet.serialize() for planet in planets]
    response_body = {
        "planets": planets_data
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        raise APIException("Character not found", status_code=404)
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    users_data = [user.serialize() for user in users]
    response_body = {
        "users": users_data
    }
    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites(user_id):
    user = Users.query.get(user_id)

    if user is None:
        raise APIException("User not found", status_code = 404)
    
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    favorites_data = [favorite.serialize() for favorite in favorites]
    response_body = {
        "user_id": user_id,
        "favorites": favorites_data
    }
    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['POST'])
def add_favorite():
    request_data = request.get_json()

    if "user_id" not in request_data or "favorite_data" not in request_data:
        raise APIException("Invalid request data.", status_code=400)

    user_id = request_data["user_id"]
    favorite_data = request_data["favorites"]

    user = Users.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)

    new_favorite = Favorites(user_id=user_id, favorite_data=favorite_data)
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "message": "Favorite load succesfull",
        "user_id": user_id,
        "favorite_data": favorite_data
    }

    return jsonify(response_body), 201


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
