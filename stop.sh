#!/bin/bash

echo "🛑 Stopping Full Stack Application..."

# Kill Django processes
echo "🐍 Stopping Django backend..."
pkill -f "python.*manage.py runserver" 2>/dev/null
pkill -f "python3.*manage.py runserver" 2>/dev/null

# Kill Vue processes
echo "⚛️  Stopping Vue frontend..."
pkill -f "npm run dev" 2>/dev/null
pkill -f "vite" 2>/dev/null

# Kill any remaining processes on the ports
echo "🔌 Releasing ports..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

echo "✅ All services stopped"
echo "📍 Ports 8000 and 3000 are now free"
