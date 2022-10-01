import sys
from finalclosefunctions import *

def openp(period):
    regions = ["EMEA","APAC","AMER_NON_US","AMER_US"]
    for region in regions:
        notifications = ""
        entities = get_entities("priandsub")
        cl = get_entities("cl")
        with open(f"{general_data_path}\\priandsub.txt","r") as ledger_config:
            ledger_list=ledger_config.read().splitlines()
        ledgers=[]
        #logger.info(f"Splitting data to compare with region {region}")
        for i in ledger_list:
            data = i.split(",")
            #if data[2]==region:
            ledgers.append(data[0])
        logger.info(f"Opening all ledgers in region {region} on period {period}")
        for key in entities.keys():
            if key in ledgers:
                opening_soap = Open_SOAP(entities[key]["Ledger"], period)
                print(opening_soap)
                response = GL_Request(opening_soap)
                print(response.text)
                name = entities[key]["Name"]
                notifications += f"{name} has been opened<br>"
                logger.info(f"{name}have been opened")
        opening_soap = Open_CL_SOAP(cl["00"]["Ledger"], period)
        response = GL_Request(opening_soap)
        print(response.text)
        name = entities[key]["Name"]
        notifications += f"{name} have been opened<br>"
        logger.info("Cl have been opened")
        print(notifications)