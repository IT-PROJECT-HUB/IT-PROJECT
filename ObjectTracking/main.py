import cv2
from tracker import *

capture = cv2.VideoCapture("highway.mp4")
tracker = DistTracker()

object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

while True:
    ret, main = capture.read()
    height, width, _ = main.shape

    frame = main[340: 720, 500: 800]

    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            x, y, w, h = cv2.boundingRect(contour)

            detections.append([x, y, w, h])

    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("mask", mask)
    cv2.imshow("main", main)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(30)
    if key & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
