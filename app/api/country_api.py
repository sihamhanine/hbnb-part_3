from flask import Blueprint, jsonify, request
from models.country import Country
from models.city import City
from persistence.datamanager import DataManager
from config import Config, db
from sqlalchemy.orm import sessionmaker
import pycountry
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.login_api import admin_only

Session = sessionmaker(bind=Config.engine)
session = Session()

country_api = Blueprint("country_api", __name__)


@country_api.route("/countries", methods=["POST"])
@jwt_required()
def country():
    """
    Function used to retrieve a new country from Pycountry
    and send it to the database via DataManager.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    is_admin = admin_only()
    if not is_admin:
        return jsonify({"Error": "Admin only !"}), 401
    country_data = request.get_json()
    country_name = country_data.get("name")
    country_code = country_data.get("code")

    pycountry_country = None
    for country in pycountry.countries:
        if country.alpha_2 == country_code:
            pycountry_country = country
            break
    if not pycountry_country or pycountry_country.name != country_name:
        return jsonify({"Error": "Country must exist in pycountry."}), 409

    existing_country = Country.query.filter_by(code=country_code).first()
    if existing_country:
        return jsonify({"Error": "Country already exists in database."}), 409

    new_country = Country(name=country_name, code=country_code)
    try:
        DataManager.save(new_country, db.session)
        return jsonify({"Success": "Country added.", "country": DataManager.read(new_country)}), 201
    except Exception as e:
        db.session.rollback()
        raise e


@country_api.route("/countries", methods=["GET"])
@jwt_required()
def read_countries_from_pycountry():
    """
    Function that retrieves and reads countries from Pycountry.
    :Returns: jsonify + message + error/success code.
    """
    countries = [{"name": country.name, "code": country.alpha_2}
                 for country in pycountry.countries]
    return jsonify(countries), 200


@country_api.route("/countries/<country_code>", methods=["GET"])
@jwt_required()
def get_country(country_code):
    """
    Function used to retrieve details of a specific country from pycountry.
    :param country_code: alpha code of a specific country.
    :Returns: jsonify + message + error/success code.
    """
    country = pycountry.countries.get(alpha_2=country_code.upper())
    if not country:
        return jsonify({"Error": "Country not found."}), 404

    country_details = {"name": country.name, "code": country.alpha_2}
    return jsonify({"Country": country_details}), 201


@country_api.route("/countries/<country_code>/cities", methods=["GET"])
@jwt_required()
def get_country_cities(country_code):
    """
    Function used to retrieve all cities belonging to a specific country*
    :param country_code: alpha code of a specific country.
    :Returns: jsonify + message + error/success code.
    """
    country = pycountry.countries.get(alpha_2=country_code.upper())
    if not country:
        return jsonify({"Error": "Country not found"}), 404

    cities = City.query.filter_by(country_code=country.alpha_2).all()
    if not cities:
        return jsonify({"error": "No cities found for this country."}), 404

    return jsonify({'Cities':
                    [DataManager.read(city) for city in cities]}), 200
