"""
Configuration file for the Real-Time Stress Detection System
Modify these parameters to customize the system behavior
"""

# ==================== MODEL CONFIGURATION ====================

# Emotion Recognition Model
EMOTION_MODEL_PATH = 'emotion_model_best.h5'
IMG_SIZE = 48
BATCH_SIZE = 32
TRAINING_EPOCHS = 50

# Facial Landmark Detector
SHAPE_PREDICTOR_PATH = 'shape_predictor_68_face_landmarks.dat'

# ==================== STRESS CALCULATION ====================

# Calibration Settings
CALIBRATION_FRAMES = 30  # Number of frames for baseline calibration

# Stress Calculation Weights
EYEBROW_STRESS_WEIGHT = 0.6  # Weight for eyebrow-based stress (60%)
EMOTION_STRESS_WEIGHT = 0.4  # Weight for emotion-based stress (40%)

# Exponential function parameter for stress calculation
STRESS_EXPONENTIAL_FACTOR = 3.0

# Emotion to Stress Mapping (0.0 = no stress, 1.0 = maximum stress)
EMOTION_STRESS_MAP = {
    'Angry': 0.9,
    'Fear': 1.0,
    'Sad': 0.7,
    'Surprise': 0.4,
    'Happy': 0.0,
    'Neutral': 0.1
}

# ==================== STRESS LEVEL THRESHOLDS ====================

# Stress level categories
LOW_STRESS_THRESHOLD = 30      # 0-30: Low stress
MODERATE_STRESS_THRESHOLD = 60 # 30-60: Moderate stress
                               # 60-100: High stress

# ==================== DISPLAY SETTINGS ====================

# Colors (BGR format for OpenCV)
COLOR_LOW_STRESS = (0, 255, 0)      # Green
COLOR_MODERATE_STRESS = (0, 255, 255)  # Yellow
COLOR_HIGH_STRESS = (0, 0, 255)     # Red

COLOR_FACE_BOX = (0, 255, 0)        # Green
COLOR_LEFT_EYEBROW = (255, 0, 0)    # Blue
COLOR_RIGHT_EYEBROW = (0, 0, 255)   # Red
COLOR_EYEBROW_LINE = (255, 255, 0)  # Yellow
COLOR_LANDMARKS = (0, 255, 0)       # Green

# Display Panel Settings
INFO_PANEL_POSITION = (10, 10)      # Top-left position
INFO_PANEL_SIZE = (400, 200)        # Width x Height
INFO_PANEL_OPACITY = 0.6            # 0.0 (transparent) to 1.0 (opaque)

# Text Settings
FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE_TITLE = 0.8
FONT_SCALE_NORMAL = 0.7
FONT_SCALE_SMALL = 0.6
FONT_THICKNESS = 2

# ==================== CAMERA SETTINGS ====================

# Camera Configuration
CAMERA_INDEX = 0  # Default camera (usually 0)
MIRROR_CAMERA = True  # Flip camera horizontally for mirror effect

# FPS Calculation
FPS_UPDATE_FREQUENCY = 30  # Calculate FPS every N frames

# ==================== FACIAL LANDMARK POINTS ====================

# Eyebrow landmark indices (dlib 68-point model)
LEFT_EYEBROW_POINTS = list(range(17, 22))   # Points 17-21
RIGHT_EYEBROW_POINTS = list(range(22, 27))  # Points 22-26

# Other facial landmarks (for future features)
LEFT_EYE_POINTS = list(range(36, 42))       # Points 36-41
RIGHT_EYE_POINTS = list(range(42, 48))      # Points 42-47
NOSE_POINTS = list(range(27, 36))           # Points 27-35
MOUTH_POINTS = list(range(48, 68))          # Points 48-67
JAW_POINTS = list(range(0, 17))             # Points 0-16

# ==================== ADVANCED SETTINGS ====================

# Data Augmentation (for training)
AUGMENTATION_ROTATION = 15       # Degrees
AUGMENTATION_SHIFT = 0.1         # Fraction of total width/height
AUGMENTATION_SHEAR = 0.1         # Shear intensity
AUGMENTATION_ZOOM = 0.1          # Zoom range
AUGMENTATION_HORIZONTAL_FLIP = True

# Model Training
LEARNING_RATE = 0.0001
EARLY_STOPPING_PATIENCE = 10
LR_REDUCTION_PATIENCE = 5
LR_REDUCTION_FACTOR = 0.5
MIN_LEARNING_RATE = 1e-7

# Random Seeds (for reproducibility)
RANDOM_SEED = 42

# ==================== EMOTION LABELS ====================

EMOTION_LABELS = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
NUM_EMOTIONS = len(EMOTION_LABELS)

# ==================== DEBUG SETTINGS ====================

# Debug options
DEBUG_MODE = False               # Enable debug logging
SHOW_ALL_LANDMARKS = True        # Show all 68 facial landmarks
SHOW_FPS = True                  # Display FPS counter
SAVE_DEBUG_IMAGES = False        # Save frames for debugging

# Verbose output
VERBOSE_TRAINING = True          # Show detailed training progress
VERBOSE_PREDICTION = False       # Show prediction probabilities
