from flask import Blueprint, redirect, render_template, request, url_for
from .forms import BookingForm
from .models import Order

bookingbp = Blueprint("booking", __name__, url_prefix="/bookings")


@bookingbp.route("/")
def show():
    orders = Order.query.all()
    form = BookingForm()
    return render_template("bookings/show.html", orders=orders, form = form)


