#!/usr/bin/env bash
# Generates the demo data and loads it into the running docker compose stack.
# Safe to re-run: documents use fixed ids and are upserted, users are skipped when they already exist.
set -euo pipefail
cd "$(dirname "$0")"

for c in quora-mongo quora-postgres quora-elasticsearch; do
  docker inspect -f '{{.State.Running}}' "$c" 2>/dev/null | grep -q true \
    || { echo "$c is not running. Start the stack first: docker compose up -d"; exit 1; }
done

if command -v python3 > /dev/null 2>&1 && [ -z "${SEED_USE_DOCKER:-}" ]; then
  python3 generate_seed.py
else
  # no Python on the host: run the generator in a throwaway container instead
  docker run --rm --user "$(id -u):$(id -g)" -v "$PWD":/seed -w /seed python:3.12-slim python generate_seed.py
fi

echo "Loading MongoDB..."
for c in tags questions answers comments likes; do
  docker cp "out/$c.ndjson" "quora-mongo:/tmp/$c.ndjson"
  UPSERT=""
  [ "$c" = "tags" ] && UPSERT="--upsertFields name"
  docker exec quora-mongo mongoimport --quiet --db quora_db --collection "$c" \
    --file "/tmp/$c.ndjson" --mode upsert --numInsertionWorkers 4 $UPSERT
  echo "  $c done"
done

echo "Loading Elasticsearch..."
rm -rf out/es_chunks && mkdir -p out/es_chunks
split -l 4000 out/es_questions.ndjson out/es_chunks/part_
for f in out/es_chunks/part_*; do
  curl -sf -X POST http://localhost:9200/_bulk -H 'Content-Type: application/x-ndjson' --data-binary "@$f" \
    | grep -q '"errors":false' || { echo "Elasticsearch bulk request failed for $f"; exit 1; }
done
curl -sf -X POST http://localhost:9200/questions/_refresh > /dev/null

echo "Loading PostgreSQL users..."
docker exec -i quora-postgres psql -q -U quora -d quora_db -v ON_ERROR_STOP=1 < out/users.sql

echo
echo "Totals now in the databases:"
docker exec quora-mongo mongosh --quiet quora_db --eval \
  'for (const c of ["tags","questions","answers","comments","likes"]) print("  mongo " + c + ": " + db[c].countDocuments())'
echo "  elasticsearch questions: $(curl -s http://localhost:9200/questions/_count | sed -E 's/.*"count":([0-9]+).*/\1/')"
echo "  postgres users: $(docker exec quora-postgres psql -U quora -d quora_db -tAc 'select count(*) from users')"
