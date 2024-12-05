#!/bin/bash
# Load the .env file
set -a
source /app/.env
set +a

# Ensure the db directory exists
mkdir -p /app/db

# Create the database and initialize the schema
sqlite3 /app/db/$DB_NAME < /app/sql/create_meal_table.sql
echo "Database initialized successfully."