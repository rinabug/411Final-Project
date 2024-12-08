#!/bin/bash

# Load environment variables
set -a
source .env
set +a

# Ensure the db directory exists
mkdir -p db

# Initialize the database
sqlite3 db/movies.db < sql/create_users_table.sql
echo "Database initialized successfully."