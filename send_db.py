# File copyright (c)2024 Max Wiencek
from datetime import datetime
import os
import shutil
import socket
import pandas as pd
import sys
import time
import csv
import binascii
from subprocess import call
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_db_now():
	now = datetime.now()
	date_string = now.strftime("%Y%m%d.%H%M")
#	intdt = int(date_string)
	strdt = str(date_string)
	my_hostname = socket.gethostname()
	os.rename("/home/walkbox/Reader/database.csv", "/home/walkbox/Reader/"+my_hostname+strdt+".csv") 
	sender_email = "walkbox@icsp.9745903.xyz"
	sender_password = "inverclyde@1"
	recipient_email = "icsp2023x@gmail.com"
	subject = "CSV database :!: " + my_hostname
	body = my_hostname+" "+strdt+" "+"database"
	csvdb = my_hostname+strdt+".csv"
	with open("/home/walkbox/Reader/"+csvdb, "rb") as attachment:
		part = MIMEBase("application", "octet-stream")
		part.set_payload(attachment.read())
		encoders.encode_base64(part)
		part.add_header("Content-Disposition", "attachment; filename= %s" % csvdb)
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
	shutil.move("/home/walkbox/Reader/"+csvdb,  "/home/walkbox/Reader/database_archive/"+csvdb)
#	f = open("/home/walkbox/Reader/database.csv", "a")
	with open('/home/walkbox/Reader/database.csv', 'w', newline='') as p_db:
		writer = csv.writer(p_db)
		cols = ["ordinary", "hexd", "dated", "datedint"]
		writer.writerow(cols)

	with open('/home/walkbox/Reader/database-a.csv', 'w', newline='') as a_db:
		writer = csv.writer(a_db)
		colsa = ["hexx", "datexint"]
		writer.writerow(colsa)

		from shutdown import shutdown
		return f"{shutdown()}"
#        call("sudo nohup shutdown -h now", shell=True)
send_db_now()
