#READ README FILE FIRST
#COPY ALL THING AND PASTE TO AI AND ASK WHAT SHOULD I DO

import cv2
from ultralytics import YOLO
import os

# Path to your trained model
model_path = 'source/best.pt'

# Check if model exists
if os.path.exists(model_path):
    print(f"Loading saved model from {model_path}")
    model = YOLO(model_path)
else: 
    # if you need train for new data or updata then remove 'source/best.pt' and comments of #model and #model.train for training 
    print(f"No model found at {model_path}. Training start")
    #model = YOLO('yolov8n.pt')
    #model.train(data='data.yml', epochs=80, imgsz=416)  # 2-hour run was expected but reality is 4-hour blyat
    #print(f"Training complete. Model saved to {model_path}")

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Couldn’t open webcam")
    exit()

# Detection loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    # Detect objects
    results = model(frame)

    # Process detections
    detections_found = False
    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            conf = box.conf[0]
            label = model.names[cls]
            if conf > 0.001:  
                detections_found = True
                print(f"Detected: {label} (Confidence: {conf:.2f})")
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                print(f"Low confidence: {label} (Confidence: {conf:.2f})")
    if not detections_found:
        print("No detections above 0.5 confidence in this frame")

    # Show frame
    cv2.imshow('Trash Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()