#!/bin/bash
set -e
echo "Running tests..."
docker-compose up --build --abort-on-container-exit test
exit_code=$?
docker-compose down
exit $exit_code
