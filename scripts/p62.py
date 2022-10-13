import os
import sys
import logzero
import zipfile
import datetime
from finalclosefunctions import *


def posting():
    Autopost_Reval_id=300000167059183
    rest_post = Create_AutoPost(Autopost_Reval_id)
    response_autopost = AutoPost(rest_post)
    Autopost_Reqid = json.loads(response_autopost.text)["ReqstId"]
    while True:
        Status = json.loads(Get_Status(Autopost_Reqid).text)["items"][0]["RequestStatus"]
        if Status == "SUCCEEDED":
            notifications = "<li>New Journasl created have been posted.</li><br>"
            break
        if Status == "ERROR" or Status == "WARNING":
            notifications = "<li>Warning or error when trying to post new journals.</li><br>"
            break
    return notifications

def P6Bot2(data):
    try:
        ledger, period = data.split(" ")
        Unposted=""
        notifications =  f"<ul>"
        entities = get_entities("priandsubr")
        print(entities)
        print("\n\n\n")
        ledger_id = entities[ledger]["Ledger"]
        ent = entities[ledger]["Name"]
        Period = period.strip()
        Month, Year = Period.split("-")
        current_month = months[int(Month) - 1]
        mpa_year = Year
        year_two_digits = str(Year[-2:])
        period_p=f"{current_month}-{year_two_digits}"
        state= Get_Ledger_Status(f"{current_month}-{year_two_digits}",ledger_id)
        if "Error" in state:
            logger.info(f"Error : {state}")
            return f"<br>{state} <br>// "
        if ledger != "85":
            logger.info(f"Checking if primary-sec ledger is posted --> {ledger}   --> {ent}")
            soap = Create_Validate_SOAP(entities[ledger]["Ledger"], period_p)
            response = Validate_Journals(soap)
            rd = response.decode()
            print(f"\n\n\n{rd} \n\n\n")
            notifications+= f"<br><b>Step 1:  Identifying unposted Journals</b><br> "
            if len(response.decode().strip().splitlines()) != valid_length:
                logger.info("Error unposted primary")
                Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
                up=rd.splitlines()
                Unposted+="<ul>"
                for ul in up:
                    if "JOURNAL_NAME"in ul:
                        Unposted += "<li>"  
                        Unposted += ul.split("JOURNAL_NAME>")[1].split("</")[0]
                        Unposted+="</li><br>"
                Unposted += "</ul>"
                return f"<br><b>Entity {ent} have unposted journals for primary ledger.</b><br>{Unposted} // "
            else:
                notifications+= f"<br><li>Entity {ent} does not have any unposted journal for primary ledger.</li> <br>"
        led = entities[ledger]["Name"]
        print(f"LEDGER ::::::::::: {ledger}")
        if ledger != "61":
            rev_entities = get_entities("revaluation")
            with open(f"{data_path}\\reval.txt", "w") as ff:
                ff.write(str(rev_entities))
            rev_ledger_id = rev_entities[ledger]["Ledger"]
            rev_ent = rev_entities[ledger]["Name"]
            rev_state= Get_Ledger_Status(f"{current_month}-{year_two_digits}",rev_ledger_id)
            if "Error" in rev_state:
                logger.info(f"Error : {rev_state}")
                return f"{rev_state} // "
            logger.info(f"Starting processing {data} to Start Financial Close")
            #try:
            Month, Year = Period.split("-")
            mpa_month = int(Month) + 1
            print(Month, mpa_month)
            if mpa_month == 13:
                mpa_month = "01" 
                mpa_year = str(int(mpa_year) + 1)
            current_month = months[int(Month) - 1]
            year_two_digits = str(Year[-2:])
            logger.info(f"Checking if revalue ledger is posted --> {ledger}   --> {ent}")
            rev_entities= get_entities("revaluation")
            if ledger in rev_entities.keys():
                led = rev_entities[ledger]["Name"]
                rev_soap = Create_Validate_SOAP(rev_entities[ledger]["Ledger"], period)
                logger.info("Validating Revalue")
                rev_response = Validate_Journals(rev_soap)
                rd =rev_response.decode()
                print(f"\n\n\n{rd} \n\n\n")
                #notifications+= f"<Br><b>Step 1 (Part B):  Identifying unposted Journals for revaluation ledgers</b><br> "
                if len(rev_response.decode().strip().splitlines()) != valid_length:
                    logger.info("Error : unposted")
                    Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
                    Unposted="\n"
                    rd=rd.splitlines()
                    Unposted+="<ul>"
                    for ul in rd:
                        if "JOURNAL_NAME"in ul:
                            Unposted += "<li>"  
                            Unposted += ul.split("JOURNAL_NAME>")[1].split("</")[0]
                            Unposted+="</li><br>"
                    Unposted += "</ul>"
                    return f"<br>        Error : Entity  {led}  have unposted journals. <br> {Unposted} //  "
                
            logger.info("creating multiperiod accounting")
            logger.info("Doing multiperiod accounting")
            if ledger !="85":
                notifications+=f"<br><b>Step 2: Running Multiperiod Accounting </b><br>"
                mpa_zipfile = Do_MPA(ledger, mpa_year, mpa_month)
                mpaf = mpa_zipfile.split("\\")[-1]
                notifications += f"<li>        Multiperiod Accounting ---> Done </li><br><li>      Please refer to file '{mpaf}' if available for more information. </li><br>"
                logger.info("MPA completted")
                if ledger != "61s":
                    logger.info("Creating Closing Period Exception")
                    logger.info("Doing CPE")
                    notifications+= f"<br> <b>Step 3 (Part A): Running the Subledger Close Exception Report</b><br>"
                    CPE_zipfile , pid = DO_CPE(ledger, f"{current_month}-{year_two_digits}", Year, Month)
                    cpef= CPE_zipfile.split("\\")[-1]
                    logger.info("Closing Period Exception Done")
                    notifications += f"<li>        Subledger Period Close Exception --> Done</li><br> <li>        Please refer to file '{cpef}' if available for more information.</li><br>"
                    logger.info("CPE creating Report")
                    print(CPE_zipfile , pid)
                    notifications+= f"<br> <b>Step 3 (Part B): Converting Subledger Close Exception Report</b><br>"
                    if int(pid)!=0:
                        print("\n")
                        print("\n")
                        print("Converting")
                        Validation = create_report(CPE_zipfile,f"{pid}",ledger)
                    logger.info("Doing Revalue")
                    print(f"verified: {Validation}")
                    if Validation =="No Exceptions found" and pid != 0:
                        notifications += f"<br>Report Created:<br><li>{Validation}.</li>"
                        notifications+= f"<br> <b>Step 4: Running the Revaluation</b><br>"
                        rev_file = Revaluation(ledger, Year, Month)
                        revf=rev_file.split("\\")[-1]
                        logger.info("REV DONE")
                        notifications += posting()
                        notifications += f"<li>        Revalue ledger --> Done </li> <br> <li>        Please refer to file '{revf}' if available for more information.</li> <br>"
                        if f"{ledger}" == "10" or f"{ledger}" == "12" or f"{ledger}" == "14" or f"{ledger}" == "15":  
                            notifications += f"<li>LEDGER --> {ledger} </li><br><li>Entity --> {ent}</li><br></ul> // {mpa_zipfile};{CPE_zipfile};{rev_file};{data_path}\\PID_{ledger}_{current_month}_{year_two_digits}.INFO"
                        else:
                            logger.info("Doing Translation")
                            notifications+= f"<br> <b>Step 5: Running the Translation</b><br>"
                            trans_zipfile = Do_Translation(ledger, f"{current_month}-{year_two_digits}")
                            transf= cpef= trans_zipfile.split("\\")[-1]
                            logger.info("Translating ledgers")
                            notifications += f"<li> Translation ledger --> Done </li> <br> <li>        Please refer to file '{transf}' if available for more information.</li> <br>"
                            notifications += f"<li>LEDGER --> {ledger} </li><br><li>Entity --> {ent}</li><br></ul> // {mpa_zipfile};{CPE_zipfile};{rev_file};{trans_zipfile};{data_path}\\PID_{ledger}_{current_month}_{year_two_digits}.INFO"
                    else:
                        valf=Validation.split("\\")[-1]
                        notifications += f"<br>Report Created:<br><li>{valf}.</li>"
                        logger.info("Exceptions found")
                        rev_file = Validation
                        notifications += f"<li>There exist some exceptions</li><br>"
                        notifications += f"<li>LEDGER --> {ledger} </li><br><li>Entity --> {ent}</li><br></ul> // {mpa_zipfile};{CPE_zipfile};{rev_file};{data_path}\\PID_{ledger}_{current_month}_{year_two_digits}.INFO"
                    print("\n")
                    print("\n")
                else:
                    rev_file = Revaluation(ledger, Year, Month)
                    notifications += posting()
                    logger.info("REV Done")
                    notifications += f"<li> Revalue ledger --> Done </li> <br> "
                    if f"{ledger}" == "10" or f"{ledger}" == "12" or f"{ledger}" == "14" or f"{ledger}" == "15" or f"{ledger}" == "61":  
                        notifications += f"<li>LEDGER --> {ledger} </li><br><li>Entity --> {ent}</li><br></ul> // {mpa_zipfile};{CPE_zipfile};{rev_file};{data_path}\\PID_{ledger}_{current_month}_{year_two_digits}.INFO"
                    else:
                        trans_zipfile = Do_Translation(ledger, f"{current_month}-{year_two_digits}")
                        logger.info("Translating ledgers")
                        transf= cpef= trans_zipfile.split("\\")[-1]
                        notifications += f"<li> Translation ledger --> Done </li> <br> <li>        Please refer to file '{transf}' if available for more information.</li> <br>"
                        notifications += f"<li>LEDGER --> {ledger} </li><br><li>Entity --> {ent}</li><br></ul> // {mpa_zipfile};{rev_file};{trans_zipfile};{data_path}\\PID_{ledger}_{current_month}_{year_two_digits}.INFO"  
                Push_To_S3(f"{logs_path}\\log.log","Process6","Log") 
                return notifications
                #except:
                #    logger.info("Error on finalcial close")
                #    Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
                #    return f"Error : Some errors has occurred  // "
            else:
                rev_file = Revaluation(ledger, Year, Month)
                notifications += posting()
                logger.info("REV Done")
                notifications += f"<li> Revalue ledger --> Done </li> <br> "
                notifications += f"<li>LEDGER --> {ledger} </li><br><li>Entity --> {ent}</li><br></ul> // {rev_file};{data_path}\\PID_{ledger}_{current_month}_{year_two_digits}.INFO"  
                Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
                return notifications
        else:
            return f"{notifications} // "
    except:
        return {"Connectivity issue occurs //"}