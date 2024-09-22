#!/bin/bash

# Path to your client directory
CLIENT_DIR="./client"

# Color variables
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color (reset)

echo -e "${BLUE}
             _                    _             
 __ __ _____| |__ ___ _ __  ___  | |_ ___       
 \ V  V / -_) / _/ _ \ '  \/ -_) |  _/ _ \_ _ _ 
  \_/\_/\___|_\__\___/_|_|_\___|  \__\___(_|_|_)
  _______ _          ____       _ _                       ____        _   
 |__   __| |        |  _ \     | | |                     |  _ \      | |  
    | |  | |__   ___| |_) | ___| | |_ __ ___   __ _ _ __ | |_) | ___ | |_ 
    | |  | '_ \ / _ \  _ < / _ \ | | '_ \` _ \ / _\` | '_ \|  _ < / _ \| __|
    | |  | | | |  __/ |_) |  __/ | | | | | | | (_| | | | | |_) | (_) | |_ 
    |_|  |_| |_|\___|____/ \___|_|_|_| |_| |_|\__,_|_| |_|____/ \___/ \__|
${NC}"

# Check if node_modules directory exists, indicating npm is initialized
if [ ! -d "$CLIENT_DIR/node_modules" ]; then
  echo -e "${RED}npm is not initialized in $CLIENT_DIR. Running npm install...${NC}"
  cd $CLIENT_DIR
  npm install
  cd -
else
  echo -e "${GREEN}npm is already initialized in $CLIENT_DIR.${NC}"
fi

# Run Docker Compose
docker compose up --build
