#!/bin/sh

# SQLAlchemy migrate
ALEMBIC_CONFIG="/usr/src/fastapi/alembic.ini"

echo "Checking for changes before generating a migration..."

# Make sure the migrations folder exists
if [ ! -d "/usr/src/fastapi/alembic/versions" ]; then
    echo "Migrations folder does not exist. Creating it..."
    mkdir -p /usr/src/fastapi/alembic/versions
fi

# Check if the folder is empty
if [ -z "$(ls -A /usr/src/fastapi/alembic/versions)" ]; then
    echo "No existing migrations found. Generating the first migration..."
    alembic -c $ALEMBIC_CONFIG revision --autogenerate -m "initial migration"

    echo "Applying the first migration..."
    alembic -c $ALEMBIC_CONFIG upgrade head
    exit 0
fi

# Generate time migration
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
