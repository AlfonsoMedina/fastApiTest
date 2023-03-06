from urllib import request
from fastapi import FastAPI
from pydantic import BaseModel
from publicaciones.pub_2023 import convert_fecha_hora, orden_emitida, orden_emitida_exp
from wipo.ipas import Insert_Action, fetch_all_do_edoc_nuxeo, fetch_all_officdoc_nuxeo, get_agente, mark_getlist, mark_getlistReg #pip install "fastapi[all]"
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

description = """
Version 2023 

## Métodos para consultar e insertar eventos de Orden de Publicación
 
Engineer in charge ***W. Alfonso Medina***

las rutas reciben un objeto **JSON** como parametro y retornar un objeto **JSON**.
"""

app = FastAPI()

origins = ["*"]

#http://192.168.71.189:3000 //bloqueo por aplicacion

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["POST"], #['*']
	allow_headers=["*"],
)

def custom_openapi():
	if app.openapi_schema:
		return app.openapi_schema
	openapi_schema = get_openapi(
		title="Api Publicaciones",
		version="3.0.0",
		description=description,
		routes=app.routes,
	)
	openapi_schema["info"]["x-logo"] = {
		"url": "https://sfe.dinapi.gov.py/assets/logo_sprint-85d552f35942e4152f997bb4875b6283a05d34f7b9b7b6126e84414c924bb041.png"
	}
	app.openapi_schema = openapi_schema
	return app.openapi_schema

#https://sfe.dinapi.gov.py/assets/home/dinapilogo4-5eef9860ea6bb48707a76c1d97e2438b195bd72171233946a40177bb27cc7f11.png	
#https://sfe.dinapi.gov.py/assets/logo_sprint-85d552f35942e4152f997bb4875b6283a05d34f7b9b7b6126e84414c924bb041.png


@app.post('/api/markgetlist', tags=["MarkGetList por expediente"], summary="#", description="Consulta una marca por su numero de expediente, devuelve parametros utiles para otros metodos")
async def mark_get_list(exp: str):
	try:
		for x in mark_getlist(exp):
			respuesta = {
						'fileIdAsString':x['fileIdAsString'],
						'fileId':x['fileId']['fileNbr']['doubleValue'], 
						'fileSeq':x['fileId']['fileSeq'], 
						'fileSeries':x['fileId']['fileSeries']['doubleValue'], 
						'fileType':x['fileId']['fileType'],
						'fileSummaryOwner':x['fileSummaryOwner'],
						'fileSummaryDescription':x['fileSummaryDescription']}	
		return (respuesta)
	except Exception as e:
		return ({'res':''})

class publicacion_Emision(BaseModel):
	fecha:str = ""
	user_id: str = ""
@app.post('/api/orden_pub_emitida', description="Devuelve los expedientes con los eventos 549, 550, 560, en funcion de una fecha  **(2022-12-19)** y id de usuario **(89)** ", tags=["Consulta los eventos Emisión Orden Publicación, 2da. Emisión Orden Publicación e Informe de renovación por fecha y id de usuario"])
async def Emisión_Orden_Publicacion(item: publicacion_Emision):#{"fecha":"2022-12-19","user_id":"89"}
	catch_exp = []
	obj_dat = orden_emitida(item.fecha,item.user_id)
	for i in range(0,len(obj_dat)):
		if obj_dat[i].lastActionName == 'Emisión Orden Publicación' or obj_dat[i].lastActionName == '2da. Emisión Orden Publicación' or obj_dat[i].lastActionName == 'Informe de renovación':
			try:
				documentId = {
									'docLog': str(obj_dat[i].documentId.docLog),
									'docNbr': {
										'doubleValue': str(obj_dat[i].documentId.docNbr.doubleValue)
									},
									'docOrigin': str(obj_dat[i].documentId.docOrigin),
									'docSeries': {
										'doubleValue': str(obj_dat[i].documentId.docSeries.doubleValue)
									},
									'selected': str(obj_dat[i].documentId.selected)
								}
			except Exception as e:
				documentId = {
								'docLog': '',
								'docNbr': '',
								'docOrigin': '',
								'docSeries': '',
								'selected': ''
							}
			try:
				officedocId = {
									'offidocNbr': {
										'doubleValue': str(obj_dat[i].officedocId.offidocNbr.doubleValue)
									},
									'offidocOrigin': str(obj_dat[i].officedocId.offidocOrigin),
									'offidocSeries': {
										'doubleValue': str(obj_dat[i].officedocId.offidocSeries.doubleValue)
									},
									'selected': str(obj_dat[i].officedocId.selected)
								}
			except Exception as e:
				officedocId = {
				'offidocNbr': '',
				'offidocOrigin': '',
				'offidocSeries': '',
				'selected': ''
			}
			try:
				upperProcessId = {
									'processNbr': {
										'doubleValue': str(obj_dat[i].upperProcessId.processNbr.doubleValue)
									},
									'processType': str(obj_dat[i].upperProcessId.processType)
								}
			except Exception as e:
				upperProcessId = {
				'processNbr': '',
				'processType': ''
			}	
			catch_exp.append(
								{
								'creationDate': {
									'dateValue': str(obj_dat[i].creationDate.dateValue)
								},
								'description': str(obj_dat[i].description),
								'documentId': documentId,
								'dueDate': str(obj_dat[i].dueDate),
								'indTopFileMark': str(obj_dat[i].indTopFileMark),
								'indTopMarkPatent': str(obj_dat[i].indTopMarkPatent),
								'lastActionName': str(obj_dat[i].lastActionName),
								'lastActionUsername': str(obj_dat[i].lastActionUsername),
								'officedocId': officedocId,
								'officedocTypeName': str(obj_dat[i].officedocTypeName),
								'processId': {
									'processNbr': {
										'doubleValue': str(int(obj_dat[i].processId.processNbr.doubleValue))
									},
									'processType': str()
								},
								'processIdAsString': str(obj_dat[i].processIdAsString),
								'relatedToWorkcode': {
									'doubleValue': str(obj_dat[i].relatedToWorkcode.doubleValue)
								},
								'responsibleUserName': str(obj_dat[i].responsibleUserName),
								'statusDate': {
									'dateValue': convert_fecha_hora(str(obj_dat[i].statusDate.dateValue))
								},
								'statusName': str(obj_dat[i].statusName),
								'topFileDescription': str(obj_dat[i].topFileDescription),
								'topFileFilingDate': {
									'dateValue': str(obj_dat[i].topFileFilingDate.dateValue)
								},
								'topFileId': {
									'fileNbr': {
										'doubleValue': str(int(obj_dat[i].topFileId.fileNbr.doubleValue))
									},
									'fileSeq': str(obj_dat[i].topFileId.fileSeq),
									'fileSeries': {
										'doubleValue': str(obj_dat[i].topFileId.fileSeries.doubleValue)
									},
									'fileType': str(obj_dat[i].topFileId.fileType)
								},
								'topFileOwner': str(obj_dat[i].topFileOwner),
								'topFileRegistrationId': {
									'registrationDup': str(obj_dat[i].topFileRegistrationId.registrationDup),
									'registrationNbr': str(obj_dat[i].topFileRegistrationId.registrationNbr),
									'registrationSeries': str(obj_dat[i].topFileRegistrationId.registrationSeries),
									'registrationType': str(obj_dat[i].topFileRegistrationId.registrationType)
								},
								'topFileStatusName': str(obj_dat[i].topFileStatusName),
								'topProcessId': {
									'processNbr': {
										'doubleValue': str(int(obj_dat[i].topProcessId.processNbr.doubleValue))
									},
									'processType': str(obj_dat[i].topProcessId.processType)
								},
								'upperProcessId': upperProcessId,
								'userdocSeqName': str(obj_dat[i].userdocSeqName),
								'userdocSeqNbr': str(obj_dat[i].userdocSeqNbr),
								'userdocSeqSeries': str(obj_dat[i].userdocSeqSeries),
								'userdocSeqType': str(obj_dat[i].userdocSeqType),
								'userdocTypeName': str(obj_dat[i].userdocTypeName),
								'workflowWarningText': str(obj_dat[i].workflowWarningText)
							})
	return(catch_exp)

class primera_emicion(BaseModel):
	fileNbr:str = ""
	fileSeq: str = ""
	fileSeries: str = ""
	fileType: str = ""
@app.post('/api/orden_pub_emitida_exp', tags=["Consulta el evento Emisión Orden Publicación por expediente"])
async def Emisión_Orden_Publicacion(item: primera_emicion):
	catch_exp = []
	obj_dat = orden_emitida_exp(item.fileNbr,item.fileSeq,item.fileSeries,item.fileType)
	for i in range(0,len(obj_dat)):
		if obj_dat[i].lastActionName == 'Emisión Orden Publicación':
			try:
				documentId = {
									'docLog': str(obj_dat[i].documentId.docLog),
									'docNbr': {
										'doubleValue': str(obj_dat[i].documentId.docNbr.doubleValue)
									},
									'docOrigin': str(obj_dat[i].documentId.docOrigin),
									'docSeries': {
										'doubleValue': str(obj_dat[i].documentId.docSeries.doubleValue)
									},
									'selected': str(obj_dat[i].documentId.selected)
								}
			except Exception as e:
				documentId = {
								'docLog': '',
								'docNbr': '',
								'docOrigin': '',
								'docSeries': '',
								'selected': ''
							}
			try:
				officedocId = {
									'offidocNbr': {
										'doubleValue': str(obj_dat[i].officedocId.offidocNbr.doubleValue)
									},
									'offidocOrigin': str(obj_dat[i].officedocId.offidocOrigin),
									'offidocSeries': {
										'doubleValue': str(obj_dat[i].officedocId.offidocSeries.doubleValue)
									},
									'selected': str(obj_dat[i].officedocId.selected)
								}
			except Exception as e:
				officedocId = {
				'offidocNbr': '',
				'offidocOrigin': '',
				'offidocSeries': '',
				'selected': ''
			}
			try:
				upperProcessId = {
									'processNbr': {
										'doubleValue': str(obj_dat[i].upperProcessId.processNbr.doubleValue)
									},
									'processType': str(obj_dat[i].upperProcessId.processType)
								}
			except Exception as e:
				upperProcessId = {
				'processNbr': '',
				'processType': ''
			}	
			catch_exp.append(
								{
								'creationDate': {
									'dateValue': str(obj_dat[i].creationDate.dateValue)
								},
								'description': str(obj_dat[i].description),
								'documentId': documentId,
								'dueDate': str(obj_dat[i].dueDate),
								'indTopFileMark': str(obj_dat[i].indTopFileMark),
								'indTopMarkPatent': str(obj_dat[i].indTopMarkPatent),
								'lastActionName': str(obj_dat[i].lastActionName),
								'lastActionUsername': str(obj_dat[i].lastActionUsername),
								'officedocId': officedocId,
								'officedocTypeName': str(obj_dat[i].officedocTypeName),
								'processId': {
									'processNbr': {
										'doubleValue': str(int(obj_dat[i].processId.processNbr.doubleValue))
									},
									'processType': str()
								},
								'processIdAsString': str(obj_dat[i].processIdAsString),
								'relatedToWorkcode': {
									'doubleValue': str(obj_dat[i].relatedToWorkcode.doubleValue)
								},
								'responsibleUserName': str(obj_dat[i].responsibleUserName),
								'statusDate': {
									'dateValue': convert_fecha_hora(str(obj_dat[i].statusDate.dateValue))
								},
								'statusName': str(obj_dat[i].statusName),
								'topFileDescription': str(obj_dat[i].topFileDescription),
								'topFileFilingDate': {
									'dateValue': str(obj_dat[i].topFileFilingDate.dateValue)
								},
								'topFileId': {
									'fileNbr': {
										'doubleValue': str(int(obj_dat[i].topFileId.fileNbr.doubleValue))
									},
									'fileSeq': str(obj_dat[i].topFileId.fileSeq),
									'fileSeries': {
										'doubleValue': str(obj_dat[i].topFileId.fileSeries.doubleValue)
									},
									'fileType': str(obj_dat[i].topFileId.fileType)
								},
								'topFileOwner': str(obj_dat[i].topFileOwner),
								'topFileRegistrationId': {
									'registrationDup': str(obj_dat[i].topFileRegistrationId.registrationDup),
									'registrationNbr': str(obj_dat[i].topFileRegistrationId.registrationNbr),
									'registrationSeries': str(obj_dat[i].topFileRegistrationId.registrationSeries),
									'registrationType': str(obj_dat[i].topFileRegistrationId.registrationType)
								},
								'topFileStatusName': str(obj_dat[i].topFileStatusName),
								'topProcessId': {
									'processNbr': {
										'doubleValue': str(obj_dat[i].topProcessId.processNbr.doubleValue)
									},
									'processType': str(obj_dat[i].topProcessId.processType)
								},
								'upperProcessId': upperProcessId,
								'userdocSeqName': str(obj_dat[i].userdocSeqName),
								'userdocSeqNbr': str(obj_dat[i].userdocSeqNbr),
								'userdocSeqSeries': str(obj_dat[i].userdocSeqSeries),
								'userdocSeqType': str(obj_dat[i].userdocSeqType),
								'userdocTypeName': str(obj_dat[i].userdocTypeName),
								'workflowWarningText': str(obj_dat[i].workflowWarningText)
							})
	return(catch_exp)

class segunda_emicion(BaseModel):
	fileNbr:str = ""
	fileSeq: str = ""
	fileSeries: str = ""
	fileType: str = ""
@app.post('/api/orden_pub_2da_emitida_exp', tags=["Consulta el evento 2da. Emisión Orden Publicación por expediente"])
async def Emision_2da__Orden_Publicacion(item: segunda_emicion):
	catch_exp = []
	obj_dat = orden_emitida_exp(item.fileNbr,item.fileSeq,item.fileSeries,item.fileType)
	for i in range(0,len(obj_dat)):
		if obj_dat[i].lastActionName == '2da. Emisión Orden Publicación':
			try:
				documentId = {
								'docLog': str(obj_dat[i].documentId.docLog),
								'docNbr': {
									'doubleValue': str(obj_dat[i].documentId.docNbr.doubleValue)
								},
								'docOrigin': str(obj_dat[i].documentId.docOrigin),
								'docSeries': {
									'doubleValue': str(obj_dat[i].documentId.docSeries.doubleValue)
								},
								'selected': str(obj_dat[i].documentId.selected)
							}
			except Exception as e:
				documentId = {
							'docLog': '',
							'docNbr': '',
							'docOrigin': '',
							'docSeries': '',
							'selected': ''
						}
			try:
				officedocId = {
								'offidocNbr': {
									'doubleValue': str(obj_dat[i].officedocId.offidocNbr.doubleValue)
								},
								'offidocOrigin': str(obj_dat[i].officedocId.offidocOrigin),
								'offidocSeries': {
									'doubleValue': str(obj_dat[i].officedocId.offidocSeries.doubleValue)
								},
								'selected': str(obj_dat[i].officedocId.selected)
							}
			except Exception as e:
				officedocId = {
			'offidocNbr': '',
			'offidocOrigin': '',
			'offidocSeries': '',
			'selected': ''
		}
			try:
				upperProcessId = {
								'processNbr': {
									'doubleValue': str(obj_dat[i].upperProcessId.processNbr.doubleValue)
								},
								'processType': str(obj_dat[i].upperProcessId.processType)
							}
			except Exception as e:
				upperProcessId = {
			'processNbr': '',
			'processType': ''
		}	
			catch_exp.append(
								{
								'creationDate': {
									'dateValue': str(obj_dat[i].creationDate.dateValue)
								},
								'description': str(obj_dat[i].description),
								'documentId': documentId,
								'dueDate': str(obj_dat[i].dueDate),
								'indTopFileMark': str(obj_dat[i].indTopFileMark),
								'indTopMarkPatent': str(obj_dat[i].indTopMarkPatent),
								'lastActionName': str(obj_dat[i].lastActionName),
								'lastActionUsername': str(obj_dat[i].lastActionUsername),
								'officedocId': officedocId,
								'officedocTypeName': str(obj_dat[i].officedocTypeName),
								'processId': {
									'processNbr': {
										'doubleValue': str(obj_dat[i].processId.processNbr.doubleValue)
									},
									'processType': str()
								},
								'processIdAsString': str(obj_dat[i].processIdAsString),
								'relatedToWorkcode': {
									'doubleValue': str(obj_dat[i].relatedToWorkcode.doubleValue)
								},
								'responsibleUserName': str(obj_dat[i].responsibleUserName),
								'statusDate': {
									'dateValue': str(obj_dat[i].statusDate.dateValue)
								},
								'statusName': str(obj_dat[i].statusName),
								'topFileDescription': str(obj_dat[i].topFileDescription),
								'topFileFilingDate': {
									'dateValue': str(obj_dat[i].topFileFilingDate.dateValue)
								},
								'topFileId': {
									'fileNbr': {
										'doubleValue': str(obj_dat[i].topFileId.fileNbr.doubleValue)
									},
									'fileSeq': str(obj_dat[i].topFileId.fileSeq),
									'fileSeries': {
										'doubleValue': str(obj_dat[i].topFileId.fileSeries.doubleValue)
									},
									'fileType': str(obj_dat[i].topFileId.fileType)
								},
								'topFileOwner': str(obj_dat[i].topFileOwner),
								'topFileRegistrationId': {
									'registrationDup': str(obj_dat[i].topFileRegistrationId.registrationDup),
									'registrationNbr': str(obj_dat[i].topFileRegistrationId.registrationNbr),
									'registrationSeries': str(obj_dat[i].topFileRegistrationId.registrationSeries),
									'registrationType': str(obj_dat[i].topFileRegistrationId.registrationType)
								},
								'topFileStatusName': str(obj_dat[i].topFileStatusName),
								'topProcessId': {
									'processNbr': {
										'doubleValue': str(obj_dat[i].topProcessId.processNbr.doubleValue)
									},
									'processType': str(obj_dat[i].topProcessId.processType)
								},
								'upperProcessId': upperProcessId,
								'userdocSeqName': str(obj_dat[i].userdocSeqName),
								'userdocSeqNbr': str(obj_dat[i].userdocSeqNbr),
								'userdocSeqSeries': str(obj_dat[i].userdocSeqSeries),
								'userdocSeqType': str(obj_dat[i].userdocSeqType),
								'userdocTypeName': str(obj_dat[i].userdocTypeName),
								'workflowWarningText': str(obj_dat[i].workflowWarningText)
							})
	return(catch_exp)

class enviar_orden(BaseModel):
	exp:str = ""
	pago: str = ""
	user_Id: str = ""	
@app.post('/api/enviar_orden_pub', tags=["Inserta el evento (554 - Orden de Publicación enviada) "])
async def insert_Action_(item: enviar_orden): 
	return(str(Insert_Action(item.exp,item.pago,item.user_Id,'Sprint V2 OP','554')))

class publicacion_enviada(BaseModel):
	fecha:str = ""
	user_id: str = ""
@app.post('/api/Orden_pub_enviada', tags=["Consulta el evento Orden de Publicación enviada por fecha y id de usuario"])
async def Orden_de_Publicacion_enviada(item: publicacion_enviada):
	catch_exp = []
	obj_dat = orden_emitida(item.fecha,item.user_id)
	for i in range(0,len(obj_dat)):
		if obj_dat[i].lastActionName == 'Orden de Publicación enviada':
			try:
				documentId = {
									'docLog': str(obj_dat[i].documentId.docLog),
									'docNbr': {
										'doubleValue': str(obj_dat[i].documentId.docNbr.doubleValue)
									},
									'docOrigin': str(obj_dat[i].documentId.docOrigin),
									'docSeries': {
										'doubleValue': str(obj_dat[i].documentId.docSeries.doubleValue)
									},
									'selected': str(obj_dat[i].documentId.selected)
								}
			except Exception as e:
				documentId = {
								'docLog': '',
								'docNbr': '',
								'docOrigin': '',
								'docSeries': '',
								'selected': ''
							}
			try:
				officedocId = {
									'offidocNbr': {
										'doubleValue': str(obj_dat[i].officedocId.offidocNbr.doubleValue)
									},
									'offidocOrigin': str(obj_dat[i].officedocId.offidocOrigin),
									'offidocSeries': {
										'doubleValue': str(obj_dat[i].officedocId.offidocSeries.doubleValue)
									},
									'selected': str(obj_dat[i].officedocId.selected)
								}
			except Exception as e:
				officedocId = {
				'offidocNbr': '',
				'offidocOrigin': '',
				'offidocSeries': '',
				'selected': ''
			}
			try:
				upperProcessId = {
									'processNbr': {
										'doubleValue': str(obj_dat[i].upperProcessId.processNbr.doubleValue)
									},
									'processType': str(obj_dat[i].upperProcessId.processType)
								}
			except Exception as e:
				upperProcessId = {
				'processNbr': '',
				'processType': ''
			}	
			catch_exp.append(
								{
								'creationDate': {
									'dateValue': str(obj_dat[i].creationDate.dateValue)
								},
								'description': str(obj_dat[i].description),
								'documentId': documentId,
								'dueDate': str(obj_dat[i].dueDate),
								'indTopFileMark': str(obj_dat[i].indTopFileMark),
								'indTopMarkPatent': str(obj_dat[i].indTopMarkPatent),
								'lastActionName': str(obj_dat[i].lastActionName),
								'lastActionUsername': str(obj_dat[i].lastActionUsername),
								'officedocId': officedocId,
								'officedocTypeName': str(obj_dat[i].officedocTypeName),
								'processId': {
									'processNbr': {
										'doubleValue': str(int(obj_dat[i].processId.processNbr.doubleValue))
									},
									'processType': str()
								},
								'processIdAsString': str(obj_dat[i].processIdAsString),
								'relatedToWorkcode': {
									'doubleValue': str(obj_dat[i].relatedToWorkcode.doubleValue)
								},
								'responsibleUserName': str(obj_dat[i].responsibleUserName),
								'statusDate': {
									'dateValue': convert_fecha_hora(str(obj_dat[i].statusDate.dateValue))
								},
								'statusName': str(obj_dat[i].statusName),
								'topFileDescription': str(obj_dat[i].topFileDescription),
								'topFileFilingDate': {
									'dateValue': str(obj_dat[i].topFileFilingDate.dateValue)
								},
								'topFileId': {
									'fileNbr': {
										'doubleValue': str(int(obj_dat[i].topFileId.fileNbr.doubleValue))
									},
									'fileSeq': str(obj_dat[i].topFileId.fileSeq),
									'fileSeries': {
										'doubleValue': str(obj_dat[i].topFileId.fileSeries.doubleValue)
									},
									'fileType': str(obj_dat[i].topFileId.fileType)
								},
								'topFileOwner': str(obj_dat[i].topFileOwner),
								'topFileRegistrationId': {
									'registrationDup': str(obj_dat[i].topFileRegistrationId.registrationDup),
									'registrationNbr': str(obj_dat[i].topFileRegistrationId.registrationNbr),
									'registrationSeries': str(obj_dat[i].topFileRegistrationId.registrationSeries),
									'registrationType': str(obj_dat[i].topFileRegistrationId.registrationType)
								},
								'topFileStatusName': str(obj_dat[i].topFileStatusName),
								'topProcessId': {
									'processNbr': {
										'doubleValue': str(int(obj_dat[i].topProcessId.processNbr.doubleValue))
									},
									'processType': str(obj_dat[i].topProcessId.processType)
								},
								'upperProcessId': upperProcessId,
								'userdocSeqName': str(obj_dat[i].userdocSeqName),
								'userdocSeqNbr': str(obj_dat[i].userdocSeqNbr),
								'userdocSeqSeries': str(obj_dat[i].userdocSeqSeries),
								'userdocSeqType': str(obj_dat[i].userdocSeqType),
								'userdocTypeName': str(obj_dat[i].userdocTypeName),
								'workflowWarningText': str(obj_dat[i].workflowWarningText)
							})
	return(catch_exp)

class Publicacion_enviada(BaseModel):
	fileNbr:str = ""
	fileSeq: str = ""
	fileSeries: str = ""
	fileType: str = ""
@app.post('/api/orden_pub_enviada_exp', tags=["Consulta el evento Orden de Publicación enviada por expediente"])
async def Publicacion_enviada_(item: Publicacion_enviada):
	catch_exp = []
	obj_dat = orden_emitida_exp(item.fileNbr,item.fileSeq,item.fileSeries,item.fileType)
	for i in range(0,len(obj_dat)):
		if obj_dat[i].lastActionName == 'Orden de Publicación enviada':
			try:
				documentId = {
									'docLog': str(obj_dat[i].documentId.docLog),
									'docNbr': {
										'doubleValue': str(obj_dat[i].documentId.docNbr.doubleValue)
									},
									'docOrigin': str(obj_dat[i].documentId.docOrigin),
									'docSeries': {
										'doubleValue': str(obj_dat[i].documentId.docSeries.doubleValue)
									},
									'selected': str(obj_dat[i].documentId.selected)
								}
			except Exception as e:
				documentId = {
								'docLog': '',
								'docNbr': '',
								'docOrigin': '',
								'docSeries': '',
								'selected': ''
							}
			try:
				officedocId = {
									'offidocNbr': {
										'doubleValue': str(obj_dat[i].officedocId.offidocNbr.doubleValue)
									},
									'offidocOrigin': str(obj_dat[i].officedocId.offidocOrigin),
									'offidocSeries': {
										'doubleValue': str(obj_dat[i].officedocId.offidocSeries.doubleValue)
									},
									'selected': str(obj_dat[i].officedocId.selected)
								}
			except Exception as e:
				officedocId = {
				'offidocNbr': '',
				'offidocOrigin': '',
				'offidocSeries': '',
				'selected': ''
			}
			try:
				upperProcessId = {
									'processNbr': {
										'doubleValue': str(obj_dat[i].upperProcessId.processNbr.doubleValue)
									},
									'processType': str(obj_dat[i].upperProcessId.processType)
								}
			except Exception as e:
				upperProcessId = {
				'processNbr': '',
				'processType': ''
			}	
			catch_exp.append(
								{
								'creationDate': {
									'dateValue': str(obj_dat[i].creationDate.dateValue)
								},
								'description': str(obj_dat[i].description),
								'documentId': documentId,
								'dueDate': str(obj_dat[i].dueDate),
								'indTopFileMark': str(obj_dat[i].indTopFileMark),
								'indTopMarkPatent': str(obj_dat[i].indTopMarkPatent),
								'lastActionName': str(obj_dat[i].lastActionName),
								'lastActionUsername': str(obj_dat[i].lastActionUsername),
								'officedocId': officedocId,
								'officedocTypeName': str(obj_dat[i].officedocTypeName),
								'processId': {
									'processNbr': {
										'doubleValue': str(int(obj_dat[i].processId.processNbr.doubleValue))
									},
									'processType': str()
								},
								'processIdAsString': str(obj_dat[i].processIdAsString),
								'relatedToWorkcode': {
									'doubleValue': str(obj_dat[i].relatedToWorkcode.doubleValue)
								},
								'responsibleUserName': str(obj_dat[i].responsibleUserName),
								'statusDate': {
									'dateValue': convert_fecha_hora(str(obj_dat[i].statusDate.dateValue))
								},
								'statusName': str(obj_dat[i].statusName),
								'topFileDescription': str(obj_dat[i].topFileDescription),
								'topFileFilingDate': {
									'dateValue': str(obj_dat[i].topFileFilingDate.dateValue)
								},
								'topFileId': {
									'fileNbr': {
										'doubleValue': str(int(obj_dat[i].topFileId.fileNbr.doubleValue))
									},
									'fileSeq': str(obj_dat[i].topFileId.fileSeq),
									'fileSeries': {
										'doubleValue': str(obj_dat[i].topFileId.fileSeries.doubleValue)
									},
									'fileType': str(obj_dat[i].topFileId.fileType)
								},
								'topFileOwner': str(obj_dat[i].topFileOwner),
								'topFileRegistrationId': {
									'registrationDup': str(obj_dat[i].topFileRegistrationId.registrationDup),
									'registrationNbr': str(obj_dat[i].topFileRegistrationId.registrationNbr),
									'registrationSeries': str(obj_dat[i].topFileRegistrationId.registrationSeries),
									'registrationType': str(obj_dat[i].topFileRegistrationId.registrationType)
								},
								'topFileStatusName': str(obj_dat[i].topFileStatusName),
								'topProcessId': {
									'processNbr': {
										'doubleValue': str(obj_dat[i].topProcessId.processNbr.doubleValue)
									},
									'processType': str(obj_dat[i].topProcessId.processType)
								},
								'upperProcessId': upperProcessId,
								'userdocSeqName': str(obj_dat[i].userdocSeqName),
								'userdocSeqNbr': str(obj_dat[i].userdocSeqNbr),
								'userdocSeqSeries': str(obj_dat[i].userdocSeqSeries),
								'userdocSeqType': str(obj_dat[i].userdocSeqType),
								'userdocTypeName': str(obj_dat[i].userdocTypeName),
								'workflowWarningText': str(obj_dat[i].workflowWarningText)
							})
	return(catch_exp)

class redpi(BaseModel):
	exp:str = ""
	pago: str = ""
	user_Id: str = ""
@app.post('/api/publicado_redpi', tags=["Inserta el evento (573 - Publicado en REDPI)"])
async def PUB_REDPI(item: redpi):
	return(str(Insert_Action(item.exp,item.pago,item.user_Id,'Publicado en REDPI','573')))

class processNbr(BaseModel):
	process_Nbr:str = ""
@app.post('/doc_firmado', tags=["Documentos firmados, consulta por (process_Nbr) "])
async def documento_firmado(item: processNbr):
	'''
	Ej:
	http://192.168.50.185:8888/nuxeo/restAPI/default/edmsAPI/getEDocPdfById?eDocId=2366311 
	'''
	edoc= []
	for i in range(0,len(fetch_all_officdoc_nuxeo(item.process_Nbr))):
		edoc.append({
			"EDOC_ID":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[0].sqlColumnValue,                
			"EDOC_TYP":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[1].sqlColumnValue,               
			"EDOC_DATE":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[2].sqlColumnValue,              
			"EDOC_SEQ":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[3].sqlColumnValue,               
			"EDOC_SER":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[4].sqlColumnValue,               
			"EDOC_NBR":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[5].sqlColumnValue,               
			"EDOC_IMAGE_LINKING_DATE":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[6].sqlColumnValue,
			"EDOC_IMAGE_LINKING_USER":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[7].sqlColumnValue,
			"ROW_VERSION":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[8].sqlColumnValue,            
			"EFOLDER_ID":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[9].sqlColumnValue,             
			"EDOC_IMAGE_CERTIF_DATE":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[10].sqlColumnValue, 
			"EDOC_IMAGE_CERTIF_USER":fetch_all_do_edoc_nuxeo(fetch_all_officdoc_nuxeo(item.process_Nbr)[i].sqlColumnList[0].sqlColumnValue)[0].sqlColumnList[11].sqlColumnValue
		})
	return(edoc)



app.openapi = custom_openapi
