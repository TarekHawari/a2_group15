from .models import User
from .forms import RegisterForm, LoginForm
from flask import Blueprint, render_template, request
from . import db

userbp = Blueprint("user", __name__)

@userbp.route("/register", methods=["GET", "POST"])
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
    return render_template("register.html", heading='Register', form=form)

# @userbp.route("/login", methods=["GET", "POST"])
# def login_user():
    # login_form = LoginForm()
    # error = None
    # if login_form.validate_on_submit():
    #     user_name = login_form.user_name.data
    #     password = login_form.password.data
    #     user = db.session.scalar(db.select(User).where(User.name==user_name))
    #     if user is None:
    #         error = 'Incorrect user name'
    #     elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
    #         error = 'Incorrect password'
    #     if error is None:
    #         login_user(user)
    #         nextp = request.args.get('next') # this gives the url from where the login page was accessed
    #         print(nextp)
    #         if next is None or not nextp.startswith('/'):
    #             return redirect(url_for('index'))
    #         return redirect(nextp)
    #     else:
    #         flash(error)
    # return render_template('user.html', form=login_form, heading='Login')

