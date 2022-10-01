import os
import sys
import logzero
import zipfile
import datetime
from finalclosefunctions import *

CPE_zipfile = DO_CPE("10", f"Dec-21", 2021, 12)



  
'''  
def transferledgerbalance(data):
    try:
        ledger_id, period = data.split(" ")
        begin_time = datetime.now()
        logzero.json()
        logzero.loglevel(logzero.INFO)
        Period = period.strip()
        Day = datetime.now().strftime("%d")
        Month, Year = Period.split("-")
        current_month = months[int(Month) - 1]
        year_two_digits = str(Year[-2:])
    except:
        return f"Python Error : Malformed Data"
    else:
        payload = get_transfer_payload(entities[ledger_id]["Ledger"], f"{current_month}-{year_two_digits}")
        print(payload)
        response_transfer = tranferledgers(payload)
        print(response_transfer.text)
        process = json.loads(response_transfer.text)["ReqstId"]
        print(process)
        Status = ""
        if int(process) != -1:
            while True:
                Status = json.loads(Get_Status(process).text)["items"][0]["RequestStatus"]
                print(Status)
                if Status == "SUCCEEDED" or Status == "ERROR" or Status == "WARNING":
                    break
            try:
                zipdata = get_files(process, "All")
            except:
                return f"Python Error : Error on downloading the zip file"
            else:
                zipfile_name = f"{zip_path}\\transfer_{ledger_id}_{process}.zip"
                try:
                    with open(f"{zipfile_name}", "wb") as zip:
                        zip.write(zipdata)
                except:
                    return f"Python Error : Error on save the zip file "
                else:
                    textfile = f"{ROOT_DIR}\\{process}.txt"
                    with zipfile.ZipFile(f"{zipfile_name}", 'r') as zip_ref:
                        zip_ref.extractall(f"{ROOT_DIR}")
                    with open(textfile, "r") as txt:
                        text = txt.read()
                    lines = text.splitlines()[0:11]
                    # print(lines)
                    Message = f'''The Transfer Ledger Balance process has been executed.<br><br>REQUEST_ID: {process}<br>STATUS: {Status}<br><br>The process was executed with the following parameters:<br><br>'''
                    for i in lines:
                        Message += f"{i}<br>"
                    Message += f'''<br>In the attached zip file you will find the output and the corresponding log of the process.<br>'''
                    # print(Message)
                    files_to_delete = os.listdir(ROOT_DIR)
                    for item in files_to_delete:
                        if item.endswith(".txt"):
                            os.remove(os.path.join(ROOT_DIR, item))
                    for item in files_to_delete:
                        if item.endswith(".log"):
                            os.remove(os.path.join(ROOT_DIR, item))
                    # os.remove(textfile.replace(".txt",".log"))
                    Push_To_S3(zipfile_name, "Process6", "Output")
                    return f" {Message}"
        else:
            return f"Error : No valid ledger"         