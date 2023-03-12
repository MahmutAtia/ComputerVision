import cv2
import time
from HandTracker.handTracker import HandDetector
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
camw = 1000
dist = 0





def main():
    cap = cv2.VideoCapture(0)
    cap.set(4,camh)
    cap.set(3,camw)
    detector = HandDetector(det_c=0.7,trac_c=0.7)
    cTime = 0
    pTime = 0
    volumeMode = False
    while True:
        suc, img = cap.read()
        img = detector.find_hands(img ,draw=False)
        cv2.flip(img,1)
        li = detector.find_postion(img,draw=False)
        #################################
        ###########wrining percenage#####

        dist=17

        #cv2.putText(img, f"{int(vol_percent)}%", (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        ########### drawing rectangle ######
        cv2.rectangle(img,(10,80),(30,350),(255,255,0),3)


        ########### drawing percentage ######
        vol_level = volume.GetMasterVolumeLevel()
        vol_level_percent = np.interp(vol_level,[minRange,maxRange],[0,100])
        cv2.putText(img, f"Volume:{int(vol_level_percent)}%", (10, 450), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)



        if li:
            x1, y1 = li[8][1], li[8][2]
            x2, y2 = (li[4][1], li[4][2])


            #####################################
            ########### trun on or off ############

            x3,y3 = li[8][1],li[8][2]
            x4,y4 = (li[12][1], li[12][2])
            dist2 = math.hypot((x4 - x3), (y4 - y3))
            if dist2<40:
                volumeMode = True

            elif dist2>40:
                volumeMode = False
            print(volumeMode)
            print(dist2)
            #############################################
            dist = math.hypot((x2-x1),(y2-y1))

            center = ((x2+x1)//2),((y2+y1)//2)

            cv2.circle(img, center, 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1,y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img,(x1,y1) ,(x2,y2), (0,255,255),3)
########################## changeVolumeMode #########################
            if volumeMode:
                if dist < 17:
                    cv2.circle(img, center, 15, (0, 0, 255), cv2.FILLED)
                elif dist > 170:
                    cv2.circle(img, center, 15, (255, 0, 0), cv2.FILLED)

                vol= np.interp(dist,[17,170],[minRange,maxRange])
                volume.SetMasterVolumeLevel(vol, None)
            ############# changing percent ##############
            vol_percent = np.interp(dist, [17, 170], [0, 100])
            cv2.putText(img, f"{int(vol_percent)}%", (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            ############# changing rectangle ##############
            y = np.interp(dist, [17, 170], [346, 84])
            cv2.rectangle(img,  (26, 346),(14, int(y)), (255, 0, 255), cv2.FILLED)




        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)

        cv2.waitKey(1)







if __name__ == '__main__':
    main()