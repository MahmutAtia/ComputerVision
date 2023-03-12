import time
import cv2
import mediapipe as mp
import math


class HandDetector():
    def __init__(self,det_c=0.5, trac_c=0.5, hands=1):

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=True,
                      max_num_hands=hands,
                      min_detection_confidence=det_c,
                      min_tracking_confidence=trac_c)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_postion(self, img ,handsNum = 0, draw=True):
        lmlist = []
        h,w,c = img.shape
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handsNum]
            for id, handLms in enumerate(myhand.landmark):

                cx,cy = int(handLms.x*w),int(handLms.y*h)
                lmlist.append((id,cx,cy))
                if draw:
                    cv2.circle(img, (cx,cy),15,(255,0,255),cv2.FILLED)
                self.lmlist=lmlist
            return self.lmlist
    def find_dist(self, index_1,index_2):
        x1, y1 = self.lmlist[index_1][1], self.lmlist[index_1][2]
        x2, y2 = self.lmlist[index_2][1], self.lmlist[index_2][2]
        dist = math.hypot((x2 - x1), (y2 - y1))
       # dist2 = math.sqrt((x2 - x1)**2+(y2 - y1)**2)
        return dist


    def find_hand_type(self):
        hands_type = []
        for hand in self.results.multi_handedness:
            hands_type.append(hand.classification[0].label)
        return hands_type
    def get_one_hand_fingers_tips(self):
        fingerTipList = []
        ##hands type
        handTypeList = self.find_hand_type()
        # thumb
        opened = True
        if handTypeList[0] == "Left":
            opened = False

        if self.lmlist[4][1] < self.lmlist[4 - 1][1]:
            fingerTipList.append(opened)
        elif self.lmlist[4][1] > self.lmlist[4 - 2][1]:
            fingerTipList.append(not opened)

        # 4 fingers
        for tip in [8, 12, 16, 20]:

            if self.lmlist[tip][2] < self.lmlist[tip - 2][2]:
                fingerTipList.append(True)
            elif self.lmlist[tip][2] > self.lmlist[tip - 2][2]:
                fingerTipList.append(False)
        return fingerTipList








