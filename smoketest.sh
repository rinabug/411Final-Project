#!/usr/bin/env bash

python3 app.py > flask.log 2>&1 &

APP_PID=$!
echo "Flask app started with PID: $APP_PID"
tail -f flask.log &  # Continuously monitor Flask logs

# Fail on any command error
set -e

BASE_URL="http://localhost:5000"
TEST_USERNAME="testuser_$(date +%s)"
TEST_PASSWORD="testpassword"

# Function to clean up background process
cleanup() {
    if [ -n "$APP_PID" ] && ps -p "$APP_PID" > /dev/null; then
        echo "Stopping Flask app..."
        kill "$APP_PID"
        wait "$APP_PID" || true
    fi
}

# Run cleanup function on EXIT to ensure background process is stopped
trap cleanup EXIT

echo "Starting the Flask app in background..."
# Start the Flask app in the background
# Adjust the command below to how you normally start your Flask app
python3 app.py &

APP_PID=$!
echo "Flask app started with PID: $APP_PID"

# Wait for the app to become responsive
echo "Waiting for the Flask app to respond..."
ATTEMPTS=0
MAX_ATTEMPTS=10
until curl -sSf "$BASE_URL/health" > /dev/null || [ $ATTEMPTS -eq $MAX_ATTEMPTS ]; do
    ATTEMPTS=$((ATTEMPTS+1))
    echo "Attempt $ATTEMPTS/$MAX_ATTEMPTS: Waiting for app to start..."
    sleep 2
done

if [ $ATTEMPTS -eq $MAX_ATTEMPTS ]; then
    echo "Flask app did not become responsive in time."
    exit 1
fi

echo "Flask app is responsive. Running smoke tests..."

echo "Creating a new user..."
CREATE_ACCOUNT_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
  -d "{\"username\": \"${TEST_USERNAME}\", \"password\": \"${TEST_PASSWORD}\"}" \
  "$BASE_URL/create_account")

echo "$CREATE_ACCOUNT_RESPONSE" 
echo "$CREATE_ACCOUNT_RESPONSE" | grep -q "Account created successfully."

echo "Logging in the newly created user..."
LOGIN_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
  -d "{\"username\": \"${TEST_USERNAME}\", \"password\": \"${TEST_PASSWORD}\"}" \
  "$BASE_URL/login")

echo "$LOGIN_RESPONSE" 
echo "$LOGIN_RESPONSE" | grep -q "Login successful."

echo "Requesting recommendations..."
RECOMMEND_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
  -d "{\"username\": \"${TEST_USERNAME}\", \"genre\": \"Action\", \"age_rating\": \"PG-13\", \"year_range\": \"2016-2020\"}" \
  "$BASE_URL/recommend")

echo "$RECOMMEND_RESPONSE" 
echo "$RECOMMEND_RESPONSE" | grep -q "recommendations"

echo "Logging in again to ensure previously recommended movies are shown..."
LOGIN_AGAIN_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
  -d "{\"username\": \"${TEST_USERNAME}\", \"password\": \"${TEST_PASSWORD}\"}" \
  "$BASE_URL/login")

echo "$LOGIN_AGAIN_RESPONSE"
echo "$LOGIN_AGAIN_RESPONSE" | grep -q "previous_recommendations"

echo "Smoke test passed successfully!"
