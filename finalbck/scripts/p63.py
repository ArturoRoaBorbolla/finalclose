import os
import logzero
import zipfile
from finalclosefunctions import *



def P6Bot3(data):
    try:
        logger.info("Closing ledgers")
        ledger, period = data.split(" ")
        entities = get_entities("priandsub")
        print(ledger,period)
        Period = period.strip()
        Month, Year = Period.split("-")
        current_month = months[int(Month) - 1]
        year_two_digits = str(Year[-2:])
        closingp = f"{current_month}-{year_two_digits}"
        logger.info("Closing period")
        ledger_id = entities[ledger]["Ledger"]
        closing_soap= Get_Close_SOAP(ledger_id, closingp)
        logger.info(f"Trying to close period for ledger {ledger} ledger_id {ledger_id}")
        response = GL_Request(closing_soap)
        print(response.text)
        logger.info("ledger {ledger} closed")
        Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
        return f' Period Closed for {ledger}<br> '
    except:
        logger.info("Error on trying to close the ledger")
        Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
        return " Something went wrong with {data} "