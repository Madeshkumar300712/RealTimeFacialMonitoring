# Real-Time Facial Stress Detection System

A comprehensive real-time stress detection system that combines emotion recognition and facial feature analysis to assess stress levels. The system uses deep learning for emotion classification and geometric analysis of eyebrow movements to calculate stress scores.

## 🎯 Overview

This project implements a two-part approach to stress detection:

1. **Emotion Recognition**: A CNN-based model trained on the FER2013 dataset that classifies facial expressions into 6 emotions (Angry, Fear, Happy, Neutral, Sad, Surprise)
2. **Stress Level Calculation**: Analyzes eyebrow contraction and displacement from baseline position to quantify stress levels (0-100 scale)

The system processes real-time webcam feed to:
- Detect faces
- Identify facial landmarks (especially eyebrows)
- Predict emotions
- Calculate stress levels based on eyebrow movement
- Provide visual feedback with stress indicators

## 📁 Project Structure

```
RealTimeFacialMonitoring/
├── fer2013/                          # Dataset directory
│   ├── train/                        # Training images
│   │   ├── Angry/
│   │   ├── Fear/
│   │   ├── Happy/
│   │   ├── Neutral/
│   │   ├── Sad/
│   │   └── Surprise/
│   └── val/                          # Validation images
│       ├── Angry/
│       ├── Fear/
│       ├── Happy/
│       ├── Neutral/
│       ├── Sad/
│       └── Surprise/
├── emotion_recognition.py            # Model training script
├── eyebrow_detection.py             # Real-time detection script
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- Webcam
- macOS, Linux, or Windows

### Step 1: Clone or Navigate to Project Directory

```bash
cd RealTimeFacialMonitoring
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Download Dlib Face Landmark Predictor

Download the pre-trained facial landmark predictor from dlib:

```bash
# Download the predictor file (68 facial landmarks)
curl -O http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

# Extract the file
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
```

The file should be placed in the same directory as `eyebrow_detection.py`.

## 🚀 Usage

### Training the Emotion Recognition Model

**Important**: Only run this if you want to retrain the model from scratch.

```bash
python emotion_recognition.py
```

This will:
- Load images from `fer2013/train` and `fer2013/val` directories
- Train a CNN model with data augmentation
- Save the best model as `emotion_model_best.h5`
- Save the final model as `emotion_model_final.h5`
- Generate training history plot (`training_history.png`)

**Training Parameters:**
- Image size: 48x48 pixels (grayscale)
- Batch size: 32
- Epochs: 50 (with early stopping)
- Optimizer: Adam (learning rate: 0.0001)

### Running Real-Time Stress Detection

**This is the main script to use:**

```bash
python eyebrow_detection.py
```

**Instructions:**
1. Sit straight in front of your webcam
2. Ensure good lighting conditions
3. The system will calibrate for the first 30 frames - **remain neutral** during this time
4. After calibration, the system will start detecting stress levels in real-time

**Controls:**
- **'q'**: Quit the application
- **'r'**: Recalibrate baseline (start calibration again)

## 📊 How It Works

### Emotion Recognition

The emotion recognition model uses a deep CNN architecture:

```
Input (48x48x1) 
→ Conv Block 1 (64 filters)
→ Conv Block 2 (128 filters)
→ Conv Block 3 (256 filters)
→ Conv Block 4 (512 filters)
→ Dense Layers (512, 256)
→ Output (6 classes)
```

Each convolutional block includes:
- 2x Convolutional layers
- Batch Normalization
- Max Pooling
- Dropout

### Stress Level Calculation

#### 1. Eyebrow-Based Stress (60% weight)

The system analyzes eyebrow movement using dlib's 68-point facial landmarks:
- Left eyebrow: landmarks 17-21
- Right eyebrow: landmarks 22-26

**Process:**
1. Calculate distance between left and right eyebrow centers
2. Establish baseline distance during calibration (neutral state)
3. Measure displacement from baseline
4. Apply exponential function: `stress = 100 * (1 - e^(-3 * displacement))`
5. Normalize to 0-100 scale

**Formula:**
```
displacement = (baseline_distance - current_distance) / baseline_distance
eyebrow_stress = 100 * (1 - exp(-3 * max(0, displacement)))
```

#### 2. Emotion-Based Stress (40% weight)

Different emotions contribute differently to stress:
- **Fear**: 100% stress contribution
- **Angry**: 90% stress contribution
- **Sad**: 70% stress contribution
- **Surprise**: 40% stress contribution
- **Neutral**: 10% stress contribution
- **Happy**: 0% stress contribution

**Combined Stress:**
```
total_stress = (0.6 × eyebrow_stress) + (0.4 × emotion_stress)
```

### Stress Level Interpretation

- **0-30**: Low Stress (Green)
- **30-60**: Moderate Stress (Yellow)
- **60-100**: High Stress (Red)

## 📈 Model Accuracy

The emotion recognition model's accuracy depends on the training data quality and quantity. With proper dataset:
- Expected validation accuracy: 60-70%
- The model performs better with clear, well-lit facial images
- Accuracy improves with diverse training data

**Note**: The current implementation is moderately accurate as noted in the project objectives. For better accuracy, ensure you have sufficient training images in each emotion category.

## 🎨 Visual Output

The real-time detection window displays:

1. **Face Detection**: Green rectangle around detected face
2. **Facial Landmarks**: Green dots showing all 68 facial landmarks
3. **Eyebrows**: Blue (left) and red (right) dots highlighting eyebrows
4. **Distance Line**: Yellow line connecting eyebrow centers
5. **Information Panel** (top-left):
   - Detected emotion and confidence
   - Eyebrow-based stress level
   - Total stress level
   - Stress bar (color-coded)
   - Stress status (LOW/MODERATE/HIGH)
6. **FPS Counter**: Top-right corner
7. **Controls**: Bottom of screen

## 🔮 Future Improvements

As outlined in the project objectives, the system can be enhanced by incorporating additional features:

### Planned Features:
1. **Lip Movement Analysis**: Detect tension in lip movements
2. **Head Positioning**: Track head pose changes indicating stress
3. **Eye Blinking**: Analyze blink rate (increased blinking = higher stress)
4. **Gaze Movement**: Track eye movement patterns

### Implementation Strategy:
- Extract additional facial landmarks (eyes: 36-47, lips: 48-67)
- Calculate movement metrics for each feature
- Define weighted combination function
- Create comprehensive stress score

**Example Extended Formula:**
```python
total_stress = (
    0.35 × eyebrow_stress +
    0.25 × emotion_stress +
    0.15 × lip_stress +
    0.10 × head_pose_stress +
    0.10 × blink_stress +
    0.05 × gaze_stress
)
```

## ⚠️ Important Notes

1. **Fakeness Detection**: The system cannot detect if someone is faking emotions - it analyzes actual facial expressions
2. **Calibration**: Always calibrate at the start or when lighting conditions change significantly
3. **Lighting**: Good lighting is crucial for accurate face detection
4. **Distance**: Maintain consistent distance from webcam (approximately 50-70cm)
5. **Model Training**: Only retrain the model if you have a substantial dataset

## 🐛 Troubleshooting

### Issue: "Error loading emotion model"
- **Solution**: Train the model first using `python emotion_recognition.py`

### Issue: "Error loading landmark predictor"
- **Solution**: Download `shape_predictor_68_face_landmarks.dat` as described in installation steps

### Issue: "No face detected"
- **Solution**: Ensure good lighting, face the camera directly, and move closer to the webcam

### Issue: "Low FPS"
- **Solution**: Close other applications, use a more powerful computer, or reduce frame processing frequency

### Issue: Model training fails
- **Solution**: Verify that images exist in `fer2013/train` and `fer2013/val` directories

## 📚 Dependencies

- **OpenCV**: Face detection and video processing
- **Dlib**: Facial landmark detection
- **TensorFlow/Keras**: Deep learning framework for emotion recognition
- **NumPy**: Numerical computations
- **Matplotlib**: Plotting training history

## 📄 License

This project is for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional facial features for stress detection
- Better model architecture
- Enhanced calibration mechanism
- Multi-face support
- Stress history tracking and visualization

## 📧 Contact

For questions or issues, please refer to the project documentation or create an issue in the repository.

---

**Remember**: This system is designed for research and educational purposes. It should not be used as the sole tool for medical or clinical stress assessment.
