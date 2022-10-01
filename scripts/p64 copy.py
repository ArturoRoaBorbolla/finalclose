import os
import sys
import logzero
import zipfile
import datetime
from finalclosefunctions import *


def P6Bot4(data):
    try:
        logger.info("Trying to get entities")
        entities = get_entities("priandsub")
    except:
        logger.info("Error on get entities")
        Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
        return "Error on getting entities"
    period,region = data.split(",")
    region=region.upper()
    logger.info(f"Reading status for region {region} and period {period}")
    Period = period.strip()
    Month, Year = Period.split("-")
    current_month = months[int(Month) - 1]
    year_two_digits = str(Year[-2:])
    Period = f"{current_month}-{year_two_digits}"
    status_string = ""
    logger.info(f"Opening file to read data about ledgers")
    try:
        with open(f"{general_data_path}\\priandsub.txt","r") as ledger_config:
            ledger_list=ledger_config.read().splitlines()
    except:
        logger.info("Error on opening config file")
        Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
        return "Error on Opening file to read data about regions"
    else:
        ledgers=[]
        logger.info(f"Splitting data to compare with region {region}")
        for i in ledger_list:
            data = i.split(",")
            if data[2]==region:
                ledgers.append(data[0])
        logger.info(f"For each ledger in region get the status")
        for key in entities.keys():
            if key in ledgers:
                status_string += Get_L_Status(Period,entities[key]["Ledger"],entities[key]["Name"]) + "<BR>"
        Push_To_S3(f"{logs_path}\\log.log","Process6","Log")
        return status_string
   