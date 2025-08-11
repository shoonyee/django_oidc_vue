#!/bin/bash

# Full Stack App Startup Script
echo "🚀 Starting Full Stack Application..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
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

# Start Django Backend
echo "🐍 Starting Django Backend..."
cd backend

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env file exists, create from example if not
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from env.example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ .env file created. Please update with your settings if needed."
    else
        echo "⚠️  No env.example found. Creating basic .env file..."
        echo "SECRET_KEY=django-insecure-change-this-in-production" > .env
        echo "DEBUG=True" >> .env
        echo "MODE=LOCAL" >> .env
    fi
fi

# Set default mode to LOCAL if not specified
if ! grep -q "MODE=" .env; then
    echo "MODE=LOCAL" >> .env
fi

# Run migrations
echo "🗄️  Running database migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser if none exists
echo "👤 Checking for superuser..."
python3 manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Creating superuser...')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Start Django server
echo "🌐 Starting Django server on http://localhost:8000..."
python3 manage.py runserver &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if ! curl -s http://localhost:8000/api/public/health_check/ > /dev/null; then
    echo "❌ Backend failed to start. Check the logs above."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Backend is running at http://localhost:8000"

# Start Vue Frontend
echo "⚛️  Starting Vue Frontend..."
cd frontend

# Install/update dependencies
echo "📥 Installing Node.js dependencies..."
npm install

# Start development server
echo "🌐 Starting Vue dev server on http://localhost:3000..."
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 5

# Check if frontend is running
if ! curl -s http://localhost:3000 > /dev/null; then
    echo "❌ Frontend failed to start. Check the logs above."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Frontend is running at http://localhost:3000"

# Display status
echo ""
echo "🎉 Both services are running successfully!"
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📍 Frontend App: http://localhost:3000"
echo "📍 Admin Panel: http://localhost:8000/admin (admin/admin123)"
echo "📍 API Docs: http://localhost:8000/api/"
echo ""
echo "🔧 Current Mode: $(cd backend && source venv/bin/activate && python3 manage.py shell -c "from django.conf import settings; print(getattr(settings, 'MODE', 'LOCAL'))")"
echo ""
echo "💡 To switch modes:"
echo "   - LOCAL mode: Edit backend/.env and set MODE=LOCAL"
echo "   - PROD mode: Edit backend/.env and set MODE=PROD"
echo ""
echo "🛑 Press Ctrl+C to stop both services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set trap for cleanup
trap cleanup INT TERM

# Wait for user to stop
wait
