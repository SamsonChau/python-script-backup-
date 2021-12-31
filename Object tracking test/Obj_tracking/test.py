import cv2

cam = cv2.VideoCapture(0)

cam.release()
cv2.destroyAllWindows() 
exit()