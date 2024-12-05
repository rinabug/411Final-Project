#!/bin/bash

# Check if CREATE_DB is true
if [ "$CREATE_DB" = "true" ]; then
    echo "Initializing the database..."

    # Ensure the database directory exists
    mkdir -p "$(dirname "$DB_PATH")"

    # Run the SQL script to initialize the database
    sqlite3 "$DB_PATH" < "$SQL_CREATE_TABLE_PATH"

    echo "Database initialized at $DB_PATH."
else
    echo "CREATE_DB is set to false. Skipping database initialization."
fi