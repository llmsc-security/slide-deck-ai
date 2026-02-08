#!/bin/bash
# Build and run the SlideDeck AI Docker container
# Port mapping: 11410 (host) -> 8501 (container)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Build the Docker image
echo "Building Docker image..."
docker build -t slide-deck-ai:latest .

# Run the container with port mapping
echo "Starting container..."
docker run -p 11410:8501 \
    --rm \
    --name slide-deck-ai \
    -v "${SCRIPT_DIR}/.streamlit:/app/.streamlit:ro" \
    slide-deck-ai:latest
