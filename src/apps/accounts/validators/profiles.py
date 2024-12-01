from datetime import date


def validate_gender(gender: str) -> None:
    if gender not in ['male', 'female']:
        raise ValueError("Gender must be either 'male' or 'female'")


def validate_birth_date(birth_date: date) -> None:
    if birth_date.year < 1900:
        raise ValueError('Invalid birth date - year must be greater than 1900.')

    age = (date.today() - birth_date).days // 365
    if age < 18:
        raise ValueError('You must be at least 18 years old to register.')
