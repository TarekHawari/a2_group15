from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
from .forms import RegisterForm, LoginForm
from . import db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # get the value of p and genre eg. http://127.0.0.1:5000/?genre=electronic, genre = electronic
    # if page or genre is not specified, the value will be None
    page = request.args.get("p")
    genre = request.args.get("genre")

    return render_template("index.html")

@main_bp.route("/register", methods=["GET", "POST"])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        # db_file_path = check_upload_file(form)
        user = User (
            name = form.username.data,
            email = form.email.data,
            password = form.email.data
        )
        db.session.add(user)
        db.session.commit()
        # return redirect(url_for("event.show", id=user.id))
    return render_template("website/user.html", heading='Register', form=form)

@main_bp.route("/login", methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    return render_template('website/user.html', heading='Login', form=form)

