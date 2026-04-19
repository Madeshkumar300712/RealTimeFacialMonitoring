// Global variables
let stream = null;
let processingInterval = null;
let reportUpdateInterval = null;

// Mode selection
function selectMode(mode) {
    document.getElementById('modeSelection').style.display = 'none';
    
    if (mode === 'upload') {
        document.getElementById('uploadMode').style.display = 'block';
    } else if (mode === 'camera') {
        document.getElementById('cameraMode').style.display = 'block';
    }
}

// Back to selection
function backToSelection() {
    // Stop camera if active
    if (stream) {
        stopCamera();
    }
    
    // Hide all modes
    document.getElementById('uploadMode').style.display = 'none';
    document.getElementById('cameraMode').style.display = 'none';
    document.getElementById('uploadResults').style.display = 'none';
    document.getElementById('cameraResults').style.display = 'none';
    
    // Show selection
    document.getElementById('modeSelection').style.display = 'block';
}

// Handle image upload
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Show loading
    showLoading();
    
    // Create form data
    const formData = new FormData();
    formData.append('image', file);
    
    // Send to server
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        displayUploadResults(data);
    })
    .catch(error => {
        hideLoading();
        console.error('Error:', error);
        alert('Error processing image. Please try again.');
    });
}

// Display upload results
function displayUploadResults(data) {
    const resultsContainer = document.getElementById('uploadResults');
    const resultsInfo = document.getElementById('uploadResultsInfo');
    
    if (data.error) {
        alert(data.error);
        return;
    }
    
    // Show annotated image
    document.getElementById('resultImage').src = data.annotated_image;
    
    // Build results HTML
    let html = '';
    
    if (data.results && data.results.length > 0) {
        data.results.forEach((result, index) => {
            const stressClass = result.stress_level < 30 ? 'stress-low' : 
                               result.stress_level < 60 ? 'stress-moderate' : 'stress-high';
            
            const stressColor = result.stress_level < 30 ? '#10b981' : 
                               result.stress_level < 60 ? '#f59e0b' : '#ef4444';
            
            html += `
                <div class="result-card">
                    <div class="result-item">
                        <div class="result-label">Face ${index + 1}</div>
                        <div class="result-value">${data.faces > 1 ? 'Detected' : 'Single Face'}</div>
                    </div>
                    <div class="result-item">
                        <div class="result-label">Emotion</div>
                        <div class="result-value">${result.emotion}</div>
                    </div>
                    <div class="result-item">
                        <div class="result-label">Confidence</div>
                        <div class="result-value">${result.confidence}%</div>
                    </div>
                    <div class="result-item">
                        <div class="result-label">Stress Level</div>
                        <div class="result-value">
                            ${result.stress_level}%
                            <div class="stress-badge ${stressClass}">${result.status}</div>
                        </div>
                        <div class="stress-progress">
                            <div class="stress-progress-fill" style="width: ${result.stress_level}%; background: ${stressColor};"></div>
                        </div>
                    </div>
                </div>
            `;
        });
    } else {
        html = '<div class="result-card"><p>No faces detected in the image.</p></div>';
    }
    
    resultsInfo.innerHTML = html;
    resultsContainer.style.display = 'block';
    
    // Update report if open
    if (document.getElementById('reportPanel').classList.contains('active')) {
        loadReport();
    }
}

// Start camera
async function startCamera() {
    try {
        // Get video stream
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        });
        
        const video = document.getElementById('video');
        video.srcObject = stream;
        
        // Update UI
        document.getElementById('startButton').style.display = 'none';
        document.getElementById('stopButton').style.display = 'inline-flex';
        document.getElementById('cameraResults').style.display = 'block';
        
        // Start processing frames
        processingInterval = setInterval(processFrame, 1000); // Process every second
        
    } catch (error) {
        console.error('Error accessing camera:', error);
        alert('Error accessing camera. Please make sure you have granted camera permissions.');
    }
}

// Stop camera
function stopCamera() {
    // Stop video stream
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    
    // Clear processing interval
    if (processingInterval) {
        clearInterval(processingInterval);
        processingInterval = null;
    }
    
    // Update UI
    const video = document.getElementById('video');
    video.srcObject = null;
    
    document.getElementById('startButton').style.display = 'inline-flex';
    document.getElementById('stopButton').style.display = 'none';
    document.getElementById('cameraResults').style.display = 'none';
}

// Process video frame
function processFrame() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    
    // Set canvas size to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw current frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to base64
    const imageData = canvas.toDataURL('image/jpeg');
    
    // Send to server
    fetch('/api/webcam', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        displayCameraResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Display camera results
function displayCameraResults(data) {
    const resultsInfo = document.getElementById('cameraResultsInfo');
    
    if (data.error) {
        resultsInfo.innerHTML = `<div class="result-card"><p>${data.error}</p></div>`;
        return;
    }
    
    // Build results HTML
    let html = '';
    
    if (data.results && data.results.length > 0) {
        data.results.forEach((result, index) => {
            const stressClass = result.stress_level < 30 ? 'stress-low' : 
                               result.stress_level < 60 ? 'stress-moderate' : 'stress-high';
            
            const stressColor = result.stress_level < 30 ? '#10b981' : 
                               result.stress_level < 60 ? '#f59e0b' : '#ef4444';
            
            html += `
                <div class="result-card">
                    <div class="result-item">
                        <div class="result-label">Faces Detected</div>
                        <div class="result-value">${data.faces}</div>
                    </div>
                    <div class="result-item">
                        <div class="result-label">Emotion</div>
                        <div class="result-value">${result.emotion}</div>
                    </div>
                    <div class="result-item">
                        <div class="result-label">Confidence</div>
                        <div class="result-value">${result.confidence}%</div>
                    </div>
                    <div class="result-item">
                        <div class="result-label">Stress Level</div>
                        <div class="result-value">
                            ${result.stress_level}%
                            <div class="stress-badge ${stressClass}">${result.status}</div>
                        </div>
                        <div class="stress-progress">
                            <div class="stress-progress-fill" style="width: ${result.stress_level}%; background: ${stressColor};"></div>
                        </div>
                    </div>
                </div>
            `;
        });
    } else {
        html = '<div class="result-card"><p>No faces detected. Please position your face in front of the camera.</p></div>';
    }
    
    resultsInfo.innerHTML = html;
    
    // Update report if open
    if (document.getElementById('reportPanel').classList.contains('active')) {
        loadReport();
    }
}

// Loading overlay
function showLoading() {
    document.getElementById('loadingOverlay').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('active');
}

// Check system status on load
window.addEventListener('load', () => {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            const statusIndicator = document.getElementById('systemStatus');
            if (data.model_loaded && data.face_detector_loaded) {
                statusIndicator.innerHTML = `
                    <span class="status-dot"></span>
                    <span class="status-text">System Ready</span>
                `;
            } else {
                statusIndicator.innerHTML = `
                    <span class="status-dot" style="background: var(--warning-color);"></span>
                    <span class="status-text" style="color: var(--warning-color);">Model Loading...</span>
                `;
            }
        })
        .catch(error => {
            console.error('Error checking status:', error);
        });
});

// Drag and drop support for upload
const uploadArea = document.getElementById('uploadArea');

if (uploadArea) {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.background = 'rgba(99, 102, 241, 0.1)';
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--border-color)';
        uploadArea.style.background = 'var(--bg-secondary)';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--border-color)';
        uploadArea.style.background = 'var(--bg-secondary)';
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            const input = document.getElementById('imageInput');
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;
            
            handleImageUpload({ target: input });
        }
    });
}

// Report Panel Functions
function toggleReport() {
    const reportPanel = document.getElementById('reportPanel');
    const isActive = reportPanel.classList.contains('active');
    
    if (isActive) {
        reportPanel.classList.remove('active');
        if (reportUpdateInterval) {
            clearInterval(reportUpdateInterval);
            reportUpdateInterval = null;
        }
    } else {
        reportPanel.classList.add('active');
        
        // Show loading state immediately
        const reportContent = document.getElementById('reportContent');
        reportContent.innerHTML = `
            <div class="report-empty">
                <div class="spinner" style="width: 40px; height: 40px; margin: 20px auto;"></div>
                <p>Loading report...</p>
            </div>
        `;
        
        // Load report data
        loadReport();
        
        // Auto-update report every 5 seconds when open
        reportUpdateInterval = setInterval(loadReport, 5000);
    }
}

function loadReport() {
    fetch('/api/report')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            displayReport(data);
        })
        .catch(error => {
            console.error('Error loading report:', error);
            const reportContent = document.getElementById('reportContent');
            reportContent.innerHTML = `
                <div class="report-empty">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                        <path d="M12 8V12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        <circle cx="12" cy="16" r="1" fill="currentColor"/>
                    </svg>
                    <p>Error loading report</p>
                    <p class="report-empty-subtext">${error.message}</p>
                </div>
            `;
        });
}

function displayReport(data) {
    const reportContent = document.getElementById('reportContent');
    
    if (!data.has_data) {
        reportContent.innerHTML = `
            <div class="report-empty">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                    <path d="M12 8V12L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <p>No detection data available yet</p>
                <p class="report-empty-subtext">Start detecting stress to generate your report</p>
            </div>
        `;
        return;
    }
    
    // Build comprehensive report
    let html = `
        <!-- Overall Status -->
        <div class="overall-status">
            <div class="status-icon" style="background: ${data.status_color}20; color: ${data.status_color};">
                ${getStatusEmoji(data.overall_status)}
            </div>
            <div class="status-label" style="color: ${data.status_color};">${data.overall_status}</div>
            <div class="status-sublabel">Average Stress: ${data.avg_stress.toFixed(1)}%</div>
            <div class="status-sublabel" style="margin-top: 8px; font-size: 12px;">
                Session: ${new Date(data.session_start).toLocaleString()}
            </div>
        </div>
        
        <!-- Statistics -->
        <div class="report-section">
            <h3 class="report-section-title">Session Statistics</h3>
            <div class="stat-grid">
                <div class="stat-item">
                    <div class="stat-label">Total Detections</div>
                    <div class="stat-value">${data.total_detections}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Avg Stress</div>
                    <div class="stat-value">${data.avg_stress.toFixed(1)}<span class="stat-unit">%</span></div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Max Stress</div>
                    <div class="stat-value">${data.max_stress.toFixed(1)}<span class="stat-unit">%</span></div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Min Stress</div>
                    <div class="stat-value">${data.min_stress.toFixed(1)}<span class="stat-unit">%</span></div>
                </div>
            </div>
        </div>
        
        <!-- Emotion Distribution -->
        <div class="report-section">
            <h3 class="report-section-title">Emotion Distribution</h3>
            <div class="emotion-chart">
                ${generateEmotionBars(data.emotion_counts, data.total_detections)}
            </div>
        </div>
        
        <!-- Stress Timeline -->
        <div class="report-section">
            <h3 class="report-section-title">Stress Timeline</h3>
            <div class="stress-timeline">
                ${generateStressChart(data.stress_history)}
            </div>
        </div>
        
        <!-- Recommendations -->
        <div class="report-section">
            <h3 class="report-section-title">Recommendations</h3>
            <div class="recommendations-list">
                ${data.recommendations.map(rec => `
                    <div class="recommendation-item">
                        <svg class="recommendation-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="recommendation-text">${rec}</span>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <!-- Actions -->
        <div class="report-actions">
            <button class="report-action-button primary" onclick="exportReport()">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 20px; height: 20px;">
                    <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M7 10L12 15L17 10M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Export Report
            </button>
            <button class="report-action-button secondary" onclick="resetSession()">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 20px; height: 20px;">
                    <path d="M4 4V9H4.582M4.582 9C5.24585 7.35812 6.43568 5.9829 7.96503 5.08985C9.49438 4.1968 11.2768 3.8364 13.033 4.06513C14.7891 4.29386 16.4198 5.09878 17.6694 6.35377C18.919 7.60875 19.7168 9.24285 19.938 11M4.582 9H9M20 20V15H19.418M19.418 15C18.7542 16.6419 17.5643 18.0171 16.035 18.9101C14.5056 19.8032 12.7232 20.1636 10.967 19.9349C9.21087 19.7061 7.58019 18.9012 6.33056 17.6462C5.08093 16.3912 4.28316 14.7572 4.062 13M19.418 15H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Reset Session
            </button>
        </div>
    `;
    
    reportContent.innerHTML = html;
}

function getStatusEmoji(status) {
    const emojis = {
        'Low Stress': '😊',
        'Moderate Stress': '😐',
        'High Stress': '😰'
    };
    return emojis[status] || '😊';
}

function generateEmotionBars(emotionCounts, total) {
    const emotionColors = {
        'Happy': '#10b981',
        'Neutral': '#6366f1',
        'Surprise': '#f59e0b',
        'Sad': '#8b5cf6',
        'Angry': '#ef4444',
        'Fear': '#ec4899'
    };
    
    let html = '';
    for (const [emotion, count] of Object.entries(emotionCounts)) {
        const percentage = (count / total * 100).toFixed(1);
        const color = emotionColors[emotion] || '#6366f1';
        
        html += `
            <div class="emotion-bar">
                <div class="emotion-bar-header">
                    <span class="emotion-name">${emotion}</span>
                    <span class="emotion-count">${count} (${percentage}%)</span>
                </div>
                <div class="emotion-bar-fill">
                    <div class="emotion-bar-inner" style="width: ${percentage}%; background: ${color};"></div>
                </div>
            </div>
        `;
    }
    
    return html || '<p style="color: var(--text-secondary);">No emotion data available</p>';
}

function generateStressChart(stressHistory) {
    if (!stressHistory || stressHistory.length === 0) {
        return '<p style="color: var(--text-secondary); text-align: center; padding: 60px 0;">No timeline data available</p>';
    }
    
    const canvas = document.createElement('canvas');
    canvas.className = 'timeline-canvas';
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = 400;
    canvas.height = 160;
    
    const padding = 20;
    const width = canvas.width - 2 * padding;
    const height = canvas.height - 2 * padding;
    
    // Draw grid
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1;
    
    // Horizontal lines
    for (let i = 0; i <= 4; i++) {
        const y = padding + (height / 4) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(canvas.width - padding, y);
        ctx.stroke();
    }
    
    // Handle single data point case
    if (stressHistory.length === 1) {
        const x = padding + width / 2;
        const y = padding + height - (stressHistory[0] / 100) * height;
        
        // Draw single point
        ctx.fillStyle = '#6366f1';
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, Math.PI * 2);
        ctx.fill();
        
        // Add label
        ctx.fillStyle = '#f1f5f9';
        ctx.font = '14px Inter';
        ctx.textAlign = 'center';
        ctx.fillText(`${stressHistory[0].toFixed(1)}%`, x, y - 15);
    } else {
        // Draw stress line for multiple points
        ctx.strokeStyle = '#6366f1';
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        stressHistory.forEach((stress, index) => {
            const x = padding + (width / (stressHistory.length - 1)) * index;
            const y = padding + height - (stress / 100) * height;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();
        
        // Draw points
        ctx.fillStyle = '#6366f1';
        stressHistory.forEach((stress, index) => {
            const x = padding + (width / (stressHistory.length - 1)) * index;
            const y = padding + height - (stress / 100) * height;
            
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fill();
        });
    }
    
    return canvas.outerHTML;
}

function exportReport() {
    fetch('/api/report')
        .then(response => response.json())
        .then(data => {
            if (!data.has_data) {
                alert('No data available to export');
                return;
            }
            
            // Create report text
            const reportText = `
STRESS DETECTION REPORT
Generated: ${new Date().toLocaleString()}
Session Start: ${new Date(data.session_start).toLocaleString()}

=== OVERALL STATUS ===
Status: ${data.overall_status}
Average Stress Level: ${data.avg_stress.toFixed(1)}%
Maximum Stress Level: ${data.max_stress.toFixed(1)}%
Minimum Stress Level: ${data.min_stress.toFixed(1)}%
Total Detections: ${data.total_detections}

=== EMOTION DISTRIBUTION ===
${Object.entries(data.emotion_counts).map(([emotion, count]) => 
    `${emotion}: ${count} (${(count / data.total_detections * 100).toFixed(1)}%)`
).join('\n')}

=== RECOMMENDATIONS ===
${data.recommendations.map((rec, i) => `${i + 1}. ${rec}`).join('\n')}

=== STRESS TIMELINE ===
${data.stress_history.map((stress, i) => `Reading ${i + 1}: ${stress.toFixed(1)}%`).join('\n')}
            `;
            
            // Download as text file
            const blob = new Blob([reportText], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `stress-report-${new Date().toISOString().split('T')[0]}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error exporting report:', error);
            alert('Error exporting report');
        });
}

function resetSession() {
    if (!confirm('Are you sure you want to reset the session data? This cannot be undone.')) {
        return;
    }
    
    fetch('/api/report/reset', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        loadReport();
        alert('Session data has been reset');
    })
    .catch(error => {
        console.error('Error resetting session:', error);
        alert('Error resetting session');
    });
}
