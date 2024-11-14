from sqlalchemy.orm import Session
from database.models.movies import Genre
from database.session import get_session
from database.utils import object_as_dict
from dto.genre import GenreDTO
from typing import List, Optional


class GenreRepository:
    def __init__(self, session: Session):
        self._session = session

    def create_genre(self, name: str) -> GenreDTO:
        genre = Genre(name=name)
        self._session.add(genre)
        self._session.commit()
        self._session.refresh(genre)
        return GenreDTO(**object_as_dict(genre))

    def get_genre(self, genre_id: int) -> Optional[GenreDTO]:
        genre = self._session.query(Genre).filter(Genre.id == genre_id).first()
        return GenreDTO(**object_as_dict(genre)) if genre else None

    def get_all_genres(self) -> List[GenreDTO]:
        genres = self._session.query(Genre).all()
        return [GenreDTO(**object_as_dict(genre)) for genre in genres]

    def update_genre(self, genre_id: int, new_name: str) -> Optional[GenreDTO]:
        genre = self._session.query(Genre).filter(Genre.id == genre_id).first()
        if genre:
            genre.name = new_name
            self._session.commit()
            self._session.refresh(genre)
            return GenreDTO(**object_as_dict(genre))
        return None

    def delete_genre(self, genre_id: int) -> bool:
        genre = self._session.query(Genre).filter(Genre.id == genre_id).first()
        if genre:
            self._session.delete(genre)
            self._session.commit()
            return True
        return False

if __name__ == '__main__':
    with get_session() as session:
        genre_repo = GenreRepository(session)

        new_genre = genre_repo.create_genre("Drama new")
        print('#' * 10)
        print("Created genre:", new_genre)
        print('#' * 10)

        genre = genre_repo.get_genre(new_genre.id)
        print('#' * 10)
        print("Fetched genre:", genre)
        print('#' * 10)

        print('#' * 10)
        updated_genre = genre_repo.update_genre(new_genre.id, "Romantic Drama")
        print("Updated genre:", updated_genre)
        print('#' * 10)

        print('#' * 10)
        success = genre_repo.delete_genre(new_genre.id)
        print("Deleted genre:", "Success" if success else "Genre not found")
        print('#' * 10)
