# Movie Database Project

This project is a movie database management system with asynchronous interaction with PostgreSQL, Alembic migrations for database management, and tools for importing data from CSV files. It uses SQLAlchemy for ORM and provides modular repositories and services for CRUD operations.

## Project Structure

```
├── alembic/                  # Database migrations
│   └── versions/             # Alembic migration versions
├── config/                   # Project settings
├── data_processing/          # Modules for data saving and cleaning
├── database/                 # Database configurations, models, and validators
│   ├── exceptions/           # Custom exceptions for database errors
│   ├── listeners/            # Event listeners for models
│   ├── models/               # SQLAlchemy database models
│   ├── session.py            # Database session setup
│   └── validators/           # Data validation for models
├── dto/                      # Data Transfer Objects (DTO) for data handling
├── files/                    # CSV files for data import
├── mappers/                  # Mappers for converting CSV data to DTOs
├── repositories/             # Repositories for CRUD operations
├── docker-compose.yml        # Docker Compose configuration
└── requirements.txt          # Project dependencies
```

## Setup

### Step 1: Install Docker

1. **Download Docker Desktop**: Go to [Docker's official website](https://www.docker.com/products/docker-desktop) and download Docker Desktop for your operating system.
2. **Install Docker**: Follow the installation steps provided by Docker.
3. **Verify Docker Installation**:
   ```bash
   docker --version
   ```
   This should display the installed version of Docker.

4. **Start Docker**: Open Docker Desktop and start Docker.

### Step 2: Set Up a Virtual Environment

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```
2. **Activate the virtual environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
3. **Install project dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Configure Environment Variables

Create a `.env` file in the root directory with the following configuration:

```env
POSTGRES_DB=movies_db
POSTGRES_DB_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=some_password
POSTGRES_HOST=localhost

PGADMIN_DEFAULT_EMAIL=admin@gmail.com
PGADMIN_DEFAULT_PASSWORD=admin
```

### Step 4: Start Docker Services

Use Docker Compose to start the PostgreSQL and pgAdmin services:

```bash
docker-compose up -d
```

- **pgAdmin** will be accessible at [http://localhost:3333](http://localhost:3333).
- You can log in to pgAdmin with the email and password specified in the `.env` file.

### Step 5: Apply Migrations

1. Initialize the database by running all migrations:
   ```bash
   alembic upgrade head
   ```

### Step 6: Run Data Import and Cleaning

1. To load data from a CSV file in `files/movies.csv`, use:
   ```bash
   python data_processing/movie_saver.py
   ```

2. To clean the movie data from the database, use:
   ```bash
   python data_processing/movie_cleaner.py
   ```

## Database Migrations with Alembic

The project uses Alembic to manage database migrations. Migration files are in the `alembic/versions/` directory.

### Common Alembic Commands

1. **Create a new migration**:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

2. **Apply migrations**:
   ```bash
   alembic upgrade head
   ```

3. **Revert the last migration**:
   ```bash
   alembic downgrade -1
   ```

## Using Docker Commands

To manage Docker containers, you can use the following commands:

1. **Stop Docker containers**:
   ```bash
   docker-compose down
   ```

2. **View running containers**:
   ```bash
   docker ps
   ```

3. **Restart Docker services**:
   ```bash
   docker-compose up -d
   ```

## License

This project is provided under the MIT License.

