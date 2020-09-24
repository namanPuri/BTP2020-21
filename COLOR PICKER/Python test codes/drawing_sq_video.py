# draws sq in the centre of video
import cv2
import numpy as np
import webcolors

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

requested_colour = (119, 172, 152)
actual_name, closest_name = get_colour_name(requested_colour)

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    cv2.rectangle(frame, (309,229), (329,249), (0,255,0), 1)       #pixel range = x ==> 0-639 and y == 0 - 479
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #frame[230:249, 310:329] = [0,0,0]
    #print(roi)
    roi = frame[230:249, 310:329]
    avg1 = np.average(roi, axis=0)
    avg2 = np.average(avg1, axis=0)
    avg2_int = avg2.astype(int)
    avg2_int = avg2_int[::-1]           #reversed for rgb 
    avg2_int_tup = tuple(avg2_int)

    actual_name, closest_name = get_colour_name(avg2_int_tup)
    print(closest_name)
    #frame = cv2.flip(frame,1)
    
    cv2.imshow('CAMERA',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
