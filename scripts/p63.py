import os
import logzero
import zipfile
from finalclosefunctions import *



def P6Bot3(data):
    try:
        logger.info("Closing ledgers")
        ledger, period = data.split(" ")
        if ledger == "48":
            ledger="47"
        entities = get_entities("priandsubr")
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
        ledgers_report = open(f"{data_path}\\ledger_report.txt","a+")
        ledger_stat = verify_closed_periods(Period,ledger_id)
        if ledger_stat == "O":
            ledgers_report.write(f"Entity: {ledger} is still open\n")
            return f'{ledger} is still OPEN please verify<br>'
        if "s" in ledger:
            ledger="61"
            ledger_id = entities[ledger]["Ledger"]
            closing_soap= Get_Close_SOAP(ledger_id, closingp)
            logger.info(f"Trying to close period for ledger {ledger} ledger_id {ledger_id}")
            response = GL_Request(closing_soap)
            print(response.text)
            ledger_stat = verify_closed_periods(Period,ledger_id)
            if ledger_stat == "O":
                ledgers_report.write(f"Entity: {ledger} is still open\n")
                return f'{ledger} is still OPEN please verify<br>'
        logger.info("ledger {ledger} closed")
        Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
        next_month = months[int(Month) % 12]
        year_two_digits = str(Year[-2:])
        openingp = f"{next_month}-{year_two_digits}"
        opening_soap = Open_SOAP(entities[ledger]["Ledger"], openingp)
        response = GL_Request(opening_soap)
        name = entities[ledger]["Name"]
        notifications = f"Period Closed for Entity {ledger}\n"
        notifications += f"Ledger {name} have been opened for next period\n     "
        ledgers_report.write(f"Entity: {ledger} is closed now<br>")
        return notifications
    except:
        logger.info("Error on trying to close the ledger")
        Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
        ledgers_report.write(f"Entity: {ledger} --> Something went wrong with {data} could  be not closed <br>")
        return f"Something went wrong with {data} could  be not closed "