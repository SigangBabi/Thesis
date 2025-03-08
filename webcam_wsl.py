import cv2

while True:

    img_path = "/mnt/e/Frames/latest_frame.jpg"
    img = cv2.imread(img_path)

    if img is not None:
        cv2.imshow("Webcam in WSL", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


