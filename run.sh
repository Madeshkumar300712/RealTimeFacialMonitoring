#!/bin/bash

# Quick launcher script for Real-Time Stress Detection
# Provides menu-driven interface for common tasks

clear
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Real-Time Facial Stress Detection System              ║"
echo "║                  Quick Launcher                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo ""
    echo "Please run setup first:"
    echo "  ./setup.sh"
    echo ""
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "What would you like to do?"
echo ""
echo "  1) Run Stress Detection (Main Application)"
echo "  2) Train Emotion Model"
echo "  3) Test System"
echo "  4) View Documentation"
echo "  5) Exit"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "Starting Real-Time Stress Detection..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        python eyebrow_detection.py
        ;;
    2)
        echo ""
        echo "Starting Model Training..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "⚠️  This may take 30-60 minutes"
        echo ""
        read -p "Continue? (y/n): " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            python emotion_recognition.py
        else
            echo "Training cancelled."
        fi
        ;;
    3)
        echo ""
        echo "Running System Tests..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        python test_system.py
        ;;
    4)
        echo ""
        echo "Documentation Files:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "📘 README.md          - Complete documentation"
        echo "🚀 QUICKSTART.md      - Quick start guide"
        echo "📊 PROJECT_SUMMARY.md - Project overview"
        echo ""
        echo "Would you like to view one?"
        echo "  1) README.md"
        echo "  2) QUICKSTART.md"
        echo "  3) PROJECT_SUMMARY.md"
        echo "  4) Back to main menu"
        echo ""
        read -p "Enter choice [1-4]: " doc_choice
        case $doc_choice in
            1)
                less README.md
                ;;
            2)
                less QUICKSTART.md
                ;;
            3)
                less PROJECT_SUMMARY.md
                ;;
            4)
                echo "Returning to main menu..."
                ;;
            *)
                echo "Invalid choice."
                ;;
        esac
        ;;
    5)
        echo ""
        echo "Goodbye! 👋"
        echo ""
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Please run the script again."
        echo ""
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press Enter to exit..."
