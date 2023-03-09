import cv2
import time
from handTracker import HandDetector
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume







devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


range = volume.GetVolumeRange()
minRange,maxRange = range[0],range[1]


camh= 1000
camw = 450






def main():
    cap = cv2.VideoCapture(0)
    cap.set(4,camh)
    cap.set(3,camw)
    detector = HandDetector()
    cTime = 0
    pTime = 0
    while True:
        suc, img = cap.read()
        img = detector.find_hands(img ,draw=False)
        li = detector.find_postion(img,draw=False)
        if li:



            #####################################
            ########### drawing Line ############
            x1,y1 = li[8][1],li[8][2]
            x2,y2 = (li[4][1], li[4][2])

            dist = math.hypot((x2-x1),(y2-y1))
            print(dist)
            center = ((x2+x1)//2),((y2+y1)//2)

            cv2.circle(img, center, 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1,y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img,(x1,y1) ,(x2,y2), (0,255,255),3)

            if dist < 17:
                cv2.circle(img, center, 15, (0, 0, 255), cv2.FILLED)
            elif dist > 170:
                cv2.circle(img, center, 15, (255, 0, 0), cv2.FILLED)

            vol= np.interp(dist,[17,170],[minRange,maxRange])
            print(vol)
            volume.SetMasterVolumeLevel(vol, None)
            #cv2.rectangle(img, )




        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)

        cv2.waitKey(1)







if __name__ == '__main__':
    main()