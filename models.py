from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

movie_actors = db.Table('movie_actors',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True)
)

movie_genres = db.Table('movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    release_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float)
    box_office = db.Column(db.Float)
    duration = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    production_company_id = db.Column(db.Integer, db.ForeignKey('production_company.id'))
    
    director = db.relationship('Director', backref='movies')
    production_company = db.relationship('ProductionCompany', backref='movies')
    actors = db.relationship('Actor', secondary=movie_actors, backref='movies')
    genres = db.relationship('Genre', secondary=movie_genres, backref='movies')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'release_date': self.release_date.isoformat(),
            'budget': self.budget,
            'box_office': self.box_office,
            'duration': self.duration,
            'director': f"{self.director.first_name} {self.director.last_name}" if self.director else None,
            'production_company': self.production_company.name if self.production_company else None,
            'actors': [f"{actor.first_name} {actor.last_name}" for actor in self.actors],
            'genres': [genre.name for genre in self.genres]
        }

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date)
    nationality = db.Column(db.String(50))
    biography = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'nationality': self.nationality,
            'biography': self.biography
        }

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date)
    nationality = db.Column(db.String(50))
    biography = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'nationality': self.nationality,
            'biography': self.biography
        }

class ProductionCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50))
    founding_date = db.Column(db.Date)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'founding_date': self.founding_date.isoformat() if self.founding_date else None,
            'description': self.description
        } 