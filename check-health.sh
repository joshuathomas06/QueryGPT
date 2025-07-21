#!/bin/bash
echo "🔍 Checking QueryGPT health..."

# Check Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Check containers
if docker-compose ps | grep -q "Up"; then
    echo "✅ Docker containers are running"
else
    echo "⚠️  Containers not running. Starting them..."
    docker-compose up -d
    sleep 10
fi

# Check backend health
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✅ Backend API is healthy"
else
    echo "❌ Backend API is not responding"
fi

# Check frontend
if curl -s -o /dev/null -w "%{http_code}" http://localhost/ | grep -q "200"; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend is not accessible"
fi

echo ""
echo "🌐 Access your app at: http://localhost"