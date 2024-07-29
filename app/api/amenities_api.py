from flask import Blueprint, jsonify, request
from models.amenity import Amenity
from persistence.datamanager import DataManager
from config import Config, db
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.login_api import admin_only

Session = sessionmaker(bind=Config.engine)
session = Session()

amenities_api = Blueprint("amenities_api", __name__)


@amenities_api.route("/amenities", methods=["POST"])
@jwt_required()
def add_amenity():
    """
    Function used to create a new amenity, send it to the database datamanager.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    amenity_data = request.get_json()
    if not amenity_data:
        return jsonify({"Error": "Problem during amenity creation."}), 400

    name = amenity_data.get("name")
    if not name:
        return jsonify({"Error": "Missing required field."}), 400

    new_amenity = Amenity()
    new_amenity.name = name
    if not new_amenity:
        return jsonify({"Error": "setting up new amenity"}), 500

    is_amenity_uniq = db.session.query(Amenity.id).filter_by(name=name).first()
    if is_amenity_uniq:
        return jsonify({"Error": "Amenity already exists."}), 409

    DataManager.save(new_amenity, db.session)
    db.session.refresh(new_amenity)
    return jsonify({"Success": "Amenity added",
                   "Amenity": DataManager.read(new_amenity)}), 201


@amenities_api.route("/amenities", methods=["GET"])
def read_all_amenities():
    """
    Function used to retrieve and read all amenities from the database.
    :Returns: jsonify + message + error/success code.
    """
    all_amenities = Amenity.query.all()
    if not all_amenities:
        return jsonify({"Error": "Amenity not found."}), 404
    return jsonify([DataManager.read(amenity) for amenity in all_amenities]), 201


@amenities_api.route("/amenities/<string:id>", methods=['GET'])
def read_one_amenity(id):
    """
    function used to retrieve and read a specific amenity from the database.
    :param id: UUID - Unique ID of the amenity.
    :Returns: jsonify + message + error/status code.
    """
    one_amenity = Amenity.query.filter_by(id=id)
    if not one_amenity:
        return jsonify({"Error": "Amenity not found."}), 404
    return jsonify([DataManager.read(amenity) for amenity in one_amenity])


@amenities_api.route("/amenities/<string:id>", methods=['PUT'])
@jwt_required()
def update_amenity(id):
    """
    Function used to update a specific amenity from the database.
    Admin only
    :param id: UUID - Unique ID of the amenity.
    :Returns: jsonify + message + error/status code.
    """
    current_user = get_jwt_identity()
    is_admin = admin_only()
    if not is_admin:
        return jsonify({"Error": "Admin only !"}), 401

    amenity = Amenity.query.get(id)
    if not amenity:
        return jsonify({'Error': 'Amenity not found'}), 404

    updates = request.get_json()
    if not updates:
        return jsonify({'Error': 'No update provided'}), 409

    DataManager.update(amenity, updates, db.session)
    db.session.refresh(amenity)
    return jsonify({"Success": "Amenity updated.",
                    "Amenity": DataManager.read(amenity)}), 201


@amenities_api.route("/amenities/<string:id>", methods=['DELETE'])
@jwt_required()
def delete_amenity(id):
    """
    Function used to delete a specific amenity from the database.
    Admin only
    :param id: UUID - ID of the amenity.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    is_admin = admin_only()
    if not is_admin:
        return jsonify({"Error": "Admin only !"}), 401

    amenity = Amenity.query.get(id)
    if not amenity:
        return jsonify({'Error': 'Amenity not found'}), 404
    DataManager.delete(amenity, db.session)
    return jsonify({'Success': 'Amenity deleted'}), 201
