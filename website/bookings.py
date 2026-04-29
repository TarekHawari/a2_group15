from flask import Blueprint, redirect, render_template, request, url_for

bookingbp = Blueprint("booking", __name__, url_prefix="/bookings")


@bookingbp.route("/")
def show():
    return render_template("bookings/show.html")
