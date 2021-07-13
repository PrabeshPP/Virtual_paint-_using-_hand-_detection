import cv2 as cv
import hand_detection as  hd
import numpy as np
import time
import os

brushThickness=15
eraseThickness=50

cap=cv.VideoCapture(0)
path="images"
list=os.listdir(path)
current_time=0
post_time=0

overlay_list=[]
for pointer in list:
    img=cv.imread(f"{path}/{pointer}")
    overlay_list.append(img)

detect=hd.detect_hand(detection=0.3)
image=overlay_list[0]
draw_color=(255,0,255)

xp,yp=0,0
imgCanavs=np.zeros((480,640,3),np.uint8)

while True:
    ret,frame=cap.read()
    frame=cv.flip(frame,1)
    height1,width1,color1=frame.shape
    height2,width2,color2=image.shape
    image=cv.resize(image,(width1,height2))
    height2,width,color=image.shape
    frame[0:height2,0:width1]=image
    frame=detect.show_hand(frame)
    list_=detect.getposition(frame,False)


    if len(list_)!=0:
        x1,y1=list_[8][1:]
        x2,y2=list_[12][1:]
        fingers = detect.finger_up()
        if fingers[1] and fingers [2]:
            xp,yp=0,0
            if y1<125:
                if 20<x1<200:
                    draw_color=(255,0,255)
                    image=overlay_list[0]
                elif 205<x1<360:
                    draw_color=(255,0,0)
                    image=overlay_list[1]
                elif 385<x1<480:
                    draw_color=(0,255,0)
                    image=overlay_list[2]
                elif 490<x1<640:
                    draw_color=(0,0,0)
                    image=overlay_list[3]

            cv.rectangle(frame,(x1,y1-15),(x2,y2+15),draw_color,-1)


        if fingers[1] and fingers[2]==False:
            cv.circle(frame,(x1,y1),15,draw_color,-1)
            if xp==0 and yp==0:
                    xp,yp=x1,y1
            if draw_color==(0,0,0):
                cv.line(frame,(xp,yp),(x1,y1),draw_color,eraseThickness)
                cv.line(imgCanavs,(xp,yp),(x1,y1),draw_color,eraseThickness)
            else:
                cv.line(frame, (xp, yp), (x1, y1), draw_color, brushThickness)
                cv.line(imgCanavs, (xp, yp), (x1, y1), draw_color, brushThickness)
            xp,yp=x1,y1

    frameGray=cv.cvtColor(imgCanavs,cv.COLOR_BGR2GRAY)
    _,frameInv=cv.threshold(frameGray,50,255,cv.THRESH_BINARY_INV)
    frameInv=cv.cvtColor(frameInv,cv.COLOR_GRAY2BGR)
    frame=cv.bitwise_and(frame,frameInv)
    frame=cv.bitwise_or(frame,imgCanavs)



    current_time=time.time()
    fps=1/(current_time-post_time)
    post_time=current_time
    # frame=cv.addWeighted(frame,0.5,imgCanavs,0.5,0)
    cv.putText(frame,f"FPS:{str(int(fps))}",(10,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2,cv.LINE_AA)
    cv.imshow("video",frame)


    if cv.waitKey(1)==ord('q'):
        break
cap.release()
cv.destroyAllWindows()