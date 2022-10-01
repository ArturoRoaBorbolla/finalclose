
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
from zipfile import ZipFile


Regions=["EMEA","AMER_NON_US","APAC","AMER_US"]

def read_credentials():
    try:
        logger.info("Reading credentials")
        usr_psw = open("credentials.txt","rb")
        user = base64.b64decode(usr_psw.readline().decode()).decode()
        passw = base64.b64decode(usr_psw.readline().decode()).decode()
        usr_psw.close()
        user = user.strip()
        passw = passw.strip()
        #user , passw="vsethi","Welcome1"
    except:
        logger.info("Error on reading credentials")
        return "Error on read credentials // "
    return user,passw


def send_mail(subject,message_to,message,attachments,region,period):
    #try:  
        user,passw = read_credentials()
        print(user,passw)
        messageto=message_to
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

        #msg['From'] = "bot_aae_is_c_dev@guidewire.com"
        msg['From'] = user
        #msg['To'] = messageto        
        msg['Subject'] = f"Revaluation for Region {region} for period {period} Finished"
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
        #mail.login('bot_aae_is_c_dev@guidewire.com', 'Vdj&Ty3?pFq;Zy')
        mail.login(user, passw)
        print("TRying to send mail")
        #mail.sendmail("bot_aae_is_c_dev@guidewire.com", recipient, msg.as_string())
        mail.sendmail(user, recipient, msg.as_string())        
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
        print(f"Trying to write on  C:\generaldata\{region}lstexc.conf")
        with  open(f"C:\generaldata\{region}lstexc.conf","w") as lstx:
            ls= time.strftime("%d-%m-%Y")
            lstx.write(ls)
            print(f"last Execution for {region} was on {ls}")
        print(f"Trying to open  C:\generaldata\priansubr.txt")
        with  open(f"C:\generaldata\priandsubr.txt","r") as lstx:
            ledgers = lstx.readlines()
            print(f"Reading ledgers: \n {ledgers}")
        print(f"Trying to open  C:\generaldata\{region}.lst")
        with  open(f"C:\generaldata\{region}.lst","r") as lstx:
            mail_list = lstx.read()
            #mail_list = mail_list.split("\n")
            print(f"Reading mailing List: \n {mail_list}")
        message =f"Region:::::: {region}\n<br> Period:::::::::{period}\n<br>"
        files = []
        for line in ledgers:
            print(f"Trying for: {line} ... {region} --- {period}")
            if region.upper() in line:
                ledger_id = line.split(",")[0]
                if ledger_id != "61":
                    print(f"Ledger ID: {ledger_id}")
                    Rev_File = P6Bot1(f"{ledger_id} {period}")
                    print(f"Execution ..... {Rev_File}")
                    Rev_File = Rev_File.split("/")
                    #Rev_File[1]=Rev_File[1].replace("\\","\\\\")
                    Rev_File[1]=Rev_File[1].split("\\")[-1]
                    print(f"Sending mail")
                    subject=f"Revaluation for the Entity {ledger_id} on the period {period} Done  ---> "
                    messa = Rev_File[0]
                    filez= Rev_File[1]
                    message += f"{subject} {messa}\n<br>"
                    files.append(f"{filez}")
                    #print(subject,mail_list,Rev_File[0],Rev_File[1])
        print(files)
        Zip = ZipFile(f"{region}.zip","w")
        for f in files:
            try:
                with zipfile.ZipFile(f, 'r') as entzip:
                    entzip.extractall(f"c:\\Revaluation")
                os.remove(f)
            except:
                pass
        for item in os.listdir("c:\\Revaluation"):
            if item.endswith(".txt"):
                Zip.write(os.path.join("c:\\Revaluation", item))
                os.remove(os.path.join("c:\\Revaluation", item))
        Zip.close()
        Done = send_mail(subject,mail_list,message,f"{region}.zip",region,period)
        os.remove(f"{region}.zip")
        print(f"Result:::::: {Done}")
    except Exception as e:
        print(e)

while True:
    lstxc = ""
    for i in Regions:
        print(f"Trying to execute for the region {i}")
        try:
            print(f"Trying to open  C:\generaldata\{i}lstexc.conf")
            with  open(f"C:\generaldata\{i}lstexc.conf","r") as lstx:
                lstxc=lstx.readline()    
                if lstxc.strip() != time.strftime("%d-%m-%Y"):
                    if i == "APAC" and int(time.strftime("%H")) == 20:
                        LaunchRevaluation(i)
                    if i == "EMEA" and int(time.strftime("%H")) == 12:
                        LaunchRevaluation(i)
                    if "AMER" in i and int(time.strftime("%H")) == 16:
                        LaunchRevaluation(i)
        except:
            print(f"Cant open  C:\generaldata\{i}lstexc.conf launching the Revaluation")
            LaunchRevaluation(i)
    sleep(10)
            

