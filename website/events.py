from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from .forms import EventForm, CommentForm
from .icons import icons

# from .models import Event, Comment
# from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from .forms import EventForm, BookingForm

eventbp = Blueprint("event", __name__, url_prefix="/events")


@eventbp.route("/<id>")
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    form = BookingForm()
    comment_form = CommentForm()
    return render_template("events/show.html", event=event, icons=icons, form=form, comment_form=comment_form)
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
            all_ages_available=form.all_ages_available.data,
            general_admission_available=form.general_admission_available.data,
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for("event.show", id=event.id))
    return render_template("events/create.html", form=form)

@eventbp.route("/<id>/comment", methods=["GET", "POST"])
def comment(id):
    form = CommentForm()
    # get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if form.validate_on_submit():
        # read the comment from the form
        comment = Comment(text=form.text.data, Event=event)
        # here the back-referencing works - comment.destination is set
        # and the link is created
        db.session.add(comment)
        db.session.commit()

        # flashing a message which needs to be handled by the html
        # flash('Your comment has been added', 'success')
        print("Your comment has been added", "success")
    # using redirect sends a GET request to destination.show
    return redirect(url_for("event.show", id=id))