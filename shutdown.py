# File Copyright (c)2024 Max Wiencek

from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import digitalio
import board
import time
import socket
from subprocess import call
spi = board.SPI()
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
BAUDRATE = 24000000

def shutdown():
	my_hostname = socket.gethostname()
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

	# Draw big box = frame
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, width, height), fill=(0, 140, 153))
	disp.image(image)
	# Draw small box = background for text
	draw.rectangle(
		(border, border, width - border - 1, height - border - 1), fill=(255, 255, 255)
	)
	# text settings
	font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
	text = my_hostname+" ready"
	left, top, right, bottom = font.getbbox(text)
	text_width = right - left
	text_height = bottom - top
	y = top
	draw.text((50, 40), my_hostname, font=font, fill=(0, 140, 153))
	draw.text((60, 90), "data sent", font=font, fill=(0, 140, 153))
#	draw.text(
#		(width // 2 - text_width // 2, height // 2 - text_height // 2),
#		text,
#		font=font,
#		fill=(0, 140, 153),
#	)
	disp.image(image)
	time.sleep(4)

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
	time.sleep(5)

	# shutdown
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
	disp.image(image)
	image = Image.open("/home/walkbox/Reader/graph/bye.jpg")
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
	time.sleep(4)
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
	disp.image(image)
	time.sleep(2)
	backlight.value = False
	call("sudo nohup shutdown -h now", shell=True)
shutdown()
