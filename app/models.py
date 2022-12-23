import os
from datetime import datetime

from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import validates

from . import db
from . import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class GasStation(db.Model):
    __tablename__ = 'gas_stations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    lat = db.Column(db.Float, index=True)
    lon = db.Column(db.Float, index=True)
    distance = db.Column(db.Float)
    fuels = db.relationship("Fuel", backref="gas_station")
    comments = db.relationship("Comment", backref="gas_station")

    def get_icon(self):
        if os.path.exists(os.path.join(
            current_app.config["STATIC_DIR"],
            "assets",
            self.name.lower() + '.ico')):
            return url_for('static', filename='/assets/' + self.name.lower() + '.ico')
        return url_for('static', filename="/assets/gas_station.ico")

    def to_json(self):
        station = {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "distance": self.distance,
            "icon": self.get_icon(),
        }
        return station


class Fuel(db.Model):
    __tablename__ = 'fuels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Numeric(5,2), nullable=False)
    gas_station_id = db.Column(db.Integer, db.ForeignKey('gas_stations.id'))

    def to_json(self):
        fuel = {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }
        return fuel


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    rate = db.Column(db.Numeric(2,1))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    user = db.relationship("User", backref="comment")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    gas_station_id = db.Column(db.Integer, db.ForeignKey('gas_stations.id'))

    def to_json(self):
        comment = {
            "id": self.id,
            "comment": self.comment,
            "rate": self.rate,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user": self.user.username,
            "user_id": self.user_id,
        }
        return comment

    @validates('rate')
    def validate_column_name(self, key, value):
        if value < 1.0:
            raise ValueError('ocena musi być wyższa lub równa 1')
        if value > 5.0:
            raise ValueError('ocena musi być niższa lub równa 5')
        return value
