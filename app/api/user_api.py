from flask import Blueprint, jsonify, request
from models.users import User
from persistence.datamanager import DataManager
from validate_email_address import validate_email
from config import Config, db
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.login_api import admin_only
Session = sessionmaker(bind=Config.engine)
session = Session()

user_api = Blueprint("user_api", __name__)


@user_api.route("/users", methods=["POST"])
def add_user():
    """
    Function used to create a new user and send it to the database.
    :Returns: jsonify + message + error/success code.
    """
    user_data = request.get_json()
    if not user_data:
        return jsonify({"Error": "Problem during user creation."}), 400

    email = user_data.get("email")
    password = user_data.get("password")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    if not all([email, first_name, last_name, password]):
        return jsonify({"Error": "Missing required field."}), 400
    if not all(c.isascii() for c in first_name) or not first_name.isalpha():
        return jsonify({"Error": "First name must contain only ascii characters."}), 400
    if not all(c.isascii() for c in last_name) or not first_name.isalpha():
        return jsonify({"Error": "Last name must contain only ascii characters."}), 400

    is_email_valid = validate_email(email)
    if not is_email_valid:
        return jsonify({"Error": "Email not valid"}), 400
    try:
        is_email_uniq = db.session.query(
            User.id).filter_by(email=email).first()
        if is_email_uniq:
            return jsonify({"Error": "User already exists"}), 409
    except FileNotFoundError:
        pass

    password_hash = User.set_password(password)
    if not password_hash:
        return jsonify({"Error": "Password not hashed"}), 500

    new_user = User(email=email, password_hash=password_hash,
                    first_name=first_name, last_name=last_name)
    if not new_user:
        return jsonify({"Error": "setting up new user"}), 500
    else:
        DataManager.save(new_user, db.session)
        db.session.refresh(new_user)
    return jsonify({"Success": "User added", 'User': DataManager.read(new_user)}), 201


@user_api.route("/users", methods=["GET"])
@jwt_required()
def read_all_users():
    """
    Function used to retrieve all users from the database.
    Admin only
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    is_admin = admin_only()
    if not is_admin:
        return jsonify({"Error": "Admin only !"}), 401
    all_users = User.query.all()
    return jsonify([DataManager.read(user) for user in all_users]), 201


@user_api.route("/users/<string:id>", methods=["GET"])
@jwt_required()
def get_one_user(id):
    """
    Function used to retrieve a specific user from the database.
    :param id: UUID - ID of this specific user.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    one_user = User.query.filter_by(id=id)
    return jsonify([DataManager.read(user) for user in one_user]), 201


@user_api.route("/users/<string:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    """
    Function used to update a specific user from the database.
    :param id: UUID - ID of this specific user.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    user = User.query.get(id)
    if not user:
        return jsonify({'Error': 'User not found'}), 404

    updates = request.get_json()
    if not updates:
        return jsonify({'Error': 'No update provided'}), 409

    updates_email = updates.get("email")
    if updates_email:
        existing_user = User.query.filter_by(email=updates_email).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({'Error': 'Email already in use'}), 409

    updates_f_name = updates.get("first_name")
    if not all(c.isascii() for c in updates_f_name) or not \
            updates_f_name.isalpha():
        return jsonify(
            {"Error": "First name must contain only ascii characters."}
), 409

    updates_l_name = updates.get("last_name")
    if not all(c.isascii() for c in updates_l_name) or not \
            updates_l_name.isalpha():
        return jsonify(
            {"Error": "Last name must contain only ascii characters."}
    ), 409

    updates_password = updates.get("password")
    if not updates_password:
        return ({"Errror": "Must have a password."}), 409
    password_hash = User.set_password(updates_password)
    if not password_hash:
        return jsonify({"Error": "Password not hashed"}), 500

    DataManager.update(user, updates, db.session)
    db.session.refresh(user)
    return jsonify({"Success": "User updated.", "User": DataManager.read(user)}), 201


@user_api.route("/users/<string:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    """
    Function used to delete a specific user from the database.
    :param id: UUID - ID of this user.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    user = User.query.get(id)
    if not user:
        return jsonify({'Error': 'User not found'}), 404
    DataManager.delete(user, db.session)
    return jsonify({'Success': 'User deleted'}), 201
