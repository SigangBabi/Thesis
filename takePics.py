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

#capture pictures while webcam is open
    filename = f"capture_{count}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Image saved: {filename}")
    count += 1

#delayed by 3 seconds to ensure that the webcam will not loop
    time.sleep(3)

#close webcam
    k = cv2.waitKey(1)

    if k%256 == 27:
        print("Closing Webcam")
        break


cap.release()
cv2.destroyAllWindows()
