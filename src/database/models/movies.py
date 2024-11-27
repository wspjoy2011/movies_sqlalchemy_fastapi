import uuid

from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from sqlalchemy.types import DECIMAL

from database.base import Base
from database.validators import movies as validators


class StaffMovie(Base):
    __abstract__ = True
    __tablename__ = None

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    def __str__(self):
        return self.name


class Genre(StaffMovie):
    __tablename__ = 'genres'
    movies = relationship('MovieGenre', back_populates='genre')


class Star(StaffMovie):
    __tablename__ = 'stars'
    movies = relationship('MovieStar', back_populates='star')


class Director(StaffMovie):
    __tablename__ = 'directors'
    movies = relationship('MovieDirector', back_populates='director')


class Certification(StaffMovie):
    __tablename__ = 'certifications'
    movies = relationship('Movie', order_by='Movie.name', back_populates='certification')


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(250), nullable=False)
    year = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    imdb = Column(Float, nullable=False)
    votes = Column(Integer, nullable=False)
    meta_score = Column(Float, nullable=True)
    gross = Column(Float, nullable=True)
    description = Column(Text, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=True)

    certification_id = Column(Integer, ForeignKey('certifications.id', ondelete='RESTRICT'), nullable=False)
    certification = relationship('Certification', back_populates='movies')

    genres = relationship('MovieGenre', back_populates='movie', cascade='all, delete-orphan')
    directors = relationship('MovieDirector', back_populates='movie', cascade='all, delete-orphan')
    stars = relationship('MovieStar', back_populates='movie', cascade='all, delete-orphan')

    __table_args__ = (
        UniqueConstraint('name', 'year', 'time', name='unique_movie_constraint'),
    )

    def __str__(self):
        return f'{self.name} - {self.year}'

    @validates('year')
    def validate_year(self, key, value):
        return validators.validate_year(value)

    @validates('imdb')
    def validate_imdb(self, key, value):
        return validators.validate_imdb(value)

    @validates('votes')
    def validate_votes(self, key, value):
        return validators.validate_votes(value)

    @validates('meta_score')
    def validate_meta_score(self, key, value):
        return validators.validate_meta_score(value)

    @validates('time')
    def validate_time(self, key, value):
        return validators.validate_time(value)

    @validates('gross')
    def validate_gross(self, key, value):
        return validators.validate_gross(value)

    def check_popularity_constraints(self):
        validators.validate_movie_popularity(self.imdb, self.votes)


class MovieGenre(Base):
    __tablename__ = 'movie_genres'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete='CASCADE'))
    genre_id = Column(Integer, ForeignKey('genres.id', ondelete='CASCADE'))

    movie = relationship('Movie', back_populates='genres')
    genre = relationship('Genre', back_populates='movies')

    __table_args__ = (
        UniqueConstraint('movie_id', 'genre_id', name='unique_movie_genre'),
    )

    def __str__(self):
        return f'{self.movie} - {self.genre}'


class MovieDirector(Base):
    __tablename__ = 'movie_directors'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete='CASCADE'))
    director_id = Column(Integer, ForeignKey('directors.id', ondelete='CASCADE'))

    movie = relationship('Movie', back_populates='directors')
    director = relationship('Director', back_populates='movies')

    __table_args__ = (
        UniqueConstraint('movie_id', 'director_id', name='unique_movie_director'),
    )

    def __str__(self):
        return f'{self.movie} - {self.director}'


class MovieStar(Base):
    __tablename__ = 'movie_stars'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete='CASCADE'))
    star_id = Column(Integer, ForeignKey('stars.id', ondelete='CASCADE'))

    movie = relationship('Movie', back_populates='stars')
    star = relationship('Star', back_populates='movies')

    __table_args__ = (
        UniqueConstraint('movie_id', 'star_id', name='unique_movie_star'),
    )

    def __str__(self):
        return f'{self.movie} - {self.star}'
