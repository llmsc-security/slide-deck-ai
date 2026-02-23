#!/bin/bash
# Entrypoint script for SlideDeck AI Docker container
# Starts the Streamlit application

set -e

# Change to the app directory
cd /app

# Start Streamlit on port 11410 (mapped port)
exec streamlit run app.py --server.port=11410 --server.enableCORS=false --server.headless=true
