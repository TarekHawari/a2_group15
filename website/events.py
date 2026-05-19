from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from .forms import EventForm
from .icons import icons

# from .models import Event, Comment
# from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures.file_storage import FileStorage
from .forms import EventForm, BookingForm

import random
import string

eventbp = Blueprint("event", __name__, url_prefix="/events")


def check_upload_file(form):
    img_path = "static/img"
    fp = form.image.data
    filename = fp.filename
    base_path = os.path.dirname(__file__)
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    f = random_string + "-" + secure_filename(filename)
    upload_path = os.path.join(base_path, img_path, f)
    db_upload_path = "/" + img_path + "/" + f
    fp.save(upload_path)
    return db_upload_path


@eventbp.route("/<id>")
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    form = BookingForm()
    ga_available = 8 if event.general_admission_available >= 8 else event.general_admission_available
    return render_template("events/show.html", event=event, icons=icons, form=form, ga_available=ga_available)
    # cform = CommentForm()
    # return render_template("events/show.html", event=event, form=cform, icons=icons)


@eventbp.route("/create", methods=["GET", "POST"])
def create():
    form = EventForm()
    if form.validate_on_submit():
        # if a new image has been uploaded, process it, else use default
        if isinstance(form.image.data, FileStorage):
            db_file_path = check_upload_file(form)
        else:
            db_file_path = "/static/img/default.jpg"

        event = Event(
            artist=form.artist.data,
            genre=form.genre.data,
            acknowledgement=form.acknowledgement.data,
            short_description=form.short_description.data,
            long_description=form.long_description.data,
            image=db_file_path,
            venue_name=form.venue_name.data,
            venue_city=form.venue_city.data,
            venue_state=form.venue_state.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            date=form.date.data,
            general_admission_price=form.general_admission_price.data,
            general_admission_available=form.general_admission_available.data,
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for("event.show", id=event.id))
    return render_template("events/create.html", form=form)


@eventbp.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    form = EventForm(obj=event)
    form.genre.default = event.genre
    form.acknowledgement.default = event.acknowledgement
    if form.validate_on_submit():
        # if a new image has been uploaded, process it, else leave event.image untouched
        if isinstance(form.image.data, FileStorage):
            db_file_path = check_upload_file(form)
            event.image = db_file_path

        event.artist = form.artist.data
        event.genre = form.genre.data
        event.acknowledgement = form.acknowledgement.data
        event.short_description = form.short_description.data
        event.long_description = form.long_description.data
        # event.image = db_file_path
        event.venue_name = form.venue_name.data
        event.venue_city = form.venue_city.data
        event.venue_state = form.venue_state.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.date = form.date.data
        event.general_admission_price = form.general_admission_price.data
        event.general_admission_available = form.general_admission_available.data

        db.session.commit()
        return redirect(url_for("event.show", id=event.id))
    return render_template("events/edit.html", form=form)


@eventbp.route("/cancel/<id>")
def cancel(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    # edit event status here
    # db.session.commit()
    return redirect(url_for("event.show", id=event.id))
