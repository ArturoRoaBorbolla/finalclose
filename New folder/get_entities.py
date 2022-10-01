import logzero
import os
import requests
from logzero import logger
import base64




#oracle_url="https://efow.fs.us2.oraclecloud.com"
#oracle_url="https://efow-test.fa.us2.oraclecloud.com"
oracle_url= "https://efow-dev1.fa.us2.oraclecloud.com"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
general_data_path = os.path.join(ROOT_DIR, "..\\generaldata")
os.makedirs(general_data_path, exist_ok=True)
logzero.loglevel(logzero.INFO)
logzero.json()
data_path = os.path.join(ROOT_DIR, "Data")
os.makedirs(data_path, exist_ok=True)

def get_entities(ledger_type):
    logger.info("Reading Ledgers Id from Oracle")
    if ledger_type.upper() == "PRIMARY":
        ledger_file=f"{general_data_path}\\primary.txt"
    elif ledger_type.upper() == "SUBLEDGER":
        ledger_file=f"{general_data_path}\\subledger.txt"
    with open(ledger_file,"r") as ledger_config:
        ledger_list=ledger_config.read().splitlines()
    try:
        ledgers= {}
        ledgers_info = get_ledgers_info()
        ledger_json=json.loads(ledgers_info.text)
        ledger_json = ledger_json["items"]
        for i in ledger_json:
            ledgers[i["Name"]] = i["LedgerId"]        
        entities={}
        for i in ledger_list:
            print(i)
            try:
                data = i.split(",")
                print(data)
                entity=data[0].strip()
                ledger_name = data[1].strip()
                entities.update({ entity: {"Name": ledger_name, "Ledger":  ledgers[ledger_name]} })  
            except:
                pass
    except:
        return "Error on set the entities // // "
    return  entities



def read_credentials():
    try:
        usr_psw = open(f"{data_path}\\credentials.txt","rb")
        user = base64.b64decode(usr_psw.readline().decode()).decode()
        passw = base64.b64decode(usr_psw.readline().decode()).decode()
        usr_psw.close()
        user = user.strip()
        passw = passw.strip()
        user , passw="vsethi","Welcome1"
    except:
        return "Error on read credentials // "
    return user,passw


def get_ledgers_info():
    try:
        logger.info("Getting ledgers info to look for closed ones")
        url = f"{oracle_url}/fscmRestApi/resources/11.13.18.05/ledgersLOV?limit=10000"
        #print(url)
        headerss = {"Content-Type": "application/json",
                "Connection":  "Keep-Alive"
                }
        user,passw  = read_credentials()
    except:
       logger.info("Ledgers info can not be read")
       return "Error on read ledger info // "
    return requests.get(url, auth=(user, passw), headers=headerss)