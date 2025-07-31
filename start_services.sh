#!/bin/bash
# Script to start both QueryGPT services

echo "🚀 Starting QueryGPT Services..."

# Function to check if port is in use
check_port() {
    lsof -i :$1 > /dev/null 2>&1
    return $?
}

# Kill any existing processes on our ports
if check_port 8000; then
    echo "⚠️  Port 8000 is in use, stopping existing process..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
fi

if check_port 3000; then
    echo "⚠️  Port 3000 is in use, stopping existing process..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null
fi

# Start API server in background
echo "🔧 Starting API server on port 8000..."
cd /Users/joshuathomas/Downloads/datastaxproj/QueryGPT
python api.py &
API_PID=$!
echo "API server PID: $API_PID"

# Wait for API to be ready
echo "⏳ Waiting for API to initialize..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ API server is ready!"
        break
    fi
    sleep 2
done

# Start frontend
echo "🎨 Starting frontend on port 3000..."
cd /Users/joshuathomas/Downloads/datastaxproj/QueryGPT/frontend
npm start &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "✅ Services starting..."
echo "📊 API: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "⚠️  Keep this terminal open. Press Ctrl+C to stop all services."
echo ""

# Function to cleanup on exit
cleanup() {
    echo "🛑 Stopping services..."
    kill $API_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    echo "✅ Services stopped"
}

# Set up cleanup on script exit
trap cleanup EXIT

# Wait for user to stop
wait