import cv2
import pickle


def get_point(e,x,y,flags,prams):
    if e == cv2.EVENT_LBUTTONDOWN:
        print(x,y)

w,h = (158-51),(194-147) #width and height for parking place

rectangle_list = []
def draw_parking_place(e,x,y,flags,prams):
    if e == cv2.EVENT_LBUTTONDOWN:
        p1 = (x,y)
        p2 = (x+w,y+h)
        rectangle_list.append((p1,p2))
    elif e == cv2.EVENT_RBUTTONUP:
        for i, (p1,p2) in enumerate(rectangle_list):
            if  p2[0] >= x >= p1[0] and p2[1] >= y >= p1[1]:
                rectangle_list.pop(i)




while True:

    img = cv2.imread("carParkImg.png")#to rerun the image again inside while loop
    for p1,p2 in rectangle_list:
        cv2.rectangle(img,p1,p2,(255,0,255),2)



    cv2.imshow("parking",img)
    cv2.setMouseCallback("parking", draw_parking_place)

    k = cv2.waitKey(1)
    if k == 27:
        cv2.destroyAllWindows()
    if k == ord("w"):
        cv2.imwrite("parking_final.png",img)
        pickle.dump(rectangle_list,open("parkinlist.pkl","wb"))