from flask import Blueprint, jsonify, request
from models.place import Place
from persistence.datamanager import DataManager
from config import Config, db
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import jwt_required, get_jwt_identity

Session = sessionmaker(bind=Config.engine)
session = Session()

place_api = Blueprint("place_api", __name__)


@place_api.route("/places", methods=["POST"])
@jwt_required()
def create_place():
    """
    Function used to create a new place, send it to the database datamanager.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    place_data = request.get_json()
    if not place_data:
        return jsonify({"Error": "Problem during place creation"})

    name = place_data.get("name")
    description = place_data.get("description")
    address = place_data.get("address")
    latitude = place_data.get("latitude")
    longitude = place_data.get("longitude")
    num_rooms = place_data.get("num_rooms")
    num_bathrooms = place_data.get("num_bathrooms")
    price_per_night = place_data.get("price_per_night")
    max_guests = place_data.get("max_guests")
    host_id = place_data.get("host_id")
    amenity_ids = place_data.get("amenity_ids")
    city_id = place_data.get("city_id")

    if not all([name, description, address, latitude, longitude,
                num_rooms, num_bathrooms, price_per_night, max_guests,
                city_id, host_id]):
        return jsonify({"Error": "Missing required field."}), 400

    if not (isinstance(arg, str)
            for arg in (name, description, address)):
        raise TypeError({"Error": "TypeError"})
    if not (isinstance(arg, int)
            for arg in (num_bathrooms, num_rooms, max_guests)):
        raise TypeError({"Error": "TypeError"})
    if not (isinstance(arg, (float, int))
            for arg in (latitude, longitude, price_per_night)):
        raise TypeError({"Error": "TypeError"})

    new_place = Place()
    new_place.name = name
    new_place.description = description
    new_place.address = address
    new_place.city_id = city_id
    new_place.latitude = latitude
    new_place.longitude = longitude
    new_place.host_id = host_id
    new_place.num_rooms = num_rooms
    new_place.num_bathrooms = num_bathrooms
    new_place.price_per_night = price_per_night
    new_place.max_guests = max_guests
    new_place.amenity_ids = amenity_ids

    if not new_place:
        return jsonify({"Error": "setting up new place"}), 500

    DataManager.save(new_place, db.session)
    db.session.refresh(new_place)
    return jsonify({"Success": "Place added"}, DataManager.read(new_place)), 201


@place_api.route("/places", methods=["GET"])
def read_all_places():
    """
    Function used to retrieve and read all places, from the database.
    :Returns: jsonify + message + error/success code.
    """
    all_places = Place.query.all()
    if not all_places:
        return jsonify({"Error": "Place not found."}), 404
    return jsonify([DataManager.read(place) for place in all_places])


@place_api.route("/places/<string:id>", methods=['GET'])
def read_one_place(id):
    """
    Function used to retrieve and read a specific place, from the database.
    :param id: UUID - ID of a specific place
    :Returns: jsonify + message + error/success code.
    """
    one_place = Place.query.filter_by(id=id)
    if not one_place:
        return jsonify({"Error": "Place not found."}), 404
    return jsonify([DataManager.read(place) for place in one_place])


@place_api.route("/places/<string:id>", methods=['PUT'])
@jwt_required()
def update_place(id):
    """
    Function used to update a specific place, from the database.
    Admin or owner only
    :param id: UUID - ID of a specific place
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    place = Place.query.get(id)
    if not place:
        return jsonify({'Error': 'Place not found'}), 404

    updates = request.get_json()
    if not updates:
        return jsonify({'Error': 'No update provided'}), 409

    DataManager.update(place, updates, db.session)
    db.session.refresh(place)
    return jsonify({"Success": "Place updated.",
                    "Place": DataManager.read(place)}), 201


@place_api.route("/places/<string:id>", methods=['DELETE'])
@jwt_required()
def delete_place(id):
    """
    Function used to delete a specific place, from the database.
    Admin or owner only
    :param id: UUID - ID of a specific place
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    place = Place.query.get(id)
    if not place:
        return jsonify({'Error': 'Place not found'}), 404
    DataManager.delete(place, db.session)
    return jsonify({'Success': 'Place deleted'}), 201
