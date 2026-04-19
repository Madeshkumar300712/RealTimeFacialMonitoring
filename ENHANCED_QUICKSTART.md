# Quick Start - Enhanced Stress Detection System

## 🚀 Starting the Application

### Option 1: Using the Run Script
```bash
cd RealTimeFacialMonitoring
./run_webapp.sh
```

### Option 2: Direct Python
```bash
cd RealTimeFacialMonitoring
python app.py
```

The application will start on `http://localhost:5000`

## 🎯 Using the New Features

### 1. Stress Detection
**Upload Photo Mode:**
1. Click "Upload Photo" on the home screen
2. Select or drag & drop an image
3. View results with stress level and progress bar
4. Results automatically tracked for report

**Live Camera Mode:**
1. Click "Live Camera" on the home screen
2. Click "Start Camera" and grant permissions
3. Real-time detection every second
4. Live stress monitoring with auto-tracking

### 2. Viewing Stress Report
1. **Open Report**: Click the "Report" button in the header
2. **View Analytics**: See comprehensive statistics:
   - Overall stress status with emoji indicator
   - Session statistics (total, avg, max, min)
   - Emotion distribution bar chart
   - Stress timeline visualization
   - Personalized recommendations
3. **Auto-Update**: Report refreshes every 5 seconds automatically

### 3. Exporting Report
1. Open the report panel
2. Click "Export Report" button
3. Text file downloads with format: `stress-report-YYYY-MM-DD.txt`
4. Contains all statistics and timeline data

### 4. Resetting Session
1. Open the report panel
2. Click "Reset Session" button
3. Confirm the action
4. All tracking data cleared, fresh start

## 📊 Understanding the Report

### Overall Status
- **😊 Low Stress** (Green): Average < 30%
  - You're doing great!
- **😐 Moderate Stress** (Orange): Average 30-60%
  - Monitor your stress levels
- **😰 High Stress** (Red): Average > 60%
  - Take action to reduce stress

### Session Statistics
- **Total Detections**: Number of times stress was detected
- **Avg Stress**: Average stress level across session
- **Max Stress**: Highest stress level recorded
- **Min Stress**: Lowest stress level recorded

### Emotion Distribution
- Visual bar chart showing percentage of each emotion
- Color-coded by emotion type
- Helps identify dominant emotional state

### Stress Timeline
- Canvas-based line chart
- Shows last 20 stress readings
- Visualizes stress progression over time

### Recommendations
Smart suggestions based on your stress level:
- **Low Stress**: Maintain current habits
- **Moderate Stress**: Monitor and practice mindfulness
- **High Stress**: Take breaks, practice breathing exercises

## 🎨 UI Features

### Visual Enhancements
- ✨ Animated gradient background
- 📊 Progress bars for stress levels
- 💫 Pulsing animations for moderate/high stress
- 🎯 Hover effects on interactive elements
- 📱 Fully responsive design

### Color Coding
- **Green**: Low stress, good state
- **Orange**: Moderate stress, be aware
- **Red**: High stress, take action

### Interactive Elements
- Smooth sliding report panel
- Drag & drop image upload
- Live camera feed with real-time detection
- Animated loading states
- Touch-friendly on mobile

## 📱 Mobile Usage

### Accessing on Mobile
1. Find your computer's IP address:
   ```bash
   # On Mac/Linux:
   ifconfig | grep "inet "
   
   # On Windows:
   ipconfig
   ```

2. Open browser on mobile device
3. Navigate to: `http://YOUR_IP_ADDRESS:5000`

### Mobile Features
- Report panel opens full-width
- Touch-friendly controls
- Responsive layout adapts to screen size
- All features work on mobile

## 🔧 Troubleshooting

### Camera Not Working
- Grant camera permissions in browser
- Check if another app is using the camera
- Try a different browser (Chrome recommended)

### No Faces Detected
- Ensure good lighting
- Face the camera directly
- Remove glasses or accessories if needed
- Try adjusting camera angle

### Report Shows No Data
- Perform at least one detection first
- Check console for errors (F12)
- Refresh the page and try again

### Export Not Working
- Check browser download settings
- Allow pop-ups if blocked
- Try different browser

## 💡 Tips for Best Results

### For Accurate Detection
1. **Good Lighting**: Face should be well-lit
2. **Direct View**: Look at camera directly
3. **Stable Position**: Keep face in frame
4. **Clear Image**: Avoid blur or obstruction

### For Better Reports
1. **Multiple Readings**: More detections = better insights
2. **Regular Intervals**: Space out detections over time
3. **Different Conditions**: Test in various situations
4. **Track Progress**: Export reports to compare over time

### For Professional Use
1. **Consistent Environment**: Same lighting/setup
2. **Baseline Measurement**: Record normal state first
3. **Document Context**: Note what you were doing
4. **Compare Reports**: Export and analyze trends

## 🎓 Understanding Metrics

### Stress Level Calculation
Based on detected emotion:
- **Fear**: 100% stress (highest)
- **Angry**: 90% stress
- **Sad**: 70% stress
- **Surprise**: 40% stress
- **Neutral**: 10% stress
- **Happy**: 0% stress (lowest)

### Confidence Score
- Indicates model's certainty (0-100%)
- Higher is better
- Below 70%: Consider retaking
- Above 85%: Very reliable

## 🔐 Privacy & Data

### Data Storage
- All data stored in memory only
- No persistent database
- Session resets on server restart
- Exports are local files

### Camera Usage
- Video never recorded
- Only single frames processed
- Processed on your machine
- No data sent to external servers

## 📞 Support & Issues

### Common Questions
**Q: How long is session data kept?**
A: Until server restart or manual reset

**Q: Can I track multiple people?**
A: System tracks all faces but reports aggregated data

**Q: How accurate is the detection?**
A: ~82-85% accuracy on validation set

**Q: Can I use this professionally?**
A: Yes, but consider it a screening tool, not diagnostic

### Getting Help
- Check [STRESS_REPORT_FEATURE.md](STRESS_REPORT_FEATURE.md) for details
- Review [UI_ENHANCEMENTS.md](UI_ENHANCEMENTS.md) for customization
- See [WEBAPP_README.md](WEBAPP_README.md) for setup info

## 🎉 Enjoy!

You now have a powerful stress detection system with:
- ✅ Real-time stress monitoring
- ✅ Comprehensive reporting
- ✅ Beautiful, modern UI
- ✅ Export capabilities
- ✅ Smart recommendations

Start detecting and track your stress levels! 🚀

---

**Version**: 2.0 Enhanced
**Last Updated**: January 24, 2026
