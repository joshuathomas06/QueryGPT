#!/bin/bash
# Production-ready QueryGPT startup script

# Set working directory
cd /Users/joshuathomas/Downloads/datastaxproj/QueryGPT

# Kill any existing processes
echo "🔄 Cleaning up existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
pkill -f "python api.py" 2>/dev/null
pkill -f "npm start" 2>/dev/null

# Function to start API with monitoring
start_api() {
    echo "🚀 Starting API server..."
    while true; do
        python api.py 2>&1 | tee -a api_production.log
        echo "❌ API crashed at $(date), restarting in 5 seconds..." | tee -a api_production.log
        sleep 5
    done
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting frontend..."
    cd frontend
    npm start 2>&1 | tee -a ../frontend_production.log
}

# Start API in background with auto-restart
start_api &
API_PID=$!

# Wait for API to be ready
echo "⏳ Waiting for API to initialize..."
for i in {1..60}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ API is ready!"
        break
    fi
    sleep 2
done

# Start frontend in background
start_frontend &
FRONTEND_PID=$!

echo ""
echo "✅ QueryGPT is starting up!"
echo "📊 API: http://localhost:8000 (PID: $API_PID)"
echo "🌐 Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "📝 Logs:"
echo "   - API: tail -f api_production.log"
echo "   - Frontend: tail -f frontend_production.log"
echo ""
echo "🛑 To stop: Press Ctrl+C or run: kill $API_PID $FRONTEND_PID"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down QueryGPT..."
    kill $API_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    echo "✅ QueryGPT stopped"
    exit 0
}

# Set up cleanup on script exit
trap cleanup EXIT INT TERM

# Keep script running
echo "🔄 Services are running. Press Ctrl+C to stop."
wait