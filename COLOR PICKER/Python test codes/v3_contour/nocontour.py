import cv2
import numpy as np
import pandas as pd
import time
import RPi.GPIO as GPIO
from pygame import mixer


btn_pin = 15
mode = 1 # 1 for color and 0 for ph
st_time = -1
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
prev_result = "nill"
count = 0


GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn_pin, GPIO.IN)
mixer.init()

def getColorName(R,G,B):
    index=["color_name","R","G","B"]
    csv = pd.read_csv('colorsV4.csv', names=index, header=None,encoding='latin-1')
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

def func_mode2():

    hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

     # Red color
    low_red = np.array([0, 60, 105])
    high_red = np.array([13, 255, 205])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    #red = cv2.bitwise_and(img, img, mask=red_mask)
    Red = cv2.countNonZero(red_mask)

    # Blue color
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    #blue = cv2.bitwise_and(img, img, mask=blue_mask)
    Blue = cv2.countNonZero(blue_mask)

    # Green color
    low_green = np.array([16, 40, 86])
    high_green = np.array([35, 180, 205])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    #green = cv2.bitwise_and(img, img, mask=green_mask)
    Ph = cv2.countNonZero(green_mask)

    print(Red,"   ",Blue,"    ",Ph,"    "," step output ")
    if(Red > Blue and Red > 50):
        print("red")
        mixer.music.load('ColorFiles(hi)/' + "RED" +'.mp3')
        mixer.music.play()
        time.sleep(0.5)
    elif(Blue > Red and Blue> 50 ):
        print("blue")
        mixer.music.load('ColorFiles(hi)/' + "BLUE" +'.mp3')
        mixer.music.play()
        time.sleep(0.5)
    elif(Ph > 50 ):
        print("ph paper")
        mixer.music.load('ColorFiles(hi)/' + "ph paper detected" +'.mp3')
        mixer.music.play()
        time.sleep(1)
    else:   
        print("..*******************")
        mixer.music.load('ColorFiles(hi)/' + "no ph paper detected" +'.mp3')
        mixer.music.play()
        time.sleep(1)
    #cv2.rectangle(img, (60,50), (580,430), (0,255,0), 3)


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
    print(new)
    mixer.music.load('ColorFiles(hi)/' + new +'.mp3')
    mixer.music.play()
    time.sleep(0.5)


while True:
    success, img = cap.read()
    time.sleep(0.1)
    if (GPIO.input(btn_pin) == False):
        time.sleep(0.01)
        if (GPIO.input(btn_pin) == False):
            time.sleep(0.2)
            if (GPIO.input(btn_pin) == True):
                count+=1
                if(st_time==-1):
                    st_time = time.time()

    if(st_time!=-1):
        if(time.time()-st_time>1 and time.time()-st_time<1.5):
            print(count)
            if(count==1):
                print(mode)
                if(mode):
                    func_mode1()
                else:
                    func_mode2()

            else:
                mixer.music.load('ColorFiles(hi)/' + "mode changed" +'.mp3')
                mixer.music.play()
                time.sleep(0.5)
                mode = not mode
                if(mode):
                    print("changed mode 1")

                    mixer.music.load('ColorFiles(hi)/' + "color detection mode" +'.mp3')
                    mixer.music.play()
                    time.sleep(0.8)
                    #sound
                else:
                    print("changed mode 2")
                    mixer.music.load('ColorFiles(hi)/' + "ph paper color detection mode" +'.mp3')
                    mixer.music.play()
                    time.sleep(1)
                    #sound

            count=0
            st_time=-1;

        if(time.time()-st_time>1.5):
            count=0
            st_time=-1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

    img = cv2.flip(img,1)
    
    cv2.imshow('CAMERA',img)
        
cap.release()

cv2.destroyAllWindows()

