from flask import Blueprint, render_template, request, redirect, url_for, flash

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
    if genre is not None and genre not in icons:
        flash("Invalid genre")
        return redirect(url_for("main.index", p=page))

    per_page = 1

    # carousel query
    carousels_statement = select(Event).where(Event.status == "Open").order_by(desc("general_admission_available")).limit(3)
    carousels = db.session.scalars(carousels_statement).all()
    carousels_length = len(carousels)

    # construct main db query
    events_statement = select(Event).limit(per_page)

    # add genre to query if there is one
    if genre is not None:
        events_statement = events_statement.where(Event.genre == genre)

    # make sure page is an int > 0
    if page is not None:
        try:
            page = int(page)
            if page < 1:
                raise Exception()
        except:
            flash("Invalid page")
            return redirect(url_for("main.index", genre=genre))

    # calculate offset for events statement
    offset = (page - 1) * per_page if page is not None else 0
    events_statement = events_statement.offset(offset)

    # perform main db query
    current_page_events_statement = events_statement.limit(per_page)
    events = db.session.scalars(current_page_events_statement).all()
    events_length = len(events)

    # check if page number was invalid
    if page is not None and page != 1 and len(events) == 0:
        flash("Invalid page")
        return redirect(url_for("main.index", genre=genre))

    # check if theres a next page
    next_page_events_statement = events_statement.limit(per_page * 2)
    next_page_events = db.session.scalars(next_page_events_statement).all()
    next_page = False
    if len(next_page_events) > len(events):
        next_page = True

    # check if theres a second next page
    second_next_page = False
    if page is None or page == 1:
        second_next_page_events_statement = events_statement.limit(per_page * 3)
        second_next_page_events = db.session.scalars(second_next_page_events_statement).all()
        if len(second_next_page_events) > len(next_page_events):
            second_next_page = True

    # # set page to 1 if it is None because we pass it to index.html
    page = 1 if page is None else page

    # update if an events date is in the past
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
        page=page,
        next_page=next_page,
        second_next_page=second_next_page,
        genre=genre,
    )
