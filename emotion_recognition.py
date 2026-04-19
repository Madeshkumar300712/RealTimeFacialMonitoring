"""
Emotion Recognition Model Training Script
Trains a CNN model on the fer2013 dataset to classify facial emotions
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt

# Configuration
IMG_SIZE = 48
BATCH_SIZE = 32
EPOCHS = 50
DATASET_PATH = 'fer2013'

def create_emotion_model():
    """
    Create a CNN model for emotion recognition
    """
    model = keras.Sequential([
        # First Convolutional Block
        layers.Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Second Convolutional Block
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Third Convolutional Block
        layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fourth Convolutional Block
        layers.Conv2D(512, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(512, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fully Connected Layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        
        # Output Layer - 6 emotions (Angry, Fear, Happy, Neutral, Sad, Surprise)
        layers.Dense(6, activation='softmax')
    ])
    
    return model

def prepare_data():
    """
    Prepare data generators for training and validation
    """
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Only rescaling for validation
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        os.path.join(DATASET_PATH, 'train'),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        color_mode='grayscale',
        class_mode='categorical',
        shuffle=True
    )
    
    # Load validation data
    val_generator = val_datagen.flow_from_directory(
        os.path.join(DATASET_PATH, 'val'),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        color_mode='grayscale',
        class_mode='categorical',
        shuffle=False
    )
    
    return train_generator, val_generator

def plot_training_history(history):
    """
    Plot training and validation accuracy/loss
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot accuracy
    axes[0].plot(history.history['accuracy'], label='Training Accuracy', linewidth=2, color='#3498db')
    axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2, color='#e74c3c')
    axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim([0, 1])
    
    # Plot loss
    axes[1].plot(history.history['loss'], label='Training Loss', linewidth=2, color='#3498db')
    axes[1].plot(history.history['val_loss'], label='Validation Loss', linewidth=2, color='#e74c3c')
    axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Loss', fontsize=12)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save to static folder for web display
    plt.savefig('static/training_history.png', dpi=100, bbox_inches='tight')
    print("Training history plot saved as 'static/training_history.png'")
    
    # Also save a copy in root directory
    plt.savefig('training_history.png', dpi=100, bbox_inches='tight')
    print("Training history plot also saved as 'training_history.png'")
    
    plt.close()
    
    # Save training metrics to JSON
    import json
    final_metrics = {
        'train_accuracy': f"{history.history['accuracy'][-1] * 100:.1f}",
        'val_accuracy': f"{history.history['val_accuracy'][-1] * 100:.1f}",
        'train_loss': f"{history.history['loss'][-1]:.4f}",
        'val_loss': f"{history.history['val_loss'][-1]:.4f}",
        'epochs': len(history.history['accuracy']),
        'classes': 6,
        'best_val_accuracy': f"{max(history.history['val_accuracy']) * 100:.1f}",
        'best_epoch': history.history['val_accuracy'].index(max(history.history['val_accuracy'])) + 1
    }
    
    with open('training_metrics.json', 'w') as f:
        json.dump(final_metrics, f, indent=4)
    print("Training metrics saved as 'training_metrics.json'")

def train_model():
    """
    Main training function
    """
    print("="*50)
    print("Starting Emotion Recognition Model Training")
    print("="*50)
    
    # Prepare data
    print("\nPreparing data generators...")
    train_generator, val_generator = prepare_data()
    
    print(f"\nTraining samples: {train_generator.samples}")
    print(f"Validation samples: {val_generator.samples}")
    print(f"Classes: {list(train_generator.class_indices.keys())}")
    
    # Create model
    print("\nCreating model architecture...")
    model = create_emotion_model()
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\nModel Summary:")
    model.summary()
    
    # Callbacks
    callbacks = [
        ModelCheckpoint(
            'emotion_model_best.h5',
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train model
    print("\n" + "="*50)
    print("Training Started...")
    print("="*50 + "\n")
    
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    model.save('emotion_model_final.h5')
    print("\n" + "="*50)
    print("Training Completed!")
    print("Models saved as 'emotion_model_best.h5' and 'emotion_model_final.h5'")
    print("="*50)
    
    # Plot training history
    plot_training_history(history)
    
    # Evaluate on validation set
    print("\nEvaluating on validation set...")
    val_loss, val_accuracy = model.evaluate(val_generator)
    print(f"\nFinal Validation Loss: {val_loss:.4f}")
    print(f"Final Validation Accuracy: {val_accuracy:.4f}")
    
    return model, history

if __name__ == "__main__":
    # Set random seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)
    
    # Train the model
    model, history = train_model()
