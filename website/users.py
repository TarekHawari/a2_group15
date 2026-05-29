from .models import User
from .forms import RegisterForm, LoginForm
from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from . import db

userbp = Blueprint("user", __name__)


@userbp.route("/register", methods=["GET", "POST"])
def register():
    error = None
    form = RegisterForm()

    if form.validate_on_submit():
        first_name = form.firstName.data.lower()
        last_name = form.surname.data.lower()
        contact_number = form.contactNumber.data.lower()
        street_address = form.streetAddress.data.lower()
        email = form.email.data.lower()
        user = User (
            firstName = first_name,
            surname = last_name,
            email = email,
            contactNumber = contact_number,
            streetAddress = street_address,
            password = generate_password_hash(form.password.data)
        )
        # if db.session.scalar(db.select(User).where(User.name==user_name)):
        #     error = 'User already exists'
        if db.session.scalar(db.select(User).where(User.email==email)):
            error = 'Email already exists'

        if error is None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))  
        
    if error is not None: flash(error)
    return render_template("users/register.html", heading='Register', form=form)


@userbp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None
    
    if form.validate_on_submit():
        email = form.email.data.lower() # xxxxxx
        password = form.password.data.lower()
        user = db.session.scalar(db.select(User).where(User.email==email))

        if user is None:
            error = 'Incorrect user'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if error is None:
            login_user(user)
            nextp = request.args.get('next')
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('users/login.html', form=form, heading='Login')


@userbp.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('user.login'))  