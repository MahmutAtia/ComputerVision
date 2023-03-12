import pickle
import time
import cv2
from handTracker import HandDetector


## capture video
cap = cv2.VideoCapture(0)

## reading hands points
w,h = 189, 253
with open("fingerCount.pkl","rb") as file:
    fingerCountList = pickle.load(file)

## create image list
fingers = []
fingersImg = cv2.imread("countimg.jpg")
for x,y in fingerCountList:
    fingers.append(fingersImg[y:y+h,x:x+w,:])

## Hand module
detector = HandDetector(0.75,0.75,2)



pTime = time.time()
while True:
    suc,img = cap.read()

    ## fliping the image
    img = cv2.flip(img,1)

    ## find hands
    img = detector.find_hands(img,True)

    ## find hand postions
    lmlist = detector.find_postion(img,draw=False)
    fingerTipList = []
    if lmlist:

        ##hands type
        handTypeList = detector.find_hand_type()
        #thumb
        opened = True
        if handTypeList[0] == "Left":
            opened = False



        if lmlist[4][1] < lmlist[4-1][1]:
            fingerTipList.append(opened)
        elif lmlist[4][1] > lmlist[4 - 2][1]:
            fingerTipList.append(not opened)


        # 4 fingers
        for tip in [8,12,16,20]:

            if lmlist[tip][2] < lmlist[tip-2][2]:
                fingerTipList.append(True)
            elif lmlist[tip][2] > lmlist[tip - 2][2]:
                fingerTipList.append(False)

        ## check fingers list
        number = fingerTipList.count(True)
        print(number)
        img[0:h,0:w,:] = fingers[number]


    ## show frames per second
    cTime = time.time()
    fps =int(1 / (cTime - pTime))
    pTime = cTime
    cv2.putText(img,f"FPS:{fps}",(500,100),cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)



    cv2.imshow("Image",img)
    k = cv2.waitKey(1)
    if k =="27":
        cv2.destroyAllWindows()