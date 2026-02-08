#!/bin/bash
# Entrypoint script for SlideDeck AI Docker container
# Starts the Streamlit application

set -e

# Change to the app directory
cd /app

# Start Streamlit on port 8501
exec streamlit run app.py --server.port=8501 --server.enableCORS=false --server.headless=true
