import os
import sys
import logzero
import zipfile
import datetime
from finalclosefunctions import *




def P6Bot2(data):
    logger.info(f"Starting processing {data} to Start Financial Close")
    notifications =  f"<ul>"
    try:
        ledger, period = data.split(" ")
        entities = get_entities("priandsub")
        ent = entities[ledger]["Name"]
        Period = period.strip()
        Month, Year = Period.split("-")
        mpa_month = int(Month) + 1
        print(Month, mpa_month)
        if mpa_month == 13:
            mpa_month = "01"
        current_month = months[int(Month) - 1]
        year_two_digits = str(Year[-2:])
        logger.info(f"Checking if revalue ledger is posted --> {ledger}   --> {ent}")
        rev_entities= get_entities("revaluation")
        period_p=f"{current_month}-{year_two_digits}"
        if ledger in rev_entities.keys():
            led = rev_entities[ledger]["Name"]
            rev_soap = Create_Validate_SOAP(rev_entities[ledger]["Ledger"], period)
            logger.info("Validating Revalue")
            rev_response = Validate_Journals(rev_soap)
            if len(rev_response.decode().strip().splitlines()) != valid_length:
                logger.info("Error : unposted")
                Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
                return f" Error : Ledger {led} unposted for revalue ledger. // "
            notifications += f"<li>verifying if {led} is unposted ..... {led} is posted<\li>"
        logger.info(f"Checking if primary-sec ledger is posted --> {ledger}   --> {ent}")
        soap = Create_Validate_SOAP(entities[ledger]["Ledger"], period)
        response = Validate_Journals(soap)
        if len(response.decode().strip().splitlines()) != valid_length:
            logger.info("Error unposted primary")
            Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
            return f" Error : Ledger {ledger} unposted for primary ledger. // "
        logger.info("creating multiperiod accounting")
        logger.info("Doing multiperiod accounting")
        mpa_zipfile = Do_MPA(ledger, Year, mpa_month)
        notifications += f"<li>Multiperiod Accounting --> Done </li><br>"
        logger.info("MPA completted")
        if ledger != "01":
            logger.info("Creating Closing Period Exception")
            logger.info("Doing CPE")
            CPE_zipfile = DO_CPE(ledger, f"{current_month}-{year_two_digits}", Year, Month)
            logger.info("Closing Period Exception Done")
            notifications += f"<li>Close Exception Period --> Done</li> <br>"
            logger.info("CPE creating Report")
            Validation = create_report(CPE_zipfile)
            logger.info("Doing Revalue")
            if Validation =="OK":
                rev_file = Revaluation(ledger, Year, Month)
                logger.info("REV DONE")
                notifications += f"<li> Revalue ledger --> Done </li> <br> "
                if f"{ledger}" == "10" or f"{ledger}" == "12" or f"{ledger}" == "14" or f"{ledger}" == "15": 
                    notifications += f"<li>LEDGER --> {ledger} </li><br><li>Entity --> {ent}</li><br></ul> // {mpa_zipfile};{CPE_zipfile};{rev_file}"
                else:
                    logger.info("Doing Translation")
                    trans_zipfile = Do_Translation(ledger,f"{current_month}-{year_two_digits}")
                    logger.info("Translating ledgers")
                    notifications += f"<li> Translation ledger --> Done </li> <br> "
                    notifications += f"<li>LEDGER --> {ledger} </li><br><li>Entity --> {ent}</li><br></ul> // {mpa_zipfile};{CPE_zipfile};{rev_file};{trans_zipfile}"
            else:
                logger.info("Exceptions found")
                rev_file = Validation
                notifications += f"<li>There exist some exceptions</li><br>"
                notifications += f"<li>LEDGER --> {ledger} </li><br><li>Entity --> {ent}</li><br></ul> // {mpa_zipfile};{CPE_zipfile};{rev_file}"
        else:
            rev_file = Revaluation(ledger, Year, Month)
            logger.info("REV Done")
            notifications += f"<li> Revalue ledger --> Done </li> <br> "
            if f"{ledger}" == "10" or f"{ledger}" == "12" or f"{ledger}" == "14" or f"{ledger}" == "15" or f"{ledger}" == "61": 
                notifications += f"<li>LEDGER --> {ledger} </li><br><li>Entity --> {ent}</li><br></ul> // {mpa_zipfile};{CPE_zipfile};{rev_file}"
            else:
                trans_zipfile = Do_Translation(ledger, f"{current_month}-{year_two_digits}")
                logger.info("Translating ledgers")
                notifications += f"<li> Translation ledger --> Done </li> <br> "
                notifications += f"<li>LEDGER --> {ledger} </li><br><li>Entity --> {ent}</li><br></ul> // {mpa_zipfile};{CPE_zipfile};{rev_file};{trans_zipfile}" 
        Push_To_S3(f"{logs_path}\\log.log","Process6","Log") 
        return notifications
    except:
        logger.info("Error on finalcial close")
        Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
        return f"Error : Some errors has occurred  // "