import cv2
import numpy as np
import pandas as pd
import RPi.GPIO as GPIO
import time
from pygame import mixer

btn_pin = 15
mode = 0 # 1 for color and 2 for ph
st_time = -1
index=["color_name","R","G","B"]
index1=["color_name","hash","R","G","B"]
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
prev_result_mode2 = "nill"
count = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn_pin, GPIO.IN)
mixer.init()

def getColorName(R,G,B):
    if(mode):
        csv = pd.read_csv('colorsV3.csv', names=index1, header=None,encoding='latin-1')
    else:
        csv = pd.read_csv('colorsT2.csv', names=index, header=None,encoding='latin-1')
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname


def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    red_count=0
    blue_count=0
    ph_count=0
    other=0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = 1000
        areaMax = 20000
        if (area > areaMin and area < areaMax):
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #time.sleep(0.1)
            if len(approx)<4 or len(approx)>6:
                break

            print(len(approx))
            x , y , w, h = cv2.boundingRect(approx)
            result = detect_color(x,y,x+w,y+h)
            if(result == 0):
                red_count +=1
            elif(result == 1):
                blue_count +=1
            elif(result == 2):
                ph_count +=1
            else:
                other +=1

    print(red_count," ",blue_count,"  ",other,"  final output   ")
    if(red_count >= blue_count and red_count >=1 ):
        mixer.music.load('ColorFiles(hi)/' + "RED" +'.mp3')
        mixer.music.play()
        time.sleep(0.5)
        if(prev_result_mode2 == "red"):
            print("Red again")
            #speak red again
        else:
            if(prev_result_mode2 != "nill"):
                print("Red")
                #speak red
            else:
                print("Its Red now")
                #speak its red now
        prev_result_mode2 = "red"
    elif(blue_count > red_count and blue_count >=1 ):
        mixer.music.load('ColorFiles(hi)/' + "BLUE" +'.mp3')
        mixer.music.play()
        time.sleep(0.5)
        if(prev_result_mode2 == "blue"):
            print("Blue again")
            #speak blue again
        else:
            if(prev_result_mode2 != "nill"):
                print("Blue")    
                #speak blue
            else:
                print("Its Blue now")
                #speak its blue now
        prev_result_mode2 = "blue"
    elif(ph_count>=1):
        print("no color detected in ph paper")
        prev_result_mode2 = "nill"
    else:
        print("No ph paper detected.....")
        #speak no change
        prev_result_mode2 = "nill"
    

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



def detect_color(s1,s2,e1,e2):

    hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

     # Red color
    low_red = np.array([0, 60, 105])
    high_red = np.array([13, 255, 205])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(img, img, mask=red_mask)

    # Blue color
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(img, img, mask=blue_mask)

    # Green color
    low_green = np.array([16, 40, 86])
    high_green = np.array([35, 180, 205])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(img, img, mask=green_mask)

    Red = 0
    Blue = 0
    Black = 0
    Ph = 0

    for x in range( s1, e1-1,12) :
        for y in range( s2 , e2-1,12) :
            if frameHeight <= x+15 or frameWidth <= y+15:
                break 


            for z in range (0,2):
                if(z==0):
                    roi = red[x:x+10, y:y+10]
                elif(z==1):
                    roi = blue[x:x+10, y:y+10]
                else:
                    roi = green[x:x+10, y:y+10]

                avg1 = np.average(roi, axis=0)
                avg2 = np.average(avg1, axis=0)
                avg2_int = avg2.astype(int)
                avg2_int = avg2_int[::-1]           #reversed for rgb 
               # avg2_int_tup = tuple(avg2_int)
                r = avg2_int[0]
                g = avg2_int[1]
                b = avg2_int[2]
               
                new = getColorName(r,g,b)
                if(new =='RED'): 
                    Red +=1
                elif(new== 'BLUE'):
                    Blue +=1
                elif(new == 'PH'):
                    Ph +=1
                else:
                    Black +=1
                    
                cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)

                cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 255, 0), 2)


    print(Red,"   ",Blue,"    ",Black,"     ",Ph,"    "," step output ")


    if(Red > Blue and Red > 10):
        print("Red detected")
        return 0
    elif(Blue > Red and Blue> 10 ):
        print("Blue detected")
        return 1
    elif(ph_count > 10 ):
        return 2
    else:   
        print("..*******************....")
        return 3




def func_mode2():
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = 20
    threshold2 = 10
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    getContours(imgDil,imgContour)
    imgStack = stackImages(0.8,([img,imgCanny],
                                [imgDil,imgContour]))
    cv2.imshow("Result", imgStack)

def func_mode1():

    cv2.rectangle(img, (309,229), (329,249), (0,255,0), 1)       #pixel range = x ==> 0-639 and y == 0 - 479
    roi = img[230:249, 310:329]
    avg1 = np.average(roi, axis=0)
    avg2 = np.average(avg1, axis=0)
    avg2_int = avg2.astype(int)
    avg2_int = avg2_int[::-1]           #reversed for rgb 
   # avg2_int_tup = tuple(avg2_int)
    r = avg2_int[0]
    g = avg2_int[1]
    b = avg2_int[2]

    new = getColorName(r,g,b)

    mixer.music.load('ColorFiles(hi)/' + new +'.mp3')
    mixer.music.play()
    time.sleep(0.5)

    img = cv2.flip(img,1)
    
    cv2.imshow('CAMERA',img)


while True:
    success, img = cap.read()
    time.sleep(0.1)
    imgContour = img.copy()
    if (GPIO.input(btn_pin) == False):
        time.sleep(0.01)
        if (GPIO.input(btn_pin) == False):
            time.sleep(0.15)
            if (GPIO.input(btn_pin) == True):
                count+=1
                if(st_time==-1):
                    st_time = time.time()

    if(st_time!=-1):
        if(time.time()-st_time>1.2 and time.time()-st_time<1.8):
            print(count)
            if(count==1):
                print(mode)
                if(mode):
                    func_mode1()
                else:
                    func_mode2()

            else:
                mode = not mode
                if(mode):
                    print("changed mode 1")
                    #sound
                else:
                    print("changed mode 2")
                    #sound


            count=0
            st_time=-1;

        if(time.time()-st_time>1.8):
            count=0
            st_time=-1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        
cap.release()

cv2.destroyAllWindows()

