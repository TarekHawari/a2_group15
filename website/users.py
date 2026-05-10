from .models import User
from .forms import RegisterForm, LoginForm
from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from . import db

userbp = Blueprint("user", __name__)

@userbp.route("/register", methods=["GET", "POST"])
def register_user():
    error = None
    form = RegisterForm()

    if form.validate_on_submit():
        user_name = form.username.data.lower()
        email = form.email.data.lower()
        user = User (
            name = user_name,
            email = email,
            password = generate_password_hash(form.password.data)
        )
        if db.session.scalar(db.select(User).where(User.name==user_name)):
            error = 'User already exists'
        elif db.session.scalar(db.select(User).where(User.email==email)):
            error = 'Email already used'

        if error is None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login_user'))  
        
    if error is not None: flash(error)
    return render_template("users/register.html", heading='Register', form=form)

@userbp.route("/login", methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        user_name = form.username.data.lower()
        password = form.password.data.lower()
        user = db.session.scalar(db.select(User).where(User.name==user_name))

        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if error is None:
            nextp = request.args.get('next')
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
        return redirect(url_for("event.show", id=user.id))
    return render_template('users/login.html', form=form, heading='Login')

