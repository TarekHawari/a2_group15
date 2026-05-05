from flask_wtf import FlaskForm
from wtforms.fields import (
    TextAreaField,
    SubmitField,
    StringField,
    PasswordField,
    FileField,
    SelectField,
    DateTimeField,
    FloatField,
    TimeField,
    DateField,
    IntegerField,
)
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed


# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired("Enter user name")])
    password = PasswordField("Password", validators=[InputRequired("Enter user password")])
    submit = SubmitField("Login")


# this is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(), EqualTo("confirm", message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")


class CommentForm(FlaskForm):
    pass


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
        ("none", "No Acknowledgement of Country"),
        ("generic", "Acknowledgement of Country: generic"),
        ("enhanced", "Acknowledgement of Country: enhanced"),
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
    acknowledgement = SelectField(
        "Acknowledgement of Country",
        choices=acknowledgement_choices,
        validators=[InputRequired(), (Length(max=8))],
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
        validators=[
            FileRequired(message="Image cannot be empty"),
            FileAllowed(allowed_files, message="Only supports jpg, jpeg, png, webp"),
        ],
    )
    venue_name = StringField(
        "Venue Name",
        validators=[
            InputRequired(),
            (Length(max=32)),
        ],
    )
    venue_address = StringField(
        "Venue Address",
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
        ],
    )
    all_ages_price = FloatField(
        "All Ages Price",
        validators=[
            InputRequired(),
            NumberRange(),
        ],
    )
    general_admission_price = FloatField(
        "General Admission Price",
        validators=[
            InputRequired(),
            NumberRange(),
        ],
    )
    all_ages_available = IntegerField(
        "All Ages Tickets Available",
        validators=[
            InputRequired(),
            NumberRange(max=200000),
        ],
    )
    general_admission_available = IntegerField(
        "General Admission Tickets Available",
        validators=[
            InputRequired(),
            NumberRange(min=1, max=200000),
        ],
    )
    submit = SubmitField("Create")
