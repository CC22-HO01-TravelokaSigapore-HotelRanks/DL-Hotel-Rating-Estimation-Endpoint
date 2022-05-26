#!/bin/bash

# Start redis
redis-server --port 6379 --daemonize yes
  
# Start python
python ./main.py
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?