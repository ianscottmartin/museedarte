from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

# This is an association table for the many-to-many relationship between Museum and Artist
museum_artist_association = db.Table(
    'museum_artist_association',
    db.Column('museum_id', db.Integer, db.ForeignKey('museums.id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'))
)

class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Define the many-to-many relationship with Museum
    museums = db.relationship('Museum', secondary=museum_artist_association, backref=db.backref('artists', lazy=True))

    def __repr__(self):
        return f"Artist {self.name}, ID: {self.id}"

class Museum(db.Model):
    __tablename__ = "museums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"Museum {self.name}, ID: {self.id}"

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    
    # Define the relationships between Review, Artist, and Museum
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    artist = db.relationship('Artist', backref='reviews')
    
    museum_id = db.Column(db.Integer, db.ForeignKey('museums.id'))
    museum = db.relationship('Museum', backref='reviews')
    
    def __repr__(self):
        return f"Review ID: {self.id}, Artist: {self.artist.name}, Museum: {self.museum.name}"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(60))

    @hybrid_property
    def password_hash(self):
        raise Exception("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        bcrypt_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        self._password_hash = bcrypt_hash

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f"User {self.username}, ID: {self.id}"
