FROM python:3.10

# Selecting a working directory
WORKDIR /usr/src/fastapi

# Setting environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR off

# Installing dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    postgresql-client \
    && apt-get clean

# Copy dependency files
COPY ./src/poetry.lock .
COPY ./src/pyproject.toml .

# Install Poetry
RUN python -m pip install --upgrade pip && \
    pip install poetry

# Configure Poetry to avoid creating a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies with Poetry
RUN poetry lock --no-update
RUN poetry install --no-root --only main

# Copy the source code
COPY ./src .

# Copy commands
COPY ./commands /commands

# Add execute bit to commands files
RUN chmod +x /commands/*.sh
