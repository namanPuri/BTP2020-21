#! /usr/bin/python

import os
import sys
import vlc

class tts():
	def __init__(self,lang):
		self.lang=lang
		return
	def speak(self,string):
		filename = "lang/"+self.lang+"/"+string+".mp3"
		print filename
		os.system("cvlc "+filename)
A = tts("en")
A.speak("1.0")
