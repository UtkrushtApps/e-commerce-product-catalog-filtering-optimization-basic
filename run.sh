#!/bin/bash
set -e
cd /root/task
echo "Starting E-commerce Product Catalog Environment..."
docker-compose up -d

# Wait for PostgreSQL to be ready
RETRIES=30
for i in $(seq 1 $RETRIES); do
  if docker exec $(docker-compose ps -q postgres) pg_isready -U fastapi_user -d ecommerce_db | grep "accepting connections"; then
    echo "Postgres is up!"
    break
  else
    if [ $i -eq $RETRIES ]; then
      echo "Failed to start PostgreSQL." >&2
      exit 1
    fi
    sleep 2
  fi
done

# Wait for FastAPI to be up
echo "Waiting for FastAPI to be up..."
COUNT=0
while [ $COUNT -lt 30 ]; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs || true)
  if [ "$STATUS" = "200" ]; then
    echo "FastAPI is up!"
    break
  fi
  COUNT=$((COUNT+1))
  sleep 2
done
if [ $COUNT -eq 30 ]; then
  echo "FastAPI app did not start successfully." >&2
  exit 1
else
  echo "E-commerce FastAPI Backend & DB Ready."
fi

docker-compose ps