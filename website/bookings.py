from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .forms import BookingForm
from .models import Order, Event
from . import db

bookingbp = Blueprint("booking", __name__, url_prefix="/bookings")


def update_db_number_of_tickets(id, quantity):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    event.general_admission_available = event.general_admission_available - quantity
    event.general_admission_available = 0 if event.general_admission_available < 0 else event.general_admission_available
    if event.general_admission_available == 0:
        event.status = "Sold Out"
    db.session.commit()


@bookingbp.route("/")
def show():
    orders = Order.query.all()
    form = BookingForm()
    return render_template("bookings/show.html", orders=orders, form=form)


@bookingbp.route("/create/<int:id>", methods=["POST"])
@login_required
def create(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    quantity = request.form.get("ga", 0, type=int)
    price = quantity * event.general_admission_price
    order = Order(event_id=id, quantity=quantity, price=price, total_price=price, user_id=current_user.id)
    db.session.add(order)
    db.session.commit()
    update_db_number_of_tickets(id, quantity)
    return redirect(url_for("booking.show"))
