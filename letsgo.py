#!/usr/bin/evn python  

### ----- Imports ----- ###  
import os
import sys

if sys.platform == "win32":
    os.system("")

# Path to your client directory
CLIENT_DIR = "./client"

# Color variables
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color (reset)

print(f"""{BLUE}
            _                     _             
 __ __ _____| |__ ___ _ __  ___  | |_ ___       
 \ V  V / -_) / _/ _ \ '  \/ -_) |  _/ _ \_ _ _ 
  \_/\_/\___|_\__\___/_|_|_\___|  \__\___(_|_|_)
  _______ _          ____       _ _                       ____        _   
 |__   __| |        |  _ \     | | |                     |  _ \      | |  
    | |  | |__   ___| |_) | ___| | |_ __ ___   __ _ _ __ | |_) | ___ | |_ 
    | |  | '_ \ / _ \  _ < / _ \ | | '_ \` _ \ / _\` | '_ \|  _ < / _ \| __|
    | |  | | | |  __/ |_) |  __/ | | | | | | | (_| | | | | |_) | (_) | |_ 
    |_|  |_| |_|\___|____/ \___|_|_|_| |_| |_|\__,_|_| |_|____/ \___/ \__|
      
      {NC}""")

# Check if node_modules directory exists, indicating npm is initialized
if not os.path.exists(CLIENT_DIR):
    print(f"{RED}npm is not initialized in {CLIENT_DIR}. Running npm install...{NC}")
    current_dir = os.getcwd()
    os.chdir(CLIENT_DIR) 
    os.system('npm install')
    os.chdir(current_dir)
    
else: 
    print(f"{GREEN}npm is already initialized in {CLIENT_DIR}{NC}")

# Run Docker Compose
os.system('docker compose up --build')
print(f"{BLUE} Start Docker Compose...")
