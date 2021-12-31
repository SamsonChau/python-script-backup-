import numpy as np
import cv2 

cam = cv2.VideoCapture("video/Swerve_HKU.mp4")

while True:
  ret,frame = cam.read()

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.medianBlur(gray, 5)

  circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=300)
  
  detected_circles = np.uint16(np.around(circles))
  for (x, y ,r) in detected_circles[0, :]:
    cv2.circle(frame, (x, y), r, (0, 0, 0), 3)
    cv2.circle(frame, (x, y), 2, (0, 255, 255), 3)

  cv2.imshow('output',frame)
  if cv2.waitKey(1) == ord('q'):
    break

cam.release()
cv2.destroyAllWindows() 
exit()