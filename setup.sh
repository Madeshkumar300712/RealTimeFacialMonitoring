#!/bin/bash

# Setup script for Real-Time Stress Detection System
# This script automates the installation process

echo "=========================================="
echo "Real-Time Stress Detection Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "Error: Python 3.8 or higher is required"
    exit 1
fi
echo "✓ Python version OK"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Check for CMake (required for dlib)
echo "Checking for CMake..."
if ! command -v cmake &> /dev/null; then
    echo "CMake not found. Installing CMake via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install cmake
        echo "✓ CMake installed"
    else
        echo "⚠️  Homebrew not found. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        brew install cmake
        echo "✓ CMake installed"
    fi
else
    cmake_version=$(cmake --version | head -n1)
    echo "✓ CMake found: $cmake_version"
fi
echo ""

# Install requirements
echo "Installing dependencies..."
echo "This may take several minutes..."
echo "Note: dlib compilation may take 5-10 minutes..."
echo ""

# Install non-dlib packages first
echo "Installing core packages..."
pip install numpy opencv-python tensorflow matplotlib Pillow scipy --quiet
echo "✓ Core packages installed"
echo ""

# Install dlib separately with better error handling
echo "Installing dlib (this may take 5-10 minutes)..."
if pip install dlib; then
    echo "✓ dlib installed successfully"
else
    echo "✗ dlib installation failed"
    echo ""
    echo "Trying alternative installation method..."
    echo "Installing build dependencies..."
    brew install boost boost-python3 2>/dev/null || true
    
    if pip install dlib --no-cache-dir; then
        echo "✓ dlib installed successfully with alternative method"
    else
        echo "✗ dlib installation failed"
        echo ""
        echo "Manual installation required:"
        echo "1. Install Xcode Command Line Tools: xcode-select --install"
        echo "2. Install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo "3. Install CMake and boost: brew install cmake boost boost-python3"
        echo "4. Install dlib: pip install dlib"
        echo ""
        echo "Or use face_recognition library as alternative (easier to install):"
        echo "pip install face_recognition"
        echo ""
        read -p "Continue without dlib? (y/n): " continue_choice
        if [ "$continue_choice" != "y" ] && [ "$continue_choice" != "Y" ]; then
            exit 1
        fi
    fi
fi
echo ""

# Download dlib facial landmark predictor
echo "Checking for dlib facial landmark predictor..."
if [ -f "shape_predictor_68_face_landmarks.dat" ]; then
    echo "✓ Facial landmark predictor already exists"
else
    echo "Downloading facial landmark predictor..."
    echo "File size: ~100MB, this may take a few minutes..."
    
    if command -v curl &> /dev/null; then
        curl -L -O http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
    elif command -v wget &> /dev/null; then
        wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
    else
        echo "Error: Neither curl nor wget is available"
        echo "Please manually download from:"
        echo "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
        exit 1
    fi
    
    echo "Extracting facial landmark predictor..."
    bunzip2 shape_predictor_68_face_landmarks.dat.bz2
    
    if [ -f "shape_predictor_68_face_landmarks.dat" ]; then
        echo "✓ Facial landmark predictor downloaded and extracted"
    else
        echo "Error: Failed to extract facial landmark predictor"
        exit 1
    fi
fi
echo ""

# Check dataset
echo "Checking dataset..."
if [ -d "fer2013/train" ] && [ -d "fer2013/val" ]; then
    train_count=$(find fer2013/train -type f -name "*.jpg" -o -name "*.png" | wc -l)
    val_count=$(find fer2013/val -type f -name "*.jpg" -o -name "*.png" | wc -l)
    echo "✓ Dataset found"
    echo "  - Training images: $train_count"
    echo "  - Validation images: $val_count"
    
    if [ $train_count -lt 100 ]; then
        echo "⚠ Warning: Low number of training images. Model accuracy may be limited."
    fi
else
    echo "⚠ Warning: Dataset not found or incomplete"
    echo "Please ensure images are placed in:"
    echo "  - fer2013/train/{Angry,Fear,Happy,Neutral,Sad,Surprise}/"
    echo "  - fer2013/val/{Angry,Fear,Happy,Neutral,Sad,Surprise}/"
fi
echo ""

# Create directories for output
echo "Creating output directories..."
mkdir -p models
mkdir -p logs
mkdir -p debug_images
echo "✓ Output directories created"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Activate the virtual environment (if not already active):"
echo "   source venv/bin/activate"
echo ""
echo "2. (Optional) Train the emotion recognition model:"
echo "   python emotion_recognition.py"
echo ""
echo "3. Run the real-time stress detection:"
echo "   python eyebrow_detection.py"
echo ""
echo "For more information, see README.md"
echo ""
