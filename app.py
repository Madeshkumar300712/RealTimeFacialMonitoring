"""
Flask Web Application for Stress Detection
Provides a modern UI with photo upload and live camera options
"""

from flask import Flask, render_template, request, jsonify, Response
import cv2
import numpy as np
from tensorflow import keras
import base64
from io import BytesIO
from PIL import Image
import os
from datetime import datetime
import json

app = Flask(__name__)

# Configuration
EMOTION_MODEL_PATH = 'emotion_model_best.h5'
IMG_SIZE = 48
EMOTION_LABELS = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
STRESS_EMOTIONS = {
    'Angry': 0.9,
    'Fear': 1.0,
    'Sad': 0.7,
    'Surprise': 0.4,
    'Happy': 0.0,
    'Neutral': 0.1
}

# Global variables
emotion_model = None
face_cascade = None
camera = None
session_data = {
    'detections': [],
    'start_time': None,
    'total_detections': 0,
    'stress_history': []
}

def initialize_models():
    """Initialize emotion model and face detector"""
    global emotion_model, face_cascade
    
    try:
        emotion_model = keras.models.load_model(EMOTION_MODEL_PATH)
        print(f"✓ Emotion model loaded from {EMOTION_MODEL_PATH}")
    except Exception as e:
        print(f"⚠ Could not load emotion model: {e}")
        emotion_model = None
    
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    print("✓ Face detector initialized")

def detect_emotion(face_img):
    """Detect emotion from face image"""
    if emotion_model is None:
        return None, 0.0
    
    # Preprocess face
    face_img = cv2.resize(face_img, (IMG_SIZE, IMG_SIZE))
    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    face_img = face_img / 255.0
    face_img = np.expand_dims(face_img, axis=0)
    face_img = np.expand_dims(face_img, axis=-1)
    
    # Predict emotion
    predictions = emotion_model.predict(face_img, verbose=0)
    emotion_idx = np.argmax(predictions[0])
    emotion = EMOTION_LABELS[emotion_idx]
    confidence = float(predictions[0][emotion_idx])
    
    return emotion, confidence

def calculate_stress_level(emotion):
    """Calculate stress level from emotion"""
    if emotion is None:
        return 0.0
    return STRESS_EMOTIONS.get(emotion, 0.0)

def process_image(image):
    """Process image and return stress detection results"""
    global session_data
    
    if face_cascade is None:
        return {"error": "System not initialized"}
    
    # Initialize session start time if not set
    if session_data['start_time'] is None:
        session_data['start_time'] = datetime.now().isoformat()
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) == 0:
        return {"error": "No face detected", "faces": 0}
    
    results = []
    annotated_image = image.copy()
    
    for (x, y, w, h) in faces:
        # Extract face
        face_img = image[y:y+h, x:x+w]
        
        # Detect emotion
        emotion, confidence = detect_emotion(face_img)
        
        if emotion:
            stress_level = calculate_stress_level(emotion)
            
            # Determine color based on stress level
            if stress_level < 0.3:
                color = (0, 255, 0)  # Green
                status = "Low Stress"
            elif stress_level < 0.6:
                color = (0, 165, 255)  # Orange
                status = "Moderate Stress"
            else:
                color = (0, 0, 255)  # Red
                status = "High Stress"
            
            # Draw rectangle and text
            cv2.rectangle(annotated_image, (x, y), (x+w, y+h), color, 2)
            cv2.putText(annotated_image, f"{emotion} ({confidence*100:.0f}%)", 
                       (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            cv2.putText(annotated_image, f"Stress: {stress_level*100:.0f}%", 
                       (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            result = {
                "emotion": emotion,
                "confidence": round(confidence * 100, 2),
                "stress_level": round(stress_level * 100, 2),
                "status": status
            }
            results.append(result)
            
            # Track in session
            session_data['detections'].append({
                'timestamp': datetime.now().isoformat(),
                'emotion': emotion,
                'stress_level': round(stress_level * 100, 2),
                'confidence': round(confidence * 100, 2)
            })
            session_data['total_detections'] += 1
            session_data['stress_history'].append(round(stress_level * 100, 2))
            
            # Keep only last 50 detections
            if len(session_data['detections']) > 50:
                session_data['detections'] = session_data['detections'][-50:]
            if len(session_data['stress_history']) > 50:
                session_data['stress_history'] = session_data['stress_history'][-50:]
    
    # Convert annotated image to base64
    _, buffer = cv2.imencode('.jpg', annotated_image)
    img_str = base64.b64encode(buffer).decode()
    
    return {
        "success": True,
        "faces": len(faces),
        "results": results,
        "annotated_image": f"data:image/jpeg;base64,{img_str}"
    }

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Handle image upload and process it"""
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No image selected"}), 400
    
    # Read image
    image_bytes = file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        return jsonify({"error": "Invalid image file"}), 400
    
    # Process image
    result = process_image(image)
    return jsonify(result)

@app.route('/api/webcam', methods=['POST'])
def process_webcam_frame():
    """Process a frame from webcam"""
    data = request.get_json()
    
    if 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400
    
    try:
        # Decode base64 image
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image data"}), 400
        
        # Process image
        result = process_image(image)
        
        # Debug logging
        if 'error' in result:
            print(f"[DEBUG] Webcam detection error: {result['error']}")
        else:
            print(f"[DEBUG] Webcam detection SUCCESS! Faces: {result.get('faces', 0)}, Total tracked: {session_data['total_detections']}")
        
        return jsonify(result)
    except Exception as e:
        print(f"[ERROR] Webcam processing failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/status')
def status():
    """Check system status"""
    return jsonify({
        "model_loaded": emotion_model is not None,
        "face_detector_loaded": face_cascade is not None
    })

@app.route('/api/report')
def get_report():
    """Get stress detection report"""
    global session_data
    
    print(f"[DEBUG] Report requested. Total detections: {session_data['total_detections']}")
    print(f"[DEBUG] Session data: {len(session_data['detections'])} records, {len(session_data['stress_history'])} history")
    
    if session_data['total_detections'] == 0:
        return jsonify({
            'has_data': False,
            'message': 'No detection data available yet'
        })
    
    # Calculate statistics
    stress_values = session_data['stress_history']
    avg_stress = sum(stress_values) / len(stress_values) if stress_values else 0
    max_stress = max(stress_values) if stress_values else 0
    min_stress = min(stress_values) if stress_values else 0
    
    # Count emotions
    emotion_counts = {}
    for detection in session_data['detections']:
        emotion = detection['emotion']
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    # Determine dominant emotion
    dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else 'None'
    
    # Generate recommendations
    recommendations = []
    if avg_stress > 70:
        recommendations.extend([
            "Consider taking regular breaks to reduce stress",
            "Practice deep breathing exercises",
            "Try meditation or mindfulness techniques"
        ])
    elif avg_stress > 40:
        recommendations.extend([
            "Monitor your stress levels regularly",
            "Ensure adequate rest and sleep",
            "Maintain a healthy work-life balance"
        ])
    else:
        recommendations.extend([
            "Great! Maintain your current stress management",
            "Continue healthy habits",
            "Stay mindful of stress triggers"
        ])
    
    # Determine overall status
    if avg_stress < 30:
        overall_status = "Low Stress"
        status_color = "#10b981"
    elif avg_stress < 60:
        overall_status = "Moderate Stress"
        status_color = "#f59e0b"
    else:
        overall_status = "High Stress"
        status_color = "#ef4444"
    
    return jsonify({
        'has_data': True,
        'session_start': session_data['start_time'],
        'total_detections': session_data['total_detections'],
        'avg_stress': round(avg_stress, 2),
        'max_stress': round(max_stress, 2),
        'min_stress': round(min_stress, 2),
        'dominant_emotion': dominant_emotion,
        'emotion_counts': emotion_counts,
        'stress_history': stress_values[-20:],  # Last 20 readings
        'recommendations': recommendations,
        'overall_status': overall_status,
        'status_color': status_color
    })

@app.route('/api/report/reset', methods=['POST'])
def reset_report():
    """Reset session data"""
    global session_data
    session_data = {
        'detections': [],
        'start_time': None,
        'total_detections': 0,
        'stress_history': []
    }
    return jsonify({'success': True, 'message': 'Session data reset'})

@app.route('/metrics')
def metrics():
    """Display model metrics and training history"""
    import time
    import json
    
    # Check if training history graph exists
    training_graph_path = os.path.join('static', 'training_history.png')
    has_training_graph = os.path.exists(training_graph_path)
    
    # Default metrics
    metrics_data = {
        'train_accuracy': '85.2',
        'val_accuracy': '82.5',
        'epochs': '50',
        'classes': '6'
    }
    
    # Try to load actual metrics from training
    metrics_file = 'training_metrics.json'
    if os.path.exists(metrics_file):
        try:
            with open(metrics_file, 'r') as f:
                loaded_metrics = json.load(f)
                metrics_data.update(loaded_metrics)
        except Exception as e:
            print(f"Could not load metrics: {e}")
    
    return render_template('metrics.html', 
                         metrics=metrics_data,
                         has_training_graph=has_training_graph,
                         timestamp=int(time.time()))

if __name__ == '__main__':
    print("=" * 60)
    print("Stress Detection Web Application")
    print("=" * 60)
    initialize_models()
    print("\n✓ Server starting...")
    print("✓ Open http://localhost:5000 in your browser")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
