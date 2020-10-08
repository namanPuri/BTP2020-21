import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.output(5,False)
GPIO.output(6,False)
GPIO.output(13,False)
GPIO.output(19,False)
GPIO.output(26,False)
GPIO.output(17,False)
GPIO.output(22,False)
GPIO.output(27,False)

# List of pins to be turned on for all numbers 
# 0 - 17,5,6,13,19,27
# 1 - 17,5
# 2 - 27,17,26,13,6
# 3 - 27,17,26,5,6
# 4 - 19,17,26,5
# 5 - 27,19,26,5,6
# 6 - 27,19,26,13,6,5
# 7 - 27,17,5
# 8 - 26,17,5,6,13,19,26
# 9 - 26,27,19,17,5,6
# Dot - 22

# Display 0
GPIO.output(19,True)
GPIO.output(27,True)
GPIO.output(17,True)
GPIO.output(13,True)
GPIO.output(6,True)
GPIO.output(5,True)
GPIO.output(26,False)
sleep(1)

# Display 1
GPIO.output(17,True)
GPIO.output(5,True)
GPIO.output(27,False)
GPIO.output(19,False)
GPIO.output(26,False)
GPIO.output(6,False)
GPIO.output(13,False)
sleep(1)

# Display 2
GPIO.output(26,True)
GPIO.output(27,True)
GPIO.output(17,True)
GPIO.output(13,True)
GPIO.output(6,True)
GPIO.output(19,False)
GPIO.output(5,False)
sleep(1)

# Display 3
GPIO.output(26,True)
GPIO.output(27,True)
GPIO.output(17,True)
GPIO.output(5,True)
GPIO.output(6,True)
GPIO.output(13,False)
GPIO.output(19,False)
sleep(1)

# Display 4
GPIO.output(19,True)
GPIO.output(26,True)
GPIO.output(17,True)
GPIO.output(5,True)
GPIO.output(6,False)
GPIO.output(13,False)
GPIO.output(27,False)
sleep(1)

# Display 5
GPIO.output(19,True)
GPIO.output(27,True)
GPIO.output(26,True)
GPIO.output(5,True)
GPIO.output(6,True)
GPIO.output(17,False)
GPIO.output(13,False)
sleep(1)

# Display 6
GPIO.output(19,True)
GPIO.output(27,True)
GPIO.output(26,True)
GPIO.output(13,True)
GPIO.output(6,True)
GPIO.output(5,True)
GPIO.output(17,False)
sleep(1)

# Display 7
GPIO.output(27,True)
GPIO.output(17,True)
GPIO.output(5,True)
GPIO.output(26,False)
GPIO.output(19,False)
GPIO.output(6,False)
GPIO.output(13,False)
sleep(1)

# Display 8
GPIO.output(19,True)
GPIO.output(27,True)
GPIO.output(17,True)
GPIO.output(13,True)
GPIO.output(26,True)
GPIO.output(5,True)
GPIO.output(6,True)
sleep(1)

# Display 9
GPIO.output(19,True)
GPIO.output(27,True)
GPIO.output(17,True)
GPIO.output(5,True)
GPIO.output(26,True)
GPIO.output(6,True)
GPIO.output(13,False)
sleep(1)

GPIO.cleanup()
