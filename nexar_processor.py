#!/usr/bin/env python3
import sys
sys.path.append('src')
from python_interface import TsotchkeInterface
import cv2
import numpy as np
import os
import time
import pandas as pd
from datetime import datetime

def process_video(video_path, tsotchke):
    print(f"🎬 {os.path.basename(video_path)}")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0
    max_risk = 0.0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        risk = tsotchke.get_collision_risk()
        max_risk = max(max_risk, risk)
        frame_count += 1
        
        if frame_count % max(1, total_frames // 5) == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            print(f"   {frame_count}/{total_frames} | Risk: {risk:.3f} | {fps:.1f} FPS")
    
    cap.release()
    processing_fps = frame_count / (time.time() - start_time)
    collision_pred = 1 if max_risk > 0.5 else 0
    
    print(f"   🏁 {processing_fps:.1f} FPS | {'🚨 COLLISION' if collision_pred else '✅ SAFE'} | Confidence: {max_risk:.3f}")
    
    return {
        'video_id': os.path.splitext(os.path.basename(video_path))[0],
        'collision_prediction': collision_pred,
        'confidence_score': max_risk,
        'fps': processing_fps
    }

def main():
    dataset_path = "./dataset"
    
    print("🏆 NEXAR PROCESSOR - COMPETITION MODE")
    print("=" * 40)
    
    # Initialize tsotchke
    tsotchke = TsotchkeInterface()
    if not tsotchke.initialize(128, 0.15):
        print("❌ Failed to initialize")
        return
    
    # Check dataset
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found: {dataset_path}")
        return
    
    # Find videos
    video_files = [f for f in os.listdir(dataset_path) if f.endswith('.mp4')]
    
    if not video_files:
        print("❌ No videos found")
        return
    
    print(f"📊 Found {len(video_files)} videos")
    
    # Process first 3 videos for test
    results = []
    for i, video_file in enumerate(video_files[:3]):
        print(f"\n🎥 [{i+1}/3] {video_file}")
        video_path = os.path.join(dataset_path, video_file)
        result = process_video(video_path, tsotchke)
        if result:
            results.append(result)
    
    # Generate submission
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        submission_data = []
        for r in results:
            submission_data.append({
                'video_id': r['video_id'],
                'collision_prediction': r['collision_prediction'],
                'confidence_score': r['confidence_score']
            })
        
        df = pd.DataFrame(submission_data)
        filename = f"/tmp/nexar_submission_{timestamp}.csv"
        df.to_csv(filename, index=False)
        
        avg_fps = np.mean([r['fps'] for r in results])
        collision_count = sum(1 for r in results if r['collision_prediction'] == 1)
        
        print(f"\n🏆 RESULTS:")
        print(f"   Videos: {len(results)}")
        print(f"   Collisions: {collision_count}")
        print(f"   Avg FPS: {avg_fps:.1f}")
        print(f"   Submission: {filename}")
        
        if avg_fps > 1000:
            print("🚀 BLAZING FAST!")
        elif avg_fps > 500:
            print("⚡ EXCELLENT!")
        else:
            print("👍 GOOD!")
    
    tsotchke.cleanup()

if __name__ == "__main__":
    main()
