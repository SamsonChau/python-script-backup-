import cv2

cam = cv2.VideoCapture("video/Swerve_HT.mp4")

if not cam.isOpened():
    print("Cannot open camera!")
    exit()
#cam.set(5, 60)
#tracker = cv2.TrackerMIL_create() #cannot recover and slow
#tracker = cv2.TrackerKCF_create()  #cannot track after lost and have shield
tracker = cv2.legacy.TrackerMOSSE_create() #fast but not so accurate
#tracker = cv2.TrackerCSRT_create() # slow and hogh accuracy
success,img = cam.read()
box = cv2.selectROI("Tracking", img, False)
tracker.init(img,box)

def drawBox(img,box):
    x,y,w,h = int(box[0]),int(box[2]),int(box[2]),int(box[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255.0,255),3,1)
    cv2.putText(img,"Sucess",(75,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
while True:
    timer = cv2.getTickCount()
    sucess,img = cam.read()
    sucess,box = tracker.update(img)
    print(box)

    if sucess:
        drawBox(img,box)
    else:
        cv2.putText(img,"Lost",(75,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)

    
    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(img,str(int(fps)),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
    cv2.imshow("Tracking",img)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows() 
exit()