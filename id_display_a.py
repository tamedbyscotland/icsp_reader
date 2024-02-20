# File Copyright (c)2024 Max Wiencek

from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import digitalio
import board
import time
import os
import RPi.GPIO as GPIO

spi = board.SPI()
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
BAUDRATE = 24000000

def admin_id():
	backlight = digitalio.DigitalInOut(board.D23)
	backlight.switch_to_output()
	backlight.value = True
	disp = st7789.ST7789(spi, rotation=270, width=170, height=320, x_offset=35, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)
	border = 25
	fontsize = 40
	if disp.rotation % 180 == 90:
		height = disp.width
		width = disp.height
	else:
		width = disp.width
		height = disp.height

	image = Image.new("RGB", (width, height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, width, height), fill=(0, 140, 153))
	disp.image(image)
	draw.rectangle(
		(border, border, width - border - 1, height - border - 1), fill=(0, 0, 0)
	)
	font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
	from reader import item_val_adm
	text = item_val_adm
	left, top, right, bottom = font.getbbox(text)
	text_width = right - left
	text_height = bottom - top
	draw.text(
		(width // 2 - text_width // 2, height // 2 - text_height // 2),
		text,
		font=font,
		fill=(0, 140, 153),
	)
	disp.image(image)
	time.sleep(2)


	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, width, height), fill=(0, 140, 153))
	disp.image(image)
	draw.rectangle(
		(border, border, width - border - 1, height - border - 1), fill=(0, 0, 0)
	)
	font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
	text = "Hi Admin!"
	left, top, right, bottom = font.getbbox(text)
	text_width = right - left
	text_height = bottom - top
	draw.text(
		(width // 2 - text_width // 2, height // 2 - text_height // 2),
		text,
		font=font,
		fill=(0, 140, 153),
	)
	disp.image(image)
#	from id_sound_a import sound_admin
	time.sleep(2)
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
	p.stop()   
	# Logo
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
	disp.image(image)
	image = Image.open("/home/walkbox/Reader/graph/at2.png")
	image_ratio = image.width / image.height
	screen_ratio = width / height
	if screen_ratio < image_ratio:
		scaled_width = image.width * height // image.height
		scaled_height = height
	else:
		scaled_width = width
		scaled_height = image.height * width // image.width
	image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
	x = scaled_width // 2 - width // 2
	y = scaled_height // 2 - height // 2
	image = image.crop((x, y, x + width, y + height))
	disp.image(image)
	time.sleep(2)
	backlight.value = False
	time.sleep(2)
	from send_db import send_db_now
	return f"{send_db_now()}"
#admin_id()
#GPIO.cleanup()
