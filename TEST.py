
from email_pdf_AG import acuse_from_AG_REG, acuse_from_AG_REN, envio_agente_recibido, envio_agente_recibido_affect
from getFileDoc import compilePDF_DOCS, getFile, getFile_reg_and_ren
from tools.send_mail import delete_file, enviar
from tools.filing_date import capture_day, capture_full, capture_full_upd
from dataclasses import replace


from cryptography.fernet import Fernet

import asyncio
import configparser
import httpx

###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################


####################################################################################################################################
####################################################################################################################################
########################################## CONSULTA PASSWORD SERVICE ###############################################################
####################################################################################################################################
####################################################################################################################################


## CAPTURE ENVIRONMENT VARIABLES
config = configparser.ConfigParser()
config.read('config.ini')
app_name = config['general']['app_name']
version = config['general']['version']
tokenApp = config['general']['tokenApp']
urlBase = config['general']['url']

## CREATE DICTIONARIES TO STORE CONNECTIONS
getThisConn = {}
getItemConn = {}

## FUNCTION THAT CONSULTS THE DATA ACCESS SERVICE
async def consultar_api(appName:str, tokenApp:str):
    url = f"{urlBase}?appName={appName}&tokenApp={tokenApp}"
    async with httpx.AsyncClient() as client:
        response = await client.post(url)
        if response.status_code == 200:
            data = response.json()
            return(data)
        else:
            print("Error al consultar la API:", response.status_code)
            return([])

loop = asyncio.get_event_loop()
getConnects = loop.run_until_complete(consultar_api(app_name,tokenApp))

## I MAP THE ANSWER IN THE DICTIONARIES
def maping_data():
    for i in getConnects:
        getThisConn[i['connName']] = i
    return(getThisConn) 
    

####################################################################################################################################
####################################################################################################################################
########################################## CONSULTA PASSWORD SERVICE ###############################################################
####################################################################################################################################
####################################################################################################################################


#IMPORTAR
#from tools.service_system import connectsDAO as connectsDAO

#DECLARAR
print(maping_data()['PUBLICACIONES'])


