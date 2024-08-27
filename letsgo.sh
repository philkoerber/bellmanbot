#!/bin/bash

# Path to your client directory
CLIENT_DIR="./client"

echo "ok lets go! welcome to...!"

echo "
  _______ _          ____       _ _                       ____        _   
 |__   __| |        |  _ \     | | |                     |  _ \      | |  
    | |  | |__   ___| |_) | ___| | |_ __ ___   __ _ _ __ | |_) | ___ | |_ 
    | |  | '_ \ / _ \  _ < / _ \ | | '_ ` _ \ / _` | '_ \|  _ < / _ \| __|
    | |  | | | |  __/ |_) |  __/ | | | | | | | (_| | | | | |_) | (_) | |_ 
    |_|  |_| |_|\___|____/ \___|_|_|_| |_| |_|\__,_|_| |_|____/ \___/ \__|"
                                                                          
                                                                          

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