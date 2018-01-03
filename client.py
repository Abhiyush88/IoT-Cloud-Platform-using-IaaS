import RPi.GPIO as GPIO
import time
import os, json
import uuid

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)

def light():
    command = "off"
    print command
    if command == "on":
        GPIO.output(17, True)
    elif command == "off":
        GPIO.output(17, False)

light()
