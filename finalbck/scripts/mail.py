import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from finalclosefunctions import *


def send_mail(subject,messageto,message,attachments):
    try:    
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        
        msg['From'] = "bot_aae_is_c_dev@guidewire.com"
        msg['To'] = messageto        
        msg['Subject'] = subject
        
        # see the code below to use template as body
        body_text = ""
        body_html = message
        
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
        
        mail = smtplib.SMTP("smtp.outlook.office365.com", 587, timeout=20)

        # if tls = True                
        mail.starttls()        

        recipient = [messageto]
        part = MIMEBase('application', "octet-stream")
        with open(f"{attachments}", 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition","attachment; filename= f'{attachments}'")
        msg.attach(part)
                    
        mail.login('bot_aae_is_c_dev@guidewire.com', 'Vdj&Ty3?pFq;Zy')        
        mail.sendmail("fromemail@domain.com", recipient, msg.as_string())        
        mail.quit()
        
    except Exception as e:
        print(e)

'''

from O365 import Message
o365_auth = ('bot_aae_is_c_dev@guidewire.com','Vdj&Ty3?pFq;Zy')
m = Message(auth=o365_auth)
m.setRecipients('aiverdevs@soaprojects.com')
m.setSubject('I made an email script.')
m.setBody('Talk to the computer, cause the human does not want to hear it any more.')
m.sendMessage()'''