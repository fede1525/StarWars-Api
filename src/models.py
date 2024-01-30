from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date, relationship

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    date_of_birth = db.Column(Date, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    phone_number = db.Column(String(12), unique=True)

    favorites = relationship("Favorites", back_populates="users")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "date_of_birth": self.date_of_birth,
            "is_active": self.is_active,
            "phone_number": self.phone_number
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    people_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    homeworld = db.Column(db.String(100), unique=False)
    hair_color = db.Column(db.String(40), unique=False)
    eye_color = db.Column(db.String(40), unique=False)

    def serialize(self):
        return {
            "id": self.people_id,
            "name": self.name,
            "homeworld": self.homeworld,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
        }

class Planets(db.Model):
    planet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    climate = db.Column(db.String(100), unique=False)
    terrain = db.Column(db.String(40), unique=False)
    orbital_period = db.Column(db.String(40), unique=False)
    rotation_period = db.Column(db.String(40), unique=False)
    gravity = db.Column(db.String(40), unique=False)
    population = db.Column(db.Integer, unique=False)

    def serialize(self):
        return {
            "id": self.planet_id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "gravity": self.gravity,
            "population": self.population
        }

class Favorites(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    planet_id = db.Column(db.Integer, ForeignKey("planets.planet_id"))
    people_id = db.Column(db.Integer, ForeignKey("people.people_id"))

    planet = relationship("Planets", back_populates="favorites")
    people = relationship("People", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id

        }