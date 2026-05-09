from . import db
from datetime import datetime
from flask_login import UserMixin

# class User(db.Model, UserMixin):
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(128))


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(64))
    genre = db.Column(db.String(10))
    acknowledgement = db.Column(db.String(8))
    short_description = db.Column(db.String(512))
    long_description = db.Column(db.String(4096))
    image = db.Column(db.String(400))
    venue_name = db.Column(db.String(32))
    venue_address = db.Column(db.String(32))
    venue_city = db.Column(db.String(32))
    venue_state = db.Column(db.String(32))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    date = db.Column(db.Date)
    all_ages_price = db.Column(db.Float)
    general_admission_price = db.Column(db.Float)
    all_ages_available = db.Column(db.Integer)
    general_admission_available = db.Column(db.Integer)

    # relation to call event.comments and comment.event
    # comments = db.relationship("Comment", backref="event")

    def __repr__(self):
        return f"Artist: {self.artist}, Venue: {self.venue_name}"


# class Comment(db.Model):


# class Order(db.Model):