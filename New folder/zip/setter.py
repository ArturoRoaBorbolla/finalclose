import base64
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
zip_path = os.path.join(ROOT_DIR, "zip")
   
def set_user(data):
    try:
       user,passw= data.split("///")
       with open(f"{zip_path}\\credentials.txt","wb") as cred:
            cred.write(base64.b64encode(user.encode()))
            cred.write(b"\n")
            cred.write(base64.b64encode(passw.encode()))
            cred.close()
       return f"{user}----{passw}"
    except:
        return "Error on set credentials // //"
