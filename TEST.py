import aiohttp
import asyncio
import phonetics
import requests
from email_pdf_AG import acuse_from_AG_REG, acuse_from_AG_REN, envio_agente_recibido, envio_agente_recibido_affect
from getFileDoc import compilePDF_DOCS, getFile, getFile_reg_and_ren
from tools.send_mail import delete_file, enviar
from tools.filing_date import capture_day, capture_full, capture_full_upd
from dataclasses import replace

import json
import time
import psycopg2
from dinapi.sfe import  rule_notification
import tools.connect as connex
import zeep
from zeep import Client
import tools.connect as conn_serv
from wipo.function_for_reception_in import user_doc_read
from wipo.ipas import Process_Read_EventList, fetch_all_user_mark, mark_getlist, mark_read
from cryptography.fernet import Fernet


#respuesta_sfe_campo('27228')

#getFile('27328','2360799')

#compilePDF_DOCS('2359729')




try:
	mark_service = 'http://192.168.50.182:8050'
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')





'''class Ipas():
	
	def File_Read(self, expediente):
		data = {
				"arg0": {
					"fileNbr": {
					"doubleValue": 2362970
					},
					"fileSeq": "PY",
					"fileSeries": {
					"doubleValue": 2023
					},
					"fileType": "M"
				}
				}
		return clientMark.service.FileRead(**data)
	
	def Mark_Update(self,exp):
		data = {
					"fileId": {
					"fileNbr": {
						"doubleValue": "2364446"
					},
					"fileSeq": "PY",
					"fileSeries": {
						"doubleValue": "2023"
					},
					"fileType": "M"
					},
					"filingData": {
					"applicationSubtype": "MS",
					"applicationType": "REG",
					"captureDate": {
						"dateValue": "2023-08-11T12:39:50-04:00"
					},
					"captureUserId": {
						"doubleValue": "26"
					},
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": {
						"dateValue": "2023-08-11T12:39:50-04:00"
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": {
						"doubleValue": "1"
					},
					"novelty1Date": "",
					"novelty2Date": "",
					"paymentList": {
						"currencyName": "Guaraníes",
						"currencyType": "GS",
						"receiptAmount": "206182",
						"receiptDate": {
						"dateValue": "2023-08-11T00:00:00-04:00"
						},
						"receiptNbr": "103398",
						"receiptNotes": "Recibo SprintV2 SFE",
						"receiptType": "1",
						"receiptTypeName": "A1 - Solicitud de Registro de Marca"
					},
					"receptionDate": {
						"dateValue": "2023-08-11T00:00:00-04:00"
					},
					"receptionDocument": {
						"documentEdmsData": {
						"edocDate": {
							"dateValue": "2023-08-11T12:39:51-04:00"
						},
						"edocId": {
							"doubleValue": "2900777"
						},
						"edocImageCertifDate": "",
						"edocImageCertifUser": "",
						"edocImageLinkingDate": "",
						"edocImageLinkingUser": "",
						"edocNbr": {
							"doubleValue": "2364446"
						},
						"edocSeq": "1",
						"edocSer": {
							"doubleValue": "2023"
						},
						"edocTyp": "205",
						"edocTypeName": "Marca de Servicio",
						"efolderId": {
							"doubleValue": "772597"
						},
						"efolderNbr": {
							"doubleValue": "2364446"
						},
						"efolderSeq": "1",
						"efolderSer": {
							"doubleValue": "2023"
						},
						"indInterfaceEdoc": "true",
						"indSpecificEdoc": "true"
						},
						"documentId": {
						"docLog": "E",
						"docNbr": {
							"doubleValue": "656663"
						},
						"docOrigin": "1",
						"docSeries": {
							"doubleValue": "1"
						},
						"selected": ""
						},
						"documentSeqId": {
						"docSeqName": "",
						"docSeqNbr": "",
						"docSeqSeries": "",
						"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
						"dataCodeId1": "",
						"dataCodeId2": "",
						"dataCodeId3": "",
						"dataCodeId4": "",
						"dataCodeId5": "",
						"dataCodeName1": "",
						"dataCodeName2": "",
						"dataCodeName3": "",
						"dataCodeName4": "",
						"dataCodeName5": "",
						"dataCodeTyp1": "",
						"dataCodeTyp2": "",
						"dataCodeTyp3": "",
						"dataCodeTyp4": "",
						"dataCodeTyp5": "",
						"dataCodeTypeName1": "",
						"dataCodeTypeName2": "",
						"dataCodeTypeName3": "",
						"dataCodeTypeName4": "",
						"dataCodeTypeName5": "",
						"dataDate1": "",
						"dataDate2": "",
						"dataDate3": "",
						"dataDate4": "",
						"dataDate5": "",
						"dataFlag1": "false",
						"dataFlag2": "false",
						"dataFlag3": "false",
						"dataFlag4": "false",
						"dataFlag5": "false",
						"dataNbr1": "",
						"dataNbr2": "",
						"dataNbr3": "",
						"dataNbr4": "",
						"dataNbr5": "",
						"dataText1": "",
						"dataText2": "",
						"dataText3": "",
						"dataText4": "",
						"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
						"description": "",
						"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						},
						"refNo": ""
						},
						"outputDocumentData": {
						"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						}
						},
						"qtyPages": ""
					},
					"receptionUserId": "",
					"validationDate": "",
					"validationUserId": ""
					},
					"notes": "",
					"ownershipData": {
					"dummy": "",
					"ownerList": {
						"indService": "true",
						"orderNbr": "",
						"ownershipNotes": "",
						"person": {
						"addressStreet": "Km7. Alto Paraná Ciudad del Este",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "Ciudad del Este",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "Lucasrodrigoojeda86@gmail.com",
						"indCompany": "false",
						"individualIdNbr": "4355368",
						"individualIdType": "CED",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "PY",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "Lucas Rodrigo Ojeda",
						"personNameInOtherLang": "",
						"residenceCountryCode": "PY",
						"stateCode": "",
						"stateName": "",
						"telephone": "994630831",
						"zipCode": ""
						}
					}
					},
					"priorityData": {
					"earliestAcceptedParisPriorityDate": "",
					"exhibitionDate": "",
					"exhibitionNotes": ""
					},
					"processId": {
					"processNbr": {
						"doubleValue": "2044686"
					},
					"processType": "1"
					},
					"publicationData": {
					"journalCode": "",
					"publicationDate": {
						"dateValue": "2023-08-25T00:00:00-04:00"
					},
					"publicationNotes": "nota publicacion",
					"specialPublicationDate": "",
					"specialPublicationRequestDate": ""
					},
					"publicationData": {
					"journalCode": "",
					"publicationDate": "",
					"publicationNotes": "",
					"specialPublicationDate": "",
					"specialPublicationRequestDate": ""
					},
					"registrationData": {
					"entitlementDate": "",
					"expirationDate": "",
					"indRegistered": "false",
					"registrationDate": "",
					"registrationId": {
						"registrationDup": "",
						"registrationNbr": "",
						"registrationSeries": "",
						"registrationType": ""
					}
					},
					"representationData": {
					"documentId_PowerOfAttorneyRegister": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"referencedPOAData": {
						"documentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
						},
						"poaDate": "",
						"poaGrantor": {
						"person": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						}
						},
						"poaRegNumber": "",
						"scope": ""
					},
					"representativeList": {
						"indService": "true",
						"person": {
						"addressStreet": "Lomas Valentinas entre Brasil y Félix Bogado",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": {
							"doubleValue": "7391"
						},
						"cityCode": "",
						"cityName": "Asunción",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "ojedaduartemarcos@gmail.com",
						"indCompany": "true",
						"individualIdNbr": "4405901",
						"individualIdType": "CED",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "PY",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "Marcos Antonio Ojeda Duarte",
						"personNameInOtherLang": "",
						"residenceCountryCode": "PY",
						"stateCode": "",
						"stateName": "",
						"telephone": "982789029",
						"zipCode": ""
						},
						"representativeType": "AG"
					}
					},
					"rowVersion": "",
					"stateValidityData": {
					"dummy": ""
					}
				}
				
		clientMark.service.MarkUpdate(**data)



fileData = Ipas()

#convert = fileData.File_Read('2364446')

convert = fileData.Mark_Update('exp')


print(convert)

primary = []
secondary = []'''



"""SELECT * FROM perfiles_agentes where habilitar = '1'"""


'''
28246/2370699 , 28247/2370690 , 28248/2370684
'''



#body = f'Su solicitud de ESCRITO ha ingresado satisfactoriamente a la Dirección Nacional de Propiedad Intelectual – DINAPI, bajo los siguientes datos:  (se adjunta archivo PDF de su solicitud).\n Seguimos Mejorando para brindarte un servicio de calidad. \n --- \n Saludos cordiales,\n DIRECCIÓN NACIONAL DE PROPIEDAD INTELECTUAL'


#envio_agente_recibido_affect('28423','2370563','2023','2360059')																#Crear PDF
#time.sleep(1)
#delete_file(enviar('notificacion-DINAPI.pdf','agente10as@gmail.com','M.E.A',body))	#Enviar Correo Agente


#acuse_from_AG_REG('S','28246','2370699')

#acuse_from_AG_REN('S','28458','2371908')							# Crear PDF									

#delete_file(enviar('notificacion-DINAPI.pdf','mpuente.dinapi@gmail.com','M.E.A',connex.msg_body_mail))



#rule_notification('ED','2360570')



#print(user_doc_read('E', '2370149', '1', '2023'))


#['filingData']['userdocTypeList'][0]['userdocType']


#Exceute enpoint from url apiRest
def create_groups(url):
	response = requests.get(url)
	if response.status_code == 200: # status de la peticion
		datos = response.json() # respuesta
		for i in datos:
			print(i['solicitante'])
	else:
		print(f'Error {response.status_code}: {response.text}')

#create_groups('http://192.168.50.228:8002/api/post_view?date_post=2023-08-14')


"""async def fetch_data(url):
	async with aiohttp.ClientSession() as apiRest:
		async with apiRest.get(url) as response:
			return await response.text()

async def main():
	try:
		url = "http://192.168.50.228:8077/sis/create_all_group"  # Sustituye con tu URL de API
		response_data = await fetch_data(url)
		print(response_data)
	except Exception as e:
		print('Create groups successfuly')

# Ejecutar el loop de eventos de asyncio
asyncio.run(main())"""







'''
def mark_getlist(fileNbr):
	try:
		MarkGetList = {'arg0': {'criteriaFileId': {'fileNbrFrom': {'doubleValue':fileNbr,},'fileNbrTo': {'doubleValue':fileNbr}},},}
		return clientMark.service.MarkGetList(**MarkGetList)
	except zeep.exceptions.Fault as e:
		return([])	

def mark_read(fileNbr, fileSeq, fileSeries, fileType):
	MarkRead = {'arg0': {'fileNbr': {'doubleValue': fileNbr,},'fileSeq': fileSeq,'fileSeries': {'doubleValue': fileSeries, },'fileType': fileType, }, 'arg1':'?', 'arg2':'?',	}
	#print(clientMark.service.MarkRead(**MarkRead))
	return clientMark.service.MarkRead(**MarkRead)

def fetch_all_user_mark(login):
	query = {
				"arg0": "SELECT USER_ID,LOGIN FROM IP_USER IU where LOGIN='"+login+"'",
				"arg1": {
						"sqlColumnList":[
											{"sqlColumnType": "String", "sqlColumnValue":"LOGIN"},
											{"sqlColumnType": "String", "sqlColumnValue":"USER_ID"},
										]
				}
		}  
	return(clientMark.service.SqlFetchAll(**query))

def Process_Read_EventList(processNbr,processType):
	eventList = {"arg0": {"processNbr": {"doubleValue": processNbr},"processType": processType}}
	return(clientMark.service.ProcessReadEventList(**eventList))
'''


#EDO

class data_insert():

	dataList:str = []

	#CAPTURAMOS PROCESSNBR Y PROCESSTYP
	def mark_data_base(self,exp):
		dataMark = mark_getlist(exp)
		processMark = mark_read(
				dataMark[0]['fileId']['fileNbr']['doubleValue'],
				dataMark[0]['fileId']['fileSeq'],
				dataMark[0]['fileId']['fileSeries']['doubleValue'],
				dataMark[0]['fileId']['fileType']
			)
		#print(processMark)
		if processMark['file']['filingData']['applicationType'] == 'REG':
			self.dataList.append(exp)
			self.dataList.append('549')
		else:
			self.dataList.append(exp)
			self.dataList.append('550')	
		return([processMark['file']['processId']['processNbr']['doubleValue'],processMark['file']['processId']['processType']])

	#DATOS DE USUARIO
	def mark_user(self,userName):
		data = fetch_all_user_mark(userName)
		self.dataList.append(f"{data[0]['sqlColumnList'][1]['sqlColumnValue']}_RE")
		return(f"{data[0]['sqlColumnList'][1]['sqlColumnValue']}_RE") 

	#NUMERO DE CERTIFICACION
	def certifyNbr(self,pNbr:str,pTyp:str):
		data=Process_Read_EventList(pNbr,pTyp)
		print(data)
		for i in range(0,len(data)):
			if data[i]['eventProcessId']['processType'] == 'OFI':
				self.dataList.append(data[i]['eventProcessId']['processNbr']['doubleValue'])
				return([
						data[i]['eventProcessId']['processNbr']['doubleValue'],
						data[i]['eventProcessId']['processType']
					])

	def send_order(self,exp:str,usr:str,orden:str,cert:str):
		url = f"http://192.168.50.228:10005/publicaciones/enviarOrdenesPublicacion/enviar/ordenPublicacion?nroExpediente={exp}&usuario={usr}&ordenPublicacion={orden}&nroCertificacion={cert}"  # Sustituye con tu URL de API
		#print(url)
		response = requests.get(url)
		if response.status_code == 200: # status de la peticion
			datos = response.json() # respuesta
			#print(datos)



testForCorrectionData = data_insert()

listExp = [2319725]

for i in listExp:
	testForCorrectionData.dataList = []
	proceso = testForCorrectionData.mark_data_base(i)
	usuario = testForCorrectionData.mark_user('RBEJARANO')
	certificacion = testForCorrectionData.certifyNbr(proceso[0],proceso[1])
	print(testForCorrectionData.dataList)

testForCorrectionData.send_order(testForCorrectionData.dataList[0],testForCorrectionData.dataList[2],testForCorrectionData.dataList[1],testForCorrectionData.dataList[3])



##CONEXION A SFE POSGRESSQL 14 (TODAVIA NO ME FUNCIONA)
def respuesta_sfe_campo(arg):
	try:
		list_campos = []
		list_valores = {}
		conn = psycopg2.connect(host="db-sfe-beta.dinapi.gov.py",database="db_sfe_development",user="user-sfe",password="sfe-201901!")
		cursor = conn.cursor()
		cursor.execute("""select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
			from tramites where expediente_electronico = true and id = {}
		""".format(arg))
		row=cursor.fetchall()
		list_valores['id'] = row[0][0]
		list_valores['fecha'] = row[0][1]
		list_valores['formulario_id'] = row[0][2]
		list_valores['estado'] = row[0][3]
		list_valores['created_at'] = str(row[0][4])
		list_valores['updated_at'] = str(row[0][5])
		list_valores['costo'] = str(row[0][7])
		list_valores['usuario_id'] = str(row[0][8])
		list_valores['codigo'] = str(row[0][10])
		list_valores['expediente_id'] = str(row[0][13])
		list_valores['firmado_at'] = str(row[0][11])
		list_valores['pagado_at'] = str(row[0][12])
		list_valores['enviado_at'] = str(row[0][15])
		list_valores['expediente_afectado'] = str(row[0][19])
		list_valores['tipo_documento_id'] = str(row[0][25])
		for i in range(0,len(row[0][6])):
			list_campos.append(row[0][6][i]['campo'])
		
		print(" ")
		print(f'[[[[[[[Lista de campos correspondiente al ID {arg}]]]]]]]]]')
		#print(list_campos)

		#print(" ")
		#print('(((((((((]Lista de valores[)))))))))')
		for item in range(0,len(list_campos)):
			for x in list_campos:
				if row[0][6][item]['campo'] == x:
					try:
						#print(row[0][6][item]['valor'])
						list_valores[x] = row[0][6][item]['valor']
					except Exception as e:
						#print(row[0][6][item]['valor'])
						list_valores[x] = ''
	except Exception as e:
		print(e)
	finally:
		conn.close()

	return(list_valores)

#print(respuesta_sfe_campo('28694'))




'''
# Parámetros de conexión
conexion = psycopg2.connect(
    host="db-sfe-beta.dinapi.gov.py",
    database="db_sfe_development",
    user="user-sfe",
    password="sfe-201901!")

# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

# Ejemplo de consulta
cursor.execute("SELECT id FROM tramites")

# Obtener los resultados
resultados = cursor.fetchall()

# Imprimir los resultados
for fila in resultados:
    print(fila)

# Cerrar la conexión y el cursor
cursor.close()
conexion.close()
'''



'''
#Fecha y Hora con retraso de 3 días
from datetime import datetime, timedelta

fecha_hora_actual = datetime.now()
fecha_hora_ajustada = fecha_hora_actual - timedelta(hours=3)
fecha_hora_formateada = fecha_hora_ajustada.strftime("%d/%m/%Y %H:%M")

print(fecha_hora_formateada)
'''

##############################################################################################################################

# BUSQUEDA FONETICA
#word1 = "Alfonso"
#word2 = "Alphonzo"
	# Usando Soundex
#soundex_word1 = phonetics.soundex(word1)
#soundex_word2 = phonetics.soundex(word2)
#print(f"{word1}: {soundex_word1}")
#print(f"{word2}: {soundex_word2}")
#print("similar" if soundex_word1 == soundex_word2 else "no similar")




##############################################################################################################################


# Generar una clave secreta para Fernet
def generar_clave():
    return Fernet.generate_key()

# Encriptar un mensaje
def encriptar(mensaje, clave):
    f = Fernet(clave)
    return f.encrypt(mensaje.encode())

# Desencriptar un mensaje
def desencriptar(mensaje_encriptado, clave):
    f = Fernet(clave)
    return f.decrypt(mensaje_encriptado).decode()

## Uso de las funciones
#clave = generar_clave()
#print(f"Clave: {clave}")

#mensaje_original = "Hola Mundo"
#mensaje_encriptado = encriptar(mensaje_original, clave)
#print(f"Mensaje encriptado: {mensaje_encriptado}")

#mensaje_desencriptado = desencriptar(mensaje_encriptado, clave)
#print(f"Mensaje desencriptado: {mensaje_desencriptado}")


##############################################################################################################################




