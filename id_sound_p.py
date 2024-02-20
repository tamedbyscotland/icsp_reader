import time
import RPi.GPIO as GPIO
import os

def sound_pupil():
	soundpin = 13
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(soundpin, GPIO.OUT)
	p = GPIO.PWM(soundpin,50)
	p.start(60)             # start the PWM on 70 percent duty cycle  
	for x in range(900, 1600):
		p.ChangeFrequency(x)  # change the frequency to x Hz (
		time.sleep(0.0003)
	for x in range(1200, 2000):
		p.ChangeFrequency(x)  # change the frequency to x Hz (
		time.sleep(0.0003)
	p.stop()                # stop the PWM output  
sound_pupil()
