"""
Real-Time Stress Detection using OpenCV (Without dlib dependency)
Uses Haar Cascades for face detection and MediaPipe for facial landmarks
Alternative solution when dlib installation fails
"""

import cv2
import numpy as np
from tensorflow import keras
import time
from collections import deque

try:
    import mediapipe as mp
    # Check if MediaPipe has the solutions module
    if hasattr(mp, 'solutions'):
        HAS_MEDIAPIPE = True
    else:
        HAS_MEDIAPIPE = False
        print("⚠ MediaPipe installed but 'solutions' module not available")
except ImportError:
    HAS_MEDIAPIPE = False
    print("MediaPipe not found. Install with: pip install mediapipe")
except Exception as e:
    HAS_MEDIAPIPE = False
    print(f"⚠ MediaPipe error: {e}")

# Configuration
EMOTION_MODEL_PATH = 'emotion_model_best.h5'
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

class StressDetectorOpenCV:
    def __init__(self):
        """
        Initialize the stress detector with emotion model and MediaPipe face mesh
        """
        print("Initializing Stress Detector (OpenCV Version)...")
        
        # Load emotion recognition model
        try:
            self.emotion_model = keras.models.load_model(EMOTION_MODEL_PATH)
            print(f"✓ Emotion model loaded from {EMOTION_MODEL_PATH}")
        except Exception as e:
            print(f"✗ Error loading emotion model: {e}")
            print("Please train the model first by running emotion_recognition.py")
            self.emotion_model = None
        
        # Initialize face detector (OpenCV Haar Cascade)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        print("✓ OpenCV Haar Cascade face detector loaded")
        
        # Initialize MediaPipe Face Mesh
        if HAS_MEDIAPIPE:
            try:
                self.mp_face_mesh = mp.solutions.face_mesh
                self.face_mesh = self.mp_face_mesh.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
                print("✓ MediaPipe Face Mesh loaded")
            except Exception as e:
                print(f"⚠ MediaPipe initialization failed: {e}")
                self.face_mesh = None
                HAS_MEDIAPIPE = False
        else:
            self.face_mesh = None
            print("⚠ MediaPipe not available - eyebrow tracking disabled")
        
        # Initialize baseline eyebrow distance
        self.baseline_eyebrow_distance = None
        self.calibration_distances = deque(maxlen=30)
        self.is_calibrated = False
        
        print("Initialization complete!\n")
    
    def get_eyebrow_points_mediapipe(self, landmarks, frame_width, frame_height):
        """
        Extract eyebrow landmark points using MediaPipe
        Left eyebrow: landmarks 70, 63, 105, 66, 107
        Right eyebrow: landmarks 336, 296, 334, 293, 300
        """
        left_eyebrow_indices = [70, 63, 105, 66, 107]
        right_eyebrow_indices = [336, 296, 334, 293, 300]
        
        left_eyebrow = []
        right_eyebrow = []
        
        for idx in left_eyebrow_indices:
            landmark = landmarks[idx]
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            left_eyebrow.append((x, y))
        
        for idx in right_eyebrow_indices:
            landmark = landmarks[idx]
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            right_eyebrow.append((x, y))
        
        return np.array(left_eyebrow), np.array(right_eyebrow)
    
    def calculate_eyebrow_distance(self, left_eyebrow, right_eyebrow):
        """Calculate distance between left and right eyebrows"""
        left_center = np.mean(left_eyebrow, axis=0)
        right_center = np.mean(right_eyebrow, axis=0)
        distance = np.linalg.norm(left_center - right_center)
        return distance
    
    def calibrate_baseline(self, distance):
        """Calibrate baseline eyebrow distance"""
        self.calibration_distances.append(distance)
        
        if len(self.calibration_distances) >= 30 and not self.is_calibrated:
            self.baseline_eyebrow_distance = np.mean(self.calibration_distances)
            self.is_calibrated = True
            print(f"\n✓ Calibration complete! Baseline distance: {self.baseline_eyebrow_distance:.2f}")
            print("Starting stress detection...\n")
    
    def calculate_stress_level_from_eyebrows(self, current_distance):
        """Calculate stress level based on eyebrow contraction"""
        if not self.is_calibrated or self.baseline_eyebrow_distance is None:
            return 0
        
        displacement = self.baseline_eyebrow_distance - current_distance
        normalized_displacement = displacement / self.baseline_eyebrow_distance
        stress_raw = 100 * (1 - np.exp(-3 * max(0, normalized_displacement)))
        stress_level = np.clip(stress_raw, 0, 100)
        
        return stress_level
    
    def predict_emotion(self, face_roi):
        """Predict emotion from face region"""
        if self.emotion_model is None:
            return None, 0.0
        
        face_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        face_resized = cv2.resize(face_gray, (IMG_SIZE, IMG_SIZE))
        face_normalized = face_resized / 255.0
        face_input = np.expand_dims(face_normalized, axis=0)
        face_input = np.expand_dims(face_input, axis=-1)
        
        emotion_probs = self.emotion_model.predict(face_input, verbose=0)[0]
        emotion_idx = np.argmax(emotion_probs)
        emotion_label = EMOTION_LABELS[emotion_idx]
        confidence = emotion_probs[emotion_idx]
        
        return emotion_label, confidence
    
    def calculate_combined_stress(self, eyebrow_stress, emotion):
        """Combine eyebrow-based stress with emotion-based stress"""
        if emotion is None:
            return eyebrow_stress
        
        emotion_stress_weight = STRESS_EMOTIONS.get(emotion, 0.5)
        combined_stress = (0.6 * eyebrow_stress) + (0.4 * emotion_stress_weight * 100)
        
        return np.clip(combined_stress, 0, 100)
    
    def draw_landmarks(self, frame, left_eyebrow, right_eyebrow):
        """Draw eyebrows on frame"""
        for point in left_eyebrow:
            cv2.circle(frame, tuple(point.astype(int)), 3, (255, 0, 0), -1)
        for point in right_eyebrow:
            cv2.circle(frame, tuple(point.astype(int)), 3, (0, 0, 255), -1)
        
        left_center = np.mean(left_eyebrow, axis=0).astype(int)
        right_center = np.mean(right_eyebrow, axis=0).astype(int)
        cv2.line(frame, tuple(left_center), tuple(right_center), (255, 255, 0), 2)
    
    def draw_stress_info(self, frame, emotion, confidence, eyebrow_stress, combined_stress, is_calibrating):
        """Draw stress information on frame"""
        height, width = frame.shape[:2]
        
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 200), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        if is_calibrating:
            text = "CALIBRATING..."
            cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            text = "Please remain neutral"
            cv2.putText(frame, text, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        else:
            if emotion:
                text = f"Emotion: {emotion} ({confidence*100:.1f}%)"
                cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            text = f"Eyebrow Stress: {eyebrow_stress:.1f}"
            cv2.putText(frame, text, (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            text = f"Total Stress: {combined_stress:.1f}"
            color = self.get_stress_color(combined_stress)
            cv2.putText(frame, text, (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            bar_width = int(350 * (combined_stress / 100))
            cv2.rectangle(frame, (20, 130), (370, 160), (100, 100, 100), 2)
            cv2.rectangle(frame, (20, 130), (20 + bar_width, 160), color, -1)
            
            if combined_stress < 30:
                status = "LOW STRESS"
            elif combined_stress < 60:
                status = "MODERATE STRESS"
            else:
                status = "HIGH STRESS"
            cv2.putText(frame, status, (20, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        cv2.putText(frame, "Press 'q' to quit | 'r' to recalibrate", (10, height - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def get_stress_color(self, stress_level):
        """Get color based on stress level"""
        if stress_level < 30:
            return (0, 255, 0)  # Green
        elif stress_level < 60:
            return (0, 255, 255)  # Yellow
        else:
            return (0, 0, 255)  # Red
    
    def run(self):
        """Main loop for real-time stress detection"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        print("="*60)
        print("REAL-TIME STRESS DETECTION (OpenCV Version)")
        print("="*60)
        print("\nInstructions:")
        print("1. Sit straight in front of the webcam")
        print("2. Remain neutral during calibration (first 30 frames)")
        print("3. Press 'q' to quit")
        print("4. Press 'r' to recalibrate")
        
        if not HAS_MEDIAPIPE:
            print("\n⚠ MediaPipe not installed - eyebrow tracking disabled")
            print("  Only emotion-based stress detection will work")
            print("  Install MediaPipe: pip install mediapipe")
        
        print("\nStarting webcam...\n")
        
        frame_count = 0
        fps_start_time = time.time()
        fps = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            frame = cv2.flip(frame, 1)
            frame_count += 1
            
            if frame_count % 30 == 0:
                fps_end_time = time.time()
                fps = 30 / (fps_end_time - fps_start_time)
                fps_start_time = fps_end_time
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            eyebrow_stress = 0
            combined_stress = 0
            emotion = None
            confidence = 0
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Predict emotion
                face_roi = frame[y:y+h, x:x+w]
                if face_roi.size > 0:
                    emotion, confidence = self.predict_emotion(face_roi)
                
                # Process eyebrows with MediaPipe
                if HAS_MEDIAPIPE and self.face_mesh:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.face_mesh.process(rgb_frame)
                    
                    if results.multi_face_landmarks:
                        face_landmarks = results.multi_face_landmarks[0]
                        h, w, _ = frame.shape
                        
                        left_eyebrow, right_eyebrow = self.get_eyebrow_points_mediapipe(
                            face_landmarks.landmark, w, h
                        )
                        
                        eyebrow_distance = self.calculate_eyebrow_distance(left_eyebrow, right_eyebrow)
                        
                        if not self.is_calibrated:
                            self.calibrate_baseline(eyebrow_distance)
                        else:
                            eyebrow_stress = self.calculate_stress_level_from_eyebrows(eyebrow_distance)
                        
                        self.draw_landmarks(frame, left_eyebrow, right_eyebrow)
                
                # Calculate combined stress
                if HAS_MEDIAPIPE and self.is_calibrated:
                    combined_stress = self.calculate_combined_stress(eyebrow_stress, emotion)
                else:
                    # Emotion-only stress if MediaPipe not available
                    if emotion:
                        combined_stress = STRESS_EMOTIONS.get(emotion, 0.5) * 100
                
                # Draw stress info
                is_calibrating = HAS_MEDIAPIPE and not self.is_calibrated
                self.draw_stress_info(frame, emotion, confidence, eyebrow_stress,
                                    combined_stress, is_calibrating)
            else:
                cv2.putText(frame, "No face detected", (20, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.putText(frame, f"FPS: {fps:.1f}", (frame.shape[1] - 120, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.imshow('Real-Time Stress Detection', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nQuitting...")
                break
            elif key == ord('r'):
                print("\nRecalibrating...")
                self.baseline_eyebrow_distance = None
                self.calibration_distances.clear()
                self.is_calibrated = False
        
        cap.release()
        cv2.destroyAllWindows()
        print("Stress detection stopped.")

def main():
    """Main entry point"""
    detector = StressDetectorOpenCV()
    detector.run()

if __name__ == "__main__":
    main()
