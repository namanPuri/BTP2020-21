#!/usr/bin/python

from gtts import gTTS

tts = gTTS(text='1.0 degrees celsius', lang='fr')
tts.save('hello.mp3') 
