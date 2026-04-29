from flask import Blueprint, redirect, render_template, request, url_for

eventbp = Blueprint("event", __name__, url_prefix="/events")


@eventbp.route("/<id>")
def show(id):
    return render_template("events/show.html")


@eventbp.route("/create")
def create():
    return render_template("events/create.html")
