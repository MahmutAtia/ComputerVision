import cv2
from handTracker import HandDetector
import math

class rect:
    def __init__(self, posCenter, size = (200,200)):
        self.posCenter = posCenter
        self.size = size
    def update(self, cursor):
        cx,cy = cursor[1],cursor[2]
        self.posCenter = cx,cy



def main():
    cap = cv2.VideoCapture(0)
    cap.set(4,1200)
    cap.set(3,1600)
    detector = HandDetector()
    color = (255,255,0)
    rectList =[]
    for i in range(5):
         rec = rect(((i+1) *150,150))
         rectList.append(rec)
    while True:
        suc , img = cap.read()
        img = cv2.flip(img,1)
        img = detector.find_hands(img,draw=True)
        lmList = detector.find_postion(img)

        if lmList:
            cursor = lmList[8]
            ########## two fingers ##########
            x3, y3 = lmList[8][1], lmList[8][2]
            x4, y4 = (lmList[12][1], lmList[12][2])
            dist2 = math.hypot((x4 - x3), (y4 - y3))
            if dist2 < 45:
                for rec in rectList:
                    cx, cy,= rec.posCenter
                    w, h = rec.size
                    if cx+w//2> cursor[1] > cx-w//2 and cy+h//2>cursor[2]>cy-h//2:
                        rec.update(cursor)
                        color = (0,255,0)

                    else:
                        color = (255, 0, 255)



        for rec in rectList:
            print(rec.posCenter)
            cx,cy = rec.posCenter
            w,h = rec.size
            cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), color, cv2.FILLED,)





        cv2.imshow("Virtual Drag Drop",img)
        cv2.waitKey(10)








if __name__ == "__main__":
    main()