#!/bin/bash

set -e

until PGPASSWORD=${POSTGRES_PASSWORD:-1234} pg_isready -h ${POSTGRES_HOST:-database} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-postgres}; do
  echo "Waiting for PG"
  sleep 2
done

echo "PG is ready"

echo "Running migrations"
alembic upgrade head


python -m services.core.worker.worker &
    uvicorn services.core.main:app --host 0.0.0.0 --port 8002