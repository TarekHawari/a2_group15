from flask import Blueprint, render_template, request

from . import db
from .models import Event
from .icons import icons

from flask_login import current_user
from sqlalchemy import select, desc

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # get the value of p and genre eg. http://127.0.0.1:5000/?genre=Electronic, genre = Electronic
    # if page or genre is not specified, the value will be None
    page = request.args.get("p")
    genre = request.args.get("genre")

    carousels_statement = select(Event).where(Event.status == "Open").order_by(desc("general_admission_available")).limit(3)
    carousels = db.session.scalars(carousels_statement).all()
    carousels_length = len(carousels)

    events_statement = select(Event)
    if genre in icons:
        events_statement = events_statement.where(Event.genre == genre)
    events = db.session.scalars(events_statement).all()
    events_length = len(events)

    return render_template(
        "index.html",
        events=events,
        icons=icons,
        selected_genre=genre,
        carousels=carousels,
        carousels_length=carousels_length,
        events_length=events_length,
    )
