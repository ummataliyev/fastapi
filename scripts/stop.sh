#!/bin/bash

PID=$(lsof -ti :8000)

if [ -z "$PID" ]; then
  echo "No FastAPI server running on port 8000"
else
  kill -9 $PID
  echo "FastAPI server stopped"
fi
