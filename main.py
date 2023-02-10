from urllib import request
from fastapi import FastAPI
from pydantic import BaseModel
from publicaciones.pub_2023 import convert_fecha_hora, orden_emitida, orden_emitida_exp

from wipo.ipas import Insert_Action, mark_getlist, mark_getlistReg #pip install "fastapi[all]"


app = FastAPI() 


@app.post('/api/markgetlist')
def getMarkGetList(exp: str):
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

#Consultar Emitidas
@app.post('/api/orden_pub_emitida')
def pub_emitir(fecha:str,user_id:str):#{"fecha":"2022-12-19","user_id":"89"}
	catch_exp = []
	obj_dat = orden_emitida(fecha,user_id)
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


class emicion(BaseModel):
    fileNbr:str = ""
    fileSeq: str = ""
    fileSeries: str = ""
    fileType: str = ""

@app.post('/api/orden_pub_emitida_exp')
def pub_emitir_exp(item: emicion):#{"fileNbr":"21104495","fileSeq":"PY","fileSeries":"2021","fileType":"M"}
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

#Consultar 2da. Emisión Orden Publicación
@app.post('/api/orden_pub_2da_emitida_exp')
def pub_emitir_2da_exp(fileNbr:str,fileSeq:str,fileSeries:str,fileType:str):#{"fileNbr":"21104495","fileSeq":"PY","fileSeries":"2021","fileType":"M"}
	catch_exp = []
	obj_dat = orden_emitida_exp(fileNbr,fileSeq,fileSeries,fileType)
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

#Enviar Emitida
@app.post('/api/enviar_orden_pub')
def enviar_orden(): #{"exp":"","pago":"","userid":"","nota":"","evento":"554"}
	return(str(Insert_Action(request.json["exp"],request.json["pago"],request.json["userid"],'Sprint V2-2023 OP','554')))

#Consultar enviadas
@app.post('/api/Orden_pub_enviada')
def pub_enviada():#{"fecha":"2022-12-19","user_id":"89"}
	catch_exp = []
	obj_dat = orden_emitida(request.json["fecha"],request.json["user_id"])
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

#Consultar Emitidas expediente
@app.post('/api/orden_pub_enviada_exp')
def pub_enviar_exp():#{"fileNbr":"21104495","fileSeq":"PY","fileSeries":"2021","fileType":"M"}
	catch_exp = []
	obj_dat = orden_emitida_exp(request.json["fileNbr"],request.json["fileSeq"],request.json["fileSeries"],request.json["fileType"])
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

#Publicado en REDPI
@app.post('/api/publicado_redpi')
def PUB_REDPI(): #{"exp":"","pago":"","userid":"","nota":"","evento":"554"}
	return(str(Insert_Action('22105981','2023-01-24','89','Publicado en REDPI V2-2023','573')))

