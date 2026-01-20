import os
import pandas as pd
from ultralytics import YOLO
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Load YOLOv8 nano model
model = YOLO('yolov8n.pt') 

def classify_image(detected_classes):
    """Categorizes image based on instructions."""
    has_person = 'person' in detected_classes
    # Proxies for medical/pharmaceutical products in general YOLO
    product_objects = ['bottle', 'cup', 'bowl', 'vase', 'toothbrush']
    has_product = any(obj in detected_classes for obj in product_objects)

    if has_person and has_product:
        return 'promotional'
    elif has_product:
        return 'product_display'
    elif has_person:
        return 'lifestyle'
    else:
        return 'other'

def run_detection():
    image_base_path = 'data/raw/images'
    detection_results = []

    if not os.path.exists(image_base_path):
        logging.error("Image directory not found!")
        return

    for channel in os.listdir(image_base_path):
        channel_path = os.path.join(image_base_path, channel)
        if not os.path.isdir(channel_path): continue

        logging.info(f"Processing images for channel: {channel}")
        
        for image_file in os.listdir(channel_path):
            if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(channel_path, image_file)
                # message_id is the filename
                message_id = image_file.split('.')[0] 

                # Run inference
                results = model(image_path, conf=0.25, verbose=False)
                
                # Get detected classes
                detected_classes = [results[0].names[int(c)] for c in results[0].boxes.cls]
                category = classify_image(detected_classes)
                
                # If no objects found, still record it as 'other'
                if not detected_classes:
                    detection_results.append({
                        'message_id': int(message_id),
                        'channel_username': channel,
                        'detected_class': 'none',
                        'confidence': 0.0,
                        'image_category': 'other'
                    })
                else:
                    for box in results[0].boxes:
                        detection_results.append({
                            'message_id': int(message_id),
                            'channel_username': channel,
                            'detected_class': results[0].names[int(box.cls)],
                            'confidence': float(box.conf),
                            'image_category': category
                        })

    # Save to CSV
    os.makedirs('data/enriched', exist_ok=True)
    df = pd.DataFrame(detection_results)
    df.to_csv('data/enriched/yolo_detections.csv', index=False)
    logging.info(f"Saved results to data/enriched/yolo_detections.csv")

if __name__ == "__main__":
    run_detection()