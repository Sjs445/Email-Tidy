#!/bin/bash

#========================================================
# This file is the entry point for the python container.
#========================================================

# Confirm the connection with the DB
python /app/pre_start.py

# Run migrations
alembic upgrade head

# Populate initial DB data
python /app/initial_data.py

# Start the app
# NOTE: use --proxy-headers after implementing nginx/traefik container
uvicorn main:app --host 0.0.0.0 --port 8000
