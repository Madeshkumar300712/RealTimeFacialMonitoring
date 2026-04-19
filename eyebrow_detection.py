"""
Real-Time Stress Detection using Facial Features
Detects stress levels based on eyebrow contraction and displacement
Combines with emotion recognition for comprehensive stress analysis
"""

import cv2
import numpy as np
import dlib
from tensorflow import keras
import time
from collections import deque

# Configuration
EMOTION_MODEL_PATH = 'emotion_model_best.h5'
SHAPE_PREDICTOR_PATH = 'shape_predictor_68_face_landmarks.dat'  # Download from dlib
IMG_SIZE = 48

# Emotion labels
EMOTION_LABELS = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Stressed emotions (weighted for stress calculation)
STRESS_EMOTIONS = {
    'Angry': 0.9,
    'Fear': 1.0,
    'Sad': 0.7,
    'Surprise': 0.4,
    'Happy': 0.0,
    'Neutral': 0.1
}

class StressDetector:
    def __init__(self):
        """
        Initialize the stress detector with emotion model and face landmarks
        """
        print("Initializing Stress Detector...")
        
        # Load emotion recognition model
        try:
            self.emotion_model = keras.models.load_model(EMOTION_MODEL_PATH)
            print(f"✓ Emotion model loaded from {EMOTION_MODEL_PATH}")
        except Exception as e:
            print(f"✗ Error loading emotion model: {e}")
            print("Please train the model first by running emotion_recognition.py")
            self.emotion_model = None
        
        # Initialize face detector and landmark predictor
        self.face_detector = dlib.get_frontal_face_detector()
        
        try:
            self.landmark_predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
            print(f"✓ Facial landmark predictor loaded")
        except Exception as e:
            print(f"✗ Error loading landmark predictor: {e}")
            print("Please download 'shape_predictor_68_face_landmarks.dat' from:")
            print("http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
            self.landmark_predictor = None
        
        # Initialize baseline eyebrow distance (calibrated during first few frames)
        self.baseline_eyebrow_distance = None
        self.calibration_distances = deque(maxlen=30)  # Store first 30 frames for calibration
        self.is_calibrated = False
        
        print("Initialization complete!\n")
    
    def get_eyebrow_points(self, landmarks):
        """
        Extract eyebrow landmark points
        Left eyebrow: points 17-21
        Right eyebrow: points 22-26
        """
        left_eyebrow = []
        right_eyebrow = []
        
        # Left eyebrow points (17-21)
        for i in range(17, 22):
            left_eyebrow.append((landmarks.part(i).x, landmarks.part(i).y))
        
        # Right eyebrow points (22-26)
        for i in range(22, 27):
            right_eyebrow.append((landmarks.part(i).x, landmarks.part(i).y))
        
        return np.array(left_eyebrow), np.array(right_eyebrow)
    
    def calculate_eyebrow_distance(self, left_eyebrow, right_eyebrow):
        """
        Calculate the distance between left and right eyebrows
        Uses the center points of each eyebrow
        """
        left_center = np.mean(left_eyebrow, axis=0)
        right_center = np.mean(right_eyebrow, axis=0)
        
        distance = np.linalg.norm(left_center - right_center)
        return distance
    
    def calibrate_baseline(self, distance):
        """
        Calibrate baseline eyebrow distance from initial neutral frames
        """
        self.calibration_distances.append(distance)
        
        if len(self.calibration_distances) >= 30 and not self.is_calibrated:
            self.baseline_eyebrow_distance = np.mean(self.calibration_distances)
            self.is_calibrated = True
            print(f"\n✓ Calibration complete! Baseline distance: {self.baseline_eyebrow_distance:.2f}")
            print("Starting stress detection...\n")
    
    def calculate_stress_level_from_eyebrows(self, current_distance):
        """
        Calculate stress level based on eyebrow contraction
        Stress increases when eyebrows move closer together (frowning)
        """
        if not self.is_calibrated or self.baseline_eyebrow_distance is None:
            return 0
        
        # Calculate displacement from baseline
        displacement = self.baseline_eyebrow_distance - current_distance
        
        # Normalize displacement (positive means eyebrows closer = more stress)
        normalized_displacement = displacement / self.baseline_eyebrow_distance
        
        # Calculate stress using exponential function
        # Stress increases exponentially with eyebrow contraction
        stress_raw = 100 * (1 - np.exp(-3 * max(0, normalized_displacement)))
        
        # Clamp between 0 and 100
        stress_level = np.clip(stress_raw, 0, 100)
        
        return stress_level
    
    def predict_emotion(self, face_roi):
        """
        Predict emotion from face region of interest
        """
        if self.emotion_model is None:
            return None, 0.0
        
        # Preprocess face for emotion model
        face_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        face_resized = cv2.resize(face_gray, (IMG_SIZE, IMG_SIZE))
        face_normalized = face_resized / 255.0
        face_input = np.expand_dims(face_normalized, axis=0)
        face_input = np.expand_dims(face_input, axis=-1)
        
        # Predict emotion
        emotion_probs = self.emotion_model.predict(face_input, verbose=0)[0]
        emotion_idx = np.argmax(emotion_probs)
        emotion_label = EMOTION_LABELS[emotion_idx]
        confidence = emotion_probs[emotion_idx]
        
        return emotion_label, confidence
    
    def calculate_combined_stress(self, eyebrow_stress, emotion):
        """
        Combine eyebrow-based stress with emotion-based stress
        """
        if emotion is None:
            return eyebrow_stress
        
        emotion_stress_weight = STRESS_EMOTIONS.get(emotion, 0.5)
        
        # Weighted combination: 60% eyebrow, 40% emotion
        combined_stress = (0.6 * eyebrow_stress) + (0.4 * emotion_stress_weight * 100)
        
        return np.clip(combined_stress, 0, 100)
    
    def draw_landmarks(self, frame, landmarks, left_eyebrow, right_eyebrow):
        """
        Draw facial landmarks and eyebrows on frame
        """
        # Draw all facial landmarks
        for i in range(68):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
        
        # Highlight eyebrows
        for point in left_eyebrow:
            cv2.circle(frame, tuple(point.astype(int)), 3, (255, 0, 0), -1)
        for point in right_eyebrow:
            cv2.circle(frame, tuple(point.astype(int)), 3, (0, 0, 255), -1)
        
        # Draw line between eyebrow centers
        left_center = np.mean(left_eyebrow, axis=0).astype(int)
        right_center = np.mean(right_eyebrow, axis=0).astype(int)
        cv2.line(frame, tuple(left_center), tuple(right_center), (255, 255, 0), 2)
    
    def draw_stress_info(self, frame, emotion, confidence, eyebrow_stress, combined_stress, is_calibrating):
        """
        Draw stress information on frame
        """
        height, width = frame.shape[:2]
        
        # Create semi-transparent overlay for info panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 200), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Display calibration status or stress info
        if is_calibrating:
            text = "CALIBRATING..."
            cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            text = "Please remain neutral"
            cv2.putText(frame, text, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        else:
            # Emotion
            if emotion:
                text = f"Emotion: {emotion} ({confidence*100:.1f}%)"
                cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Eyebrow-based stress
            text = f"Eyebrow Stress: {eyebrow_stress:.1f}"
            cv2.putText(frame, text, (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Combined stress level
            text = f"Total Stress: {combined_stress:.1f}"
            color = self.get_stress_color(combined_stress)
            cv2.putText(frame, text, (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            # Stress bar
            bar_width = int(350 * (combined_stress / 100))
            cv2.rectangle(frame, (20, 130), (370, 160), (100, 100, 100), 2)
            cv2.rectangle(frame, (20, 130), (20 + bar_width, 160), color, -1)
            
            # Stress level text
            if combined_stress < 30:
                status = "LOW STRESS"
            elif combined_stress < 60:
                status = "MODERATE STRESS"
            else:
                status = "HIGH STRESS"
            cv2.putText(frame, status, (20, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Instructions
        cv2.putText(frame, "Press 'q' to quit | 'r' to recalibrate", (10, height - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def get_stress_color(self, stress_level):
        """
        Get color based on stress level (green -> yellow -> red)
        """
        if stress_level < 30:
            return (0, 255, 0)  # Green
        elif stress_level < 60:
            return (0, 255, 255)  # Yellow
        else:
            return (0, 0, 255)  # Red
    
    def run(self):
        """
        Main loop for real-time stress detection
        """
        if self.landmark_predictor is None:
            print("Cannot run without landmark predictor. Exiting...")
            return
        
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        print("="*60)
        print("REAL-TIME STRESS DETECTION")
        print("="*60)
        print("\nInstructions:")
        print("1. Sit straight in front of the webcam")
        print("2. Remain neutral during calibration (first 30 frames)")
        print("3. Press 'q' to quit")
        print("4. Press 'r' to recalibrate")
        print("\nStarting webcam...\n")
        
        frame_count = 0
        fps_start_time = time.time()
        fps = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            frame_count += 1
            
            # Calculate FPS
            if frame_count % 30 == 0:
                fps_end_time = time.time()
                fps = 30 / (fps_end_time - fps_start_time)
                fps_start_time = fps_end_time
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_detector(gray)
            
            if len(faces) > 0:
                # Process first detected face
                face = faces[0]
                
                # Draw face rectangle
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Get facial landmarks
                landmarks = self.landmark_predictor(gray, face)
                
                # Get eyebrow points
                left_eyebrow, right_eyebrow = self.get_eyebrow_points(landmarks)
                
                # Calculate eyebrow distance
                eyebrow_distance = self.calculate_eyebrow_distance(left_eyebrow, right_eyebrow)
                
                # Calibration phase
                if not self.is_calibrated:
                    self.calibrate_baseline(eyebrow_distance)
                    eyebrow_stress = 0
                    combined_stress = 0
                    emotion = None
                    confidence = 0
                else:
                    # Calculate stress from eyebrows
                    eyebrow_stress = self.calculate_stress_level_from_eyebrows(eyebrow_distance)
                    
                    # Predict emotion
                    face_roi = frame[max(0, y):min(frame.shape[0], y+h), 
                                    max(0, x):min(frame.shape[1], x+w)]
                    if face_roi.size > 0:
                        emotion, confidence = self.predict_emotion(face_roi)
                    else:
                        emotion, confidence = None, 0
                    
                    # Calculate combined stress
                    combined_stress = self.calculate_combined_stress(eyebrow_stress, emotion)
                
                # Draw landmarks
                self.draw_landmarks(frame, landmarks, left_eyebrow, right_eyebrow)
                
                # Draw stress information
                self.draw_stress_info(frame, emotion, confidence, eyebrow_stress, 
                                    combined_stress, not self.is_calibrated)
            else:
                # No face detected
                cv2.putText(frame, "No face detected", (20, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Display FPS
            cv2.putText(frame, f"FPS: {fps:.1f}", (frame.shape[1] - 120, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Show frame
            cv2.imshow('Real-Time Stress Detection', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nQuitting...")
                break
            elif key == ord('r'):
                print("\nRecalibrating...")
                self.baseline_eyebrow_distance = None
                self.calibration_distances.clear()
                self.is_calibrated = False
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("Stress detection stopped.")

def main():
    """
    Main entry point
    """
    detector = StressDetector()
    detector.run()

if __name__ == "__main__":
    main()
