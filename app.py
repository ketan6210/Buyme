from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from extensions import db
import importlib
import pkgutil
import sys


def import_all_models(package_name):
  package = importlib.import_module(package_name)
  for loader, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
    full_module_name = f"{package_name}.{module_name}"
    importlib.import_module(full_module_name)


def register_blueprints(app):
  """Register all blueprints"""
  from routes.auth import bp as auth_bp

  app.register_blueprint(auth_bp)

  from routes.home import bp as home_bp

  app.register_blueprint(home_bp)

  # Register other blueprints as you create them
  # from routes.auctions import bp as auctions_bp
  # app.register_blueprint(auctions_bp)


def create_app(config_name="default"):
  app = Flask(__name__)
  app.config["SECRET_KEY"] = "random"
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///buyme.sqlite3"
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

  db.init_app(app)

  # Register blueprints
  register_blueprints(app)

  # Import models to register them
  import_all_models("models")

  # create db
  with app.app_context():
    db.create_all()

  # @app.route("/hello")
  # def index():
  #   return render_template("index.html")

  app.add_url_rule("/", endpoint="index")

  return app


if __name__ == "__main__":
  app = create_app()
  app.run(debug=True)
