#!/bin/bash

# Quick fix for dlib installation issue
# This script installs CMake and necessary build tools for dlib

echo "=========================================="
echo "Dlib Installation Fix"
echo "=========================================="
echo ""

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install Xcode Command Line Tools
echo "Step 1: Checking Xcode Command Line Tools..."
if ! xcode-select -p &> /dev/null; then
    echo "Installing Xcode Command Line Tools..."
    echo "Please follow the prompts in the dialog box..."
    xcode-select --install
    echo "After installation completes, press Enter to continue..."
    read
else
    echo "✓ Xcode Command Line Tools found"
fi
echo ""

# Install Homebrew if not present
echo "Step 2: Checking Homebrew..."
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
    
    echo "✓ Homebrew installed"
else
    echo "✓ Homebrew found"
fi
echo ""

# Install CMake
echo "Step 3: Installing CMake..."
if ! command -v cmake &> /dev/null; then
    brew install cmake
    echo "✓ CMake installed"
else
    echo "✓ CMake already installed: $(cmake --version | head -n1)"
fi
echo ""

# Install boost (optional but helps with dlib)
echo "Step 4: Installing boost libraries..."
brew install boost boost-python3 2>/dev/null || brew upgrade boost boost-python3 2>/dev/null || true
echo "✓ boost installed/updated"
echo ""

# Upgrade pip and setuptools
echo "Step 5: Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel
echo "✓ Build tools upgraded"
echo ""

# Install dlib
echo "Step 6: Installing dlib..."
echo "This will take 5-10 minutes. Please be patient..."
echo ""

pip uninstall dlib -y 2>/dev/null || true  # Remove any failed installation
pip install --no-cache-dir dlib

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ SUCCESS! dlib installed successfully"
    echo "=========================================="
    echo ""
    echo "Now run: python test_system.py"
else
    echo ""
    echo "=========================================="
    echo "✗ dlib installation still failed"
    echo "=========================================="
    echo ""
    echo "Alternative Solution:"
    echo "Use OpenCV for face detection instead of dlib."
    echo ""
    echo "Would you like to:"
    echo "1. Try manual compilation (advanced)"
    echo "2. Use alternative (OpenCV only - no eyebrow detection)"
    echo "3. Use face_recognition library (easier alternative)"
    echo ""
    read -p "Enter choice [1-3]: " choice
    
    case $choice in
        1)
            echo "Manual compilation steps:"
            echo "1. git clone https://github.com/davisking/dlib.git"
            echo "2. cd dlib"
            echo "3. mkdir build && cd build"
            echo "4. cmake .."
            echo "5. cmake --build . --config Release"
            echo "6. cd .."
            echo "7. python setup.py install"
            ;;
        2)
            echo "Creating OpenCV-only version..."
            echo "Note: This will only detect faces, not eyebrows"
            ;;
        3)
            echo "Installing face_recognition (includes dlib precompiled)..."
            pip install face_recognition
            if [ $? -eq 0 ]; then
                echo "✓ face_recognition installed successfully!"
                echo "This includes a precompiled version of dlib"
            fi
            ;;
    esac
fi

echo ""
