import requests
import base64
import logzero
import os
from logzero import logger
import pandas as pd




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
logzero.json()


oracle_url= "https://efow-dev1.fa.us2.oraclecloud.com"

def read_credentials():
    try:
        logger.info("Reading credentials")
        usr_psw = open(f"{data_path}\\credentials.txt","rb")
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

'''
def get_spreedsheet(soap):
    # print(soap)
    logger.info("Getting xlsx file to get the revalue id's")
    url = f"{oracle_url}/xmlpserver/services/ExternalReportWSSService?WSDL"
    headerss = {"Content-Type": "application/soap+xml",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "Keep-Alive"
                }
    user,passw = read_credentials()
    resp = requests.post(url, data=soap, auth=(user, passw), headers=headerss)
    print(resp.text)
    respcod = resp.text.split("Bytes>")[1].split("</ns2")[0]
    respdec = base64.b64decode(respcod)
    return respdec
'''

def get_data(soap):
    # print(soap)
    logger.info("Getting xlsx file to get the revalue id's")
    url = f"{oracle_url}:443/xmlpserver/services/v2/ReportService?wsdl"
    headerss = {"Content-Type": "application/soap+xml",
                "Accept-Encoding": "text, xml",
                "Connection": "Keep-Alive"
                }
    user,passw = read_credentials()
    resp = requests.post(url, data=soap, headers=headerss)
    print(resp.text)
    respcod = resp.text.split("Bytes>")[1].split("</report")[0]
    print(respcod)
    respdec = base64.b64decode(respcod)
    return respdec



def get_report(report_type):
    if report_type == "Allocation":
        soap_report=Create_allocation_report_SOAP()
        xlsx_name = f"{config_path}\\allocation.csv"
    elif report_type == "Revalue":
        soap_report=Create_revalue_report_SOAP()
        xlsx_name = f"{config_path}\\revalue.csv"
    else: 
        return "No report type detected" 
    data = get_data(soap_report)
    with open(f"{xlsx_name}", "wb") as xl:
        data.replace(b'"',b"")
        xl.write(data)
    #read_file = pd.read_excel (f"{xlsx_name}")
    #csv_file = xlsx_name.split("xlsx")[0]
    #csv_file = f"{csv_file}csv"
    #read_file.to_csv (f'{csv_file}', index = None, header=False)
    return f"{report_type} report created"
        
        
        
#def Create_allocation_report_SOAP():
#    return f'''<soap:Envelope xmlns:pub="http://xmlns.oracle.com/oxp/service/PublicReportService" xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
'''    <soap:Header></soap:Header>
    <soap:Body>
        <pub:runReport>
            <pub:reportRequest>
                <pub:parameterNameValues>
                    <pub:item>
                        <pub:name/>
                        <pub:values>
                            <pub:item/>
                        </pub:values>
                    </pub:item>
                </pub:parameterNameValues>
            <pub:reportAbsolutePath>/Custom/RPA/GW Allocation Rues/GW Allocation Rules.xdo</pub:reportAbsolutePath>
            <pub:sizeOfDataChunkDownload>-1</pub:sizeOfDataChunkDownload>
            </pub:reportRequest>
        </pub:runReport>
    </soap:Body>
</soap:Envelope>
'''

     
        
def Create_revalue_report_SOAP():
    return f'''<soap:Envelope xmlns:pub="http://xmlns.oracle.com/oxp/service/PublicReportService" xmlns:soap="http://www.w3.org/2003/05/soap-envelope"> 
    <soap:Header></soap:Header>
    <soap:Body>
        <pub:runReport>
            <pub:reportRequest>
                <pub:parameterNameValues>
                    <pub:item>
                        <pub:name/>
                        <pub:values>
                    <pub:item/>
                        </pub:values>
                    </pub:item>
                </pub:parameterNameValues>
                <pub:reportAbsolutePath>/Custom/RPA/GW Revaluation Rules/GW Revaluation Rules.xdo</pub:reportAbsolutePath>
                <pub:sizeOfDataChunkDownload>-1</pub:sizeOfDataChunkDownload>
            </pub:reportRequest>
        </pub:runReport>
    </soap:Body>
</soap:Envelope>'''




def Create_allocation_report_SOAP():
    user,passw = read_credentials()
    logger.info("Creating allocation report payload")
    return f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://xmlns.oracle.com/oxp/service/v2">
        <soapenv:Header/>
        <soapenv:Body>
            <v2:runReport>
                <v2:reportRequest>
                    <v2:attributeFormat>csv</v2:attributeFormat>
                    <v2:byPassCache>y</v2:byPassCache>
                    <v2:flattenXML>y</v2:flattenXML>
                    <v2:reportAbsolutePath>/Custom/RPA/GW Allocation Rules/GW Allocation Rules.xdo</v2:reportAbsolutePath>
                <v2:sizeOfDataChunkDownload>-1</v2:sizeOfDataChunkDownload>
                </v2:reportRequest>
                <v2:userID>{user}</v2:userID>
                <v2:password>{passw}</v2:password>
            </v2:runReport>
        </soapenv:Body>
    </soapenv:Envelope>'''


def get_rev():
    report = get_report("Revalue")
    if "No" not in report:
        csv_file = f"{data_path}\\revalue.csv"
        with open(csv_file,"r") as csv_data:
            revids = csv_data.read().splitlines()
        del revids[0]
        remove = ["SL", "Switzerland"  ,"Bermuda","Hong"]
        #data = any(element not in remove for element in data )
        revids = [element for element in revids if element not in remove ]
        revaluation={}
        with open(f"{data_path}\\revid.txt","r") as rev_data:
            revent = rev_data.read().splitlines()
        for i in revent:
            current_ent = i.split(",")[0]
            rev_name=i.split(",")[1]
            for j in revids:
                if rev_name in j:
                    current_id = j.split(",")[0]
                    revaluation[current_ent] = {"Ledger": current_id, "Name": rev_name}
        return revaluation
                    