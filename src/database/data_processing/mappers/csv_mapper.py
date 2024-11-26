import ast

import pandas as pd
from tqdm import tqdm

from config.settings import PATH_TO_MOVIES_CSV_FILE
from apps.movies.dto.movie import MoviesDTO, MovieDTO


class MovieCSVMapper:
    def __init__(self, filename: str):
        self._filename = filename

    def _read_csv_file(self) -> pd.DataFrame:
        return pd.read_csv(self._filename, encoding='utf-8')

    def _extract_unique_values(self, movies_df: pd.DataFrame):
        genres = set()
        directors = set()
        stars = set()
        certifications = set()

        for _, row in tqdm(movies_df.iterrows(), desc='Converting data', total=len(movies_df)):
            movie_genres = {genre.strip() for genre in ast.literal_eval(row['Genre'])}
            genres.update(movie_genres)

            movie_directors = {director.strip() for director in ast.literal_eval(row['Director'])}
            directors.update(movie_directors)

            movie_stars = {star.strip() for star in ast.literal_eval(row['Stars'])}
            stars.update(movie_stars)

            certification = row['Certification'].strip() if pd.notna(row['Certification']) else 'Not Rated'
            certifications.add(certification)

        return genres, directors, stars, certifications

    def _create_movie_dto(self, row: pd.Series) -> MovieDTO:
        name = row['Movie Name'].strip()
        year = int(row['Year of Release'])
        time = int(row['Run Time in minutes'])
        imdb = float(row['Movie Rating'])
        votes = int(row['Votes'])
        meta_score = float(row['MetaScore']) if pd.notna(row['MetaScore']) else None
        gross = float(row['Gross']) if pd.notna(row['Gross']) else None

        movie_genres = {genre.strip() for genre in ast.literal_eval(row['Genre'])}
        movie_directors = {director.strip() for director in ast.literal_eval(row['Director'])}
        movie_stars = {star.strip() for star in ast.literal_eval(row['Stars'])}
        certification = row['Certification'].strip() if pd.notna(row['Certification']) else 'Not Rated'
        description = ' '.join([word.strip() for word in ast.literal_eval(row['Description'])])

        return MovieDTO(
            name=name,
            year=year,
            time=time,
            imdb=imdb,
            votes=votes,
            meta_score=meta_score,
            gross=gross,
            genres=movie_genres,
            directors=movie_directors,
            stars=movie_stars,
            certification=certification,
            description=description
        )

    def _map_rows_to_dto(self, movies_df: pd.DataFrame) -> MoviesDTO:
        genres, directors, stars, certifications = self._extract_unique_values(movies_df)
        movies = [self._create_movie_dto(row) for _, row in movies_df.iterrows()]
        return MoviesDTO(
            genres=genres,
            directors=directors,
            stars=stars,
            certifications=certifications,
            movies=movies
        )

    def read_csv_and_map_to_dto(self) -> MoviesDTO:
        movies_df = self._read_csv_file()
        movies_dto = self._map_rows_to_dto(movies_df)
        return movies_dto

    def check_duplicates(self) -> MoviesDTO:
        movies_df = self._read_csv_file()
        duplicates_df = movies_df[movies_df.duplicated(subset=['Movie Name', 'Year of Release'], keep=False)]
        duplicates_movies = [self._create_movie_dto(row) for _, row in duplicates_df.iterrows()]

        return MoviesDTO(
            genres=set(),
            directors=set(),
            stars=set(),
            certifications=set(),
            movies=duplicates_movies
        )


if __name__ == '__main__':
    mapper = MovieCSVMapper(PATH_TO_MOVIES_CSV_FILE)
    movies = mapper.read_csv_and_map_to_dto()
    print(movies)
    # movies_duplicates = parser.check_duplicates()
    # for movie in movies_duplicates.movies:
    #     print(movie.name, movie.year, movie.imdb, movie.description)


