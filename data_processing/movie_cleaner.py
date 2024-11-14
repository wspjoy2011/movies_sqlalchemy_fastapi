from sqlalchemy.orm import Session

from database.models.movies import Movie, Genre, Director, Star, Certification, MovieGenre, MovieDirector, MovieStar
from database.session import SessionLocal


class MovieDatabaseCleaner:
    def __init__(self, session: Session):
        self._session = session

    def clean_all_movie_data(self):
        self._session.query(MovieGenre).delete()
        self._session.query(MovieDirector).delete()
        self._session.query(MovieStar).delete()

        self._session.query(Movie).delete()
        self._session.query(Genre).delete()
        self._session.query(Director).delete()
        self._session.query(Star).delete()
        self._session.query(Certification).delete()

        self._session.commit()


if __name__ == '__main__':
    session = SessionLocal()
    cleaner = MovieDatabaseCleaner(session)
    cleaner.clean_all_movie_data()

    session.close()
