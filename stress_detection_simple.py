"""
Simple Stress Detection using OpenCV Only
Emotion-based stress detection without facial landmarks
Works without MediaPipe or dlib dependencies
"""

import cv2
import numpy as np
from tensorflow import keras
import time

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

class SimpleStressDetector:
    def __init__(self):
        """Initialize the simple stress detector"""
        print("Initializing Simple Stress Detector...")
        print("Note: This version uses emotion-only detection")
        print("Install MediaPipe for eyebrow tracking: pip install mediapipe")
        print()
        
        # Load emotion recognition model
        try:
            self.emotion_model = keras.models.load_model(EMOTION_MODEL_PATH)
            print(f"✓ Emotion model loaded from {EMOTION_MODEL_PATH}")
        except Exception as e:
            print(f"⚠ Could not load emotion model: {e}")
            print("  The model is still training. This may take 30-60 minutes.")
            print("  Run 'python emotion_recognition.py' if not already running.")
            print()
            print("  For now, the app will run in demo mode (face detection only)")
            self.emotion_model = None
        
        # Initialize face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        print("✓ OpenCV face detector loaded")
        print()
        
    def predict_emotion(self, face_roi):
        """Predict emotion from face region"""
        if self.emotion_model is None:
            return None, 0.0
        
        try:
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
        except Exception as e:
            print(f"Error predicting emotion: {e}")
            return None, 0.0
    
    def calculate_stress(self, emotion):
        """Calculate stress level from emotion"""
        if emotion is None:
            return 0
        
        return STRESS_EMOTIONS.get(emotion, 0.5) * 100
    
    def get_stress_color(self, stress_level):
        """Get color based on stress level"""
        if stress_level < 30:
            return (0, 255, 0)  # Green
        elif stress_level < 60:
            return (0, 255, 255)  # Yellow
        else:
            return (0, 0, 255)  # Red
    
    def draw_info(self, frame, emotion, confidence, stress_level):
        """Draw information overlay"""
        height, width = frame.shape[:2]
        
        # Create semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 180), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        if self.emotion_model is None:
            # Demo mode message
            cv2.putText(frame, "DEMO MODE", (20, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(frame, "Training model...", (20, 75),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, "Run: python emotion_recognition.py", (20, 105),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        elif emotion:
            # Show emotion and stress
            text = f"Emotion: {emotion} ({confidence*100:.1f}%)"
            cv2.putText(frame, text, (20, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            text = f"Stress Level: {stress_level:.1f}"
            color = self.get_stress_color(stress_level)
            cv2.putText(frame, text, (20, 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            # Stress bar
            bar_width = int(350 * (stress_level / 100))
            cv2.rectangle(frame, (20, 100), (370, 130), (100, 100, 100), 2)
            cv2.rectangle(frame, (20, 100), (20 + bar_width, 130), color, -1)
            
            # Stress status
            if stress_level < 30:
                status = "LOW STRESS"
            elif stress_level < 60:
                status = "MODERATE STRESS"
            else:
                status = "HIGH STRESS"
            cv2.putText(frame, status, (20, 160),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Controls
        cv2.putText(frame, "Press 'q' to quit", (10, height - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def run(self):
        """Main detection loop"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Error: Could not open webcam")
            print("\nTroubleshooting:")
            print("  1. Check camera permissions in System Preferences")
            print("  2. Close other apps using the camera")
            print("  3. Try unplugging and replugging the camera")
            return
        
        print("="*60)
        print("REAL-TIME STRESS DETECTION")
        print("="*60)
        print("\nCamera opened successfully!")
        
        if self.emotion_model:
            print("Detecting emotions and stress levels...")
        else:
            print("Demo mode: Face detection only")
            print("Train the model first: python emotion_recognition.py")
        
        print("\nPress 'q' to quit\n")
        
        frame_count = 0
        fps_start_time = time.time()
        fps = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame")
                    break
                
                frame = cv2.flip(frame, 1)
                frame_count += 1
                
                # Calculate FPS
                if frame_count % 30 == 0:
                    fps_end_time = time.time()
                    fps = 30 / (fps_end_time - fps_start_time)
                    fps_start_time = fps_end_time
                
                # Detect faces
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                emotion = None
                confidence = 0
                stress_level = 0
                
                if len(faces) > 0:
                    # Process first face
                    x, y, w, h = faces[0]
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    # Predict emotion
                    face_roi = frame[y:y+h, x:x+w]
                    if face_roi.size > 0:
                        emotion, confidence = self.predict_emotion(face_roi)
                        stress_level = self.calculate_stress(emotion)
                else:
                    # No face detected
                    cv2.putText(frame, "No face detected", (20, 200),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(frame, "Please face the camera", (20, 240),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Draw info overlay
                self.draw_info(frame, emotion, confidence, stress_level)
                
                # Show FPS
                cv2.putText(frame, f"FPS: {fps:.1f}", (frame.shape[1] - 120, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Display frame
                cv2.imshow('Stress Detection', frame)
                
                # Handle key press
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\nQuitting...")
                    break
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Stress detection stopped.")

def main():
    """Main entry point"""
    print()
    print("="*60)
    print("  SIMPLE STRESS DETECTION SYSTEM")
    print("="*60)
    print()
    
    detector = SimpleStressDetector()
    detector.run()

if __name__ == "__main__":
    main()
