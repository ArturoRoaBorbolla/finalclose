
from finalclosefunctions import *
from p61 import P6Bot1
import time
from time import sleep
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from finalclosefunctions import *

with  open(f"C:\generaldata\list.lst","r") as lstx:
    mail_list = lstx.read()

attachments="rev_10_2021_12.zip"
subject="testing"
message="testing"
messageto=mail_list
#print(message_to)
#messageto= ", ".join(message_to).replace("\n","")
print("Entrando..........")
#for i in message_to:
#    messageto += f"{i},"
#messageto=messageto.replace("\n","")    
#messageto = messageto[:-1]
print(f"Messaging to::::::    {messageto}")      
# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')

msg['From'] = "bot_aae_is_c_dev@guidewire.com"
#msg['To'] = messageto        
msg['Subject'] = subject
print(f"Subject::::::: {subject}")
# see the code below to use template as body
body_text = ""
body_html = message
print(f"Message::::::: {message}")

# Create the body of the message (a plain-text and an HTML version).
# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(body_text, 'plain')
part2 = MIMEText(body_html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.
print(f"Files::::::::{attachments}")
mail = smtplib.SMTP("smtp.outlook.office365.com", 587, timeout=20)

# if tls = True                
mail.starttls()        
print("Connecting.........")
recipient = messageto.split(",")
part = MIMEBase('application', "octet-stream")
with open(attachments, 'rb') as file:
    part.set_payload(file.read())
encoders.encode_base64(part)
print("File loading..........")
attached=attachments
#attached=attachments.split("\\")[-1]
part.add_header("Content-Disposition",f"attachment; filename= {attached}")
msg.attach(part)
print("Headering........")
mail.login('bot_aae_is_c_dev@guidewire.com', 'Vdj&Ty3?pFq;Zy')
print("TRying to send mail")
mail.sendmail("bot_aae_is_c_dev@guidewire.com", recipient, msg.as_string())        
mail.quit()
print("Sended")
