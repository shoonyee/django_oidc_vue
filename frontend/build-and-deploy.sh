#!/bin/bash

# Frontend Build and Deploy Script
# This script builds the frontend locally and then creates a Docker image

set -e  # Exit on any error

echo "🚀 Starting frontend build and Docker image creation..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 22+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
else
    echo "📦 Dependencies already installed"
fi

# Clean previous build
if [ -d "dist" ]; then
    echo "🧹 Cleaning previous build..."
    rm -rf dist
fi

# Build production bundle
echo "🔨 Building production bundle..."
npm run build

# Verify build output
if [ ! -d "dist" ]; then
    echo "❌ Build failed - dist folder not created"
    exit 1
fi

echo "✅ Build completed successfully"
echo "📁 Build output:"
ls -la dist/

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t frontend-openshift .

echo "✅ Docker image built successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Test locally: docker run -d --name frontend-test -p 8088:8088 frontend-openshift"
echo "2. Test health: curl http://localhost:8088/health"
echo "3. Tag for registry: docker tag frontend-openshift your-registry/namespace/frontend:latest"
echo "4. Push to registry: docker push your-registry/namespace/frontend:latest"
echo "5. Deploy to OpenShift"
