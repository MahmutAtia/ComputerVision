import cv2
from handTracker import HandDetector


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
        print(dist_517)







    cv2.imshow("Game",img)
    cv2.waitKey(1)


