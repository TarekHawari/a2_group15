from flask_wtf import FlaskForm
from wtforms.fields import (
    TextAreaField,
    SubmitField,
    StringField,
    PasswordField,
    FileField,
    SelectField,
    RadioField,
    DateTimeField,
    FloatField,
    TimeField,
    DateField,
    IntegerField,
    TelField
)
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, ValidationError
from flask_wtf.file import FileRequired, FileField, FileAllowed
from datetime import date


def date_in_future(form, field):
    if field.data < date.today():
        raise ValidationError("The date must not be in the past")


class LoginForm(FlaskForm):
    email = StringField("email", validators=[InputRequired("Enter user email"), Email("Please enter a valid email")])
    password = PasswordField("Password", validators=[InputRequired("Enter user password")])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    firstName = StringField("First Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email("Please enter a valid email")])
    contactNumber = TelField("Contact Number", validators=[InputRequired()])
    streetAddress = StringField("Street Address", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm = PasswordField("Confirm Password", validators=[EqualTo("password", message="Passwords should match")])
    submit = SubmitField("Register")


class CommentForm(FlaskForm):
    text = TextAreaField("Write a comment", [InputRequired()])

    # submit button
    submit = SubmitField("Post Comment")


class EventForm(FlaskForm):
    allowed_files = {
        "jpg",
        "jpeg",
        "png",
        "webp",
        "JPG",
        "JPEG",
        "PNG",
        "WEBP",
    }

    genre_choices = [
        ("Electronic", "Electronic"),
        ("Hip-Hop", "Hip-Hop"),
        ("Jazz", "Jazz"),
        ("Metal", "Metal"),
        ("Pop", "Pop"),
        ("Rock", "Rock"),
    ]

    acknowledgement_choices = [
        ("No Acknowledgement of Country", "No Acknowledgement of Country"),
        ("Acknowledgement of Country: Generic", "Acknowledgement of Country: Generic"),
        ("Acknowledgement of Country: Enhanced", "Acknowledgement of Country: Enhanced"),
    ]

    state_choices = [
        ("QLD", "QLD"),
        ("NSW", "NSW"),
        ("ACT", "ACT"),
        ("VIC", "VIC"),
        ("TAS", "TAS"),
        ("NT", "NT"),
        ("SA", "SA"),
        ("WA", "WA"),
    ]

    artist = StringField(
        "Artist",
        validators=[
            InputRequired(),
            (Length(max=64)),
        ],
    )
    genre = SelectField(
        "Genre",
        choices=genre_choices,
        validators=[
            InputRequired(),
            (Length(max=10)),
        ],
    )
    acknowledgement = RadioField(
        "Acknowledgement of Country",
        choices=acknowledgement_choices,
        validators=[InputRequired(), (Length(max=36))],
    )
    short_description = TextAreaField(
        "Short Description",
        validators=[
            InputRequired(),
            (Length(max=512)),
        ],
    )
    long_description = TextAreaField(
        "Long Description",
        validators=[
            InputRequired(),
            (Length(max=4096)),
        ],
    )
    image = FileField(
        "Event Image",
        # validators=[
        #     FileRequired(message="Image cannot be empty"),
        #     FileAllowed(allowed_files, message="Only supports jpg, jpeg, png, webp"),
        # ],
    )
    venue_name = StringField(
        "Venue Name",
        validators=[
            InputRequired(),
            (Length(max=32)),
        ],
    )
    venue_city = StringField(
        "Venue City",
        validators=[
            InputRequired(),
            (Length(max=32)),
        ],
    )
    venue_state = SelectField(
        "Venue State",
        choices=state_choices,
        validators=[
            InputRequired(),
            (Length(max=3)),
        ],
    )
    start_time = TimeField(
        "Start Time",
        format="%H:%M",
        validators=[
            InputRequired(),
        ],
    )
    end_time = TimeField(
        "End Time",
        format="%H:%M",
        validators=[
            InputRequired(),
        ],
    )
    date = DateField(
        "Date",
        format="%Y-%m-%d",
        validators=[
            InputRequired(),
            date_in_future,
        ],
    )
    general_admission_price = FloatField(
        "Ticket Price",
        validators=[
            InputRequired(),
            NumberRange(),
        ],
    )
    general_admission_available = IntegerField(
        "Tickets Available",
        validators=[
            InputRequired(),
            NumberRange(min=1, max=200000),
        ],
    )
    submit = SubmitField("Submit")


class BookingForm(FlaskForm):
    quantity = IntegerField("Quantity", validators=[InputRequired(), NumberRange(min=1)])
    submit = SubmitField("Book Now")
