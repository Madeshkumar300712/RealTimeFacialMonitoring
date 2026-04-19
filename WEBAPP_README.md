# 🎯 Stress Detection Web Application

A modern, attractive web-based UI for real-time stress detection using facial emotion analysis.

## ✨ Features

### 🎨 Modern UI
- **Dark Theme**: Easy on the eyes with a professional dark mode interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Smooth Animations**: Polished user experience with fluid transitions
- **Real-time Feedback**: Instant results with visual stress level indicators

### 📸 Two Detection Modes

#### 1. Photo Upload
- Upload images from your device
- Drag and drop support
- Supports PNG, JPG, and other common formats
- Instant analysis with annotated results

#### 2. Live Camera
- Real-time webcam monitoring
- Continuous stress level detection
- Live emotion tracking
- Stop/start controls

### 🧠 AI-Powered Analysis
- **Emotion Recognition**: Detects 6 emotions (Angry, Fear, Happy, Neutral, Sad, Surprise)
- **Stress Level Calculation**: Converts emotions to stress scores
- **Multi-face Support**: Can detect multiple faces simultaneously
- **Visual Annotations**: Color-coded boxes and labels on detected faces

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam (for live camera mode)
- Trained emotion model (`emotion_model_best.h5`)

### Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Ensure Model is Available**
- If you don't have `emotion_model_best.h5`, train it first:
```bash
python emotion_recognition.py
```

3. **Launch the Web App**
```bash
./run_webapp.sh
```

Or directly:
```bash
python app.py
```

4. **Open in Browser**
Navigate to: **http://localhost:5000**

## 📖 Usage Guide

### Photo Upload Mode
1. Click on "Upload Photo" card
2. Click the upload area or drag & drop an image
3. Wait for analysis (usually takes 1-2 seconds)
4. View results with:
   - Annotated image with face boxes
   - Detected emotion
   - Confidence score
   - Stress level percentage
   - Status (Low/Moderate/High Stress)

### Live Camera Mode
1. Click on "Live Camera" card
2. Click "Start Camera" button
3. Allow camera permissions in your browser
4. View real-time stress detection
5. Results update every second
6. Click "Stop Camera" when done

## 🎨 UI Features

### Color-Coded Stress Levels
- 🟢 **Green (0-29%)**: Low Stress - Relaxed state
- 🟠 **Orange (30-59%)**: Moderate Stress - Slightly stressed
- 🔴 **Red (60-100%)**: High Stress - Significantly stressed

### Visual Elements
- **Status Indicator**: Shows system readiness
- **Loading Animations**: Smooth feedback during processing
- **Result Cards**: Clean, organized display of analysis results
- **Responsive Layout**: Adapts to different screen sizes

## 🔧 Technical Details

### Backend (Flask)
- **Framework**: Flask 2.3.3
- **AI Model**: TensorFlow/Keras CNN for emotion recognition
- **Face Detection**: OpenCV Haar Cascade Classifier
- **API Endpoints**:
  - `GET /`: Main UI page
  - `POST /api/upload`: Process uploaded images
  - `POST /api/webcam`: Process webcam frames
  - `GET /api/status`: Check system status

### Frontend
- **HTML5**: Semantic structure
- **CSS3**: Modern styling with gradients, shadows, animations
- **JavaScript**: Vanilla JS for interactivity
- **WebRTC**: For webcam access
- **Canvas API**: For frame processing

### Project Structure
```
RealTimeFacialMonitoring/
├── app.py                 # Flask backend
├── templates/
│   └── index.html        # Main UI template
├── static/
│   ├── style.css         # Modern styling
│   └── script.js         # Frontend logic
├── emotion_model_best.h5 # Trained AI model
├── requirements.txt      # Python dependencies
└── run_webapp.sh        # Startup script
```

## 🎯 Stress Detection Algorithm

### Emotion Weights
Each emotion contributes differently to stress level:
- **Fear**: 100% (highest stress indicator)
- **Angry**: 90%
- **Sad**: 70%
- **Surprise**: 40%
- **Neutral**: 10%
- **Happy**: 0% (no stress)

### Calculation
```
Stress Level = Emotion Weight × Confidence Score × 100
```

## 🌐 Browser Compatibility

### Recommended Browsers
- ✅ Chrome/Edge (v90+)
- ✅ Firefox (v88+)
- ✅ Safari (v14+)
- ✅ Opera (v76+)

### Required Features
- WebRTC (for camera access)
- Canvas API (for image processing)
- ES6 JavaScript support
- CSS Grid & Flexbox

## 🔒 Privacy & Security

- **Local Processing**: All analysis happens on your machine
- **No Data Storage**: Images are not saved or transmitted
- **Camera Permissions**: Only accessed when you click "Start Camera"
- **No External APIs**: Completely offline capable

## 🐛 Troubleshooting

### Camera Not Working
- Ensure browser has camera permissions
- Check if another app is using the camera
- Try a different browser
- Check browser console for errors

### Model Not Loading
- Verify `emotion_model_best.h5` exists in the directory
- Train the model: `python emotion_recognition.py`
- Check file permissions

### Slow Processing
- Use smaller images (recommended: 1920x1080 or less)
- Close other resource-intensive applications
- Consider using a GPU-enabled TensorFlow installation

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
python app.py --port 5001
```

## 🚀 Performance Tips

1. **Image Size**: Smaller images process faster
2. **Camera Resolution**: Lower resolution = faster processing
3. **Processing Interval**: Adjust frame processing rate in `script.js`
4. **Model Optimization**: Use quantized models for faster inference

## 📊 Future Enhancements

- [ ] Real-time video recording with analysis overlay
- [ ] Historical stress level tracking and charts
- [ ] Export results as PDF/CSV
- [ ] Multiple language support
- [ ] Dark/Light theme toggle
- [ ] Advanced analytics dashboard
- [ ] Mobile app version

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests!

## 📄 License

This project is part of the Real-Time Facial Monitoring system.

## 🙏 Acknowledgments

- TensorFlow/Keras for deep learning framework
- OpenCV for computer vision capabilities
- Flask for web framework
- FER2013 dataset for emotion training data

---

**Made with ❤️ for stress-free living**
