#!/usr/bin/env bash
# One command to build and start the whole app and, on first run, fill it with demo data.
# Usage: ./start.sh [--no-seed]
set -euo pipefail
cd "$(dirname "$0")"

SEED=auto
[ "${1:-}" = "--no-seed" ] && SEED=no

command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Install Docker Desktop first."; exit 1; }
docker info > /dev/null 2>&1 || { echo "Docker is not running. Start Docker Desktop and try again."; exit 1; }

echo "Building and starting the containers (the first build takes a few minutes)..."
docker compose up -d --build || {
  echo
  echo "Start-up failed. If the error mentions a port, stop whatever uses port 3000."
  exit 1
}

echo "Waiting for the app to answer..."
ready=""
for _ in $(seq 1 60); do
  if curl -sf -o /dev/null http://localhost:3000/api/tags; then ready=yes; break; fi
  sleep 3
done
[ -n "$ready" ] || { echo "The app did not become ready. See: docker compose logs backend"; exit 1; }

if [ "$SEED" = "auto" ]; then
  if [ "$(curl -s 'http://localhost:3000/api/questions?size=1')" = "[]" ]; then
    echo "No data yet, loading the demo data..."
    bash seed/load_seed.sh
  else
    echo "Data already present, skipping the demo data."
  fi
fi

echo
echo "Ready: http://localhost:3000"
