# import flask - from 'package' import 'Class'
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


# create a function that creates a web application
# a web server will run this web application
def create_app():
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    # Should be set to false in a production environment
    app.debug = True
    app.secret_key = "somesecretkey"
    # set the app configuration data
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sitedata.sqlite"
    # initialise db with flask app
    db.init_app(app)

    # config upload folder
    UPLOAD_FOLDER = "/static/img"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    Bootstrap5(app)

    # set the name of the login function that lets user login
    login_manager.login_view = "user.login"
    login_manager.init_app(app)

    from . import views

    app.register_blueprint(views.main_bp)

    from . import events

    app.register_blueprint(events.eventbp)

    from . import bookings

    app.register_blueprint(bookings.bookingbp)

    from . import users

    app.register_blueprint(users.userbp)

    return app
