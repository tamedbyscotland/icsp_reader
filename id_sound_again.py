import time
import RPi.GPIO as GPIO
import os

def sound_again():
	soundpin = 13
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(soundpin, GPIO.OUT)
	p = GPIO.PWM(soundpin,50)
	p.start(60)             # start the PWM on 70 percent duty cycle  
	for x in range(100, 300):
		p.ChangeFrequency(x)  # change the frequency to x Hz (
		time.sleep(0.0002)
	for x in range(50, 300):
		p.ChangeFrequency(x)  # change the frequency to x Hz (
		time.sleep(0.0005)
	for x in range(100, 300):
		p.ChangeFrequency(x)  # change the frequency to x Hz (
		time.sleep(0.0007)
	p.stop()                # stop the PWM output  
sound_again()
