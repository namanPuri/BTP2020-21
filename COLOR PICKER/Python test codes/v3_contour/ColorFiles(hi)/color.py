import os
from gtts import gTTS



arr=[
"RED",
"YELLOW",
"GREEN",
"ORANGE",
"MAGENTA",
"VIOLET",
"BLUE",
"WHITE",
"GREY",
"no ph paper detected","mode changed","ph paper color detection mode","color detection mode","ph paper detected"]

i=0
language = 'hi'

while(i<len(arr)):
    tts = gTTS(text=arr[i], lang=language, slow=False) 
    name=arr[i] + ".mp3"
    tts.save(name)
    i=i+1
    print("1 more ")
print("over!!")
    
