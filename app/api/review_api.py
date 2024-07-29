from flask import Blueprint, jsonify, request
from models.review import Review
from models.place import Place
from models.users import User
from persistence.datamanager import DataManager
from config import Config, db
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import jwt_required, get_jwt_identity

Session = sessionmaker(bind=Config.engine)
session = Session()

review_api = Blueprint("review_api", __name__)


@review_api.route("/places/<string:id>/reviews", methods=["POST"])
@jwt_required()
def create_review(id):
    """
    Function used to create reviews of a place and send them to the database.
    :param id: UUID - id of the place.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    place_id = id
    review_data = request.get_json()
    if not review_data:
        return jsonify({"Error": "Problem during review creation"}), 400

    rating = review_data.get("rating")
    if not isinstance(rating, int):
        return jsonify({"Error": "rating must be an integer."}), 400
    if not 1 <= rating <= 5:
        return jsonify({"Error":
                        "rating must be included between 1 and 5."}), 400

    comment = review_data.get("comment")
    if not isinstance(comment, str):
        return jsonify({"Error": "comment must be a string."}), 400

    user_id = review_data.get("user_id")
    if not all(rating, comment, user_id, place_id):
        return jsonify({"Error": "Missing recquired field."}), 409

    is_host = \
        db.session.query(Place.id).filter_by(host_id=Place.host_id).first()
    if is_host == user_id:
        return jsonify({"Error": "You cannot review your own place."}), 400

    existing_review = db.session.query(Review)\
        .filter_by(user_id=user_id, place_id=place_id).first()
    if existing_review:
        return jsonify({"Error": "You cannot review a place twice."}), 400

    new_review = Review()
    new_review.rating = rating
    new_review.comment = comment
    new_review.user_id = user_id
    new_review.place_id = place_id

    if not new_review:
        return jsonify({"Error": "creating a new review."}), 400

    DataManager.save(new_review, db.session)
    db.session.refresh(new_review)
    return jsonify({"Success": "Review added",
                    "review": DataManager.read(new_review)}), 201


@review_api.route("/users/<string:id>/reviews", methods=['GET'])
@jwt_required()
def user_review(id):
    """
    Function used to retrieve reviews posted by a user from the database.
    :param id: UUID - id of the place.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    those_reviews = db.session.query(Review.id).filter_by(id=id)
    if not those_reviews:
        return jsonify({"Error": "Review not found."}), 404
    return jsonify({"Reviews": DataManager.read(review)
                    for review in those_reviews}), 201


@review_api.route("/reviews/<string:id>", methods=['GET'])
@jwt_required()
def read_one_review(id):
    """
    Function used to retrieve and read a specific review, from the database.
    :param id: UUID - id of the review.
    :Returns: jsonify + message + error/success code.
    """
    one_review = Review.query.filter_by(id=id)
    if not one_review:
        return jsonify({"Error": "Review not found."}), 404
    return jsonify([DataManager.read(review) for review in one_review]), 201


@review_api.route("/reviews/<string:id>", methods=['PUT'])
@jwt_required()
def update_review(id):
    """
    Function used to update a specific review, from the database.
    :param id: UUID - id of the review.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    review = Review.query.get(id)
    if not review:
        return jsonify({'Error': 'Review not found'}), 404

    updates = request.get_json()
    if not updates:
        return jsonify({'Error': 'No update provided'}), 409

    DataManager.update(review, updates, db.session)
    db.session.refresh(review)
    return jsonify({"Success": "Review updated.",
                    "Place": DataManager.read(review)}), 201


@review_api.route("/reviews/<string:id>", methods=['DELETE'])
@jwt_required()
def delete_review(id):
    """
    Function used to delete a specific review, from the database.
    :param id: UUID - id of the review.
    :Returns: jsonify + message + error/success code.
    """
    current_user = get_jwt_identity()
    review = Review.query.get(id)
    if not review:
        return jsonify({'Error': 'Review not found'}), 404
    DataManager.delete(review, db.session)
    return jsonify({'Success': 'Review deleted'}), 201
