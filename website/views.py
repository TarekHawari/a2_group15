from flask import Blueprint, render_template, request, redirect, url_for

from . import db
from .models import Event
from .icons import icons
from datetime import date

from flask_login import current_user
from sqlalchemy import select, desc

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # get the value of p and genre eg. http://127.0.0.1:5000/?genre=Electronic&p=2, genre = Electronic, page = 2
    # if page or genre is not specified, the value will be None
    page = request.args.get("p")
    genre = request.args.get("genre")

    per_page = 3

    # carousel query
    carousels_statement = select(Event).where(Event.status == "Open").order_by(desc("general_admission_available")).limit(3)
    carousels = db.session.scalars(carousels_statement).all()
    carousels_length = len(carousels)

    # construct main db query
    events_statement = select(Event).limit(per_page)
    if genre in icons:
        events_statement = events_statement.where(Event.genre == genre)

    if page is not None:
        try:
            page = int(page)
            if page < 1:
                raise Exception("Page out of bounds")
        except:
            return redirect(url_for("main.index"))

    # perform main db query
    events = db.session.scalars(events_statement).all()
    events_length = len(events)

    # update if events date is in the past
    for event in events:
        if event.date < date.today():
            event.status = "Inactive"
            db.session.commit()

    return render_template(
        "index.html",
        events=events,
        icons=icons,
        selected_genre=genre,
        carousels=carousels,
        carousels_length=carousels_length,
        events_length=events_length,
    )
