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
        csv = pd.read_csv('colorsT10.csv', names=index, header=None,encoding='latin-1')
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
    other=0
    prev_area=0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = 2000
        areaMax = 20000
        if (area > areaMin and area < areaMax and area > prev_area):
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #time.sleep(0.1)
            if len(approx)<4 or len(approx)>5:
                break

            print(len(approx))
            x , y , w, h = cv2.boundingRect(approx)
            result = detect_color(x+10,y+10,x+w-20,y+h-20)
            if(result == 0):
                red_count +=1
            elif(result == 1):
                blue_count +=1
            else:
                other +=1

        prev_area = cv2.contourArea(cnt)
    print(red_count," ",blue_count,"  ",other,"  final output   ")
    if(red_count > 3):
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
    if(blue_count > 3):
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
    else:
        print("No ph paper.....")
        #speak no change
        prev_result_mode2 = "nill"
    





def detect_color(s1,s2,e1,e2):

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

    print(red,"   ",blue,"    ",white,"     ",ph,"    ",count," step output ")


    if(red > blue and red > 10):
        print("Red detected")
        return 0
    elif(blue > red and blue> 10 ):
        print("Blue detected")
        return 1
    else:   
        print("..*******************....")
        return 2




def func_mode2():
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = 40
    threshold2 = 10
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    getContours(imgDil,imgContour)

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

    mixer.music.load('ColorFiles(en)/' + new +'.mp3')
    mixer.music.play()
    #print(GPIO.input(btn_pin))
    time.sleep(0.5)



while True:
    success, img = cap.read()
    time.sleep(0.1)
    imgContour = img.copy()
    if (GPIO.input(btn_pin) == False):
        time.sleep(0.01)
        if (GPIO.input(btn_pin) == False):
            time.sleep(0.3)
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
    img = cv2.flip(img,1)
    
    cv2.imshow('CAMERA',img)

        
cap.release()

cv2.destroyAllWindows()

