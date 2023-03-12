import cv2
from HandTracker.handTracker import HandDetector
import numpy as np
import random
import time
## Video
cap = cv2.VideoCapture(0)

## Hand Detector
detector = HandDetector(det_c=0.75, trac_c=0.75, hands=1)

## seting window width and height
cap.set(4,1200)
cap.set(3,1600)


## fitting polynomial to get CMs
x = [214,114,95,86,70,62,56,51,47]
y = [20,36,45.5,53.5,60,67,73.5,81.5,90]
p = np.poly1d(np.polyfit(x,y,deg=2))

## class for the aim
class Aim:
    def __init__(self, center , z):
        self.center = center
        self.z = z
        self.color_1 =(255,255,255)
        self.color_2 = (0,255,0)
        self.counter = 0
        self.score = 0
    def put_new_aim(self):

            x = random.randint(300,900)
            y = random.randint(100, 700)
            self.center=(x,y)
            z = random.randint(16,65)
            self.z= z
            self.counter=0

    def change_color(self):
        self.color_2 = (0,0,255)


    def orginal_color(self):
        self.color_2 = (0,255,0)

    def add_to_counter(self):
        self.counter+=1



## create an Aim
aim = Aim((500,500), 30)

## second and total
total = 10
start_time = time.time()

## Window loop
while True:
    ## read and flip image
    suc ,img = cap.read()
    img = cv2.flip(img,1)
    if total > time.time() - start_time:
        print(start_time)
        ## detect hands in the image
        img = detector.find_hands(img)

        ## find the positions of the hands
        lmList = detector.find_postion(img,draw = False)

        ############### Game Logic ###################
        ## Aims
        cv2.circle(img, aim.center,10, aim.color_1, 10)
        cv2.circle(img, aim.center, 20, aim.color_2, 10)
        cv2.circle(img, aim.center, 25, aim.color_1, 10)
        cv2.circle(img, aim.center, 30, aim.color_2, 10)

        ## Score text
        cv2.putText(img,f"Score:{aim.score}", (100,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,255),2)

        ## Time text




        cv2.putText(img, f"Time:{int(total-(time.time()-start_time))}", (1000, 100), cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,255) , 2)




        ## find the distnce between two points on  the palm if hand is detected
        if lmList:
            dist_517 = detector.find_dist(5,17)


            ## draw rectangle arround the hand
            x1,y1= lmList[4][1]+3 , min([lmList[i][2] + 3 for i in [4,8,12,16,20]])
            x2,y2 = lmList[20][1]+ 3,lmList[0][2]+ 3
            w,h =  x2-x1 , y2-y1
            cv2.rectangle(img,(x1,y1),(x1+w,y1+h),(0,255,0),3)

            ## put CM as text
            orgn = lmList[12][1],lmList[12][2]
            cms = int(p(dist_517))
            cv2.putText(img,(str(cms)+ "cm"),orgn,cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),5)

            ## On touch change color of aim
            if cms+10 >= aim.z >= cms-10 and x1+w >= aim.center[0] >= x1 and y1+h >= aim.center[1] >= y1:
                aim.counter =+1

            else:
                aim.orginal_color()

            ## game logic
            if aim.counter:
                aim.change_color()
                aim.counter +=1
                if aim.counter ==3:
                    aim.put_new_aim()

                    ## Score
                    aim.score +=1
    else:
        cv2.putText(img, f"Game Over", (300, 500), cv2.FONT_HERSHEY_SIMPLEX, 4,
                    (255, 0, 255), 5)
        cv2.putText(img, f"Score {aim.score}", (300, 600), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (255, 0, 255), 5)
        cv2.putText(img, f"Press R to reset", (300, 700), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (255, 0, 255), 5)

    cv2.imshow("Game",img)
    k= cv2.waitKey(1)
    if k==27:
        cv2.destroyAllWindows()
    if k ==ord("r"):
        start_time = time.time()
        aim.score = 0

