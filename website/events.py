from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from .forms import EventForm
from .icons import icons

# from .models import Event, Comment
# from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename

eventbp = Blueprint("event", __name__, url_prefix="/events")


@eventbp.route("/<id>")
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    return render_template("events/show.html", event=event, icons=icons)
    # cform = CommentForm()
    # return render_template("events/show.html", event=event, form=cform, icons=icons)


@eventbp.route("/create", methods=["GET", "POST"])
def create():
    def check_upload_file(form):
        img_path = "static/img"
        fp = form.image.data
        filename = fp.filename
        base_path = os.path.dirname(__file__)
        upload_path = os.path.join(base_path, img_path, secure_filename(filename))
        db_upload_path = "/" + img_path + "/" + secure_filename(filename)
        fp.save(upload_path)
        return db_upload_path

    form = EventForm()
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        event = Event(
            artist=form.artist.data,
            genre=form.genre.data,
            acknowledgement=form.acknowledgement.data,
            short_description=form.short_description.data,
            long_description=form.long_description.data,
            image=db_file_path,
            venue_name=form.venue_name.data,
            venue_address=form.venue_address.data,
            venue_city=form.venue_city.data,
            venue_state=form.venue_state.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            date=form.date.data,
            all_ages_price=form.all_ages_price.data,
            general_admission_price=form.general_admission_price.data,
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for("event.show", id=event.id))
    return render_template("events/create.html", form=form)
