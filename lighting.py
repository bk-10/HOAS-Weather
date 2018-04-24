import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

while(True):
    if(GPIO.input(4)!=0):
        GPIO.output(17,True)
    else:
        GPIO.output(17,False)

    if(GPIO.input(22)==0):
        print("System Down")
        break
