# Training and Validation Accuracy Graph Guide

## Overview
This guide explains how to view and generate training/validation accuracy graphs (like Figure 3.2) for the facial emotion recognition model.

## Accessing the Metrics Dashboard

### Method 1: Through the Web UI
1. Start the web application:
   ```bash
   ./run_webapp.sh
   ```
2. Open your browser to `http://localhost:5000`
3. Click the **chart icon** (📊) in the top-right header
4. You'll be taken to the `/metrics` page showing:
   - Training and validation accuracy trends
   - Model performance metrics
   - Architecture details

### Method 2: Direct URL
Navigate directly to: `http://localhost:5000/metrics`

## Generating the Training Graph

### Option 1: Generate Sample Graph (Quick Demo)
If you want to see the graph immediately without training:

```bash
python generate_training_graph.py
```

This creates:
- `static/training_history.png` - Graph displayed in the web UI
- `training_metrics.json` - Metrics data for the dashboard

### Option 2: Train the Model (Real Data)
To generate graphs from actual model training:

```bash
python emotion_recognition.py
```

This will:
1. Train the CNN model on FER2013 dataset
2. Automatically generate `training_history.png`
3. Save to both root directory and `static/` folder
4. Create `training_metrics.json` with real metrics

**Note:** Training requires:
- FER2013 dataset in `fer2013/` directory
- TensorFlow/Keras installed
- Approximately 30-60 minutes (depending on hardware)

## What the Graph Shows

The training graph displays two plots side by side:

### Left Plot: Model Accuracy
- **Blue line**: Training accuracy over epochs
- **Red line**: Validation accuracy over epochs
- Shows how well the model learns over time
- Validation accuracy indicates generalization performance

### Right Plot: Model Loss
- **Blue line**: Training loss over epochs
- **Red line**: Validation loss over epochs
- Lower loss = better performance
- Gap between lines indicates overfitting/underfitting

## Metrics Dashboard Features

The `/metrics` page displays:

1. **Performance Cards**
   - Training Accuracy
   - Validation Accuracy
   - Total Epochs
   - Number of Classes

2. **Training Graph**
   - Dual plot showing accuracy and loss trends
   - Automatically refreshes if new training data is available

3. **Model Architecture**
   - CNN structure details
   - Layer configuration
   - Hyperparameters

## Integrating into Reports/Papers

### To include the graph in your documentation:

1. **Copy the graph:**
   ```bash
   cp static/training_history.png ~/Documents/my_report/
   ```

2. **In LaTeX:**
   ```latex
   \begin{figure}[h]
   \centering
   \includegraphics[width=0.8\textwidth]{training_history.png}
   \caption{Training and validation accuracy trends of facial emotion recognition model.}
   \label{fig:training_accuracy}
   \end{figure}
   ```

3. **In Markdown:**
   ```markdown
   ![Figure 3.2: Training and validation accuracy trends](training_history.png)
   ```

## Customizing the Graph

To modify the appearance, edit `emotion_recognition.py` function `plot_training_history()`:

```python
# Change colors
axes[0].plot(..., color='#yourcolor')

# Adjust figure size
fig, axes = plt.subplots(1, 2, figsize=(width, height))

# Change title/labels
axes[0].set_title('Your Custom Title')
```

## Troubleshooting

### Graph Not Showing?
1. Check if `static/training_history.png` exists:
   ```bash
   ls -la static/training_history.png
   ```

2. Generate sample graph:
   ```bash
   python generate_training_graph.py
   ```

3. Refresh the metrics page (browser cache issue):
   - Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

### Metrics Show Default Values?
- Run `generate_training_graph.py` or `emotion_recognition.py` to create `training_metrics.json`
- The app will automatically load real metrics when available

## Quick Commands Summary

```bash
# Generate sample graph immediately
python generate_training_graph.py

# Train model and generate real graphs
python emotion_recognition.py

# Start web app to view graphs
./run_webapp.sh

# View metrics page
# Navigate to: http://localhost:5000/metrics
```

## File Locations

- **Web-accessible graph**: `static/training_history.png`
- **Backup copy**: `training_history.png`
- **Metrics data**: `training_metrics.json`
- **Metrics page template**: `templates/metrics.html`
- **Training script**: `emotion_recognition.py`

## Next Steps

1. Generate a sample graph to see the UI: `python generate_training_graph.py`
2. Start the web app: `./run_webapp.sh`
3. Visit: `http://localhost:5000/metrics`
4. When ready, train with real data: `python emotion_recognition.py`

---

**Note**: The metrics dashboard is automatically integrated into your web UI. Users can easily access it via the chart icon in the header.
