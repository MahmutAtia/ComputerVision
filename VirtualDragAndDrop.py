import cv2
import numpy as np

from HandTracker.handTracker import HandDetector


class rect:
    def __init__(self, posCenter, size = (200,200)):
        self.posCenter = posCenter
        self.size = size
        self.color =  (255, 0, 255)
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
         rec = rect(((150*i)+150,150))
         rectList.append(rec)
    while True:
        suc , img = cap.read()
        img = cv2.flip(img,1)
        img = detector.find_hands(img)
        lmList = detector.find_postion(img,draw=False)
        imgNew = np.zeros_like(img)
        if lmList:
            cursor = lmList[8]
            ########## two fingers ##########
            dist2 = detector.find_dist(8,12)
            print(dist2)
            print(detector.lmList)
            if dist2 < 50:
                for rec in rectList:
                    cx, cy,= rec.posCenter
                    w, h = rec.size
                    if cx+w//2> cursor[1] > cx-w//2 and cy+h//2>cursor[2]>cy-h//2:
                        rec.update(cursor)
                        rec.color = (0,255,0)

                    else:
                        rec.color = (255, 0, 255)


        ######### draw filled rectaangle #############
      #  for rec in rectList:
       #     print(rec.posCenter)
        #    cx,cy = rec.posCenter
         #   w,h = rec.size
          #  cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), color, cv2.FILLED,)

        ######### draw transparent rectaangle #############


        for rec in rectList:

            cx, cy = rec.posCenter
            w, h = rec.size
            cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), rec.color, cv2.FILLED, )
        alpha = 0.4
        mask = imgNew.astype(bool)
        out =img.copy()
        out[mask] = cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]
        cv2.imshow("Virtual Drag Drop",out)
        cv2.waitKey(1)








if __name__ == "__main__":
    main()