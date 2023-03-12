import cv2
from HandTracker.handTracker import HandDetector
import numpy as np

##################################
x = [214,114,95,86,70,62,56,51,47]
y = [20,36,45.5,53.5,60,67,73.5,81.5,90]
#create polynomial relationship
p = np.poly1d(np.polyfit(x,y,deg=2))
#plt.plot(x,y)
#plt.show()
###################################

cap = cv2.VideoCapture(0)
detector = HandDetector(det_c=0.75, trac_c=0.75, hands=1)


while True:
    suc ,img = cap.read()
    img = cv2.flip(img,1)
    img = detector.find_hands(img)
    ########### find positins list  ################
    lmList = detector.find_postion(img,draw = False)
    ########### find distnce in palm  ################
    if lmList:

        dist_517 = detector.find_dist(5,17)
        orgn = lmList[12][1],lmList[12][2]
        cv2.putText(img,str(int(p(dist_517)))+ "cm",orgn,cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),5)







    cv2.imshow("Game",img)
    k= cv2.waitKey(1)
    if k==27:
        cv2.destroyAllWindows()


