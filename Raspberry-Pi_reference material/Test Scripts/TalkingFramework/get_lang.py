#!/usr/bin/python

from gtts import gTTS
import os
import sys

print "Talking Thermometer v1.0"
print "Language File Accumulator"
print "Language selected : "+ sys.argv[1]
count = float(sys.argv[2])
os.system('mkdir ./lang/'+sys.argv[1])
dirpath="./lang/"+sys.argv[1]+"/"
print "Commencing Download from Google TTS..."
while count <= float(sys.argv[3]):
	print "Downloading file for "+ `count`
	tts = gTTS(text=`count`, lang=sys.argv[1])
	filename = `count`+ ".mp3"
	tts.save(dirpath+filename)
	os.system("mpg123 -w "+dirpath+`count`+".wav "+dirpath+`count`+".mp3") 
	os.system("rm "+dirpath+`count`+".mp3")	
	count += 0.5
print "Downloading file for '-' "
tts = gTTS(text="minus", lang=sys.argv[1])
filename = "minus.mp3"
tts.save(dirpath+filename)
os.system("mpg123 -w "+dirpath+"minus.wav "+dirpath+ "minus.mp3")
os.system("rm "+dirpath+"minus.mp3")

print "Downloading file for 'degree celsius' "
tts = gTTS(text="degree celsius", lang=sys.argv[1])
filename = "degree_celsius.mp3"
tts.save(dirpath+filename)
os.system("mpg123 -w "+dirpath+ "degree_celsius.wav "+dirpath+"degree_celsius.mp3")
os.system("rm "+dirpath+"degree_celsius.mp3")


