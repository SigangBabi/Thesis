#!/usr/bin/env python3
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# Path to shared image in WSL2
img_path = "/mnt/e/Frames/latest_frame.jpg"

# Initialize ROS node
rospy.init_node("webcam_publisher")
image_pub = rospy.Publisher("/camera/image_raw", Image, queue_size=10)
bridge = CvBridge()

while not rospy.is_shutdown():
    img = cv2.imread(img_path)

    if img is not None:
        image_msg = bridge.cv2_to_imgmsg(img, encoding="bgr8")
        image_pub.publish(image_msg)
        cv2.imshow("Webcam Test", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()