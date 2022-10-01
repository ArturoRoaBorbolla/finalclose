import os
import sys
import logzero
import datetime
from finalclosefunctions import *

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = f"{ROOT_DIR}\\finalclose"
logs_path = os.path.join(ROOT_DIR, "Logs")
os.makedirs(logs_path, exist_ok=True)
logzero.loglevel(logzero.INFO)
logzero.json()

def P6Bot1(data):
    #try:
        logger.info("Starting Daily Revalue")
        entities = get_entities("priandsubr")
        print(entities)
        ledger, period = data.split(" ")
        print(ledger,period)
        ent = entities[ledger]["Name"]
        Period = period.strip()
        Month, Year = Period.split("-")
        logger.info(f"Doing Revaluation for the ledger {ledger}")
        print(f"\n\n\n trying to do rev")
        rev = Revaluation(ledger, Year, Month)
        print("\n\n\n")
        print("Revalue done \n\n\n\n")
        if "Error" in rev:
            logger.info("Error on revaluation")
            Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
            return f"Error / {rev}"
        print(f"{rev}\n\n\n")
        logger.info("autoposting")
        autopost_soap = Create_AutoPost(Autopost_id)
        Response_autopost = GL_Request(autopost_soap)
        Autopost_Reqid = json.loads(Response_autopost.text)["ReqstId"]
        logger.info("Getting posting status")
        while True:
            Status = json.loads(Get_Status(Autopost_Reqid).text)["items"][0]["RequestStatus"]
            print(f"Status: {Status}")
            if Status == "SUCCEEDED":
                logger.info("Succeeded")
                break
            if Status == "ERROR" or Status == "WARNING":
                logger.info("Error : status {Status} on autopost for {ent} / {rev}")
                Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
                break
                ##return f"Execution Error: Warning/Error on Autopost for {ent} / {rev}"
        logger.info("Trying to validate")
        soap = Create_Validate_SOAP(entities[ledger]["Ledger"], period)
        logger.info(f"Validating unposted jurnal ledger {ledger}")
        response = Validate_Journals(soap)
        print(response.decode().strip().splitlines())
        if len(response.decode().strip().splitlines()) != valid_length:
            ent = entities[ledger]["Name"]
            logger.error(f"Error: Ledgers {ent} Unposted")
            Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
            return f"Ledger: {ent} / {rev}"
            #return f"Error: Ledgers {ent} Unposted / {rev}"
        else:
            ent = entities[ledger]["Name"]
            logger.info("Saving configuration")
            with open(f"{config_path}\\config{Month}{Year}.cfg", "w") as config:
                    config.write(f"{ledger}\n")
            Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
            return f"Ledger: {ent} / {rev}"
    #except:
    #    logger.error("Some errors ocurred")
    #    Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
    #    return f"Error: Some errors has occurred / "

