import cv2 as cv
import mediapipe as mp
import time
class detect_hand:
    def __init__(self,mode=False,maxhands=2,detection=0.5,tracking=0.5):
        self.mode=mode
        self.maxhands=maxhands
        self.detection=detection
        self.tracking=tracking

        self.hand = mp.solutions.hands
        self.hands = self.hand.Hands(False,self.maxhands,self.detection,self.tracking)
        self.draw = mp.solutions.drawing_utils
        self.tipID = [4, 8, 12, 16, 20]
    def show_hand(self,frame,draw=True):
        self.frame_rgb=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        self.result=self.hands.process(self.frame_rgb)
        self.lmark=self.result.multi_hand_landmarks
        if self.lmark:
            for pointer in self.lmark:
                if draw:
                    self.draw.draw_landmarks(frame,pointer,self.hand.HAND_CONNECTIONS)
        return frame
    def getposition(self,frame,handno=0,draw=True):
        self.lmlist=[]
        if self.lmark:

            pointer=self.lmark[handno]

            for id, lm in enumerate(pointer.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lmlist.append([id,cx,cy])
                    if draw:
                        self.draw.draw_landmarks(frame, pointer, self.hand.HAND_CONNECTIONS)
        return self.lmlist
    def finger_up(self):
        fingers=[]

        if self.lmlist[self.tipID[0]][1] < self.lmlist[self.tipID[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for tid in range(1, 5):
            if self.lmlist[self.tipID[tid]][2] < self.lmlist[self.tipID[tid] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers



def videocapture():
    cap=cv.VideoCapture(0)
    current_time=0
    post_time=0
    detector=detect_hand()
    while True:
        ret,frame=cap.read()
        frame=cv.flip(frame,1)
        frame1=detector.show_hand(frame)
        lm_list=detector.getposition(frame)
        if len(lm_list)!=0:
            print(lm_list[4])
        current_time=time.time()
        fps=1/(current_time-post_time)
        post_time = current_time
        if fps>40:
            cv.putText(frame1,str(int(fps)),(10,40),cv.FONT_ITALIC,1,(0,255,0),2)
        else:
            cv.putText(frame1, str(int(fps)), (10, 40), cv.FONT_ITALIC, 1, (0, 0, 255), 2)
        cv.imshow("hand_detection",frame1)
        if cv.waitKey(1)==ord('q'):
            break
if __name__=="__main__":
    videocapture()
