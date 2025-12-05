import os
import csv
import sys
from datetime import datetime
from ultralytics import YOLO

def log_attendance(model_path, image_dir, csv_path, conf=0.3):
    model = YOLO(model_path)
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    csv_exists = os.path.exists(csv_path)
    
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not csv_exists:
            writer.writerow(['Timestamp', 'Image_Name', 'Students_Detected'])
        
        for img_file in image_files:
            img_path = os.path.join(image_dir, img_file)
            results = model(img_path, conf=conf)
            count = len(results[0].boxes)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, img_file, count])
            print(f"{timestamp} | {img_file} → {count} students")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python log_attendance.py <model.pt> <image_dir> <output.csv>")
        sys.exit(1)
    
    model_path = sys.argv[1]
    image_dir = sys.argv[2]
    csv_path = sys.argv[3]
    log_attendance(model_path, image_dir, csv_path)
