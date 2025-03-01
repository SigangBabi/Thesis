import cv2
import supervision as sv
from ultralytics import YOLO

#Arduino Communication


model = YOLO(f'bestest.pt')

boundingBoxAnnotator = sv.BoxAnnotator()
labelAnnotator = sv.LabelAnnotator()


cap = cv2.VideoCapture(0)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
vertical_center = frame_width // 2
line_width = 450

if not cap.isOpened():
    print("Unable to read Camera Feed")

cap.set(cv2.CAP_PROP_FPS, 90)  # Try setting to 60 FPS or a higher value



while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)

    band_start = vertical_center - line_width // 2
    band_end = vertical_center + line_width // 2

    personInTheWay = False

    for detection in detections.xyxy:
        x1, y1, x2, y2 = map(int, detection[:4])



        if x1 <= band_end and x2 >= band_start:
            personInTheWay = True
    '''
    if personInTheWay:
        arduino.write(b'T\n')
    else:
        arduino.write(b'F/n')
    '''

        # Check if the object is not centered


    annotatedImages = boundingBoxAnnotator.annotate(scene=frame, detections=detections)
    annotatedImages = labelAnnotator.annotate(scene=annotatedImages, detections=detections)


    cv2.imshow('Webcam', annotatedImages)

    k = cv2.waitKey(1)

    if k%256 == 27:
        print("Closing Webcam")
        break

cap.release()
cv2.destroyAllWindows()
