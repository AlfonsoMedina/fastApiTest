
from email_pdf_AG import acuse_from_AG_REG, acuse_from_AG_REN, envio_agente_recibido, envio_agente_recibido_affect
from getFileDoc import compilePDF_DOCS, getFile, getFile_reg_and_ren
from tools.send_mail import delete_file, enviar
from tools.filing_date import capture_day, capture_full, capture_full_upd
from dataclasses import replace
import tools.connect as connex
import psycopg2
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
#print(maping_data()['PUBLICACIONES'])

#expediente_id = null and and formulario_id in (3,4,27,100,101) and enviado_at >= '2023-09-27 00:59:59' and  expediente_electronico = true and enviado_at <= '2023-09-27 23:59:59' order by enviado_at asc

def cambio_():
	try:
		connA = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursorA = connA.cursor()
		cursorA.execute("""select id from tramites where expediente_id = 2378490 """)
		row=cursorA.fetchall()
		for i in row:
			print(i)
	except Exception as e:
		print(e)
	finally:
		connA.close()


#cambio_()





def cambio_estadoXXXXXX(estado):
	try:
		connA = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursorA = connA.cursor()
		cursorA.execute("""select * from tramites where expediente_id = {}""".format(estado))
		row=cursorA.fetchall()
		for i in row:
			print(i)

	except Exception as e:
		print(e)
	finally:
		connA.close()

#print(cambio_estadoXXXXXX('2378663'))



# CONSULTAR LISTA DE ERRORES SI EXISTE SOPORTE
"""
?
"""
#EGECUTAR ESTA ACCION SI ES 99 PERO NO ESTA EN LISTA DE ERRORES
def cambio_estado(estado):
	try:
		connA = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursorA = connA.cursor()
		cursorA.execute("""select * from tramites where estado = {}""".format(estado))
		row=cursorA.fetchall()
		for i in row:
			conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
			cursor = conn.cursor()
			cursor.execute("""UPDATE public.tramites set estado = 8 WHERE estado = {};""".format(estado))
			cursor.rowcount
			conn.commit()
			conn.close()
	except Exception as e:
		print(e)
	finally:
		connA.close()

#cambio_estado('99')

