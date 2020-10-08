import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
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
LED_PIN = 18
GPIO.setup(23,GPIO.IN)
GPIO.setup(LED_PIN,GPIO.OUT)
FLAG = 0
def enable_led(should_enable):
	if should_enable:

		GPIO.output(LED_PIN,False)
	else:
		GPIO.output(LED_PIN, True)
def sevseg():
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

while True:
    input_state = GPIO.input(23)
    if input_state:
        FLAG=0
    else:
        FLAG=1
    if FLAG:
        sevseg()
    else:
        enable_led(False)
	sleep(0.5)
	enable_led(True)
	sleep(0.5)
    FLAG=0
GPIO.cleanup()
        
    
