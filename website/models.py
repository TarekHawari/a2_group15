from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(64), index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"Name: {self.name}"


@login_manager.user_loader
def load_user(user_id):
    return db.session.scalar(db.select(User).where(User.id == user_id))


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    artist = db.Column(db.String(64))
    genre = db.Column(db.String(10))
    acknowledgement = db.Column(db.String(8))
    short_description = db.Column(db.String(512))
    long_description = db.Column(db.String(4096))
    image = db.Column(db.String(400))
    venue_name = db.Column(db.String(32))
    venue_city = db.Column(db.String(32))
    venue_state = db.Column(db.String(32))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    date = db.Column(db.Date)
    general_admission_price = db.Column(db.Float)
    general_admission_available = db.Column(db.Integer)
    status = db.Column(db.String(16))

    # relation to call event.comments and comment.event
    # comments = db.relationship("Comment", backref="event")
    user = db.relationship("User", backref="event")

    def __repr__(self):
        return f"Artist: {self.artist}, Venue: {self.venue_name}"


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    date_create = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))

    def __repr__(self):
        return f"Comment: {self.text}"


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    total_price = db.Column(db.Float)
    date_time = db.Column(db.DateTime, default=datetime.now)

    # relationships
    event = db.relationship("Event", backref="order")
    user = db.relationship("User", backref="order")
