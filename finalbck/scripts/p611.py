
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


Regions=["emea","amer_us","apac","_amer_non_us"]


def send_mail(subject,region,message,attachments):
    #try:  
        with  open(f"C:\generaldata\{region}.lst","r") as lstx:
            mail_list = lstx.read()
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
        msg['To'] = messageto        
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
        print(f"recipient .;;;;;; {recipient }")
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
        print("Trying to send mail")
        mail.sendmail("bot_aae_is_c_dev@guidewire.com", recipient, msg.as_string())        
        mail.quit()

        return "Sended"
        
    #except Exception as e:
    #   return e



def LaunchRevaluation(region):
    try:
        print(f"Trying to open  C:\daily\{region}.txt")
        with  open(f"C:\daily\{region}.txt","r") as lstx:
            period=lstx.readline() 
            print(f"Period: {period}")
        print(f"Trying to write on  C:\generaldata\{region}lstexc.cong")
        with  open(f"C:\generaldata\{region}lstexc.cong","w") as lstx:
            ls= time.strftime("%d-%m-%Y")
            lstx.write(ls)
            print(f"last Execution for {region} was on {ls}")
        print(f"Trying to open  C:\generaldata\priansub.txt")
        with  open(f"C:\generaldata\priandsub.txt","r") as lstx:
            ledgers = lstx.readlines()
            print(f"Reading ledgers: \n {ledgers}")
        print(f"Trying to open  C:\generaldata\{region}.lst")
        with  open(f"C:\generaldata\{region}.lst","r") as lstx:
            mail_list = lstx.read()
            print(f"Reading mailing List: \n {mail_list}")
        for line in ledgers:
            print(f"Trying for: {line} ... {region} --- {period}")
            if region.upper() in line:
                ledger_id = line.split(",")[0]
                print(f"Ledger ID: {ledger_id}")
                Rev_File = P6Bot1(f"{ledger_id} {period}")
                print(f"Execution ..... {Rev_File}")
                Rev_File = Rev_File.split("/")
                #Rev_File[1]=Rev_File[1].replace("\\","\\\\")
                Rev_File[1]=Rev_File[1].split("\\")[-1]
                print(f"Sending mail")
                subject=f"Revaluation for the ledger {ledger_id} on the period {period} Done"
                print(subject,mail_list,Rev_File[0],Rev_File[1])
                Done = send_mail(subject,region,Rev_File[0],Rev_File[1])
                print(f"Result:::::: {Done}")
    except:
        pass

while True:
    lstxc = ""
    for i in Regions:
        print(f"Trying to execute for region {i}")
        try:
            print(f"Trying to open  C:\generaldata\{i}lstexc.cong")
            with  open(f"C:\generaldata\{i}lstexc.cong","r") as lstx:
                lstxc=lstx.readline()    
                if lstxc.strip() != time.strftime("%d-%m-%Y"):
                    LaunchRevaluation(i)
        except:
            print(f"Cant open  C:\generaldata\{i}lstexc.cong launching the Revaluation")
            LaunchRevaluation(i)
    sleep(20)
        

