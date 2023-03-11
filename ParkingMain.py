import cv2
import pickle

import numpy as np

## reading vidio
cap = cv2.VideoCapture("carPark.mp4")

## import car postions
with open("parkinlist.pkl","rb") as file:
    parkingList = pickle.load(file)

## width and height for parking place
w,h = (158-51),(194-147)

## check boxes
def  check_box(imgNEW,p1,img):
        ## is it embty space
        embty = False
        ## corp parking places
        parkPlace = imgNEW[p1[1]:p1[1]+h,p1[0]:p1[0]+w]

        ## count white spots
        nonZero = cv2.countNonZero(parkPlace)

        # put non zero text
        if nonZero < 900:
            color = (0,255,0)
            embty = True
        else :
            color = (0, 0, 255)
        cv2.putText(img,str(nonZero),p1,cv2.FONT_HERSHEY_PLAIN,1,color,2)
        return color, embty
## prepare_image
def prepare_image(img):
    ##gray scale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ## Hist equal or clahe
    # imgHE = cv2.equalizeHist(imgGray)
    ## denoising - normal dist noise
    imgGaus = cv2.GaussianBlur(imgGray,(3,3),1, borderType= cv2.BORDER_CONSTANT)
    ##theshholding
    imgThresh = cv2.adaptiveThreshold(imgGaus,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,25,20)
    ## denoising - salt pepper noise
    imgMedian = cv2.medianBlur(imgThresh,3)
    #opening erotion then dialtion
    kernel = np.ones((3,3),np.uint8)
    #imgOpen = cv2.morphologyEx(imgMedian,cv2.MORPH_OPEN,kernel)
    imgdilate = cv2.dilate(imgMedian,kernel,iterations=1)
    cv2.imshow("denoise",imgdilate)
    return imgMedian



while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    suc ,img = cap.read()

    ## image preparation
    newImage = prepare_image(img)

    # embty spaces
    spaces = 0

    ## drawing boxes
    for p1,_ in parkingList:
        p2 = p1[0]+w,p1[1]+h





        ## check car boxes
        color,embty = check_box(newImage,p1,img)
        if embty:
            spaces+=1

        ## boxes
        img = cv2.rectangle(img, p1, p2, color, 2)

    # writing how many spaces
    cv2.putText(img, f"Total : {len(parkingList)}", (30,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 5)
    cv2.putText(img, f"Embty : {spaces}", (30,60), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 5)

    cv2.imshow("parking",img)

    k = cv2.waitKey(1)
    if k == 27:
        cv2.destroyAllWindows()
