from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wisk.config import Config

db = SQLAlchemy() # Create a SQLAlchemy instance.

# It allows you to create multiple instances of the application for testing, etc.
# This is a design pattern recommended on the flask documentation.
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config) # Load the configs from config.py.

    db.init_app(app)

    # Importing the Blueprint object from each section.
    from wisk.articles.routes import articles
    from wisk.main.routes import main
    from wisk.errors.handlers import errors

    # After importing the Blueprint, we need to register the same.
    app.register_blueprint(articles)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
