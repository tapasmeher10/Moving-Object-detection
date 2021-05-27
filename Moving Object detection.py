import cv2
import time
import datetime
import imutils

cam=cv2.VideoCapture(0)
time.sleep(1)


firstframe=None
area=500
while True:
    ret, img=cam.read()
    text="Normal"
    img =imutils.resize(img, width=500)
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussian=cv2.GaussianBlur(gray,(21,21),0)
    if firstframe is None:
        firstframe=gaussian
        continue
    imgdiff=cv2.absdiff(firstframe, gaussian)
    threshimg=cv2.threshold(imgdiff, 25, 225, cv2.THRESH_BINARY)[1]
    threshimg=cv2.dilate(threshimg,None,iterations=2)
    cnts=cv2.findContours(threshimg.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)
    cntnumber=len(cnts)
    for c in cnts:
        if cv2.contourArea(c)<area:
            continue
        (x,y,w,h)=cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 225, 0), 2)
        text ="Moving object detect"
    print(text)
    print("numer of object detect =",cntnumber)
    cv2.putText(img, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 225), 2)
    datet=str(datetime.datetime.now())
    cv2.putText(img, datet, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 225, 225), 2)

    cv2.imshow("camerafeed", img)
    key=cv2.waitKey(1) & 0xff
    if key==ord("q"):
        break
cam.release()
cv2.destroyAllWindows()
