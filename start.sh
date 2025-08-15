#!/bin/bash

# Full Stack App Startup Script with Docker
echo "🚀 Starting Full Stack Application with Docker..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running. Please start Docker first."
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Environment check passed"

# Start Backend
echo "🐍 Starting Django Backend..."
cd backend/dockercompose

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo "⚠️  No .env file found in backend directory. Creating from env.example..."
    if [ -f "../env.example" ]; then
        cp ../env.example ../.env
        echo "✅ .env file created from env.example. Please update with your settings if needed."
    else
        echo "❌ No env.example found. Please create a .env file with your database configuration."
        exit 1
    fi
fi

# Start backend services
echo "🔧 Starting backend services..."
docker compose up -d

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 10

# Check backend health
echo "🔍 Checking backend health..."
if curl -s http://localhost:8080/api/public/health_check/ > /dev/null; then
    echo "✅ Backend is healthy and running on port 8080"
else
    echo "⚠️  Backend health check failed, but continuing..."
fi

# Start Frontend
echo "🎨 Starting Vue.js Frontend..."
cd ../../frontend

# Check if node_modules exists, install if not
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Start frontend development server
echo "🔧 Starting frontend development server..."
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to be ready
echo "⏳ Waiting for frontend to be ready..."
sleep 5

# Check frontend health
echo "🔍 Checking frontend health..."
if curl -s http://localhost:8088/ > /dev/null; then
    echo "✅ Frontend is healthy and running on port 8088"
else
    echo "⚠️  Frontend health check failed, but continuing..."
fi

echo ""
echo "🎉 Full Stack Application Started Successfully!"
echo ""
echo "📱 Services:"
echo "   - Frontend: http://localhost:8088"
echo "   - Backend API: http://localhost:8080"
echo "   - Backend Admin: http://localhost:8080/admin/"
echo ""
echo "🔧 Development Commands:"
echo "   - View backend logs: cd backend/dockercompose && docker compose logs -f"
echo "   - View frontend logs: The frontend is running in the foreground"
echo "   - Stop all services: ./stop.sh"
echo ""
echo "📝 Notes:"
echo "   - Frontend runs on port 8088 for development"
echo "   - Backend runs on port 8080"
echo "   - API calls from frontend are automatically proxied to backend"
echo "   - Frontend uses hot-reloading for development"
echo "   - Frontend process ID: $FRONTEND_PID"
echo ""
