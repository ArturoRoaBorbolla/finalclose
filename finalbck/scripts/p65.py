
import os
import sys
import logzero
import datetime
from finalclosefunctions import *


def P6Bot5(data):
    logger.info("Trying to close CL and open ALL Ledgers in ALL regions")
    notifications=""
    period, region = data.split(",")
    Period = period.strip()
    Month, Year = Period.split("-")
    next_month = months[int(Month) % 12]
    year_two_digits = str(Year[-2:])
    openingp = f"{next_month}-{year_two_digits}"
    logger.info("trying to get region entities")
    entities = get_entities("priandsub")
    logger.info("Trying to get CL entity")
    cl = get_entities("cl")
    print(cl)
    try:
        logger.info("Closing CL")
        current_month = months[int(Month) - 1]
        year_two_digits = str(Year[-2:])
        closingp = f"{current_month}-{year_two_digits}"
        closing_soap= Get_Close_CL_SOAP(cl["00"]["Ledger"], closingp)
        logger.info(f"Trying to close period for CL on {period}")
        response = GL_Request(closing_soap)
        print(response.text)
    except:
        logger.info("Error on close CL")
    try:
        with open(f"{general_data_path}\\priandsub.txt","r") as ledger_config:
            ledger_list=ledger_config.read().splitlines()
    except:
        logger.info("Error on opening file to get region info")
        Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
        return "Error on Opening file to read data about regions"
    else:
        ledgers=[]
        #logger.info(f"Splitting data to compare with region {region}")
        for i in ledger_list:
            data = i.split(",")
            #if data[2]==region:
            ledgers.append(data[0])
        logger.info(f"Opening all ledgers in region {region}  period {next_month}")
        for key in entities.keys():
            if key in ledgers:
                opening_soap = Open_SOAP(entities[key]["Ledger"], openingp)
                print(opening_soap)
                response = GL_Request(opening_soap)
                print(response.text)
                name = entities[key]["Name"]
                notifications += f"{name} has been opened<br>"
                logger.info(f"{name}have been opened")
        opening_soap = Open_CL_SOAP(cl["00"]["Ledger"], openingp)
        response = GL_Request(opening_soap)
        print(response.text)
        name = entities[key]["Name"]
        notifications += f"{name} have been opened<br>"
        logger.info("Cl have been opened")
        Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
        return notifications
    
    
    