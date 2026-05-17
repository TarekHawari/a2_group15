from flask import Blueprint, render_template, request

from . import db
from .models import Event
from .icons import icons

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # get the value of p and genre eg. http://127.0.0.1:5000/?genre=Electronic, genre = Electronic
    # if page or genre is not specified, the value will be None
    page = request.args.get("p")
    genre = request.args.get("genre")

    if genre in icons:
        # events = Event.query.filter(Event.genre == genre).all()
        events = db.session.execute(db.select(Event).filter_by(genre=genre)).scalars()
    else:
        # events = Event.query.all()
        events = db.session.execute(db.select(Event)).scalars()

    return render_template("index.html", events=events, icons=icons)
