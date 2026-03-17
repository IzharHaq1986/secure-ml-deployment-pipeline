#!/usr/bin/env bash

set -euo pipefail

# Start the Compose deployment in detached mode
docker compose up --build -d

# Allow the container a few seconds to initialize
sleep 5

# Validate the deployed health endpoint
curl --fail http://localhost:8000/health

echo
echo "Deployment smoke test passed."

# Show current container status for visibility
docker ps --filter "name=secure-ml-api"
