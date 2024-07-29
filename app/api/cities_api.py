from flask import Blueprint, jsonify, request
from models.country import Country
from models.city import City
from persistence.datamanager import DataManager
from config import Config, db
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.login_api import admin_only

Session = sessionmaker(bind=Config.engine)
session = Session()

cities_api = Blueprint("cities_api", __name__)


@cities_api.route("/cities", methods=["POST"])
@jwt_required()
def create_cities():
    """
    Function used to create a new city, send it to the database datamanager.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    city_data = request.get_json()
    country_code = city_data.get('country_code')
    city_name = city_data.get('city_name')

    if not all([country_code, city_name]):
        return jsonify({"Error": "Missing required field."}), 400

    new_city = City(city_name=city_name, country_code=country_code)
    if not new_city:
        return jsonify({"Error": "setting up new user."}), 500

    is_city_uniq = \
        db.session.query(City.id).filter_by(city_name=city_name,
                                            country_code=country_code).first()
    if is_city_uniq:
        return jsonify({"Error": "City already exists in this country."}), 409

    DataManager.create(new_city, db.session)
    db.session.refresh(new_city)
    return jsonify({"Success": "City added."}), 201


@cities_api.route("/cities", methods=["GET"])
def read_all_cities():
    """
    Function used to read all cities from te database.
    :Returns: jsonify + message + error/success code.
    """
    all_cities = City.query.all()
    if not all_cities:
        return jsonify({"Error": "City not found."}), 404
    return jsonify([DataManager.read(city) for city in all_cities]), 201


@cities_api.route("/cities/<country_code>", methods=["GET"])
def read_one_cities(id):
    """
    Function used to retrieve one city from the database
    :param id: UUID - ID of the specific city.
    :Returns: jsonify + message + error/success code.
    """
    one_city = City.query.filter_by(id=id)
    if not one_city:
        return jsonify({"Error": "City not found."}), 404
    return jsonify([DataManager.read(city) for city in one_city])


@cities_api.route("/cities/<country_code>", methods=["PUT"])
@jwt_required()
def update_city(id):
    """
    Function used to update a specific city from the database.
    Admin only
    :param id: UUID - ID of the specific city.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    is_admin = admin_only()
    if not is_admin:
        return jsonify({"Error": "Admin only !"}), 401

    city = City.query.get(id)
    if not city:
        return jsonify({'Error': 'City not found'}), 404

    updates = request.get_json()
    if not updates:
        return jsonify({'Error': 'No update provided'}), 409

    DataManager.update(city, updates, db.session)
    db.session.refresh(city)
    return jsonify({"Success": "City updated.", "City": DataManager.read(city)}), 201


@cities_api.route("/cities/<country_code>", methods=["DELETE"])
@jwt_required()
def delete_city(id):
    """
    Function used to delete a specific city from the database.
    Admin only
    :param id: UUID - ID of the specific city.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    is_admin = admin_only()
    if not is_admin:
        return jsonify({"Error": "Admin only !"}), 401
    city = City.query.get(id)
    if not city:
        return jsonify({'Error': 'City not found'}), 404
    DataManager.delete(city, db.session)
    return jsonify({'Success': 'City deleted'}), 201
