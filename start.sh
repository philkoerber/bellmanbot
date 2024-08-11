#!/bin/bash

# start python script in a subshell
( python3 server/server.py > /dev/null 2> /dev/null & ) 

cd client && npm run dev & 
