from datetime import datetime
import sys
import time
import RPi.GPIO as GPIO
import pn532.pn532 as nfc
import csv
import binascii
from pn532 import *
from subprocess import call
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
triggerPIN = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPIN,GPIO.OUT)

# pn532 = PN532_SPI(cs=4, reset=20, debug=False)
pn532 = PN532_I2C(debug=False, reset=20, req=16)
# pn532 = PN532_UART(debug=False, reset=20)
# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
def main():
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    x = time.time()
    print('Present your RFID tag...')    
    # Check if a card is available to read
    while True:
        uid = pn532.read_passive_target(timeout=1)

#   print('.', end="")
    # Try again if no card is available.
# print('Found card with UID: ',([hex(i) for i in uid]))
        if uid is not None:
            break
#    else:
        
    # Try again if no card is available.

#print('Found card with UID:', [hex(i) for i in uid])
#def main()
    key_c = [hex(i) for i in uid]
    key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'
#print('Pure UID ' ,key_c)
    keya = bytearray([ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF ])
#print("UID Length: {:d}".format(len(uid)))
#print("UID Value: " ,binascii.unhexlify(keya))
# Now we try to go through all 16 sectors (each having 4 blocks)
#for i in range(64):
#    try:
#print('ID numberH: ',key_a.decode)
#cxz = b'key_a.decode'
#key_d = key_a.decode
    qwe = binascii.b2a_hex(uid)
    zaq = int(qwe,16)
#print('UID Value: ' ,binascii.hexlify(uid))
    print('ID short: ' , qwe)
    qaz = int.from_bytes(qwe, byteorder='big', signed=False)
#    print('IDqaz: ' ,qaz)
#print('ID number: ',qaz)
    print('Date and time: ' ,dt)
# b = int(qaz)
    b=open('admin-database.csv', 'a',)
    a=csv.writer(b)
    a.writerow([qwe])
    b.close()
    time.sleep(0.1)
    
    buzzer = GPIO.PWM(triggerPIN, 587)
    buzzer.start(5)
    time.sleep(0.3)
    
    if zaq == 3198077303:
        sender_email = "walkbox@icsp.9745903.xyz"
        sender_password = "inverclyde"
        recipient_email = "icsp2023x@gmail.com"
        subject = "CSV database"
        body = "NFC database"

        with open("/home/walkbox/Reader/raspberrypi/python/database.csv", "rb") as attachment:
    # Add the attachment to the message
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
            "Content-Disposition",
            f"attachment; filename=database.csv",
)
            message = MIMEMultipart()
            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = recipient_email
            html_part = MIMEText(body)
            message.attach(html_part)
            message.attach(part)

        with smtplib.SMTP_SSL('serwer2377698.home.pl', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        print('CSV sent!!!')

        call("sudo nohup shutdown -h now", shell=True)
def more():
    main()
    while True:
        main()
more()
GPIO.cleanup()
