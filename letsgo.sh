#!/bin/bash

# Path to your client directory
CLIENT_DIR="./client"

# Check if node_modules directory exists, indicating npm is initialized
if [ ! -d "$CLIENT_DIR/node_modules" ]; then
  echo "npm is not initialized in $CLIENT_DIR. Running npm install..."
  cd $CLIENT_DIR
  npm install
  cd -
else
  echo "npm is already initialized in $CLIENT_DIR."
fi

# Run Docker Compose
docker compose up --build