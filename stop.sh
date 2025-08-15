#!/bin/bash

# Full Stack App Stop Script
echo "🛑 Stopping Full Stack Application..."

# Stop Frontend
echo "🎨 Stopping Vue.js Frontend..."
# Find and kill the frontend npm process
FRONTEND_PID=$(pgrep -f "npm run dev")
if [ ! -z "$FRONTEND_PID" ]; then
    echo "🔄 Stopping frontend process (PID: $FRONTEND_PID)..."
    kill $FRONTEND_PID
    sleep 2
    # Force kill if still running
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "🔄 Force killing frontend process..."
        kill -9 $FRONTEND_PID
    fi
    echo "✅ Frontend stopped"
else
    echo "⚠️  Frontend process not found"
fi

# Stop Backend
echo "🐍 Stopping Django Backend..."
cd backend/dockercompose
if [ -f "docker-compose.yml" ]; then
    docker compose down
    echo "✅ Backend stopped"
else
    echo "⚠️  Backend docker-compose.yml not found"
fi

# Return to root directory
cd ../..

echo ""
echo "🎉 All services stopped successfully!"
echo ""
echo "💡 To start services again, run: ./start.sh"
echo "💡 To view logs: cd backend/dockercompose && docker compose logs -f"
echo "💡 Frontend logs are displayed in the terminal where start.sh was run"
echo ""
