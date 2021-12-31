import cv2

cam = cv2.VideoCapture("video/Swerve_HT.mp4")

if not cam.isOpened():
    print("Cannot open camera!")
    exit()
cam.set(5, 60)

# Object Detector from stable camera 
detector = cv2.createBackgroundSubtractorMOG2(history = 300, varThreshold = 600)
#detector = cv2.createBackgroundSubtractorKNN(history= 300)
while True:
    ret,frame = cam.read()
    #h,w,_ = frame.shape
    #print(h,w)

    # Area extraction
    #roi = frame[60:120,360:480]

    # Object Extraction
    mask = detector.apply(frame)
    _,mask = cv2.threshold(mask,254,255,cv2.THRESH_BINARY)

    contours,_=cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1200: #and area < 3000: 
            #cv2.drawContours(frame,[cnt],-1,(0,255,0),2)
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),((x+w),(y+h)),(0,255,0),3)


    cv2.imshow("Frame",frame)
    cv2.imshow("Mask",mask)
    #cv2.imshow("ROI",roi)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows() 
exit()