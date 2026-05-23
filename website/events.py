from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from .icons import icons

# from .models import Event, Comment
# from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures.file_storage import FileStorage
from .forms import EventForm, BookingForm
from flask_login import current_user, login_required
from datetime import date


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
    comment_form = CommentForm()

    # update if events date is in the past
    if event.date < date.today():
        event.status = "Inactive"
        db.session.commit()

    # display up to 8 tickets or however many are available
    ga_available = 8 if event.general_admission_available >= 8 else event.general_admission_available

    # check if user is admin
    try:
        admin = True if event.user_id == current_user.id else False
    except:
        admin = False

    # get number of comments
    comments = db.session.scalars(db.select(Comment).where(Event.id == id)).all()
    comments_length = len(comments)

    return render_template(
        "events/show.html",
        event=event,
        icons=icons,
        form=form,
        comment_form=comment_form,
        ga_available=ga_available,
        admin=admin,
        comments_length=comments_length,
    )


@eventbp.route("/create", methods=["GET", "POST"])
@login_required
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
            status="Open",
            user_id=current_user.id,
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for("event.show", id=event.id))
    return render_template("events/create.html", form=form)


@eventbp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    try:
        event = db.session.scalar(db.select(Event).where(Event.id == id))
        if event.user_id == current_user.id:
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

                if event.status == "Sold Out" and form.general_admission_available.data > 0:
                    event.status = "Open"

                db.session.commit()
                return redirect(url_for("event.show", id=event.id))
            return render_template("events/edit.html", form=form)
        else:
            flash("You must be the event owner to edit an event")
            raise Exception("User is not event owner")
    except:
        return redirect(url_for("event.show", id=event.id))


@eventbp.route("/cancel/<id>")
@login_required
def cancel(id):
    try:
        event = db.session.scalar(db.select(Event).where(Event.id == id))
        if event.user_id == current_user.id:
            event.status = "Cancelled"
            db.session.commit()
            return redirect(url_for("event.show", id=event.id))
        else:
            flash("You must be the event owner to cancel an event")
            raise Exception("User is not event owner")
    except:
        return redirect(url_for("event.show", id=event.id))


@eventbp.route("/<id>/comment", methods=["GET", "POST"])
def comment(id):
    form = CommentForm()
    # get the destination object associated to the page and the comment
    if form.validate_on_submit():
        # read the comment from the form
        comment = Comment(text=form.text.data, event_id=id, user_id=current_user.id)
        # here the back-referencing works - comment.destination is set
        # and the link is created
        db.session.add(comment)
        db.session.commit()

        # flashing a message which needs to be handled by the html
        # flash('Your comment has been added', 'success')
        print("Your comment has been added", "success")
    # using redirect sends a GET request to destination.show
    return redirect(url_for("event.show", id=id))
