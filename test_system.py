"""
Utility script to test camera and system components
Run this before starting the main stress detection to verify everything works
"""

import sys
import cv2
import numpy as np

def test_camera():
    """Test if webcam is accessible"""
    print("\n" + "="*60)
    print("Testing Camera...")
    print("="*60)
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("✗ ERROR: Cannot access webcam")
        print("  Please check:")
        print("  - Camera is connected")
        print("  - Camera permissions are granted")
        print("  - No other application is using the camera")
        return False
    
    ret, frame = cap.read()
    if not ret or frame is None:
        print("✗ ERROR: Cannot read frame from webcam")
        cap.release()
        return False
    
    height, width = frame.shape[:2]
    print(f"✓ Camera is working")
    print(f"  Resolution: {width}x{height}")
    print(f"  Press any key to close the test window...")
    
    cv2.imshow('Camera Test', frame)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    
    cap.release()
    return True

def test_imports():
    """Test if all required packages are installed"""
    print("\n" + "="*60)
    print("Testing Package Imports...")
    print("="*60)
    
    packages = {
        'opencv-python': 'cv2',
        'numpy': 'numpy',
        'tensorflow': 'tensorflow',
        'dlib': 'dlib',
        'matplotlib': 'matplotlib'
    }
    
    all_ok = True
    for package_name, import_name in packages.items():
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {package_name}: {version}")
        except ImportError as e:
            print(f"✗ {package_name}: NOT INSTALLED")
            print(f"  Error: {e}")
            all_ok = False
    
    return all_ok

def test_files():
    """Test if required files exist"""
    print("\n" + "="*60)
    print("Testing Required Files...")
    print("="*60)
    
    import os
    
    files_to_check = [
        ('shape_predictor_68_face_landmarks.dat', 'Facial landmark predictor (required)', True),
        ('emotion_model_best.h5', 'Trained emotion model (required for detection)', False),
        ('emotion_recognition.py', 'Training script', True),
        ('eyebrow_detection.py', 'Detection script', True),
        ('config.py', 'Configuration file', True),
    ]
    
    all_ok = True
    for filename, description, required in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename) / (1024 * 1024)  # MB
            print(f"✓ {filename}")
            print(f"  {description}")
            print(f"  Size: {size:.2f} MB")
        else:
            status = "✗ REQUIRED" if required else "⚠ OPTIONAL"
            print(f"{status}: {filename}")
            print(f"  {description}")
            if required and filename == 'shape_predictor_68_face_landmarks.dat':
                print("  Download from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
            if not required and filename == 'emotion_model_best.h5':
                print("  Train the model using: python emotion_recognition.py")
            if required:
                all_ok = False
    
    return all_ok

def test_dataset():
    """Test if dataset exists and count images"""
    print("\n" + "="*60)
    print("Testing Dataset...")
    print("="*60)
    
    import os
    
    dataset_path = 'fer2013'
    
    if not os.path.exists(dataset_path):
        print("✗ Dataset directory not found: fer2013/")
        print("  Please create the directory and add training images")
        return False
    
    emotions = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    splits = ['train', 'val']
    
    total_train = 0
    total_val = 0
    
    for split in splits:
        print(f"\n{split.capitalize()} set:")
        split_path = os.path.join(dataset_path, split)
        
        if not os.path.exists(split_path):
            print(f"  ✗ Directory not found: {split_path}")
            continue
        
        for emotion in emotions:
            emotion_path = os.path.join(split_path, emotion)
            if os.path.exists(emotion_path):
                images = [f for f in os.listdir(emotion_path) 
                         if f.endswith(('.jpg', '.jpeg', '.png'))]
                count = len(images)
                
                if split == 'train':
                    total_train += count
                else:
                    total_val += count
                
                status = "✓" if count > 0 else "⚠"
                print(f"  {status} {emotion}: {count} images")
            else:
                print(f"  ✗ {emotion}: Directory not found")
    
    print(f"\nTotal training images: {total_train}")
    print(f"Total validation images: {total_val}")
    
    if total_train < 100:
        print("⚠ Warning: Very few training images. Model may not train well.")
        return False
    elif total_train < 1000:
        print("⚠ Warning: Limited training images. Model accuracy may be moderate.")
    
    return True

def test_face_detection():
    """Test face detection capability"""
    print("\n" + "="*60)
    print("Testing Face Detection...")
    print("="*60)
    
    try:
        import dlib
        
        detector = dlib.get_frontal_face_detector()
        
        # Test with camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("✗ Cannot test face detection - camera not available")
            return False
        
        print("Looking for faces...")
        print("Please look at the camera...")
        print("Testing for 5 seconds...")
        
        faces_detected = False
        start_time = cv2.getTickCount()
        
        while (cv2.getTickCount() - start_time) / cv2.getTickFrequency() < 5:
            ret, frame = cap.read()
            if not ret:
                continue
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            
            if len(faces) > 0:
                faces_detected = True
                for face in faces:
                    x, y, w, h = face.left(), face.top(), face.width(), face.height()
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, "Face Detected!", (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            cv2.imshow('Face Detection Test', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if faces_detected:
            print("✓ Face detection is working")
            return True
        else:
            print("⚠ No faces detected")
            print("  Please ensure:")
            print("  - You are facing the camera")
            print("  - Lighting is adequate")
            print("  - Your face is clearly visible")
            return False
            
    except Exception as e:
        print(f"✗ Error testing face detection: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("STRESS DETECTION SYSTEM - DIAGNOSTIC TEST")
    print("="*60)
    
    results = {
        'Package Imports': test_imports(),
        'Required Files': test_files(),
        'Dataset': test_dataset(),
        'Camera': test_camera(),
        'Face Detection': test_face_detection()
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("="*60)
        print("\nYou are ready to run the stress detection system!")
        print("Run: python eyebrow_detection.py")
    else:
        print("✗ SOME TESTS FAILED")
        print("="*60)
        print("\nPlease fix the issues above before running the system.")
        print("Refer to README.md for installation instructions.")
    print("")

if __name__ == "__main__":
    main()
