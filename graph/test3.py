# SPDX-FileCopyrightText: 2024 MW for Inverclyde Council
# SPDX-License-Identifier: MIT

from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import digitalio
import board

spi = board.SPI()
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
BAUDRATE = 24000000
disp = st7789.ST7789(spi, rotation=270, width=170, height=320, x_offset=35, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)

if disp.rotation % 180 == 90:
    height = disp.width
    width = disp.height
else:
    width = disp.width
    height = disp.height

border = 25
fontsize = 40

image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)
# Draw big box = frame
draw.rectangle((0, 0, width, height), fill=(0, 140, 153))
disp.image(image)
# Draw small box = background for text
draw.rectangle(
    (border, border, width - border - 1, height - border - 1), fill=(255, 255, 255)
)
# text settings
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)

text = "Hello World!"
left, top, right, bottom = font.getbbox(text)
text_width = right - left
text_height = bottom - top

draw.text(
    (width // 2 - text_width // 2, height // 2 - text_height // 2),
    text,
    font=font,
    fill=(0, 140, 153),
)

# Display image.
disp.image(image)
