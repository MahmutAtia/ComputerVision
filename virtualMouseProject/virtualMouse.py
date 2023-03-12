import time
import cv2
from HandTracker.handTracker import HandDetector
import pyautogui
import numpy as np


## capture video
url = "http://192.168.1.101:8080/video"
cap = cv2.VideoCapture(0)

## get screen size
screenW , screenH = pyautogui.size()





## Hand module
detector = HandDetector(0.75,0.75,1)

## mouse modes
moveMode = False
clickMode = False

## Window props
pTime = time.time()
capW =600
capH =500
moveFrame=100
plocX = 0
plocY = 0
smoothing = 2

## Ranges
moveRangeX = np.array([moveFrame,capW-moveFrame])
moveRangeY = np.array([moveFrame,capH-moveFrame])
screenRangeX = np.array([0,screenW])
screenRangeY = np.array([0,screenH])
pyautogui.FAILSAFE = False




while True:
    suc,img = cap.read()

    ## fliping the image
    img = cv2.flip(img,1)

    ## create an area for moving mouse
    cv2.rectangle(img,(moveFrame,moveFrame),(capW-moveFrame,capH-moveFrame),(255,0,255), 3)

    ## find hands
    img = detector.find_hands(img,True)

    ## find hand postions
    lmlist = detector.find_postion(img,draw=False)

    ## if hands detected
    if lmlist:
        fingers = detector.get_one_hand_fingers_tips()
        print(fingers)

        #detect if finger up
        if fingers[1] and not fingers[2]:

            #draw a circle as pointer
            cv2.circle(img,(lmlist[8][1],lmlist[8][2]),5,(255,0,255),5,cv2.FILLED )

            ## moving the mouse
            mouseX = np.interp(lmlist[8][1], moveRangeX, screenRangeX)
            mouseY = np.interp(lmlist[8][2], moveRangeY, screenRangeY)

            ## to control the movement we will update current values ans previos values
            clocX = plocX + ((mouseX - plocX) / smoothing)
            clocY = plocY + ((mouseY - plocY) / smoothing)

            pyautogui.moveTo(clocX, clocY)
            plocX,plocY =clocX,clocY

        elif fingers[1] and [2]:
            ## find the distance
            dist = detector.find_dist(8,12)



            ## click logic
            color = (0, 0, 255)
            if dist < 35:
                color= (0,255,0)
                pyautogui.click()
            else:
                color = (0, 0, 255)

            ##drawline and center
            x1, x2, y1, y2 = lmlist[8][1], lmlist[12][1], lmlist[8][2], lmlist[12][2]
            center = ((x2 + x1) // 2), ((y2 + y1) // 2)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 4)
            cv2.circle(img, center, 10, color, cv2.FILLED )














## show frames per second
    cTime = time.time()
    fps =int(1 / (cTime - pTime))
    pTime = cTime
    cv2.putText(img,f"FPS:{fps}",(500,100),cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)



    cv2.imshow("Image",img)
    k = cv2.waitKey(1)
    if k =="27":
        cv2.destroyAllWindows()