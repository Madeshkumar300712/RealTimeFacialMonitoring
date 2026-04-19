#!/usr/bin/env python3
"""
Dataset Information and Statistics
Displays comprehensive information about the fer2013 dataset
"""

import os
from collections import defaultdict

def count_images_in_directory(directory):
    """Count image files in a directory"""
    extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    count = 0
    for file in os.listdir(directory):
        if file.lower().endswith(extensions):
            count += 1
    return count

def analyze_dataset():
    """Analyze the fer2013 dataset structure"""
    
    print("\n" + "="*70)
    print("FER2013 DATASET ANALYSIS")
    print("="*70)
    
    dataset_path = 'fer2013'
    emotions = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    splits = ['train', 'val']
    
    stats = defaultdict(dict)
    
    # Check if dataset exists
    if not os.path.exists(dataset_path):
        print("\n❌ Dataset directory not found: fer2013/")
        print("\nPlease create the dataset structure:")
        print("  fer2013/")
        print("    ├── train/")
        print("    │   ├── Angry/")
        print("    │   ├── Fear/")
        print("    │   ├── Happy/")
        print("    │   ├── Neutral/")
        print("    │   ├── Sad/")
        print("    │   └── Surprise/")
        print("    └── val/")
        print("        ├── Angry/")
        print("        ├── Fear/")
        print("        ├── Happy/")
        print("        ├── Neutral/")
        print("        ├── Sad/")
        print("        └── Surprise/")
        return False
    
    print("\n📊 Dataset Statistics\n")
    
    total_train = 0
    total_val = 0
    
    for split in splits:
        split_path = os.path.join(dataset_path, split)
        print(f"\n{split.upper()} SET:")
        print("-" * 50)
        
        if not os.path.exists(split_path):
            print(f"  ❌ Not found: {split_path}")
            continue
        
        for emotion in emotions:
            emotion_path = os.path.join(split_path, emotion)
            
            if os.path.exists(emotion_path):
                count = count_images_in_directory(emotion_path)
                stats[split][emotion] = count
                
                # Determine status emoji
                if count == 0:
                    status = "❌"
                elif count < 100:
                    status = "⚠️ "
                else:
                    status = "✅"
                
                print(f"  {status} {emotion:12s}: {count:5d} images")
                
                if split == 'train':
                    total_train += count
                else:
                    total_val += count
            else:
                print(f"  ❌ {emotion:12s}: Directory not found")
                stats[split][emotion] = 0
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\n📦 Total Training Images:   {total_train:,}")
    print(f"📦 Total Validation Images: {total_val:,}")
    print(f"📦 Total Dataset Size:      {total_train + total_val:,}")
    
    # Distribution analysis
    print("\n" + "-"*70)
    print("CLASS DISTRIBUTION")
    print("-"*70)
    
    if total_train > 0:
        print("\nTraining Set:")
        for emotion in emotions:
            count = stats['train'].get(emotion, 0)
            percentage = (count / total_train * 100) if total_train > 0 else 0
            bar_length = int(percentage / 2)  # Scale to 50 chars max
            bar = "█" * bar_length
            print(f"  {emotion:12s} [{bar:<50s}] {percentage:5.1f}% ({count:,})")
    
    if total_val > 0:
        print("\nValidation Set:")
        for emotion in emotions:
            count = stats['val'].get(emotion, 0)
            percentage = (count / total_val * 100) if total_val > 0 else 0
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            print(f"  {emotion:12s} [{bar:<50s}] {percentage:5.1f}% ({count:,})")
    
    # Quality assessment
    print("\n" + "="*70)
    print("QUALITY ASSESSMENT")
    print("="*70)
    
    issues = []
    recommendations = []
    
    # Check minimum samples
    min_samples_per_class = 100
    for emotion in emotions:
        train_count = stats['train'].get(emotion, 0)
        if train_count < min_samples_per_class:
            issues.append(f"Low training samples for '{emotion}': {train_count} (recommended: >{min_samples_per_class})")
    
    # Check balance
    if total_train > 0:
        train_counts = [stats['train'].get(e, 0) for e in emotions]
        max_count = max(train_counts)
        min_count = min(train_counts)
        imbalance_ratio = max_count / min_count if min_count > 0 else float('inf')
        
        if imbalance_ratio > 3:
            issues.append(f"High class imbalance: {imbalance_ratio:.1f}x difference between largest and smallest class")
            recommendations.append("Consider data augmentation or class weighting during training")
    
    # Check validation split
    if total_train > 0 and total_val > 0:
        val_ratio = total_val / (total_train + total_val)
        if val_ratio < 0.1:
            recommendations.append(f"Small validation set ({val_ratio*100:.1f}%). Consider 15-20% for better evaluation")
        elif val_ratio > 0.3:
            recommendations.append(f"Large validation set ({val_ratio*100:.1f}%). Consider using more data for training")
    
    if issues:
        print("\n⚠️  Issues Detected:\n")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("\n✅ No major issues detected")
    
    if recommendations:
        print("\n💡 Recommendations:\n")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    
    # Training estimates
    print("\n" + "="*70)
    print("TRAINING ESTIMATES")
    print("="*70)
    
    if total_train > 0:
        # Rough estimates
        epochs = 50
        batch_size = 32
        steps_per_epoch = total_train // batch_size
        
        # Time estimates (rough)
        seconds_per_step_cpu = 0.5  # Approximate
        seconds_per_step_gpu = 0.05
        
        total_time_cpu = steps_per_epoch * epochs * seconds_per_step_cpu / 60  # minutes
        total_time_gpu = steps_per_epoch * epochs * seconds_per_step_gpu / 60
        
        print(f"\nEstimated Training Time:")
        print(f"  • With CPU: ~{total_time_cpu:.0f} minutes ({total_time_cpu/60:.1f} hours)")
        print(f"  • With GPU: ~{total_time_gpu:.0f} minutes ({total_time_gpu/60:.1f} hours)")
        print(f"\nTraining Configuration:")
        print(f"  • Epochs: {epochs}")
        print(f"  • Batch Size: {batch_size}")
        print(f"  • Steps per Epoch: {steps_per_epoch}")
        print(f"  • Total Steps: {steps_per_epoch * epochs:,}")
    
    print("\n" + "="*70)
    
    # Overall readiness
    ready = total_train >= 600 and total_val >= 100
    
    if ready:
        print("\n✅ Dataset is ready for training!")
        print("\nNext steps:")
        print("  1. Run: python emotion_recognition.py")
        print("  2. Wait for training to complete")
        print("  3. Run: python eyebrow_detection.py")
    else:
        print("\n⚠️  Dataset needs more images before training")
        print("\nPlease add more images to the dataset directories")
    
    print()
    return ready

if __name__ == "__main__":
    analyze_dataset()
