# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Option 1: Automated Setup (Recommended)

```bash
# Run the automated setup script
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Download the facial landmark predictor
- Check your dataset

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download facial landmark predictor
curl -O http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
```

## ✅ Test Your Installation

Run the diagnostic test:

```bash
python test_system.py
```

This will verify:
- All packages are installed
- Camera is working
- Required files exist
- Face detection works
- Dataset is ready

## 🎯 Run the Application

### Step 1: (Optional) Train the Model

**Only needed if you want to train from scratch:**

```bash
python emotion_recognition.py
```

Expected time: 30-60 minutes depending on dataset size and hardware.

### Step 2: Run Real-Time Detection

```bash
python eyebrow_detection.py
```

**During first 30 frames**: Remain neutral for calibration
**After calibration**: System will detect stress in real-time

## 🎮 Controls

- **q**: Quit application
- **r**: Recalibrate baseline

## 📊 Understanding the Display

| Element | Description |
|---------|-------------|
| Green box | Detected face |
| Green dots | All facial landmarks |
| Blue/Red dots | Left/Right eyebrows |
| Yellow line | Distance between eyebrows |
| Top panel | Emotion, stress levels, status |
| Colored bar | Visual stress indicator |

## 🎨 Stress Levels

- **0-30** (Green): Low Stress - Relaxed state
- **30-60** (Yellow): Moderate Stress - Mild tension
- **60-100** (Red): High Stress - Significant stress

## ⚠️ Troubleshooting

### Camera not working?
- Check permissions in System Preferences > Security & Privacy > Camera
- Close other apps using the camera (Zoom, Skype, etc.)

### No face detected?
- Ensure good lighting
- Face the camera directly
- Move closer to webcam (50-70cm optimal)

### Model not found?
- Train the model first: `python emotion_recognition.py`
- Or request pre-trained model if available

### Poor accuracy?
- Add more training images to fer2013 dataset
- Ensure images are properly categorized
- Retrain the model

## 📂 Project Files

| File | Purpose |
|------|---------|
| `eyebrow_detection.py` | Main application - Run this! |
| `emotion_recognition.py` | Train the emotion model |
| `test_system.py` | Test installation |
| `config.py` | Customize settings |
| `setup.sh` | Automated setup |

## 🎓 Tips for Best Results

1. **Lighting**: Use even, front-facing light
2. **Position**: Center your face in frame
3. **Distance**: Stay 50-70cm from camera
4. **Calibration**: Be neutral during calibration
5. **Expression**: Be genuine - system detects real expressions

## 🔄 Recalibration

Recalibrate (press 'r') when:
- Lighting changes significantly
- You change your sitting position
- You take a break and return
- Baseline seems inaccurate

## 📈 Next Steps

1. Run the system regularly to understand your stress patterns
2. Add more training data for better accuracy
3. Customize settings in `config.py`
4. Explore future improvements (see README.md)

## 🆘 Need Help?

1. Run diagnostic: `python test_system.py`
2. Check README.md for detailed documentation
3. Review error messages carefully
4. Ensure all dependencies are installed

---

**Ready?** Run `python eyebrow_detection.py` and start detecting stress! 🎯
