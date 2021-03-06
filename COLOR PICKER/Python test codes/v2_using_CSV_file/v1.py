# draws sq in the centre of video
import cv2
import numpy as np
import pandas as pd

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
    index=["color","color_name","hex","R","G","B"]
    csv = pd.read_csv('colors.csv', names=index, header=None)
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

    color = getColorName(r,g,b)
    print(color)
    frame = cv2.flip(frame,1)
    
    cv2.imshow('CAMERA',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
