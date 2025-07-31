#!/bin/bash
# Script to run API with auto-restart on failure

cd /Users/joshuathomas/Downloads/datastaxproj/QueryGPT

echo "🚀 Starting QueryGPT API with auto-restart..."

while true; do
    echo "Starting API at $(date)"
    python api.py
    
    # If we get here, the API crashed
    echo "❌ API crashed at $(date), restarting in 5 seconds..."
    sleep 5
done