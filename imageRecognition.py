import cv2
from ultralytics import YOLO

# Load your YOLOv8 model
model = YOLO("imageRecog.pt")  # Replace with your model path

# Class name mapping (matches your YAML file)
class_names = {
    0: "animal",
    1: "human",
    2: "vehicle"
}

# Color for each class
class_colors = {
    0: (255, 0, 0),     # Blue - Human
    1: (0, 255, 0),     # Green - Animal
    2: (0, 0, 255)      # Red - Vehicle
}

# OpenCV webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO inference
    results = model(frame, verbose=False)[0]

    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        label = f"{class_names.get(cls_id, 'unknown')} {conf:.2f}"
        color = class_colors.get(cls_id, (255, 255, 255))

        # Draw bounding box and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Show result
    cv2.imshow("YOLO Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
