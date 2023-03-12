import cv2
import pickle





#assign w and h
w,h = 182-43 ,298-25
def get_point(e,x,y,flags,prams):
    if e == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
try:
    with open("fingerCount.pkl","rb") as file:
        fingerCount_list = pickle.load(file)

except:
    fingerCount_list = []


## tradtional way
def draw_count_images(e,x,y,flags,prams):
    if e == cv2.EVENT_LBUTTONDOWN:
        fingerCount_list.append((x,y))
    elif e == cv2.EVENT_RBUTTONUP:
        for i, (xi,yi) in enumerate(fingerCount_list):
            if  xi+w >= x >= xi and yi+h >= y >= yi:
                fingerCount_list.pop(i)



## way 2 draw line but rectangle failed
drawing = False
ix = 0
iy = 0
# Adding Function Attached To Mouse Callback
def draw(event,x,y,flags,params):
    global ix,iy,drawing
    # Left Mouse Button Down Pressed
    if(event==1):
        drawing = True
        ix = x
        iy = y
    if(event==0):
        if(drawing==True):
            #For Drawing Line
            #cv2.line(img,pt1=(ix,iy),pt2=(x,y),color=(255,255,255),thickness=3)
            ix = x
            iy = y
            # For Drawing Rectangle
            cv2.rectangle(img,pt1=(ix,iy),pt2=(x,y),color=(255,255,255),thickness=3)
    if(event==4):
        drawing = False


## way 3 faided
xs = 0
ys = 0
drawing = False
points = []

def draw_rectangle_on_pressed(e,x,y,flags,prams):
    global drawing
    global xs,ys

    if e == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points.append(x, y)

    if e == cv2.EVENT_MOUSEMOVE:
        if drawing:

            xs,ys = points[0]
            xe, ye = points[-1]

            cv2.rectangle(img, (xs,ys), (xe,ye), (255, 0, 255), 2)
    if (e == cv2.EVENT_LBUTTONUP):
        drawing = False





while True:
    ## reading the image
    img = cv2.imread("countimg.jpg")

    for x,y in fingerCount_list:
         print(w,h)
         cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)



    cv2.imshow("count",img)
    cv2.setMouseCallback("count", draw_count_images)





    k = cv2.waitKey(1)
    if k == 27:
        cv2.destroyAllWindows()
    if k == ord("w"):
        cv2.imwrite("parking_final.png",img)
        pickle.dump(fingerCount_list,open("fingerCount.pkl","wb"))

    ## add width to the rectangle
    if k == ord("a"):
        w+=10
    if k == ord("s"):
        w-=10
    if k == ord("y"):
        h+=10
    if k == ord("x"):
        h-=10