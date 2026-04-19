#!/bin/bash

# Stress Detection Web App Launcher
echo "========================================"
echo "  Stress Detection Web Application"
echo "========================================"
echo ""

# Virtual environment directory
VENV_DIR="venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Check if Flask is installed in venv
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Installing Flask and dependencies..."
    pip install --upgrade pip
    pip install Flask==2.3.3
    echo "✓ Flask installed"
    echo ""
fi

# Check if emotion model exists
if [ ! -f "emotion_model_best.h5" ]; then
    echo "⚠ Emotion model not found!"
    echo "  Please train the model first by running:"
    echo "  python emotion_recognition.py"
    echo ""
    echo "  Or download a pre-trained model."
    echo ""
fi

echo "🚀 Starting web application..."
echo "📱 Open your browser and go to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

# Run the Flask app
python app.py
