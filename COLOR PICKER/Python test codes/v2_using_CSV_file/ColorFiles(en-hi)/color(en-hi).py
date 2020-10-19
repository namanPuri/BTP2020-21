import os
from gtts import gTTS
import time



arr=["RED",
"DARK RED",
"CRIMSON",
"INDIAN RED",
"BLOOD RED",
"MAGENTA",
"MAROON",
"VIOLET RED",
"ORANGE RED",
"PALE VIOLET RED",
"PINK",
"LIGHT PINK",
"DEEP PINK",
"LIGHT SALMON",
"TOMATO",
"DARK ORANGE",
"ORANGE",
"YELLOW",
"LIGHT YELLOW",
"LAVENDER",
"VIOLET",
"MEDIUM PURPLE",
"BLUE VIOLET",
"DARK VIOLET",
"DARK MAGENTA",
"PURPLE",
"INDIGO",
"GREEN YELLOW",
"LIME",
"LIME GREEN",
"PALE GREEN",
"LIGHT GREEN",
"SEA GREEN",
"GREEN",
"DARK GREEN",
"YELLOW GREEN",
"DARK CYAN",
"BRIGHT GREEN",
"CYAN",
"LIGHT CYAN",
"LIGHT BLUE",
"SKY BLUE",
"LIGHT SKY BLUE",
"BLUE",
"MEDIUM BLUE",
"DARK BLUE",
"NAVY",
"SANDY BROWN",
"CHOCOLATE",
"BROWN",
"WHITE",
"SNOW WHITE",
"LIGHT GRAY",
"SILVER",
"DARK GRAY",
"GRAY",
"DIM GRAY",
"BLACK",
]
i=0
language = 'en-IN'

while(i<58):
    tts = gTTS(text=arr[i], lang=language, slow=True) 
    name=arr[i] + ".mp3"
    tts.save(name)
    i=i+1
    time.sleep(0.1)
print("over!!")
    
