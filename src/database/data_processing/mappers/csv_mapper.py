import ast
from decimal import Decimal
import random

import pandas as pd
from tqdm import tqdm

from apps.movies.dto.movie import MoviesDTO, MovieDTO


class MovieCSVMapper:
    """
    A class responsible for reading a CSV file and mapping its data to a MoviesDTO object.

    Attributes:
        _filename (str): The path to the CSV file containing movie data.
    """

    def __init__(self, filename: str):
        """
        Initializes the MovieCSVMapper with the given CSV file name.

        Args:
            filename (str): The path to the CSV file containing movie data.
        """
        self._filename = filename

    def _read_csv_file(self) -> pd.DataFrame:
        """
        Reads the CSV file into a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the data from the CSV file.
        """
        return pd.read_csv(self._filename, encoding='utf-8')

    def _extract_unique_values(self, movies_df: pd.DataFrame):
        """
        Extracts unique values for genres, directors, stars, and certifications from the movies DataFrame.

        Args:
            movies_df (pd.DataFrame): The DataFrame containing movie data.

        Returns:
            tuple: A tuple containing four sets (genres, directors, stars, certifications).
        """
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
        """
        Maps a row from the DataFrame to a MovieDTO object.

        Args:
            row (pd.Series): A row from the DataFrame representing a single movie.

        Returns:
            MovieDTO: A data transfer object representing the movie.
        """
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
            description=description,
            price=self.generate_random_price()
        )

    def _map_rows_to_dto(self, movies_df: pd.DataFrame) -> MoviesDTO:
        """
        Maps rows of a DataFrame to a MoviesDTO object, including unique values for related entities.

        Args:
            movies_df (pd.DataFrame): The DataFrame containing movie data.

        Returns:
            MoviesDTO: A data transfer object containing all movies and their related entities.
        """
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
        """
        Reads the CSV file, maps its data to a MoviesDTO object.

        Returns:
            MoviesDTO: A data transfer object containing all movies and their related entities.
        """
        movies_df = self._read_csv_file()
        movies_dto = self._map_rows_to_dto(movies_df)
        return movies_dto

    def check_duplicates(self) -> MoviesDTO:
        """
        Checks for duplicate entries in the CSV file based on movie name and year of release.

        Returns:
            MoviesDTO: A data transfer object containing only the duplicate movies.
        """
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

    @staticmethod
    def generate_random_price(min_price: float = 5.0, max_price: float = 20.0) -> Decimal:
        """
        Generates a random price between min_price and max_price as a Decimal.

        Args:
            min_price (float): Minimum price (inclusive).
            max_price (float): Maximum price (inclusive).

        Returns:
            Decimal: A random price with two decimal places.
        """
        random_price = round(random.uniform(min_price, max_price), 2)
        return Decimal(f"{random_price}")

