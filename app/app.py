import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from config import *
from dotenv import load_dotenv

load_dotenv()
host = os.environ.get('HOST')
port = int(os.environ.get('PORT', 5000))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def unauthorized_response(callback): return jsonify(
        {'Error': 'Missing Authorization Header'}), 401

    # Add swagger documentation
    CORS(app, resources={r"/*": {"origins": "http://localhost"}})
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test application"
        },
    )

    # register blueprint routes
    app.register_blueprint(swaggerui_blueprint)
    from api.amenities_api import amenities_api
    app.register_blueprint(amenities_api)
    from api.cities_api import cities_api
    app.register_blueprint(cities_api)
    from api.country_api import country_api
    app.register_blueprint(country_api)
    from api.place_api import place_api
    app.register_blueprint(place_api)
    from api.review_api import review_api
    app.register_blueprint(review_api)
    from api.user_api import user_api
    app.register_blueprint(user_api)
    from api.login_api import login_api
    app.register_blueprint(login_api)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config['DEBUG'], host=host, port=port)
