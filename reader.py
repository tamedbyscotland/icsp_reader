# File copyright (c)2024 Max Wiencek

from datetime import datetime
import os
import socket
import pandas as pd
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
pn532 = PN532_I2C(debug=False, reset=14, req=15)

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
# Email send
def main():
	dt = datetime.now()
	ts = datetime.timestamp(dt)
	x = time.time()
	print('Present your RFID tag...')
# Check if a card is available to read
	while True:
		uid = pn532.read_passive_target(timeout=1)
#   print('.', end="")
# print('Found card with UID: ',([hex(i) for i in uid]))
		if uid is not None:
			break
#	else:
# Try again if no card is available.
# Proper code:
	now = datetime.now()
	date_string = now.strftime("%Y%m%d%H%M")
	intdt = int(date_string)
	strdt = str(intdt)
	my_hostname = socket.gethostname()
	global df
	global qwe
	global hexdb_item
	global item_val
	global barf
	global hexadm_val
	global item_val_adm
	qwe = binascii.b2a_hex(uid)
	barf = qwe.decode('utf-8')

#	db_column_names = [['ordinary','hexd','dated','datedint']]
#	db_file = [[]]
#	dfa = pd.DataFrame(db_file, columns=db_column_names)
#	dfa = pd.DataFrame(db_column_names)
#	dfa.to_csv("/home/walkbox/Reader/database.csv", index=False)
#	with open('/home/walkbox/Reader/database.csv', 'w', newline='') as file:
#		writer = csv.writer(file)
#		field = ["ordinary", "hexd", "dated", "datedint"]
#		writer.writerow(field)
#
	dfx = pd.read_csv('/home/walkbox/Reader/admin-database.csv', sep = ',', dtype = str)
	hexvaladm = dfx[dfx['hexdb_adm'].str.contains(barf, case=False)]
	for index, row in hexvaladm.iterrows():
		hexadm_val = row['hexdb_adm']
		item_val_adm = row['admin_name']
		if item_val_adm:
			print('HexVal:', hexadm_val, 'ItemVal:', item_val_adm, ":!: Hello Admin :)")
			b=open('/home/walkbox/Reader/database_admin_log.csv', 'a',)
			a=csv.writer(b)
			a.writerow([item_val_adm,barf,dt,intdt])
			b.close()
			from id_display_a import admin_id
			return f"{admin_id()}"
	else:
		dfagain = pd.read_csv('/home/walkbox/Reader/database-a.csv', sep = ',', dtype = str)
		hexvalx = dfagain[dfagain['hexx'].str.contains(barf, case=False)]
		for index, row in hexvalx.iterrows():
			hexvalagain = row['hexx']
			date_val_again = row['datexint']
			if int(date_val_again) > 0:
				print("Once a day please!")
				from id_display_p_again import pupil_id_again
				return f"{pupil_id_again()}"
		else:
			df = pd.read_csv('/home/walkbox/Reader/icsp-database.csv', sep = ',', dtype = str)
			hexval = df[df['hexdb'].str.contains(barf, case=False)]
			for index, row in hexval.iterrows():
				hexdb_item = row['hexdb']
				item_val = row['ordinary']
				if  int(item_val) > 0:
					print('HexVal:', hexdb_item, 'ItemVal:', item_val)
					bx=open('/home/walkbox/Reader/database-a.csv', 'a',)
					ax=csv.writer(bx)
					ax.writerow([barf,intdt])
					bx.close()

				#	p_db=open('/home/walkbox/Reader/database.csv', 'a',)
				#	p_data=csv.writer(p_db)
				#	p_data.writerow([item_val,barf,dt,intdt])
				#	p_db.close()
				#
					db_column_names = [['ordinary','hexd','dated','datedint']]
					db_data = [[item_val,barf,dt,intdt]]
					dfa = pd.DataFrame(db_data, columns=db_column_names)
					dfa['ordinary'] = dfa['ordinary'].astype('str')
				#	dfa['ordinary'] = dfa['ordinary'].apply(lambda x: x.zfill(3))
					dfa.to_csv('/home/walkbox/Reader/database.csv', mode='a', float_format=str, header=False, index=False)

					from id_display_p import pupil_id
					return f"{pupil_id()}"
				break
			else:
				print("Tag is not in database!")

# Database file
#	print('Date and time: ' ,dt)
#	time.sleep(0.5)
def more():
    main()
    while True:
        main()
more()
GPIO.cleanup()
