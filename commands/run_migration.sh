#!/bin/sh

# SQLAlchemy migrate
ALEMBIC_CONFIG="/usr/src/fastapi/alembic.ini"

echo "Checking for changes before generating a migration..."

# Ensure the migrations folder exists
if [ ! -d "/usr/src/fastapi/alembic/versions" ]; then
    echo "Migrations folder does not exist. Creating it..."
    mkdir -p /usr/src/fastapi/alembic/versions
fi

# Check if the alembic_version table exists in the database
if ! psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\dt" | grep -q "alembic_version"; then
    echo "Alembic version table not found. Applying all migrations..."

    # Check if there are existing migration files
    if [ -z "$(ls -A /usr/src/fastapi/alembic/versions)" ]; then
        echo "No migration files found. Generating initial migration..."
        alembic -c $ALEMBIC_CONFIG revision --autogenerate -m "initial migration"
    fi

    echo "Applying all migrations..."
    alembic -c $ALEMBIC_CONFIG upgrade head

    # Run database saver script only if alembic_version table was just created
    echo "Running database saver script..."
    python -m database.data_processing.movies.saver
    echo "Database saver script completed."

    exit 0
fi

# Generate temporary migration
if ! alembic -c $ALEMBIC_CONFIG revision --autogenerate -m "temp_migration"; then
    echo "Error generating migration. Exiting."
    exit 1
fi

# Find the last created migration file
LAST_MIGRATION=$(find /usr/src/fastapi/alembic/versions -type f -printf '%T+ %p\n' | sort | tail -n 1 | awk '{print $2}')

# Check if the migration contains real changes
if grep -q "pass" "$LAST_MIGRATION"; then
    echo "No changes detected. Deleting temporary migration."
    rm "$LAST_MIGRATION"
else
    echo "Changes detected. Applying migration."
    alembic -c $ALEMBIC_CONFIG upgrade head
fi

# Run database saver script
echo "Running database saver script..."
python -m database.data_processing.movies.saver
echo "Database saver script completed."
