import time
import RPi.GPIO as GPIO
import os

def sound_admin():
	soundpin = 13
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(soundpin, GPIO.OUT)
	p = GPIO.PWM(soundpin,50)
	p.start(60)             # start the PWM on 70 percent duty cycle  
	for x in range(600, 800):
		p.ChangeFrequency(x)  # change the frequency to x Hz (
		time.sleep(0.002)
	for x in range(600, 800):
		p.ChangeFrequency(x)  # change the frequency to x Hz (
		time.sleep(0.002)
	p.stop()                # stop the PWM output  
sound_admin()
