import cv2
import time

cap = cv2.VideoCapture(0)
count = 0

while True:
    ret, frame = cap.read()

#if camera failed to start
    if not ret:
        print("Failed to start Camera")
        break

#open webcam
    cv2.imshow('Webcam', frame)

#close webcam
    k = cv2.waitKey(1)

    if k%256 == 27:
        print("Closing Webcam")
        break


cap.release()
cv2.destroyAllWindows()
