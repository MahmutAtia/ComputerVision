import time
import cv2
import mediapipe as mp


class HandDetector():
    def __init__(self):

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=True,
                      max_num_hands=2,
                      min_detection_confidence=0.3,
                      min_tracking_confidence=0.3)
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

            return lmlist







def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    cTime = 0
    pTime = 0
    while True:
        suc, img = cap.read()
        img = detector.find_hands(img ,draw=False)
        li = detector.find_postion(img)
        if li: print(li[0])




        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)

        cv2.waitKey(1)







if __name__ =="__main__":
    main()