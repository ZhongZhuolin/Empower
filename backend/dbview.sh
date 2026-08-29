#!/usr/bin/env bash
# Shows everything in the empower database.
# Usage:  ./dbview.sh            -> show all tables
#         ./dbview.sh reports    -> show just one table
#         ./dbview.sh -c         -> open an interactive psql shell

cd "$(dirname "$0")"
URL=$(grep DATABASE_URL .env | cut -d= -f2- | sed 's|+asyncpg||')

if [ "$1" = "-c" ]; then
    exec psql "$URL"
fi

if [ -n "$1" ]; then
    psql "$URL" -c "\d $1" -c "SELECT * FROM $1 ORDER BY id;"
    exit
fi

for t in users companies watches job_postings reports; do
    echo "=============== $t ==============="
    psql "$URL" -c "SELECT * FROM $t ORDER BY id;"
done
