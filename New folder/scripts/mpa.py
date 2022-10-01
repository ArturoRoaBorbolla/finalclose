from finalclosefunctions import *
import logzero
import json
from logzero import logger
import os
import zipfile
import pandas as pd
from openpyxl import load_workbook
from openpyxl import Workbook
import xmltodict


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
zip_path = os.path.join(ROOT_DIR, "zip")
os.makedirs(zip_path, exist_ok=True)
config_path = os.path.join(ROOT_DIR, "Config")
os.makedirs(config_path, exist_ok=True)
logs_path = os.path.join(ROOT_DIR, "Logs")
os.makedirs(logs_path, exist_ok=True)
data_path = os.path.join(ROOT_DIR, "Data")
os.makedirs(data_path, exist_ok=True)
valid_response_Posted = "<ROWSET>\n<ROW>\n<P_LEDGER_ID>300000001414016</P_LEDGER_ID>\n<P_PERIOD_NAME>Aug-22</P_PERIOD_NAME>\n</ROW>\n</ROWSET>"
valid_length = len(valid_response_Posted.splitlines())
Fail_Flag_Posted = 0
unzip_path = os.path.join(ROOT_DIR, "Unzip")
os.makedirs(unzip_path, exist_ok=True)
general_data_path = os.path.join(ROOT_DIR, "..\\generaldata")
os.makedirs(general_data_path, exist_ok=True)
logzero.loglevel(logzero.INFO)
logzero.logfile(f"{logs_path}\\log.log")
logzero.json()



def Do_MPA(ledger_id, Year, Month):
    logger.info("Trying to do multiperiod accounting")
    try:
        with open(f"{data_path}\\mpa_{ledger_id}{Year}{Month}.cfg","r") as mpa_file:
            return f"{zip_path}\\mpa_{ledger_id}_{Year}_{Month}.zip"
    except:
       pass
    zipfile_name = ""
    entities = get_entities("priandsub")
    if ledger_id not in entities.keys():
        logger.info("LEdger id not in entities")
        return f"{zip_path}\\mpa_{ledger_id}_{Year}_{Month}.zip"
    ledger = entities[ledger_id]["Ledger"]
    Entity = entities[ledger_id]["Name"]
    logger.info(f"Creating Multi-Period-Accounting for ledger {ledger} --> {Entity}  ")
    soap = Create_Multi_Period_Accounting(ledger, Year, Month)
    response = GL_Request(soap)
    PID = json.loads(response.text)["ReqstId"]
    logger.info("Verifying status for multiperios accounting ")
    while True:
        Status = json.loads(Get_Status(PID).text)["items"][0]["RequestStatus"]
        if Status == "SUCCEEDED" or Status == "ERROR" or Status == "WARNING":
            logger.info("Multiperiod accounting Completed")
            break
    zipdata = get_files(PID, "All")
    zipfile_name = f"{zip_path}\\mpa_{ledger_id}_{Year}_{Month}.zip"
    with open(f"{zipfile_name}", "wb+") as zip:
        zip.write(zipdata)
    with open(f"{data_path}\\mpa_{ledger_id}{Year}{Month}.cfg","w+") as mpa_file:
            mpa_file.write(f"{ledger_id}{Year}{Month}\n")
    with zipfile.ZipFile(f"{zipfile_name}", 'r') as zip_mpa:
            zip_mpa.extractall(f"{unzip_path}")
    txt_file=f"{unzip_path}\\{PID}.txt"
    with open(txt_file,"r") as text:
        pid_to_download = text.read()    
        pid_to_download = pid_to_download.split("identifier")[1].split("for")[0].strip()
    while True:
        Status = json.loads(Get_Status(pid_to_download).text)["items"][0]["RequestStatus"]
        if Status == "SUCCEEDED" or Status == "ERROR" or Status == "WARNING":
            logger.info("Verifing reporting")
            break
    print(f"\n\n\n{pid_to_download}\n\n\n")
    zipdata = get_files(pid_to_download, "All")
    zipfile_name = f"{zip_path}\\mpa_{pid_to_download}.zip"
    with open(f"{zipfile_name}", "wb+") as zip:
        zip.write(zipdata)
    return f"{zipfile_name}"

