"""
Generate Training History Graph
This script creates a sample training/validation accuracy graph for demonstration
You can also modify this to use actual training history data
"""

import matplotlib.pyplot as plt
import numpy as np
import json
import os

def generate_sample_graph():
    """
    Generate a sample training history graph
    """
    # Sample data (replace with actual training data if available)
    epochs = 50
    x = np.arange(1, epochs + 1)
    
    # Simulated training accuracy (starts low, increases with some noise)
    train_acc = 0.5 + 0.4 * (1 - np.exp(-x/10)) + np.random.normal(0, 0.02, epochs)
    train_acc = np.clip(train_acc, 0, 1)
    
    # Simulated validation accuracy (slightly lower, more noise)
    val_acc = 0.45 + 0.38 * (1 - np.exp(-x/12)) + np.random.normal(0, 0.03, epochs)
    val_acc = np.clip(val_acc, 0, 1)
    
    # Simulated losses (decreasing)
    train_loss = 1.5 * np.exp(-x/10) + 0.3 + np.random.normal(0, 0.05, epochs)
    val_loss = 1.6 * np.exp(-x/12) + 0.35 + np.random.normal(0, 0.07, epochs)
    
    # Create the plot
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot accuracy
    axes[0].plot(x, train_acc, label='Training Accuracy', linewidth=2, color='#3498db')
    axes[0].plot(x, val_acc, label='Validation Accuracy', linewidth=2, color='#e74c3c')
    axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim([0, 1])
    
    # Plot loss
    axes[1].plot(x, train_loss, label='Training Loss', linewidth=2, color='#3498db')
    axes[1].plot(x, val_loss, label='Validation Loss', linewidth=2, color='#e74c3c')
    axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Loss', fontsize=12)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Save to static folder for web display
    plt.savefig('static/training_history.png', dpi=100, bbox_inches='tight')
    print("✓ Training history plot saved as 'static/training_history.png'")
    
    # Also save a copy in root directory
    plt.savefig('training_history.png', dpi=100, bbox_inches='tight')
    print("✓ Training history plot also saved as 'training_history.png'")
    
    plt.close()
    
    # Generate sample metrics
    final_metrics = {
        'train_accuracy': f"{train_acc[-1] * 100:.1f}",
        'val_accuracy': f"{val_acc[-1] * 100:.1f}",
        'train_loss': f"{train_loss[-1]:.4f}",
        'val_loss': f"{val_loss[-1]:.4f}",
        'epochs': epochs,
        'classes': 6,
        'best_val_accuracy': f"{np.max(val_acc) * 100:.1f}",
        'best_epoch': int(np.argmax(val_acc) + 1)
    }
    
    with open('training_metrics.json', 'w') as f:
        json.dump(final_metrics, f, indent=4)
    print("✓ Training metrics saved as 'training_metrics.json'")
    
    print("\n" + "="*60)
    print("Training Graph Generated Successfully!")
    print("="*60)
    print(f"Final Training Accuracy: {final_metrics['train_accuracy']}%")
    print(f"Final Validation Accuracy: {final_metrics['val_accuracy']}%")
    print(f"Best Validation Accuracy: {final_metrics['best_val_accuracy']}% (Epoch {final_metrics['best_epoch']})")
    print("="*60)

def load_real_training_history(history_file):
    """
    Load actual training history from a pickle file (if available)
    Usage: python generate_training_graph.py --history history.pkl
    """
    import pickle
    
    with open(history_file, 'rb') as f:
        history = pickle.load(f)
    
    # Create the plot using real data
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot accuracy
    axes[0].plot(history['accuracy'], label='Training Accuracy', linewidth=2, color='#3498db')
    axes[0].plot(history['val_accuracy'], label='Validation Accuracy', linewidth=2, color='#e74c3c')
    axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim([0, 1])
    
    # Plot loss
    axes[1].plot(history['loss'], label='Training Loss', linewidth=2, color='#3498db')
    axes[1].plot(history['val_loss'], label='Validation Loss', linewidth=2, color='#e74c3c')
    axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Loss', fontsize=12)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Save plots
    plt.savefig('static/training_history.png', dpi=100, bbox_inches='tight')
    plt.savefig('training_history.png', dpi=100, bbox_inches='tight')
    print("✓ Training history plot generated from real data")
    
    plt.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2 and sys.argv[1] == '--history':
        # Load from actual history file
        history_file = sys.argv[2]
        if os.path.exists(history_file):
            load_real_training_history(history_file)
        else:
            print(f"Error: History file '{history_file}' not found")
    else:
        # Generate sample graph
        print("Generating sample training history graph...")
        print("(To use real training data, run: python generate_training_graph.py --history history.pkl)")
        print()
        generate_sample_graph()
