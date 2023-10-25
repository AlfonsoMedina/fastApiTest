
from ast import Num
from tools.data_format import date_not_hour
from email_pdf_AG import acuse_from_AG_REG, acuse_from_AG_REN, envio_agente_recibido, envio_agente_recibido_affect, registro_pdf_con_acuse
from getFileDoc import compilePDF_DOCS, getFile, getFile_reg_and_ren
from dinapi.sfe import pendiente_sfe, registro_sfe, renovacion_sfe, respuesta_sfe_campo, rule_notification, titulare_reg
from tools.send_mail import delete_file, enviar
from tools.filing_date import capture_day, capture_full, capture_full_upd
from dataclasses import replace
import tools.connect as connex
import psycopg2
from cryptography.fernet import Fernet
import time
import asyncio
import configparser
import httpx
from wipo.insertGroupProcessMEA import group_addressing
from wipo.ipas import getPoder, mark_getlistFecha
import logging as logs

import os



####################################################################################################################################
####################################################################################################################################
########################################## CONSULTA PASSWORD SERVICE ###############################################################
####################################################################################################################################
####################################################################################################################################

"""
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
"""
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



# EJECUTAR CONSULTAS 29486 29553
def queryfind():
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""SELECT id,expediente_id,estado FROM tramites where estado in (7,99) and expediente_electronico = true and enviado_at >= '2023-10-23'; """)
		row=cursor.fetchall()
		print(row)
		for i in row:
			return(i)	
	except Exception as e:
		print(e)
	finally:
		conn.close()
"""
SELECT id, expediente_id, formulario_id, estado  FROM tramites where estado = 7 and expediente_electronico = true and enviado_at >= '2023-10-03';"""
#queryfind()

#print(respuesta_sfe_campo('30219'))

#registro_pdf_con_acuse('30278')


"""tituPck = []
for i in range(len(titulare_reg('30031','5'))):
	if titulare_reg('30031','5')[i]['person']['personName'] != '':
		tituPck.append(titulare_reg('30031','5')[i])
	else:
		pass

print(tituPck)"""



#VERIFICAR CAMPOS EN RESPUESTA DE LA TABLA TRAMITES
#print(respuesta_sfe_campo('29386'))



#getFile('29386','2380107')




#EJECUTAR ESTA ACCION SI ES 99 PERO NO ESTA EN LISTA DE ERRORES
def cambio_estado(estado):
	try:
		connA = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursorA = connA.cursor()
		cursorA.execute("""select * from tramites where estado = {}""".format(estado))
		row=cursorA.fetchall()
		for i in row:
			conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
			cursor = conn.cursor()
			cursor.execute("""UPDATE public.tramites set estado = 99  WHERE estado = {};""".format(estado))
			cursor.rowcount
			conn.commit()
			conn.close()
	except Exception as e:
		print(e)
	finally:
		connA.close()

#cambio_estado('99')




# CONSULTAR DATOS DE RENOVACION POR ID TRAMITE
#print(renovacion_sfe('29146')['expediente'])




#####################################################################################################################
############## REGISTRAR ID DE TRAMITE EN LOG DE PROCESO ############################################################
#####################################################################################################################
#####################################################################################################################

# Configurar el nivel de registro
#LOG_FILENAME = f'logs/app_mea_{date_not_hour()}.log'
#logs.basicConfig(filename=LOG_FILENAME,level=logs.INFO)

def test():
	# Ejemplo de uso de los logs
	logs.info('2777')
	
#test()


###########################################################################
############# Buscador para saber si ya fue procesado un ID ###############
################ Guardado en el archivo log de procesos ###################
###########################################################################
def ifExistId(findId):
	archivo = open(f"logs/app_mea_{date_not_hour()}.log", "r")  # Abrir el archivo en modo lectura
	contenido = archivo.read()  # Leer el contenido del archivo
	archivo.close()  # Cerrar el archivo

	palabra_buscar = f"root:{findId}"
	ocurrencias = contenido.count(palabra_buscar)  # Contar las ocurrencias de la palabra

	return(f"La palabra '{palabra_buscar}' se encontró {ocurrencias} veces en el archivo.")

#print(ifExistId('2777'))

###########################################################################
################### ELIMINAR UN REGISTRO DE LISTA DE PROCESOS #############
###########################################################################

def delete_id_file(nombre_archivo, palabra):
	with open(nombre_archivo, 'r') as archivo:
		contenido = archivo.read()
		contenido_modificado = contenido.replace(f'INFO:root:{palabra}', '')

	with open(nombre_archivo, 'w') as archivo:
		archivo.write(contenido_modificado)

#delete_id_file(f'logs/app_mea_{date_not_hour()}.log', '2777')


###########################################################################
####################BUSCAR SI EXISTE LOG DEL ERROR 99######################
###########################################################################

query_error ="SELECT id_tramite FROM public.log_error where evento = 'E00' and id_tramite ="

def data_validator(arg:str):
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(f"""{query_error} {arg}; """)
		row=cursor.fetchall()
		for i in range(0,len(row)):
			print(row[i][0])			
	except Exception as e:
		print(e)
	finally:
		conn.close()

#data_validator('29239')


def logging_me(arg0,arg1):
	# Configurar el nivel de registro y el archivo de salida
	logs.basicConfig(filename=arg0, level=logs.DEBUG)

	# Capturar todos los registros en el archivo
	logs.captureWarnings(True)

	# Ejemplo de uso de los logs
	#logs.debug('Este es un mensaje de debug')
	logs.info(arg1)
	#logs.warning('Este es un mensaje de advertencia')
	#logs.error('Este es un mensaje de error')
	#logs.critical('Este es un mensaje crítico')

#logging_me('log_File1.log','Este es un mensaje informativo 2023')




# INICIO DE PROCESO DE VALIDACION POR MARCAS DUPLICADAS

def check_mark_ipas(fecha:str,desc:str,tipoM:str,subTipoM:str,claseM:str):
	#METODO DE CONSULTA A IPAS
	dataList = mark_getlistFecha(fecha, fecha)

	# RECORRER RESULTADO DE dataList 
	for i in range(0,len(dataList)):

		# DATOS A EVALUAR
		tipo = dataList[i]['filingData']['applicationType']
		subTipo = dataList[i]['filingData']['applicationSubtype']
		clase = str(dataList[i]['fileSummaryClasses'])[16:18]
		descript = dataList[i]['fileSummaryDescription']
		#print(descript)
		#print(f'{descript} == {desc} {str(tipo).strip()} == {str(tipoM).strip()}  {str(subTipo).strip()} == {str(subTipoM).strip()}  {str(clase).strip()} == {str(claseM).strip()}')
		
		# CONDICIONAL QUE CONFIRMARA SI EXISTE
		if str(descript).strip() == str(desc).strip() and str(tipoM).strip() == str(tipo).strip() and str(subTipo).strip() == str(subTipoM).strip() and str(clase).strip() == str(claseM).strip():
			return(True)


#print(check_mark_ipas('2023-10-06','AUTOMAX','REG','MP','12'))



#print(respuesta_sfe_campo('29553')['observacion_documentos'])





"""
intentos:Num = 5
for i in range(intentos):
	try:
		if i == 4:
			print('Cuarta iteracion ==> ok')
			break  # Si la función se ejecuta correctamente, salir del bucle
		print(f'Iteracion {i}')
	except Exception as e:
		print(f"Error en el intento {i+1}: {str(e)}")
	time.sleep(1)
else:
	print("Se ha alcanzado el máximo número de intentos sin éxito")
	
"""



"""
class magazine_redpi():
	
	def __init__(self) -> None:
		pass

	def pages(self,arg:str):
		carpeta = f'revistas/{arg}'
		archivos = os.listdir(carpeta)
		archivos = [archivo for archivo in archivos if os.path.isfile(os.path.join(carpeta, archivo))]
		return(archivos)

	def folders(self,arg:str):
		carpeta = arg
		elementos = os.listdir(carpeta)
		carpetas = [elemento for elemento in elementos if os.path.isdir(os.path.join(carpeta, elemento))]
		return(carpetas)

	def editions(self):
		edit_list = []
		folder = self.folders('revistas')
		for i in range(len(folder)):
			edit_dataill = {}
			urls = []
			edit_dataill['edicion'] = folder[i]
			for x in self.pages(folder[i]):
				urls.append(f'/pagina/{folder[i]}/{x}')
			edit_dataill['paginas'] = urls
			edit_list.append(edit_dataill)
		return(edit_list)

revistas = magazine_redpi()

print(revistas.editions())
"""




#Reenviar correo con acuse
#acuse_from_AG_REG('S','30278','2386574')

#delete_file(enviar('notificacion-DINAPI.pdf','email','M.E.A',connex.msg_body_mail))



iteraciones = 5

for i in range(iteraciones):
    print("Iteración", i+1)
    time.sleep(2)
    print("Pausa de 2 segundos")

print("Finalizado")