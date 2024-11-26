#!/bin/sh

# Wait for PostgreSQL database to be ready
echo "Checking if the PostgreSQL host ($POSTGRES_HOST $POSTGRES_DB_PORT) is ready..."
until nc -z -v -w30 $POSTGRES_HOST $(( $POSTGRES_DB_PORT ));
do
    echo 'Waiting for the DB to be ready...'
    sleep 2
done

# SQLAlchemy migrate
ALEMBIC_CONFIG="/usr/src/fastapi/alembic.ini"

echo "Running Alembic migrations..."
alembic -c $ALEMBIC_CONFIG revision --autogenerate
alembic -c $ALEMBIC_CONFIG upgrade head

# docker-compose run --rm migrator
