import requests
from email_pdf_AG import acuse_from_AG_REG, acuse_from_AG_REN, envio_agente_recibido, envio_agente_recibido_affect
from getFileDoc import compilePDF_DOCS, getFile
from tools.send_mail import delete_file, enviar
from tools.filing_date import capture_day, capture_full, capture_full_upd
from dataclasses import replace
import json
import time
import psycopg2
from dinapi.sfe import respuesta_sfe_campo, rule_notification
import tools.connect as connex

import aiohttp
import asyncio

from zeep import Client
import tools.connect as conn_serv
from wipo.function_for_reception_in import user_doc_read


#respuesta_sfe_campo('27228')

#getFile('27328','2360799')

#compilePDF_DOCS('2359729')




try:
	mark_service = 'http://192.168.50.194:8050'
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









#body = f'Su solicitud de ESCRITO ha ingresado satisfactoriamente a la Dirección Nacional de Propiedad Intelectual – DINAPI, bajo los siguientes datos:  (se adjunta archivo PDF de su solicitud).\n Seguimos Mejorando para brindarte un servicio de calidad. \n --- \n Saludos cordiales,\n DIRECCIÓN NACIONAL DE PROPIEDAD INTELECTUAL'


#envio_agente_recibido_affect('28423','2370563','2023','2360059')																#Crear PDF
#time.sleep(1)
#delete_file(enviar('notificacion-DINAPI.pdf','agente10as@gmail.com','M.E.A',body))	#Enviar Correo Agente


#acuse_from_AG_REG('S','28429','2370674')

#acuse_from_AG_REN('S','28458','2371908')							# Crear PDF									

#delete_file(enviar('notificacion-DINAPI.pdf','agente10as@gmail.com','M.E.A',connex.msg_body_mail))



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
























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































def campo_scan(arg):
	try:
		list_campos = []
		list_valores = {}
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
			from tramites where formulario_id in (27,28,29,4,70,95,3,100,101,102) and id = {}
		""".format(arg))
		row=cursor.fetchall()
		#print(row[0][6])
		for i in row[0][6]:
			try:
				if i['campo'] == 'titular2_nombreapellido2':
					i['campo'] = 'titular2_nombreapellido'
				
				if i['campo'] != 'descripcion_documentos2':
					list_campos.append({"campo": i["campo"],"valor": i["valor"],"isValId": "true","condicion": "","requerido": "false","componente": "textview","validacion": "","descripcion": i["descripcion"]})			
			
			except Exception as e:
				list_campos.append({"campo": "","valor": "","isValId": "true","condicion": "","requerido": "false","componente": "textview","validacion": "","descripcion": ""})

		connUP = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = connUP.cursor()
		cursor.execute("""UPDATE public.tramites SET  respuestas='{}' WHERE id={};""".format( json.dumps(list_campos), arg))
		cursor.rowcount
		connUP.commit()
		connUP.close()		
	except Exception as e:
		print(e)
	finally:
		conn.close()

	#print(json.dumps(list_campos))
	
	return('true')

def create_list(arg):
	listId = []
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""SELECT id FROM public.tramites WHERE created_at >= '{} 00:59' and formulario_id in (27,28,29,95,4,70,3,100,101,102) and created_at <= '{} 22:59'""".format(arg,arg))
		row=cursor.fetchall()
		for i in row:
			campo_scan(i[0])
			listId.append(i[0])
		return listId
	except Exception as e:
		print(e)
	finally:
		conn.close()	 

def timer(step):
	#print('')
	#reset()
	i = 0
	while i < step:
	##############################################################################################################                
		try:
			create_list(capture_day()) # '2023-08-16'
		except Exception as e:
			pass
	##############################################################################################################
		time.sleep(3)

def reset():
	try:
		connUP = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = connUP.cursor()
		cursor.execute("""UPDATE perfiles_agentes set habilitar='0'""")
		cursor.rowcount
		connUP.commit()
		connUP.close()
	except Exception as e:
		print(e)
	finally:
		connUP.close()

#print(create_list('2023-08-29'))

timer(20000)




















































































































































































































































































































































































































































































































































































































































































































































