#!bin/bash

set -e

while ! nc -z ${POSTGRES_HOST:-postgres} ${POSTGRES_PORT:-5432}; do
    sleep 0.5
done

alembic upgrade head

python -m services.core.worker &
    exec uvicorn services.core.main:app --host 0.0.0.0 --port 8002
