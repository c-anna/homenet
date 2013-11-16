#!/usr/bin/python3

import cgi
import cgitb
import os
import smtplib
import datetime
import grp
import sys
from email.mime.text import MIMEText

cgitb.enable()

#Find out what is year it is right now. This year will determine which
#folder on the server the bill is placed in.
d = datetime.date.today()
yr = d.year

#Get the names of users in the "billpayers" group on the server, and
#the number of payers. The dictionary 'emails' associates a Linux user
#name to an email address -- if there is a mismatch between the number
#of users in the billpayers group and the number of email addresses in
#this dictionary, we will halt (later).
billpayers = grp.getgrnam('billpayers')[3]
n_billpayers = len(billpayers)

emails = {"chris":"canna12@gmail.com"}#,
		#"heather":"xxxx",
		#"logan":"xxxx"}
		
#The next several lines retrieve the simple text/numeric/button input
#from the Bill Informer form.
form = cgi.FieldStorage()
billType = form["billType"].value
month = form["month"].value
dollarAmount = float(form["dollarAmount"].value)

#Retrieving the uploaded file takes a little more finesse. This
#block will retrieve the file and copy it to its correct location
#on the server, if it exists. If not, the user is redirected
#to an error page.
if "fileInput" in form and form["fileInput"].file:
	uploadedFile = form["fileInput"].file
	fn = month + ".pdf"
	
	fpath = os.path.join('../bills/', billType, str(yr), fn)
	fout = open(fpath, 'wb') 
	fout.write(uploadedFile.read())
	fout.close()
else:
	print("Status:404")
	print("Location: no_file.html")
	print()
	sys.exit()

#Build the message that will be emailed to the billpayers.
msg = "The new {0} bill for {1} is available on homenet. The total cost of the bill is ${2} " \
"and the cost for each of the {3} payers is ${4}. The bill is available for viewing in the {0} " \
"section of homenet's bill system as {1}.pdf.".format(billType, 
month, dollarAmount, n_billpayers, round(dollarAmount/n_billpayers,2))

#Add a link to the new bill. Some email clients may automatically make this a
#link (Gmail does), but perhaps not all. Consider adding an HTML message in the
#future.
msg += "\n\nThe bill is available for viewing at this location: " \
"http://canna.no-ip.org/homenet/bills/{0}/{1}/{2}.pdf".format(billType, yr, month)

#If the user specified an additional message, add it on here.
if 'msg' in form:
	msg += "\n\n" + form["msg"].value
else:
	msg += ""

#Create the email message and add the subject
emailMsg = MIMEText(msg)
emailMsg['Subject'] = "New {} bill on homenet".format(billType)

#Begin the process of emailing notifications to each billpayer
relay = smtplib.SMTP_SSL('smtp.gmail.com')
relay.login('canna12','xxxx')	
	
#Because the email will be routed through my personal Gmail account,
#the fromaddr here will be clobbered. If I ever get my own domain, I'll
#add a billmaster user for this purpose.
fromaddr = "billmaster@oberon"
toaddrs = ""

#Here's that payer/email mismatch I mentioned earlier.
if len(billpayers) != len(emails):
	print("Status:404")
	print("Location: payer_mismatch.html")
	print()
	sys.exit()
else:	
	for i in billpayers:
		toaddrs += emails[i] + ", "

#This will send all the emails and then close the SMTP relay. In the future,
#add some error handling here in case sendmail doesn't work.
relay.sendmail(fromaddr, toaddrs, emailMsg.as_string())
relay.quit()

#Show the user some confirmation that what they did worked. Then redirect them
#back to the homenet main page.
print("Status:200")
print("Content-Type: text/plain; charset=utf-8")
print("Refresh: 5; url=/homenet/index.html")
print()
print("The following email addresses have been informed of the new bill:")
print("\n")
print(toaddrs.replace(", ","\n"))
print("Redirecting back to homenet in 5 seconds...")



