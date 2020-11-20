import os
from gtts import gTTS



arr=["RED",
"YELLOW",
"GREEN",
"ORANGE",
"MAGENTA",
"VIOLET",
"BLUE",
"WHITE",
"GREY",
"PH"
]
i=0
language = 'hi'

while(i<10):
    tts = gTTS(text=arr[i], lang=language, slow=True) 
    name=arr[i] + ".mp3"
    tts.save(name)
    i=i+1
    print("1 more ")
print("over!!")
    
