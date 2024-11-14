### Init alembic

alembic init alembic

### Make migrations 

alembic revision --autogenerate -m "Your message"

### Migrate

alembic upgrade head

### Downgrade migration

alembic downgrade -1
alembic downgrade -N
alembic downgrade <revision_id>
alembic downgrade base

### Migration history

alembic history
