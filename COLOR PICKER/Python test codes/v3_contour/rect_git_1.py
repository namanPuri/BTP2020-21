import cv2
import time
import numpy as np
import pandas as pd 






"""
prev = new = ''
cap = cv2.VideoCapture(0)

def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

while True:
    index=["color_name","hex","R","G","B"]
    csv = pd.read_csv('colorsV3.csv', names=index, header=None,encoding='latin-1')
    ret, frame = cap.read()

    cv2.rectangle(frame, (309,229), (329,249), (0,255,0), 1)       #pixel range = x ==> 0-639 and y == 0 - 479
    roi = frame[230:249, 310:329]
    avg1 = np.average(roi, axis=0)
    avg2 = np.average(avg1, axis=0)
    avg2_int = avg2.astype(int)
    avg2_int = avg2_int[::-1]           #reversed for rgb 
   # avg2_int_tup = tuple(avg2_int)
    r = avg2_int[0]
    g = avg2_int[1]
    b = avg2_int[2]

    print(r," ",g," ",b )
    time.sleep(1)
    '''new = getColorName(r,g,b)

    if (new != prev):
        print(new)    
        prev = new
    frame = cv2.flip(frame,1)
    
    cv2.imshow('CAMERA',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    '''

cap.release()

cv2.destroyAllWindows()

"""

index=["color_name","R","G","B"]
csv = pd.read_csv('colorsT2.csv', names=index, header=None,encoding='latin-1')
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname


def detect_color(s1,s2,e1,e2):
    #print((e1-s1)*(e2-s2))
    red = 0
    blue = 0
    white = 0
    ph = 0
    count = 0
    for x in range( s1, e1-1,10) :
        for y in range( s2 , e2-1,10) :
            count+=1
            if frameHeight <= x+10 or frameWidth <= y+10:
                break 
            roi = img[x:x+10, y:y+10]

            avg1 = np.average(roi, axis=0)
            avg2 = np.average(avg1, axis=0)
            avg2_int = avg2.astype(int)
            avg2_int = avg2_int[::-1]           #reversed for rgb 
           # avg2_int_tup = tuple(avg2_int)
            r = avg2_int[0]
            g = avg2_int[1]
            b = avg2_int[2]
           
            new = getColorName(r,g,b)
            if(new =='Red'): 
                red +=1
            elif(new== 'Blue'):
                blue +=1
            elif(new == 'Ph'):
                ph +=1
            else:
                white +=1

    print(red,"   ",blue,"    ",white,"     ",ph,"    ",count)


    if(red > blue and red > 10):
        print("Red detected")
    elif(blue > red and blue> 10 ):
        print("Blue detected")
    elif(ph>30):
        print("Ph paper only")
    else:   
        print("no ph paper detected")




frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",15,255,empty)
cv2.createTrackbar("Threshold2","Parameters",10,255,empty)
cv2.createTrackbar("Area","Parameters",1000,30000,empty)


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            #time.sleep(0.1)

            if len(approx)<4 or len(approx)>6:
                break

            print(len(approx))
    

            x , y , w, h = cv2.boundingRect(approx)
            detect_color(x,y,x+w,y+h)
            x=x+10
            y=y+10
            w=w-20
            h=h-20

            cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)

            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)

            #time.sleep(0.2)

            

while True:
    success, img = cap.read()
    time.sleep(0.1)
    imgContour = img.copy()
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    getContours(imgDil,imgContour)
    imgStack = stackImages(0.8,([img,imgCanny],
                                [imgDil,imgContour]))
    cv2.imshow("Result", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break