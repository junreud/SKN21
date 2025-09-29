#!/bin/bash
# Build script for Solitaire Game - Cross Platform

set -e  # Exit on any error

echo "🃏 Building Solitaire Game..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ from https://python.org"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "solitaire_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv solitaire_env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source solitaire_env/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install pygame==2.6.1 pyinstaller==6.16.0

echo "Creating executable..."

# For macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Building for macOS..."
    pyinstaller --onedir --windowed --name "Solitaire" solitaire_pygame.py
    
    echo
    echo "✅ Build complete!"
    echo "📦 Your Solitaire.app is in the 'dist' folder"
    echo "📊 App bundle size: approximately 20-25 MB"
    echo
    echo "🚀 To distribute:"
    echo "1. Copy dist/Solitaire.app to Applications folder"
    echo "2. Or zip the .app file and share it"
    echo "3. Recipients can double-click to run (no Python needed!)"
    
    # Optional: Create DMG
    read -p "Create DMG installer? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Creating DMG..."
        if command -v hdiutil &> /dev/null; then
            hdiutil create -volname "Solitaire Game" -srcfolder dist/Solitaire.app -ov -format UDZO dist/Solitaire.dmg
            echo "📦 DMG created: dist/Solitaire.dmg"
        else
            echo "⚠️  hdiutil not available. DMG creation skipped."
        fi
    fi

# For Linux
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Building for Linux..."
    pyinstaller --onefile --windowed --name "Solitaire" solitaire_pygame.py
    
    echo
    echo "✅ Build complete!"
    echo "📦 Your Solitaire executable is in the 'dist' folder"
    echo "📊 File size: approximately 15-20 MB"
    echo
    echo "🚀 To distribute:"
    echo "1. Copy dist/Solitaire to any Linux computer"
    echo "2. Make sure it's executable: chmod +x Solitaire"
    echo "3. Run with: ./Solitaire"

# For Windows (via WSL or similar)
else
    echo "Building for current platform..."
    pyinstaller --onefile --windowed --name "Solitaire" solitaire_pygame.py
    
    echo
    echo "✅ Build complete!"
    echo "📦 Check the 'dist' folder for your executable"
fi

echo
echo "🎮 Game features:"
echo "- Classic Klondike Solitaire"
echo "- Beautiful graphics"
echo "- No installation required"
echo "- Cross-platform compatibility"