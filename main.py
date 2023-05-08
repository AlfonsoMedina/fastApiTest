from time import sleep
from urllib import request
from fastapi import  FastAPI
from pydantic import BaseModel
from auto_process import insert_list, insertReg, insertRen
from models.insertRegModel import insertRegModel
from models.insertRenModel import insertRenModel
from tools.send_mail import enviar
from tools.connect import MEA_TIEMPO_ACTUALIZACION
from dinapi.sfe import count_pendiente, format_userdoc, oposicion_sfe, pendientes_sfe, pendientes_sfe_not_pag, pendientes_sfe_soporte, registro_sfe, reglas_me, renovacion_sfe, tip_doc
from models.InsertUserDocModel import userDocModel
from tools.params_seting import  get_parametro, get_parametros, get_parametros_mea, upDate_parametro
from tools.base64Decode import image_url_to_b64
from wipo.ipas import  Insert_user_doc, Insert_user_doc_con_recibo_poder, Insert_user_doc_sin_recibo_con_relacion, Insert_user_doc_sin_recibo_relacion, disenio_getlist, disenio_getlist_fecha, disenio_user_doc_getlist_fecha, get_agente, mark_getlist, mark_getlistFecha, mark_getlistReg, mark_insert_reg, mark_insert_ren, patent_getlist_fecha, patent_user_doc_getlist_fecha, personAgente, personAgenteDisenio, personAgentePatent, personTitular, personTitularDisenio, personTitularPatent, user_doc_getlist_fecha, user_doc_receive, user_doc_update, user_doc_update_sin_recibo #pip install "fastapi[all]"
from wipo.function_for_reception_in import insert_user_doc_escritos, user_doc_read, user_doc_read_disenio, user_doc_read_patent
import zeep
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

description = """
Version 2023 

## Métodos para consultar e insertar eventos de Mesa de Entrada Automatica  
Engineer in charge ***W. Alfonso Medina***

las rutas reciben un objeto **JSON** como parametro y retornar un objeto **JSON**.

"""

app = FastAPI()

origins = ["*"]

default_val_e99 = lambda arg: arg if arg != "" else "E99"

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=['*'], #["POST"]
	allow_headers=["*"],
)

def custom_openapi():
	if app.openapi_schema:
		return app.openapi_schema
	openapi_schema = get_openapi(
		title="Api Mesa de Entrada Automatica",
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

class agent_code(BaseModel):
	code:str = ""
@app.post('/api/getAgente_ipas', summary="Marcas", tags=["Consulta nombre de agente   por agent_code"])
async def getAgente_ipas(item: agent_code):
	return({"nombre":get_agente(item.code).agentName})

@app.post('/api/getAgente', summary="Marcas", tags=["Consulta datos de agente como persona  por agent_code"])
async def consulta_agente(item: agent_code):
	data = []
	try:
		data.append({
					"addressStreet":personAgente(item.code)[0].addressStreet,
					"agentCode":personAgente(item.code)[0].agentCode.doubleValue,
					"personName":personAgente(item.code)[0].personName,
					"residenceCountryCode":personAgente(item.code)[0].residenceCountryCode,
					"nationalityCountryCode":personAgente(item.code)[0].nationalityCountryCode,
					"email":personAgente(item.code)[0].email,
					"individualIdType":personAgente(item.code)[0].individualIdType,
					"individualIdNbr":personAgente(item.code)[0].individualIdNbr,
					"telephone":personAgente(item.code)[0].telephone,
					"zipCode":personAgente(item.code)[0].zipCode})
		return(data)
	except Exception as e:
		data = []
		return(data)

@app.post('/api/getAgentePatent', summary="Patentes", tags=["Consulta datos de agente como persona de patentes por agent_code"])
async def consulta_agente_Patent(item: agent_code):
	data = []
	data.append({
					"addressStreet":personAgentePatent(item.code)[0].addressStreet,
					"agentCode":personAgentePatent(item.code)[0].agentCode.doubleValue,
					"personName":personAgentePatent(item.code)[0].personName,
					"residenceCountryCode":personAgentePatent(item.code)[0].residenceCountryCode,
					"nationalityCountryCode":personAgentePatent(item.code)[0].nationalityCountryCode,
					"email":personAgentePatent(item.code)[0].email,
					"individualIdType":personAgentePatent(item.code)[0].individualIdType,
					"individualIdNbr":personAgentePatent(item.code)[0].individualIdNbr,
					"telephone":personAgentePatent(item.code)[0].telephone,
					"zipCode":personAgentePatent(item.code)[0].zipCode})
	
	return(data)

@app.post('/api/getAgenteDisenio', summary="Diseño", tags=["Consulta datos de agente como persona de diseño por agent_code"])
async def consulta_agente_Disenio(item: agent_code):
	data = []
	#for i in range(0,len(personAgenteDisenio(item.code))):
	data.append({
					"addressStreet":personAgenteDisenio(item.code)[0].addressStreet,
					"agentCode":personAgenteDisenio(item.code)[0].agentCode.doubleValue,
					"personName":personAgenteDisenio(item.code)[0].personName,
					"residenceCountryCode":personAgenteDisenio(item.code)[0].residenceCountryCode,
					"nationalityCountryCode":personAgenteDisenio(item.code)[0].nationalityCountryCode,
					"email":personAgenteDisenio(item.code)[0].email,
					"individualIdType":personAgenteDisenio(item.code)[0].individualIdType,
					"individualIdNbr":personAgenteDisenio(item.code)[0].individualIdNbr,
					"telephone":personAgenteDisenio(item.code)[0].telephone,
					"zipCode":personAgenteDisenio(item.code)[0].zipCode})
	#print(data)
	return(data)

class gettitular(BaseModel):
	nombre:str = ""
@app.post('/api/getTitular', summary="Marcas", tags=["Consulta datos de titular como persona de marcas por nombre/denominacion"])
async def consulta_titular(item: gettitular):
	personName = item.nombre					
	return(personTitular(str(personName)))

@app.post('/api/getTitularPatent', summary="Patentes", tags=["Consulta datos de titular como persona de patentes por nombre/denominacion"])
async def consulta_titularPatent(item: gettitular):
	personName = item.nombre					
	return(personTitularPatent(str(personName)))

@app.post('/api/getTitularDisenio', summary="Diseño", tags=["Consulta datos de titular como persona de diseño por nombre/denominacion"])
async def consulta_titularDisenio(item: gettitular):
	personName = item.nombre					
	return(personTitularDisenio(str(personName)))

class process_fecha(BaseModel):
	fecha_from:str = ""
	fecha_to:str = ""
@app.post('/api/procesados_marcas', summary="Marcas", tags=["Consulta expedientes y escritos procesados de marcas por rango de fecha (yy-mm-dd)"])
async def procesados_marcas(item: process_fecha):
	resp=[]
	try:
		for x in mark_getlistFecha(item.fecha_from,item.fecha_to):
			resp.append({
								"fileNbr":str(int(x.fileId.fileNbr.doubleValue)),
								"applicationType":x.filingData.applicationType,
								"filingDate":str(x.filingData.filingDate.dateValue),
								"fileSummaryOwner":x.fileSummaryOwner
							})

		for i in user_doc_getlist_fecha(item.fecha_from,item.fecha_to):
			owner = user_doc_read(i.documentId.docLog, i.documentId.docNbr.doubleValue, i.documentId.docOrigin, i.documentId.docSeries.doubleValue)
			try:
				fileSummaryOwner = owner['affectedFileSummaryList']['fileSummaryOwner']
			except Exception as e:
				fileSummaryOwner = ""
			try:
				note = owner['notes']
			except Exception as e:
				note = ""				
			
			try:	
				resp.append({
						"fileNbr":int(i.documentId.docNbr.doubleValue),
						"userdocSummaryTypes":i.userdocSummaryTypes,
						"filingDate":str(i.filingDate.dateValue),
						"ownwe":fileSummaryOwner,
						"note": note
						})
			except Exception as e:
				print(e)						
	except Exception as e:
		print(e)
	return(resp)

@app.post('/api/procesados_patentes', summary="Patentes", tags=["Consulta expedientes y escritos procesados de patentes por rango de fecha (yy-mm-dd)"])
async def procesados_patentes(item: process_fecha):
	try:	
		resp=[]
		for i in patent_getlist_fecha(item.fecha_from,item.fecha_to):
			resp.append({
							"fileNbr":str(int(i.fileId.fileNbr.doubleValue)),
							"applicationType":i.filingData.applicationType,
							"fileSummaryOwner":i.fileSummaryOwner,
							"filingDate":str(i.filingData.filingDate.dateValue),
							"applicationSubtype":i.filingData.applicationSubtype
						})

		for i in patent_user_doc_getlist_fecha(item.fecha_from,item.fecha_to):
			owner=user_doc_read_patent(i.documentId.docLog, i.documentId.docNbr.doubleValue, i.documentId.docOrigin, i.documentId.docSeries.doubleValue)
			try:	
				personN = owner['applicant']['person']['personName']
			except Exception as e:
				personN = ""
			try:	
				noteN = owner['notes']
			except Exception as e:
				noteN = ""
			resp.append({
					"docSeqNbr":str(int(i.docSeqId.docSeqNbr.doubleValue)),
					"filingDate":str(i.filingDate.dateValue),
					"userdocSummaryTypes":i.userdocSummaryTypes,
					"personName":personN,
					"note":noteN
					})

	except Exception as e:
		print(e)	
	return(resp)

@app.post('/api/procesados_disenios', summary="Diseño", tags=["Consulta expedientes y escritos procesados de diseño por rango de fecha (yy-mm-dd)"])
async def procesados_disenios(item: process_fecha):
	try:	
		resp=[]
		for i in disenio_getlist_fecha(item.fecha_from,item.fecha_to):
			resp.append({
						"fileNbr":str(int(i.fileId.fileNbr.doubleValue)),
						"applicationType":i.filingData.applicationType,
						"fileSummaryOwner":i.fileSummaryOwner,
						"filingDate":str(i.filingData.filingDate.dateValue),
						"applicationSubtype":i.filingData.applicationSubtype
						})


		for i in disenio_user_doc_getlist_fecha(item.fecha_from,item.fecha_to):
			owner=user_doc_read_disenio(i.documentId.docLog, i.documentId.docNbr.doubleValue, i.documentId.docOrigin, i.documentId.docSeries.doubleValue)
			try:
				fileSummaryOwner = owner['applicant']['person']['personName']
			except Exception as e:
				fileSummaryOwner = ""
			try:
				note = owner['notes']
			except Exception as e:
				note = ""	
			
			resp.append({
				"docSeqNbr":str(int(i.docSeqId.docSeqNbr.doubleValue)),
				"filingDate":str(i.filingDate.dateValue),
				"userdocSummaryTypes":i.userdocSummaryTypes,
				"personName":fileSummaryOwner,
				"note":note
				})
	except Exception as e:
		print(e)	
	return(resp)

@app.post('/api/user_doc_patentes', summary="Patentes", tags=["Consulta escritos procesados de patentes por rango de fecha (yy-mm-dd)"])
async def user_doc_patent(item: process_fecha):
	try:
		resp = []
		for i in patent_user_doc_getlist_fecha(item.fecha_from,item.fecha_to):
			owner=user_doc_read_patent(i.documentId.docLog, i.documentId.docNbr.doubleValue, i.documentId.docOrigin, i.documentId.docSeries.doubleValue)
			try:	
				personN = owner['applicant']['person']['personName']
			except Exception as e:
				personN = ""
			try:	
				noteN = owner['notes']
			except Exception as e:
				noteN = ""							
			#print(i.filingDate.dateValue)
			resp.append({
				"docSeqNbr":str(int(i.docSeqId.docSeqNbr.doubleValue)),
				"filingDate":i.filingDate.dateValue,
				"personName":personN,
				"note":noteN
				})
	except Exception as e:
		print(e)	
	return(resp)

@app.post('/api/user_doc_disenios', summary="Diseño", tags=["Consulta escritos procesados de diseño por rango de fecha (yy-mm-dd)"])
async def user_doc_disenio(item: process_fecha):
	try:
		resp = []
		for i in disenio_user_doc_getlist_fecha(item.fecha_from,item.fecha_to):
			owner=user_doc_read_disenio(i.documentId.docLog, i.documentId.docNbr.doubleValue, i.documentId.docOrigin, i.documentId.docSeries.doubleValue)
			try:	
				personN = owner['applicant']['person']['personName'] 
			except Exception as e:
				personN = ""
			try:	
				noteN = owner['notes'] 
			except Exception as e:
				noteN = ""			
			#print(i.filingDate.dateValue)
			resp.append({
				"docSeqNbr":str(int(i.docSeqId.docSeqNbr.doubleValue)),
				"filingDate":i.filingDate.dateValue,
				"personName":personN,
				"note":noteN
				})
	except Exception as e:
		print(e)	
	return(resp)

class for_exp(BaseModel):
	expediente:str = ""
@app.post('/api/disenio_por_exp', summary="Diseño", tags=["Consulta diseño por expediente"])
async def disenio_for_fileNBR(item: for_exp):
	try:
		data = disenio_getlist(item.expediente, item.expediente)[0]
		return({
						"fileNbr":str(int(data.fileId.fileNbr.doubleValue)),
						"fileSeq":str(data.fileId.fileSeq),
						"fileSeries":str(data.fileId.fileSeries.doubleValue),
						"fileType":str(data.fileId.fileType),
						"fileSummaryDescription":str(data.fileSummaryDescription).replace("'","\'")
					})
	except Exception as e:
		return([])

################################# Insert ################################################################## 
class userdoc_insert_OPO(BaseModel):
	affectedFileIdList_fileNbr:str = ""
	affectedFileIdList_fileSeq:str = ""
	affectedFileIdList_fileSeries:str = ""
	affectedFileIdList_fileType:str = ""
	affectedFileSummaryList_fileId_fileNbr:str = ""
	affectedFileSummaryList_fileId_fileSeq:str = ""
	affectedFileSummaryList_fileId_fileSeries:str = ""
	affectedFileSummaryList_fileId_fileType:str = ""
	affectedFileSummaryList_fileSummaryDescription:str = ""
	affectedFileSummaryList_fileSummaryOwner:str = ""
	applicant_applicantNotes:str = ""
	applicant_person_addressStreet:str = ""
	applicant_person_email:str = ""
	applicant_person_nationalityCountryCode:str = ""
	applicant_person_personName:str = ""
	applicant_person_residenceCountryCode:str = ""
	applicant_person_telephone:str = ""
	documentId_docLog:str = ""
	documentId_docNbr:str = ""
	documentId_docOrigin:str = ""
	documentId_docSeries:str = ""
	documentId_selected:str = ""
	documentSeqId_docSeqNbr:str = ""
	documentSeqId_docSeqSeries:str = ""
	documentSeqId_docSeqType:str = ""
	filingData_captureDate:str = ""
	filingData_captureUserId:str = ""
	filingData_filingDate:str = ""
	filingData_paymentList_receiptAmount:str = ""
	filingData_paymentList_receiptDate:str = ""
	filingData_paymentList_receiptNbr:str = ""
	filingData_paymentList_receiptNotes:str = ""
	filingData_paymentList_receiptType:str = ""
	filingData_paymentList_receiptTypeName:str = ""
	filingData_documentId_docLog:str = ""
	filingData_documentId_docNbr:str = ""
	filingData_documentId_docOrigin:str = ""
	filingData_documentId_docSeries:str = ""
	filingData_documentId_selected:str = ""
	filingData_userdocTypeList_userdocType:str = ""
	ownerList_personName:str = ""
	ownerList_addressStreet:str = ""
	ownerList_nationalityCountryCode:str = ""
	ownerList_residenceCountryCode:str = ""
	notes:str = ""
	representationData_representativeList_addressStreet:str = ""
	representationData_representativeList_agentCode:str = ""
	representationData_representativeList_email:str = ""
	representationData_representativeList_nationalityCountryCode:str = ""
	representationData_representativeList_personName:str = ""
	representationData_representativeList_residenceCountryCode:str = ""
	representationData_representativeList_telephone:str = ""
	representationData_representativeList_zipCode:str = ""
@app.post('/sfe/insert_userdoc_opo', summary="Marcas", tags=["Insert Escrito de Oposición de marca"])
async def insert_user_doc_mde(item: userdoc_insert_OPO):
	try:
		return(str(Insert_user_doc(
									item.affectedFileIdList_fileNbr,
									item.affectedFileIdList_fileSeq,
									item.affectedFileIdList_fileSeries,
									item.affectedFileIdList_fileType,
									item.affectedFileSummaryList_fileId_fileNbr,
									item.affectedFileSummaryList_fileId_fileSeq,
									item.affectedFileSummaryList_fileId_fileSeries,
									item.affectedFileSummaryList_fileId_fileType,
									item.affectedFileSummaryList_fileSummaryDescription,
									item.affectedFileSummaryList_fileSummaryOwner,
									item.applicant_applicantNotes,
									item.applicant_person_addressStreet,
									item.applicant_person_email,
									item.applicant_person_nationalityCountryCode,
									item.applicant_person_personName,
									item.applicant_person_residenceCountryCode,
									item.applicant_person_telephone,
									item.documentId_docLog,
									item.documentId_docNbr,
									item.documentId_docOrigin,
									item.documentId_docSeries,
									item.documentId_selected,
									item.documentSeqId_docSeqNbr,
									item.documentSeqId_docSeqSeries,
									item.documentSeqId_docSeqType,
									item.filingData_captureDate,
									item.filingData_captureUserId,
									item.filingData_filingDate,
									item.filingData_paymentList_receiptAmount,
									item.filingData_paymentList_receiptDate,
									item.filingData_paymentList_receiptNbr,
									item.filingData_paymentList_receiptNotes,
									item.filingData_paymentList_receiptType,
									item.filingData_paymentList_receiptTypeName,
									item.filingData_documentId_docLog,
									item.filingData_documentId_docNbr,
									item.filingData_documentId_docOrigin,
									item.filingData_documentId_docSeries,
									item.filingData_documentId_selected,
									item.filingData_userdocTypeList_userdocType,
									item.ownerList_personName,
									item.ownerList_addressStreet,
									item.ownerList_nationalityCountryCode,
									item.ownerList_residenceCountryCode,
									item.notes,
									item.representationData_representativeList_addressStreet,
									item.representationData_representativeList_agentCode,
									item.representationData_representativeList_email,
									item.representationData_representativeList_nationalityCountryCode,
									item.representationData_representativeList_personName,
									item.representationData_representativeList_residenceCountryCode,
									item.representationData_representativeList_telephone,
									item.representationData_representativeList_zipCode)))
	except zeep.exceptions.Fault as e:
			return(str(e.message))

class userdoc_insert_sr_sr(BaseModel):
	applicant_person_applicantNotes:str = ""
	applicant_person_addressStreet:str = ""
	applicant_person_nationalityCountryCode:str = ""
	applicant_person_personName:str = ""
	applicant_person_residenceCountryCode:str = ""
	documentId_docLog:str = ""
	documentId_docNbr:str = ""
	documentId_docOrigin:str = ""
	documentId_docSeries:str = ""
	documentId_selected:str = ""
	documentSeqId_docSeqNbr:str = ""
	documentSeqId_docSeqSeries:str = ""
	documentSeqId_docSeqType:str = ""
	filingData_captureDate:str = ""
	filingData_captureUserId:str = ""
	filingData_filingDate:str = ""
	filingData_receptionDocument_documentId_docLog:str = ""
	filingData_receptionDocument_documentId_docNbr:str = ""
	filingData_receptionDocument_documentId_docOrigin:str = ""
	filingData_receptionDocument_documentId_docSeries:str = ""
	filingData_receptionDocument_documentId_selected:str = ""
	filingData_userdocTypeList_userdocName:str = ""
	filingData_userdocTypeList_userdocType:str = ""
	ownerList_person_addressStreet:str = ""
	ownerList_person_nationalityCountryCode:str = ""
	ownerList_person_personName:str = ""
	ownerList_person_residenceCountryCode:str = ""
	notes:str = ""
	representativeList_person_addressStreetAgente:str = ""
	representativeList_person_agentCode:str = ""
	representativeList_person_email:str = ""
	representativeList_person_nationalityCountryCode:str = ""
	representativeList_person_AgentepersonName:str = ""
	representativeList_person_residenceCountryCode:str = ""
	representativeList_person_telephone:str = ""
	representativeList_person_zipCode:str = ""
	processNbr:str = ""
	processType:str = ""
@app.post('/sfe/insertuserdoc_sr_sr', summary="Marcas", tags=["Insert Escrito sin recibo sin relacion"])
async def insert_sr_sr(item:userdoc_insert_sr_sr):
	try:
		return(Insert_user_doc_sin_recibo_relacion(
												item.applicant_person_applicantNotes,
												item.applicant_person_addressStreet,
												item.applicant_person_nationalityCountryCode,
												item.applicant_person_personName,
												item.applicant_person_residenceCountryCode,
												item.documentId_docLog,
												item.documentId_docNbr,
												item.documentId_docOrigin,
												item.documentId_docSeries,
												item.documentId_selected,
												item.documentSeqId_docSeqNbr,
												item.documentSeqId_docSeqSeries,
												item.documentSeqId_docSeqType,
												item.filingData_captureDate,
												item.filingData_captureUserId,
												item.filingData_filingDate,
												item.filingData_receptionDocument_documentId_docLog,
												item.filingData_receptionDocument_documentId_docNbr,
												item.filingData_receptionDocument_documentId_docOrigin,
												item.filingData_receptionDocument_documentId_docSeries,
												item.filingData_receptionDocument_documentId_selected,
												item.filingData_userdocTypeList_userdocName,
												item.filingData_userdocTypeList_userdocType,
												item.ownerList_person_addressStreet,
												item.ownerList_person_nationalityCountryCode,
												item.ownerList_person_personName,
												item.ownerList_person_residenceCountryCode,
												item.notes,
												item.representativeList_person_addressStreetAgente,
												item.representativeList_person_agentCode,
												item.representativeList_person_email,
												item.representativeList_person_nationalityCountryCode,
												item.representativeList_person_AgentepersonName,
												item.representativeList_person_residenceCountryCode,
												item.representativeList_person_telephone,
												item.representativeList_person_zipCode,
												item.processNbr,
												item.processType))
	except zeep.exceptions.Fault as e:
		return(str(e.message))

class userdoc_insert_rp(BaseModel):
	applicant_applicantNotes:str = ""
	applicant_person_addressStreet:str = ""
	applicant_person_agentCode:str = ""
	applicant_person_cityCode:str = ""
	applicant_person_cityName:str = ""
	applicant_person_email:str = ""
	applicant_person_nationalityCountryCode:str = ""
	applicant_person_personName:str = ""
	applicant_person_residenceCountryCode:str = ""
	applicant_person_telephone:str = ""
	applicant_person_zipCode:str = ""
	documentId_docLog:str = ""
	documentId_docNbr:str = ""
	documentId_docOrigin:str = ""
	documentId_docSeries:str = ""
	documentId_selected:str = ""
	documentSeqId_docSeqNbr:str = ""
	documentSeqId_docSeqSeries:str = ""
	documentSeqId_docSeqType:str = ""
	filingData_captureDate:str = ""
	filingData_captureUserId:str = ""
	filingData_filingDate:str = ""
	filingData_paymentList_currencyName:str = ""
	filingData_paymentList_currencyType:str = ""
	filingData_paymentList_receiptAmount:str = ""
	filingData_paymentList_receiptDate:str = ""
	filingData_paymentList_receiptNbr:str = ""
	filingData_paymentList_receiptNotes:str = ""
	filingData_paymentList_receiptType:str = ""
	filingData_paymentList_receiptTypeName:str = ""
	filingData_userdocTypeList_userdocName:str = ""
	filingData_userdocTypeList_userdocType:str = ""
	filingData_receptionDocument_documentId_docLog:str = ""
	filingData_receptionDocument_docNbr:str = ""
	filingData_receptionDocument_docOrigin:str = ""
	filingData_receptionDocument_docSeries:str = ""
	receptionDocument_extraData_dataNbr1:str = ""
	poaAgpoaData_poaGranteeList_person_agentCode:str = ""
	poaData_poaDate:str = ""
	ownerList_person_addressStreet:str = ""
	ownerList_person_agentCode:str = ""
	ownerList_person_nationalityCountryCode:str = ""
	ownerList_person_personName:str = ""
	ownerList_person_residenceCountryCode:str = ""
	ownerList_person_telephone:str = ""
	ownerList_person_zipCode:str = ""
	poaData_poaGranteeList_person_addressStreet:str = ""
	poaData_poaGranteeList_person_addressZone:str = ""
	poaData_poaGranteeList_person_cityName:str = ""
	poaData_poaGranteeList_person_email:str = ""
	poaData_poaGranteeList_person_nationalityCountryCode:str = ""
	poaData_poaGranteeList_person_personName:str = ""
	poaData_poaGranteeList_person_residenceCountryCode:str = ""
	poaData_poaGranteeList_person_telephone:str = ""
	poaData_poaGranteeList_person_zipCode:str = ""
	poaData_poaGranteeList_representativeType:str = ""
	poaData_poaGrantor_person_addressStreet:str = ""
	poaData_poaGrantor_person_agentCode:str = ""
	poaData_poaGrantor_person_cityName:str = ""
	poaData_poaGrantor_person_email:str = ""
	poaData_poaGrantor_person_nationalityCountryCode:str = ""
	poaData_poaGrantor_person_personName:str = ""
	poaData_poaGrantor_person_residenceCountryCode:str = ""
	poaData_poaGrantor_person_telephone:str = ""
	poaData_poaGrantor_person_zipCode:str = ""
	poaData_poaRegNumber:str = ""
	poaData_scope:str = ""
	representationData_representativeList_person_addressStreet:str = ""
	representationData_representativeList_person_addressZone:str = ""
	representationData_representativeList_person_agentCode:str = ""
	representationData_representativeList_person_cityName:str = ""
	representationData_representativeList_person_nationalityCountryCode:str = ""
	representationData_representativeList_person_personName:str = ""
	representationData_representativeList_person_residenceCountryCode:str = ""
	representationData_representativeList_person_telephone:str = ""
	representationData_representativeList_person_zipCode:str = ""
	representativeList_representativeType:str = ""
	notes:str = ""
	userdocProcessId_processNbr:str = ""
	userdocProcessId_processType:str = ""
@app.post('/sfe/insertuserdoc_registro_de_poder', summary="Marcas", tags=["Insert Escrito registro de poder"])
async def insert_user_doc_rp(item:userdoc_insert_rp):
	try:
		return(Insert_user_doc_con_recibo_poder(item.applicant_applicantNotes,
											item.applicant_person_addressStreet,
											item.applicant_person_agentCode,
											item.applicant_person_cityCode,
											item.applicant_person_cityName,
											item.applicant_person_email,
											item.applicant_person_nationalityCountryCode,
											item.applicant_person_personName,
											item.applicant_person_residenceCountryCode,
											item.applicant_person_telephone,
											item.applicant_person_zipCode,
											item.documentId_docLog,
											item.documentId_docNbr,
											item.documentId_docOrigin,
											item.documentId_docSeries,
											item.documentId_selected,
											item.documentSeqId_docSeqNbr,
											item.documentSeqId_docSeqSeries,
											item.documentSeqId_docSeqType,
											item.filingData_captureDate,
											item.filingData_captureUserId,
											item.filingData_filingDate,
											item.filingData_paymentList_currencyName,
											item.filingData_paymentList_currencyType,
											item.filingData_paymentList_receiptAmount,
											item.filingData_paymentList_receiptDate,
											item.filingData_paymentList_receiptNbr,
											item.filingData_paymentList_receiptNotes,
											item.filingData_paymentList_receiptType,
											item.filingData_paymentList_receiptTypeName,
											item.filingData_userdocTypeList_userdocName,
											item.filingData_userdocTypeList_userdocType,
											item.filingData_receptionDocument_documentId_docLog,
											item.filingData_receptionDocument_docNbr,
											item.filingData_receptionDocument_docOrigin,
											item.filingData_receptionDocument_docSeries,
											item.receptionDocument_extraData_dataNbr1,
											item.poaAgpoaData_poaGranteeList_person_agentCode,
											item.poaData_poaDate,
											item.ownerList_person_addressStreet,
											item.ownerList_person_agentCode,
											item.ownerList_person_nationalityCountryCode,
											item.ownerList_person_personName,
											item.ownerList_person_residenceCountryCode,
											item.ownerList_person_telephone,
											item.ownerList_person_zipCode,
											item.poaData_poaGranteeList_person_addressStreet,
											item.poaData_poaGranteeList_person_addressZone,
											item.poaData_poaGranteeList_person_cityName,
											item.poaData_poaGranteeList_person_email,
											item.poaData_poaGranteeList_person_nationalityCountryCode,
											item.poaData_poaGranteeList_person_personName,
											item.poaData_poaGranteeList_person_residenceCountryCode,
											item.poaData_poaGranteeList_person_telephone,
											item.poaData_poaGranteeList_person_zipCode,
											item.poaData_poaGranteeList_representativeType,
											item.poaData_poaGrantor_person_addressStreet,
											item.poaData_poaGrantor_person_agentCode,
											item.poaData_poaGrantor_person_cityName,
											item.poaData_poaGrantor_person_email,
											item.poaData_poaGrantor_person_nationalityCountryCode,
											item.poaData_poaGrantor_person_personName,
											item.poaData_poaGrantor_person_residenceCountryCode,
											item.poaData_poaGrantor_person_telephone,
											item.poaData_poaGrantor_person_zipCode,
											item.poaData_poaRegNumber,
											item.poaData_scope,
											item.representationData_representativeList_person_addressStreet,
											item.representationData_representativeList_person_addressZone,
											item.representationData_representativeList_person_agentCode,
											item.representationData_representativeList_person_cityName,
											item.representationData_representativeList_person_nationalityCountryCode,
											item.representationData_representativeList_person_personName,
											item.representationData_representativeList_person_residenceCountryCode,
											item.representationData_representativeList_person_telephone,
											item.representationData_representativeList_person_zipCode,
											item.representativeList_representativeType,
											item.notes,
											item.userdocProcessId_processNbr,
											item.userdocProcessId_processType))
	except zeep.exceptions.Fault as e:
		return(str(e.message))

class receive(BaseModel):
	arg0:str = ""
	arg1:str = ""
	arg3:str = ""
	arg4_offidocNbr:str = ""
	arg4_offidocOrigin:str = ""
	arg4_offidocSeries:str = ""
	arg4_selected:str = ""
	arg5_officeDepartmentCode:str = ""
	arg5_officeDivisionCode:str = ""
	arg5_officeSectionCode:str = ""
	arg6:str = ""
	arg7_currencyType:str = ""
	arg7_DReceiptAmount:str = ""
	arg7_receiptDate:str = ""
	arg7_receiptNbr:str = ""
	arg7_receiptType:str = ""
	arg8:str = ""
	arg9:str = ""
	arg10_docLog:str = ""
	arg10_docNbr:str = ""
	arg10_docOrigin:str = ""
	arg10_docSeries:str = ""
	arg10_selected:str = ""
	arg11_docSeqName:str = ""
	arg11_docSeqNbr:str = ""
	arg11_docSeqSeries:str = ""
	arg11_docSeqType:str = ""
	arg12_docLog:str = ""
	arg12_docNbr:str = ""
	arg12_docOrigin:str = ""
	arg12_docSeries:str = ""
	arg12_selected:str = ""	
@app.post('/sfe/UserdocReceive', summary="Marcas", tags=["Insert para Escrito afecta Escrito"])
async def insert_receive(item: receive):
	"""
		**Ej:**\n
			"arg0": "1",
			"arg1": "DAJ1",						(tipo de documento)
			"arg3": "true",
			"arg4_offidocNbr": "",
			"arg4_offidocOrigin": "",
			"arg4_offidocSeries": "",
			"arg4_selected": "",
			"arg5_officeDepartmentCode": "",
			"arg5_officeDivisionCode": "",
			"arg5_officeSectionCode": "",
			"arg6": "2023-02-17",					(fecha del evento)
			"arg7_currencyType": "",
			"arg7_DReceiptAmount": "",
			"arg7_receiptDate": "",
			"arg7_receiptNbr": "",
			"arg7_receiptType": "",
			"arg8": "298",						(UserID)
			"arg9": "SFE test - Aplicante SPRINT",
			"arg10_docLog": "E",					(escrito relacionado)
			"arg10_docNbr": "2225891",				(escrito relacionado)
			"arg10_docOrigin": "1",					(escrito relacionado)
			"arg10_docSeries": "2022",				(escrito relacionado)
			"arg10_selected": "",
			"arg11_docSeqName": "",
			"arg11_docSeqNbr": "",
			"arg11_docSeqSeries": "",
			"arg11_docSeqType": "",
			"arg12_docLog": "E",					(escrito nuevo)
			"arg12_docNbr": "22102468",				(escrito nuevo)
			"arg12_docOrigin": "1",					(escrito nuevo)
			"arg12_docSeries": "2022",				(escrito nuevo)
			"arg12_selected": "DAJ1"				(tipo de documento)

	"""
	try:
		return(user_doc_receive(
								item.arg0,
								item.arg1,
								item.arg3,
								item.arg4_offidocNbr,
								item.arg4_offidocOrigin,
								item.arg4_offidocSeries,
								item.arg4_selected,
								item.arg5_officeDepartmentCode,
								item.arg5_officeDivisionCode,
								item.arg5_officeSectionCode,
								item.arg6,
								item.arg7_currencyType,
								item.arg7_DReceiptAmount,
								item.arg7_receiptDate,
								item.arg7_receiptNbr,
								item.arg7_receiptType,
								item.arg8,
								item.arg9,
								item.arg10_docLog,
								item.arg10_docNbr,
								item.arg10_docOrigin,
								item.arg10_docSeries,
								item.arg10_selected,
								item.arg11_docSeqName,
								item.arg11_docSeqNbr,
								item.arg11_docSeqSeries,
								item.arg11_docSeqType,
								item.arg12_docLog,
								item.arg12_docNbr,
								item.arg12_docOrigin,
								item.arg12_docSeries,
								item.arg12_selected
		))
	except zeep.exceptions.Fault as e:
		return(str(e.message))

class userdoc_upd(BaseModel):
	affectedDocumentId_docLog:str = ""
	affectedDocumentId_docNbr:str = ""
	affectedDocumentId_docOrigin:str = ""
	affectedDocumentId_docSeries:str = ""
	applicant_applicantNotes:str = ""
	applicant_person_addressStreet:str = ""
	applicant_person_agentCode:str = ""
	applicant_person_cityCode:str = ""
	applicant_person_cityName:str = ""
	applicant_person_email:str = ""
	applicant_person_nationalityCountryCode:str = ""
	applicant_person_personGroupCode:str = ""
	applicant_person_personGroupName:str = ""
	applicant_person_personName:str = ""
	applicant_person_residenceCountryCode:str = ""
	applicant_person_stateCode:str = ""
	applicant_person_stateName:str = ""
	applicant_person_telephone:str = ""
	applicant_person_zipCode:str = ""
	documentId_docLog:str = ""
	documentId_docNbr:str = ""
	documentId_docOrigin:str = ""
	documentId_docSeries:str = ""
	documentSeqId_docSeqNbr:str = ""
	documentSeqId_docSeqSeries:str = ""
	documentSeqId_docSeqType:str = ""
	filingData_captureDate:str = ""
	filingData_captureUserId:str = ""
	filingData_filingDate:str = ""
	filingData_receptionDate:str = ""
	filingData_paymentList_currencyName:str = ""
	filingData_paymentList_currencyType:str = ""
	filingData_paymentList_receiptAmount:str = ""
	filingData_paymentList_receiptDate:str = ""
	filingData_paymentList_receiptNbr:str = ""
	filingData_paymentList_receiptNotes:str = ""
	filingData_paymentList_receiptType:str = ""
	filingData_paymentList_receiptTypeName:str = ""
	filingData_userdocTypeList_userdocName:str = ""
	filingData_userdocTypeList_userdocType:str = ""
	filingData_documentId_docLog:str = ""
	filingData_documentId_receptionDocument_docNbr:str = ""
	filingData_documentId_receptionDocument_docOrigin:str = ""
	filingData_documentId_receptionDocument_docSeries:str = ""
	filingData_documentId_receptionDocument_selected:str = ""
	newOwnershipData_ownerList_orderNbr:str = ""
	newOwnershipData_ownerList_ownershipNotes:str = ""
	newOwnershipData_ownerList_addressStreet:str = ""
	newOwnershipData_ownerList_cityName:str = ""
	newOwnershipData_ownerList_email:str = ""
	newOwnershipData_ownerList_nationalityCountryCode:str = ""
	newOwnershipData_ownerList_personName:str = ""
	newOwnershipData_ownerList_residenceCountryCode:str = ""
	newOwnershipData_ownerList_telephone:str = ""
	newOwnershipData_ownerList_zipCode:str = ""
	notes:str = ""
	representationData_representativeList_person_addressStreet:str = ""
	representationData_representativeList_person_addressZone:str = ""
	representationData_representativeList_person_agentCode:str = ""
	representationData_representativeList_person_cityName:str = ""
	representationData_representativeList_person_email:str = ""
	representationData_representativeList_person_individualIdNbr:str = ""
	representationData_representativeList_person_individualIdType:str = ""
	representationData_representativeList_person_legalIdNbr:str = ""
	representationData_representativeList_person_legalIdType:str = ""
	representationData_representativeList_person_legalNature:str = ""
	representationData_representativeList_person_nationalityCountryCode:str = ""
	representationData_representativeList_person_personName:str = ""
	representationData_representativeList_person_personNameInOtherLang:str = ""
	representationData_representativeList_person_residenceCountryCode:str = ""
	representationData_representativeList_person_telephone:str = ""
	representationData_representativeList_person_zipCode:str = ""
	representationData_representativeList_representa:str = ""	
@app.post('/sfe/UserdocUpdate', summary="Marcas", tags=["UserDocUpDate con y sin pago"])
async def userdoc_update(item: userdoc_upd):
	try:
		return(user_doc_update(item.affectedDocumentId_docLog,
			item.affectedDocumentId_docNbr,
			item.affectedDocumentId_docOrigin,
			item.affectedDocumentId_docSeries,
			item.applicant_applicantNotes,
			item.applicant_person_addressStreet,
			item.applicant_person_agentCode,
			item.applicant_person_cityCode,
			item.applicant_person_cityName,
			item.applicant_person_email,
			item.applicant_person_nationalityCountryCode,
			item.applicant_person_personGroupCode,
			item.applicant_person_personGroupName,
			item.applicant_person_personName,
			item.applicant_person_residenceCountryCode,
			item.applicant_person_stateCode,
			item.applicant_person_stateName,
			item.applicant_person_telephone,
			item.applicant_person_zipCode,
			item.documentId_docLog,
			item.documentId_docNbr,
			item.documentId_docOrigin,
			item.documentId_docSeries,
			item.documentSeqId_docSeqNbr,
			item.documentSeqId_docSeqSeries,
			item.documentSeqId_docSeqType,
			item.filingData_captureDate,
			item.filingData_captureUserId,
			item.filingData_filingDate,
			item.filingData_receptionDate,
			item.filingData_paymentList_currencyName,
			item.filingData_paymentList_currencyType,
			item.filingData_paymentList_receiptAmount,
			item.filingData_paymentList_receiptDate,
			item.filingData_paymentList_receiptNbr,
			item.filingData_paymentList_receiptNotes,
			item.filingData_paymentList_receiptType,
			item.filingData_paymentList_receiptTypeName,
			item.filingData_userdocTypeList_userdocName,
			item.filingData_userdocTypeList_userdocType,
			item.filingData_documentId_docLog,
			item.filingData_documentId_receptionDocument_docNbr,
			item.filingData_documentId_receptionDocument_docOrigin,
			item.filingData_documentId_receptionDocument_docSeries,
			item.filingData_documentId_receptionDocument_selected,
			item.newOwnershipData_ownerList_orderNbr,
			item.newOwnershipData_ownerList_ownershipNotes,
			item.newOwnershipData_ownerList_addressStreet,
			item.newOwnershipData_ownerList_cityName,
			item.newOwnershipData_ownerList_email,
			item.newOwnershipData_ownerList_nationalityCountryCode,
			item.newOwnershipData_ownerList_personName,
			item.newOwnershipData_ownerList_residenceCountryCode,
			item.newOwnershipData_ownerList_telephone,
			item.newOwnershipData_ownerList_zipCode,
			item.notes,
			item.representationData_representativeList_person_addressStreet,
			item.representationData_representativeList_person_addressZone,
			item.representationData_representativeList_person_agentCode,
			item.representationData_representativeList_person_cityName,
			item.representationData_representativeList_person_email,
			item.representationData_representativeList_person_individualIdNbr,
			item.representationData_representativeList_person_individualIdType,
			item.representationData_representativeList_person_legalIdNbr,
			item.representationData_representativeList_person_legalIdType,
			item.representationData_representativeList_person_legalNature,
			item.representationData_representativeList_person_nationalityCountryCode,
			item.representationData_representativeList_person_personName,
			item.representationData_representativeList_person_personNameInOtherLang,
			item.representationData_representativeList_person_residenceCountryCode,
			item.representationData_representativeList_person_telephone,
			item.representationData_representativeList_person_zipCode,
			item.representationData_representativeList_representa))
	except zeep.exceptions.Fault as e:
		return(str(e.message))

class userdoc_updsr(BaseModel):
	affectedDocumentId_docLog:str = ""
	affectedDocumentId_docNbr:str = ""
	affectedDocumentId_docOrigin:str = ""
	affectedDocumentId_docSeries:str = ""
	applicant_applicantNotes:str = ""
	affectedDocumentId_selected:str = ""
	filingData_userdocTypeList_userdocType:str = ""
	applicant_person_addressStreet:str = ""
	applicant_person_cityName:str = ""
	applicant_person_email:str = ""
	applicant_person_nationalityCountryCode:str = ""
	applicant_person_personName:str = ""
	applicant_person_residenceCountryCode:str = ""
	applicant_person_telephone:str = ""
	applicant_person_zipCode:str = ""
	documentId_docLog:str = ""
	documentId_docNbr:str = ""
	documentId_docOrigin:str = ""
	documentId_docSeries:str = ""
	documentSeqId_docSeqNbr:str = ""
	documentSeqId_docSeqSeries:str = ""
	documentSeqId_docSeqType:str = ""
	filingData_captureDate:str = ""
	filingData_captureUserId:str = ""
	filingData_filingDate:str = ""
	filingData_receptionDate:str = ""
	filingData_receptionDocument_documentId_docLog:str = ""
	filingData_receptionDocument_documentId_docNbr:str = ""
	filingData_receptionDocument_documentId_docOrigin:str = ""
	filingData_receptionDocument_documentId_docSeries:str = ""
	filingData_receptionDocument_documentId_selected:str = ""
	filingData_userdocTypeList_userdocName:str = ""
	newOwnershipData_ownerList_orderNbr:str = ""
	newOwnershipData_ownerList_ownershipNotes:str = ""
	newOwnershipData_ownerList_addressStreet:str = ""
	newOwnershipData_ownerList_cityName:str = ""
	newOwnershipData_ownerList_email:str = ""
	newOwnershipData_ownerList_nationalityCountryCode:str = ""
	newOwnershipData_ownerList_personName:str = ""
	newOwnershipData_ownerList_residenceCountryCode:str = ""
	newOwnershipData_ownerList_telephone:str = ""
	newOwnershipData_ownerList_zipCode:str = ""
	notes:str = ""
	representationData_representativeList_person_addressStreet:str = ""
	representationData_representativeList_person_addressZone:str = ""
	representationData_representativeList_person_agentCode:str = ""
	representationData_representativeList_person_cityName:str = ""
	representationData_representativeList_person_email:str = ""
	representationData_representativeList_person_individualIdNbr:str = ""
	representationData_representativeList_person_individualIdType:str = ""
	representationData_representativeList_person_legalIdNbr:str = ""
	representationData_representativeList_person_legalIdType:str = ""    
	representationData_representativeList_person_legalNature:str = ""
	representationData_representativeList_person_nationalityCountryCode:str = ""
	representationData_representativeList_person_personName:str = ""
	representationData_representativeList_person_personNameInOtherLang:str = ""
	representationData_representativeList_person_residenceCountryCode:str = ""
	representationData_representativeList_person_telephone:str = ""
	representationData_representativeList_person_zipCode:str = ""
	representationData_representativeList_representativeType:str = ""
@app.post('/sfe/UserdocUpdateNotPayment', summary="Marcas", tags=["Escrito con Tipo Documento que afecta a Escritos sin costo"])
async def userdoc_updatesin_recibo(item: userdoc_updsr):
	try:
		return(user_doc_update_sin_recibo(
						item.affectedDocumentId_docLog,
						item.affectedDocumentId_docNbr,
						item.affectedDocumentId_docOrigin,
						item.affectedDocumentId_docSeries,
						item.applicant_applicantNotes,
						item.affectedDocumentId_selected,
						item.filingData_userdocTypeList_userdocType,
						item.applicant_person_addressStreet,
						item.applicant_person_cityName,
						item.applicant_person_email,
						item.applicant_person_nationalityCountryCode,
						item.applicant_person_personName,
						item.applicant_person_residenceCountryCode,
						item.applicant_person_telephone,
						item.applicant_person_zipCode,
						item.documentId_docLog,
						item.documentId_docNbr,
						item.documentId_docOrigin,
						item.documentId_docSeries,
						item.documentSeqId_docSeqNbr,
						item.documentSeqId_docSeqSeries,
						item.documentSeqId_docSeqType,
						item.filingData_captureDate,
						item.filingData_captureUserId,
						item.filingData_filingDate,
						item.filingData_receptionDate,
						item.filingData_receptionDocument_documentId_docLog,
						item.filingData_receptionDocument_documentId_docNbr,
						item.filingData_receptionDocument_documentId_docOrigin,
						item.filingData_receptionDocument_documentId_docSeries,
						item.filingData_receptionDocument_documentId_selected,
						item.filingData_userdocTypeList_userdocName,
						item.newOwnershipData_ownerList_orderNbr,
						item.newOwnershipData_ownerList_ownershipNotes,
						item.newOwnershipData_ownerList_addressStreet,
						item.newOwnershipData_ownerList_cityName,
						item.newOwnershipData_ownerList_email,
						item.newOwnershipData_ownerList_nationalityCountryCode,
						item.newOwnershipData_ownerList_personName,
						item.newOwnershipData_ownerList_residenceCountryCode,
						item.newOwnershipData_ownerList_telephone,
						item.newOwnershipData_ownerList_zipCode,
						item.notes,
						item.representationData_representativeList_person_addressStreet,
						item.representationData_representativeList_person_addressZone,
						item.representationData_representativeList_person_agentCode,
						item.representationData_representativeList_person_cityName,
						item.representationData_representativeList_person_email,
						item.representationData_representativeList_person_individualIdNbr,
						item.representationData_representativeList_person_individualIdType,
						item.representationData_representativeList_person_legalIdNbr,
						item.representationData_representativeList_person_legalIdType,    
						item.representationData_representativeList_person_legalNature,
						item.representationData_representativeList_person_nationalityCountryCode,
						item.representationData_representativeList_person_personName,
						item.representationData_representativeList_person_personNameInOtherLang,
						item.representationData_representativeList_person_residenceCountryCode,
						item.representationData_representativeList_person_telephone,
						item.representationData_representativeList_person_zipCode,
						item.representationData_representativeList_representativeType))
	except zeep.exceptions.Fault as e:
		return(str(e.message))

class userdoc_upd_sr_cr(BaseModel):
	affectedFileIdList_fileNbr:str = ""
	affectedFileIdList_fileSeq:str = ""
	affectedFileIdList_fileSeries:str = ""
	affectedFileIdList_fileType:str = ""                                           
	affectedFileSummaryList_fileId_fileNbr:str = ""
	affectedFileSummaryList_fileId_fileSeq:str = ""
	affectedFileSummaryList_fileId_fileSeries:str = ""
	affectedFileSummaryList_fileId_fileType:str = ""
	affectedFileSummaryList_fileSummaryDescription:str = ""
	affectedFileSummaryList_fileSummaryOwner:str = ""
	applicant_applicantNotes:str = ""
	applicant_addressStreet:str = ""
	applicant_nationalityCountryCode:str = ""
	applicant_personName:str = ""
	applicant_residenceCountryCode:str = ""
	documentId_docLog:str = ""
	documentId_docNbr:str = ""
	documentId_docOrigin:str = ""
	documentId_docSeries:str = ""
	documentId_selected:str = ""
	documentSeqId_docSeqNbr:str = ""
	documentSeqId_docSeqSeries:str = ""
	documentSeqId_docSeqType:str = ""
	filingData_captureDate:str = ""
	filingData_captureUserId:str = ""
	filingData_filingDate:str = ""
	filingData_documentId_docLog:str = ""
	filingData_documentId_docNbr:str = ""
	filingData_documentId_docOrigin:str = ""
	filingData_documentId_docSeries:str = ""
	filingData_userdocTypeList_userdocName:str = ""
	filingData_userdocTypeList_userdocType:str = ""
	ownerList_person_addressStreet:str = ""
	ownerList_person_email:str = ""
	ownerList_person_nationalityCountryCode:str = ""
	ownerList_person_personName:str = ""
	ownerList_person_residenceCountryCode:str = ""
	ownerList_person_telephone:str = ""
	ownerList_person_zipCode:str = ""
	notes:str = ""
	representativeList_person_addressStreet:str = ""
	representativeList_person_agentCode:str = ""
	representativeList_person_email:str = ""
	representativeList_person_nationalityCountryCode:str = ""
	representativeList_person_personName:str = ""
	representativeList_person_residenceCountryCode:str = ""
	representativeList_person_telephone:str = ""
	representativeList_person_zipCode:str = ""
	representativeList_representativeType:str = ""
@app.post('/sfe/insertuserdoc_sr_cr', summary="Marcas", tags=["Escrito con Tipo Documento que afecta a Expedientes sin costo"])
def insert_user_doc_sin_recibo_con_exp(item:userdoc_upd_sr_cr):
	try:
		return(Insert_user_doc_sin_recibo_con_relacion(
				item.affectedFileIdList_fileNbr,
				item.affectedFileIdList_fileSeq,
				item.affectedFileIdList_fileSeries,
				item.affectedFileIdList_fileType,                                           
				item.affectedFileSummaryList_fileId_fileNbr,
				item.affectedFileSummaryList_fileId_fileSeq,
				item.affectedFileSummaryList_fileId_fileSeries,
				item.affectedFileSummaryList_fileId_fileType,
				item.affectedFileSummaryList_fileSummaryDescription,
				item.affectedFileSummaryList_fileSummaryOwner,
				item.applicant_applicantNotes,
				item.applicant_addressStreet,
				item.applicant_nationalityCountryCode,
				item.applicant_personName,
				item.applicant_residenceCountryCode,
				item.documentId_docLog,
				item.documentId_docNbr,
				item.documentId_docOrigin,
				item.documentId_docSeries,
				item.documentId_selected,
				item.documentSeqId_docSeqNbr,
				item.documentSeqId_docSeqSeries,
				item.documentSeqId_docSeqType,
				item.filingData_captureDate,
				item.filingData_captureUserId,
				item.filingData_filingDate,
				item.filingData_documentId_docLog,
				item.filingData_documentId_docNbr,
				item.filingData_documentId_docOrigin,
				item.filingData_documentId_docSeries,
				item.filingData_userdocTypeList_userdocName,
				item.filingData_userdocTypeList_userdocType,
				item.ownerList_person_addressStreet,
				item.ownerList_person_email,
				item.ownerList_person_nationalityCountryCode,
				item.ownerList_person_personName,
				item.ownerList_person_residenceCountryCode,
				item.ownerList_person_telephone,
				item.ownerList_person_zipCode,
				item.notes,
				item.representativeList_person_addressStreet,
				item.representativeList_person_agentCode,
				item.representativeList_person_email,
				item.representativeList_person_nationalityCountryCode,
				item.representativeList_person_personName,
				item.representativeList_person_residenceCountryCode,
				item.representativeList_person_telephone,
				item.representativeList_person_zipCode,
				item.representativeList_representativeType))
	except zeep.exceptions.Fault as e:
		return(str(e.message))


class insert_reg(BaseModel):
	file_fileId_fileNbr:str = ""
	file_fileId_fileSeq:str = ""
	file_fileId_fileSeries:str = ""
	file_fileId_fileType:str = ""
	file_filingData_applicationSubtype:str = ""
	file_filingData_applicationType:str = ""
	file_filingData_captureUserId:str = ""
	file_filingData_filingDate:str = ""
	file_filingData_captureDate:str = ""
	file_filingData_lawCode:str = ""
	file_filingData_paymentList_currencyType:str = ""
	file_filingData_paymentList_receiptAmount:str = ""
	file_filingData_paymentList_receiptDate:str = ""
	file_filingData_paymentList_receiptNbr:str = ""
	file_filingData_paymentList_receiptNotes:str = ""
	file_filingData_paymentList_receiptType:str = ""
	file_filingData_receptionUserId:str = ""
	file_ownershipData_ownerList_person_addressStreet:str = ""
	file_ownershipData_ownerList_person_nationalityCountryCode:str = ""
	file_ownershipData_ownerList_person_personName:str = ""
	file_ownershipData_ownerList_person_residenceCountryCode:str = ""
	file_rowVersion:str = ""
	agentCode:str = ""
	file_representationData_representativeList_representativeType:str = ""
	rowVersion:str = ""
	protectionData_dummy:str = ""
	protectionData_niceClassList_niceClassDescription:str = ""
	protectionData_niceClassList_niceClassDetailedStatus:str = ""
	protectionData_niceClassList_niceClassEdition:str = ""
	protectionData_niceClassList_niceClassGlobalStatus:str = ""
	protectionData_niceClassList_niceClassNbr:str = ""
	protectionData_niceClassList_niceClassVersion:str = ""
	logoData:str = ""
	logoType:str = ""
	signData_markName:str = ""
	signData_signType:str = ""
@app.post('/sfe/insert_reg', summary="Marcas", tags=["Insert para registro de marcas"])
async def insertreg(item: insert_reg):
	try:
		if str(item.logoData).count('https:') >= 1:
			imageurltob64 = image_url_to_b64(str(item.logoData))
			return(mark_insert_reg(
								item.file_fileId_fileNbr,
								item.file_fileId_fileSeq,
								item.file_fileId_fileSeries,
								item.file_fileId_fileType,
								item.file_filingData_applicationSubtype,
								item.file_filingData_applicationType,
								item.file_filingData_captureUserId,
								item.file_filingData_filingDate,
								item.file_filingData_captureDate,
								item.file_filingData_lawCode,
								item.file_filingData_paymentList_currencyType,
								item.file_filingData_paymentList_receiptAmount,
								item.file_filingData_paymentList_receiptDate,
								item.file_filingData_paymentList_receiptNbr,
								item.file_filingData_paymentList_receiptNotes,
								item.file_filingData_paymentList_receiptType,
								item.file_filingData_receptionUserId,
								item.file_ownershipData_ownerList_person_addressStreet,
								item.file_ownershipData_ownerList_person_nationalityCountryCode,
								item.file_ownershipData_ownerList_person_personName,
								item.file_ownershipData_ownerList_person_residenceCountryCode,
								item.file_rowVersion,
								item.agentCode,
								item.file_representationData_representativeList_representativeType,
								item.rowVersion,
								item.protectionData_dummy,
								item.protectionData_niceClassList_niceClassDescription,
								item.protectionData_niceClassList_niceClassDetailedStatus,
								item.protectionData_niceClassList_niceClassEdition,
								item.protectionData_niceClassList_niceClassGlobalStatus,
								item.protectionData_niceClassList_niceClassNbr,
								item.protectionData_niceClassList_niceClassVersion,
								imageurltob64,
								item.logoType,
								item.signData_markName,
								item.signData_signType))
		else:
			return(mark_insert_reg(
								item.file_fileId_fileNbr,
								item.file_fileId_fileSeq,
								item.file_fileId_fileSeries,
								item.file_fileId_fileType,
								item.file_filingData_applicationSubtype,
								item.file_filingData_applicationType,
								item.file_filingData_captureUserId,
								item.file_filingData_filingDate,
								item.file_filingData_captureDate,
								item.file_filingData_lawCode,
								item.file_filingData_paymentList_currencyType,
								item.file_filingData_paymentList_receiptAmount,
								item.file_filingData_paymentList_receiptDate,
								item.file_filingData_paymentList_receiptNbr,
								item.file_filingData_paymentList_receiptNotes,
								item.file_filingData_paymentList_receiptType,
								item.file_filingData_receptionUserId,
								item.file_ownershipData_ownerList_person_addressStreet,
								item.file_ownershipData_ownerList_person_nationalityCountryCode,
								item.file_ownershipData_ownerList_person_personName,
								item.file_ownershipData_ownerList_person_residenceCountryCode,
								item.file_rowVersion,
								item.agentCode,
								item.file_representationData_representativeList_representativeType,
								item.rowVersion,
								item.protectionData_dummy,
								item.protectionData_niceClassList_niceClassDescription,
								item.protectionData_niceClassList_niceClassDetailedStatus,
								item.protectionData_niceClassList_niceClassEdition,
								item.protectionData_niceClassList_niceClassGlobalStatus,
								item.protectionData_niceClassList_niceClassNbr,
								item.protectionData_niceClassList_niceClassVersion,
								item.logoData,
								item.logoType,
								item.signData_markName,
								item.signData_signType))			
	except zeep.exceptions.Fault as e:
		return(str(e.message))

class insert_ren(BaseModel):
	file_fileId_fileNbr:str = ""
	file_fileId_fileSeq:str = ""
	file_fileId_fileSeries:str = ""
	file_fileId_fileType:str = ""
	file_filingData_applicationSubtype:str = ""
	file_filingData_applicationType:str = ""
	file_filingData_captureUserId:str = ""
	file_filingData_captureDate:str = ""
	file_filingData_filingDate:str = ""
	file_filingData_lawCode:str = ""
	file_filingData_paymentList_currencyType:str = ""
	file_filingData_paymentList_receiptAmount:str = ""
	file_filingData_paymentList_receiptDate:str = ""
	file_filingData_paymentList_receiptNbr:str = ""
	file_filingData_paymentList_receiptNotes:str = ""
	file_filingData_paymentList_receiptType:str = ""
	file_filingData_receptionUserId:str = ""
	file_ownershipData_ownerList_person_addressStreet:str = ""
	file_ownershipData_ownerList_person_nationalityCountryCode:str = ""
	file_ownershipData_ownerList_person_personName:str = ""
	file_ownershipData_ownerList_person_residenceCountryCode:str = ""
	file_representationData_representativeList_representativeType:str = ""
	agentCode:str = ""
	file_relationshipList_fileId_fileNbr:str = ""
	file_relationshipList_fileId_fileSeq:str = ""
	file_relationshipList_fileId_fileSeries:str = ""
	file_relationshipList_fileId_fileType:str = ""
	file_relationshipList_relationshipRole:str = ""
	file_relationshipList_relationshipType:str = ""
	file_rowVersion:str = ""
	protectionData_dummy:str = ""
	protectionData_niceClassList_niceClassDescription:str = ""
	protectionData_niceClassList_niceClassDetailedStatus:str = ""
	protectionData_niceClassList_niceClassEdition:str = ""
	protectionData_niceClassList_niceClassGlobalStatus:str = ""
	protectionData_niceClassList_niceClassNbr:str = ""
	protectionData_niceClassList_niceClassVersion:str = ""
	rowVersion:str = ""
	logoData:str = ""
	logoType:str = ""
	signData_markName:str = ""
	signData_signType:str = ""
@app.post('/sfe/insert_ren', summary="Marcas", tags=["Insert para renovacion de marcas"])
async def insertren(item: insert_ren):
	try:
		return(mark_insert_ren(item.file_fileId_fileNbr,
							item.file_fileId_fileSeq,
							item.file_fileId_fileSeries,
							item.file_fileId_fileType,
							item.file_filingData_applicationSubtype,
							item.file_filingData_applicationType,
							item.file_filingData_captureUserId,
							item.file_filingData_captureDate,
							item.file_filingData_filingDate,
							item.file_filingData_lawCode,
							item.file_filingData_paymentList_currencyType,
							item.file_filingData_paymentList_receiptAmount,
							item.file_filingData_paymentList_receiptDate,
							item.file_filingData_paymentList_receiptNbr,
							item.file_filingData_paymentList_receiptNotes,
							item.file_filingData_paymentList_receiptType,
							item.file_filingData_receptionUserId,
							item.file_ownershipData_ownerList_person_addressStreet,
							item.file_ownershipData_ownerList_person_nationalityCountryCode,
							item.file_ownershipData_ownerList_person_personName,
							item.file_ownershipData_ownerList_person_residenceCountryCode,
							item.file_representationData_representativeList_representativeType,
							item.agentCode,
							item.file_relationshipList_fileId_fileNbr,
							item.file_relationshipList_fileId_fileSeq,
							item.file_relationshipList_fileId_fileSeries,
							item.file_relationshipList_fileId_fileType,
							item.file_relationshipList_relationshipRole,
							item.file_relationshipList_relationshipType,
							item.file_rowVersion,
							item.protectionData_dummy,
							item.protectionData_niceClassList_niceClassDescription,
							item.protectionData_niceClassList_niceClassDetailedStatus,
							item.protectionData_niceClassList_niceClassEdition,
							item.protectionData_niceClassList_niceClassGlobalStatus,
							item.protectionData_niceClassList_niceClassNbr,
							item.protectionData_niceClassList_niceClassVersion,
							item.rowVersion,
							item.logoData,
							item.logoType,
							item.signData_markName,
							item.signData_signType))
	except zeep.exceptions.Fault as e:
		return(str(e.message))

class insert_user_doc_full(BaseModel):
	affectedFileIdList_fileNbr:str = ""
	affectedFileIdList_fileSeq:str = ""
	affectedFileIdList_fileSeries:str = ""
	affectedFileIdList_fileType:str = ""
	affectedFileSummaryList_disclaimer:str = ""
	affectedFileSummaryList_disclaimerInOtherLang:str = ""
	affectedFileSummaryList_fileNbr:str = ""
	affectedFileSummaryList_fileSeq:str = ""
	affectedFileSummaryList_fileSeries:str = ""
	affectedFileSummaryList_fileType:str = ""
	affectedFileSummaryList_fileIdAsString:str = ""
	affectedFileSummaryList_fileSummaryClasses:str = ""
	affectedFileSummaryList_fileSummaryCountry:str = ""
	affectedFileSummaryList_fileSummaryDescription:str = ""
	affectedFileSummaryList_fileSummaryDescriptionInOtherLang:str = ""
	affectedFileSummaryList_fileSummaryOwner:str = ""
	affectedFileSummaryList_fileSummaryOwnerInOtherLang:str = ""
	affectedFileSummaryList_fileSummaryRepresentative:str = ""
	affectedFileSummaryList_fileSummaryRepresentativeInOtherLang:str = ""
	affectedFileSummaryList_fileSummaryResponsibleName:str = ""
	affectedFileSummaryList_fileSummaryStatus:str = ""
	applicant_applicantNotes:str = ""
	applicant_person_addressStreet:str = ""
	applicant_person_addressStreetInOtherLang:str = ""
	applicant_person_addressZone:str = ""
	applicant_person_agentCode:str = ""
	applicant_person_cityCode:str = ""
	applicant_person_cityName:str = ""
	applicant_person_companyRegisterRegistrationDate:str = ""
	applicant_person_companyRegisterRegistrationNbr:str = ""
	applicant_person_email:str = ""
	applicant_person_individualIdNbr:str = ""
	applicant_person_individualIdType:str = ""
	applicant_person_legalIdNbr:str = ""
	applicant_person_legalIdType:str = ""
	applicant_person_legalNature:str = ""
	applicant_person_legalNatureInOtherLang:str = ""
	applicant_person_nationalityCountryCode:str = ""
	applicant_person_personGroupCode:str = ""
	applicant_person_personGroupName:str = ""
	applicant_person_personName:str = ""
	applicant_person_personNameInOtherLang:str = ""
	applicant_person_residenceCountryCode:str = ""
	applicant_person_stateCode:str = ""
	applicant_person_stateName:str = ""
	applicant_person_telephone:str = ""
	applicant_person_zipCode:str = ""
	documentId_docLog:str = ""
	documentId_docNbr:str = ""
	documentId_docOrigin:str = ""
	documentId_docSeries:str = ""
	documentId_selected:str = ""
	documentSeqId_docSeqName:str = ""
	documentSeqId_docSeqNbr:str = ""
	documentSeqId_docSeqSeries:str = ""
	documentSeqId_docSeqType:str = ""
	filingData_applicationSubtype:str = ""
	filingData_applicationType:str = ""
	filingData_captureDate:str = ""
	filingData_captureUserId:str = ""
	filingData_filingDate:str = ""
	filingData_lawCode:str = ""
	filingData_novelty1Date:str = ""
	filingData_novelty2Date:str = ""
	filingData_paymentList_currencyName:str = ""
	filingData_paymentList_currencyType:str = ""
	filingData_paymentList_receiptAmount:str = ""
	filingData_paymentList_receiptDate:str = ""
	filingData_paymentList_receiptNbr:str = ""
	filingData_paymentList_receiptNotes:str = ""
	filingData_paymentList_receiptType:str = ""
	filingData_paymentList_receiptTypeName:str = ""
	filingData_receptionDate:str = ""
	filingData_documentId_receptionDocument_docLog:str = ""
	filingData_documentId_receptionDocument_docNbr:str = ""
	filingData_documentId_receptionDocument_docOrigin:str = ""
	filingData_documentId_receptionDocument_docSeries:str = ""
	filingData_documentId_receptionDocument_selected:str = ""
	filingData_userdocTypeList_userdocName:str = ""
	filingData_userdocTypeList_userdocType:str = ""
	newOwnershipData_ownerList_orderNbr:str = ""
	newOwnershipData_ownerList_ownershipNotes:str = ""
	newOwnershipData_ownerList_person_addressStreet:str = ""
	newOwnershipData_ownerList_person_addressStreetInOtherLang:str = ""
	newOwnershipData_ownerList_person_addressZone:str = ""
	newOwnershipData_ownerList_person_agentCode:str = ""
	newOwnershipData_ownerList_person_cityCode:str = ""
	newOwnershipData_ownerList_person_cityName:str = ""
	newOwnershipData_ownerList_person_companyRegisterRegistrationDate:str = ""
	newOwnershipData_ownerList_person_companyRegisterRegistrationNbr:str = ""
	newOwnershipData_ownerList_person_email:str = ""
	newOwnershipData_ownerList_person_individualIdNbr:str = ""
	newOwnershipData_ownerList_person_individualIdType:str = ""
	newOwnershipData_ownerList_person_legalIdNbr:str = ""
	newOwnershipData_ownerList_person_legalIdType:str = ""
	newOwnershipData_ownerList_person_legalNature:str = ""
	newOwnershipData_ownerList_person_legalNatureInOtherLang:str = ""
	newOwnershipData_ownerList_person_nationalityCountryCode:str = ""
	newOwnershipData_ownerList_person_personGroupCode:str = ""
	newOwnershipData_ownerList_person_personGroupName:str = ""
	newOwnershipData_ownerList_person_personName:str = ""
	newOwnershipData_ownerList_person_personNameInOtherLang:str = ""
	newOwnershipData_ownerList_person_residenceCountryCode:str = ""
	newOwnershipData_ownerList_person_stateCode:str = ""
	newOwnershipData_ownerList_person_stateName:str = ""
	newOwnershipData_ownerList_person_telephone:str = ""
	newOwnershipData_ownerList_person_zipCode:str = ""
	notes:str = ""
	poaData_poaGranteeList_person_addressStreet:str = ""
	poaData_poaGranteeList_person_addressStreetInOtherLang:str = ""
	poaData_poaGranteeList_person_addressZone:str = ""
	poaData_poaGranteeList_person_agentCode:str = ""
	poaData_poaGranteeList_person_cityCode:str = ""
	poaData_poaGranteeList_person_cityName:str = ""
	poaData_poaGranteeList_person_companyRegisterRegistrationDate:str = ""
	poaData_poaGranteeList_person_companyRegisterRegistrationNbr:str = ""
	poaData_poaGranteeList_person_email:str = ""
	poaData_poaGranteeList_person_individualIdNbr:str = ""
	poaData_poaGranteeList_person_individualIdType:str = ""
	poaData_poaGranteeList_person_legalIdNbr:str = ""
	poaData_poaGranteeList_person_legalIdType:str = ""
	poaData_poaGranteeList_person_legalNature:str = ""
	poaData_poaGranteeList_person_legalNatureInOtherLang:str = ""
	poaData_poaGranteeList_person_nationalityCountryCode:str = ""
	poaData_poaGranteeList_person_personGroupCode:str = ""
	poaData_poaGranteeList_person_personGroupName:str = ""
	poaData_poaGranteeList_person_personName:str = ""
	poaData_poaGranteeList_person_personNameInOtherLang:str = ""
	poaData_poaGranteeList_person_residenceCountryCode:str = ""
	poaData_poaGranteeList_person_stateCode:str = ""
	poaData_poaGranteeList_person_stateName:str = ""
	poaData_poaGranteeList_person_telephone:str = ""
	poaData_poaGranteeList_person_zipCode:str = ""
	poaData_poaGrantor_person_addressStreet:str = ""
	poaData_poaGrantor_person_addressStreetInOtherLang:str = ""
	poaData_poaGrantor_person_addressZone:str = ""
	poaData_poaGrantor_person_agentCode:str = ""
	poaData_poaGrantor_person_cityCode:str = ""
	poaData_poaGrantor_person_cityName:str = ""
	poaData_poaGrantor_person_companyRegisterRegistrationDate:str = ""
	poaData_poaGrantor_person_companyRegisterRegistrationNbr:str = ""
	poaData_poaGrantor_person_email:str = ""
	poaData_poaGrantor_person_individualIdNbr:str = ""
	poaData_poaGrantor_person_individualIdType:str = ""
	poaData_poaGrantor_person_legalIdNbr:str = ""
	poaData_poaGrantor_person_legalIdType:str = ""
	poaData_poaGrantor_person_legalNature:str = ""
	poaData_poaGrantor_person_legalNatureInOtherLang:str = ""
	poaData_poaGrantor_person_nationalityCountryCode:str = ""
	poaData_poaGrantor_person_personGroupCode:str = ""
	poaData_poaGrantor_person_personGroupName:str = ""
	poaData_poaGrantor_person_personName:str = ""
	poaData_poaGrantor_person_personNameInOtherLang:str = ""
	poaData_poaGrantor_person_residenceCountryCode:str = ""
	poaData_poaGrantor_person_stateCode:str = ""
	poaData_poaGrantor_person_stateName:str = ""
	poaData_poaGrantor_person_telephone:str = ""
	poaData_poaGrantor_person_zipCode:str = ""
	poaData_poaRegNumber:str = ""
	poaData_scope:str = ""
	representationData_representativeList_person_addressStreet:str = ""
	representationData_representativeList_person_addressStreetInOtherLang:str = ""
	representationData_representativeList_person_addressZone:str = ""
	representationData_representativeList_person_agentCode:str = ""
	representationData_representativeList_person_cityCode:str = ""
	representationData_representativeList_person_cityName:str = ""
	representationData_representativeList_person_companyRegisterRegistrationDate:str = ""
	representationData_representativeList_person_companyRegisterRegistrationNbr:str = ""
	representationData_representativeList_person_email:str = ""
	representationData_representativeList_person_individualIdNbr:str = ""
	representationData_representativeList_person_individualIdType:str = ""
	representationData_representativeList_person_legalIdNbr:str = ""
	representationData_representativeList_person_legalIdType:str = ""
	representationData_representativeList_person_legalNature:str = ""
	representationData_representativeList_person_legalNatureInOtherLang:str = ""
	representationData_representativeList_person_nationalityCountryCode:str = ""
	representationData_representativeList_person_personGroupCode:str = ""
	representationData_representativeList_person_personGroupName:str = ""
	representationData_representativeList_person_personName:str = ""
	representationData_representativeList_person_personNameInOtherLang:str = ""
	representationData_representativeList_person_residenceCountryCode:str = ""
	representationData_representativeList_person_stateCode:str = ""
	representationData_representativeList_person_stateName:str = ""
	representationData_representativeList_person_telephone:str = ""
	representationData_representativeList_person_zipCode:str = ""
	representationData_representativeList_representativeType:str = ""
@app.post('/sfe/insertEscrito', summary="SFE", tags=["InsertUserDocMarcas prueba para insertar todos los escritos"])
async def insert_escritos(item:insert_user_doc_full):
	return(insert_user_doc_escritos(item.affectedFileIdList_fileNbr,
							item.affectedFileIdList_fileSeq,
							item.affectedFileIdList_fileSeries,
							item.affectedFileIdList_fileType,
							item.affectedFileSummaryList_disclaimer,
							item.affectedFileSummaryList_disclaimerInOtherLang,
							item.affectedFileSummaryList_fileNbr,
							item.affectedFileSummaryList_fileSeq,
							item.affectedFileSummaryList_fileSeries,
							item.affectedFileSummaryList_fileType,
							item.affectedFileSummaryList_fileIdAsString,
							item.affectedFileSummaryList_fileSummaryClasses,
							item.affectedFileSummaryList_fileSummaryCountry,
							item.affectedFileSummaryList_fileSummaryDescription,
							item.affectedFileSummaryList_fileSummaryDescriptionInOtherLang,
							item.affectedFileSummaryList_fileSummaryOwner,
							item.affectedFileSummaryList_fileSummaryOwnerInOtherLang,
							item.affectedFileSummaryList_fileSummaryRepresentative,
							item.affectedFileSummaryList_fileSummaryRepresentativeInOtherLang,
							item.affectedFileSummaryList_fileSummaryResponsibleName,
							item.affectedFileSummaryList_fileSummaryStatus,
							item.applicant_applicantNotes,
							item.applicant_person_addressStreet,
							item.applicant_person_addressStreetInOtherLang,
							item.applicant_person_addressZone,
							item.applicant_person_agentCode,
							item.applicant_person_cityCode,
							item.applicant_person_cityName,
							item.applicant_person_companyRegisterRegistrationDate,
							item.applicant_person_companyRegisterRegistrationNbr,
							item.applicant_person_email,
							item.applicant_person_individualIdNbr,
							item.applicant_person_individualIdType,
							item.applicant_person_legalIdNbr,
							item.applicant_person_legalIdType,
							item.applicant_person_legalNature,
							item.applicant_person_legalNatureInOtherLang,
							item.applicant_person_nationalityCountryCode,
							item.applicant_person_personGroupCode,
							item.applicant_person_personGroupName,
							item.applicant_person_personName,
							item.applicant_person_personNameInOtherLang,
							item.applicant_person_residenceCountryCode,
							item.applicant_person_stateCode,
							item.applicant_person_stateName,
							item.applicant_person_telephone,
							item.applicant_person_zipCode,
							item.documentId_docLog,
							item.documentId_docNbr,
							item.documentId_docOrigin,
							item.documentId_docSeries,
							item.documentId_selected,
							item.documentSeqId_docSeqName,
							item.documentSeqId_docSeqNbr,
							item.documentSeqId_docSeqSeries,
							item.documentSeqId_docSeqType,
							item.filingData_applicationSubtype,
							item.filingData_applicationType,
							item.filingData_captureDate,
							item.filingData_captureUserId,
							item.filingData_filingDate,
							item.filingData_lawCode,
							item.filingData_novelty1Date,
							item.filingData_novelty2Date,
							item.filingData_paymentList_currencyName,
							item.filingData_paymentList_currencyType,
							item.filingData_paymentList_receiptAmount,
							item.filingData_paymentList_receiptDate,
							item.filingData_paymentList_receiptNbr,
							item.filingData_paymentList_receiptNotes,
							item.filingData_paymentList_receiptType,
							item.filingData_paymentList_receiptTypeName,
							item.filingData_receptionDate,
							item.filingData_documentId_receptionDocument_docLog,
							item.filingData_documentId_receptionDocument_docNbr,
							item.filingData_documentId_receptionDocument_docOrigin,
							item.filingData_documentId_receptionDocument_docSeries,
							item.filingData_documentId_receptionDocument_selected,
							item.filingData_userdocTypeList_userdocName,
							item.filingData_userdocTypeList_userdocType,
							item.newOwnershipData_ownerList_orderNbr,
							item.newOwnershipData_ownerList_ownershipNotes,
							item.newOwnershipData_ownerList_person_addressStreet,
							item.newOwnershipData_ownerList_person_addressStreetInOtherLang,
							item.newOwnershipData_ownerList_person_addressZone,
							item.newOwnershipData_ownerList_person_agentCode,
							item.newOwnershipData_ownerList_person_cityCode,
							item.newOwnershipData_ownerList_person_cityName,
							item.newOwnershipData_ownerList_person_companyRegisterRegistrationDate,
							item.newOwnershipData_ownerList_person_companyRegisterRegistrationNbr,
							item.newOwnershipData_ownerList_person_email,
							item.newOwnershipData_ownerList_person_individualIdNbr,
							item.newOwnershipData_ownerList_person_individualIdType,
							item.newOwnershipData_ownerList_person_legalIdNbr,
							item.newOwnershipData_ownerList_person_legalIdType,
							item.newOwnershipData_ownerList_person_legalNature,
							item.newOwnershipData_ownerList_person_legalNatureInOtherLang,
							item.newOwnershipData_ownerList_person_nationalityCountryCode,
							item.newOwnershipData_ownerList_person_personGroupCode,
							item.newOwnershipData_ownerList_person_personGroupName,
							item.newOwnershipData_ownerList_person_personName,
							item.newOwnershipData_ownerList_person_personNameInOtherLang,
							item.newOwnershipData_ownerList_person_residenceCountryCode,
							item.newOwnershipData_ownerList_person_stateCode,
							item.newOwnershipData_ownerList_person_stateName,
							item.newOwnershipData_ownerList_person_telephone,
							item.newOwnershipData_ownerList_person_zipCode,
							item.notes,
							item.poaData_poaGranteeList_person_addressStreet,
							item.poaData_poaGranteeList_person_addressStreetInOtherLang,
							item.poaData_poaGranteeList_person_addressZone,
							item.poaData_poaGranteeList_person_agentCode,
							item.poaData_poaGranteeList_person_cityCode,
							item.poaData_poaGranteeList_person_cityName,
							item.poaData_poaGranteeList_person_companyRegisterRegistrationDate,
							item.poaData_poaGranteeList_person_companyRegisterRegistrationNbr,
							item.poaData_poaGranteeList_person_email,
							item.poaData_poaGranteeList_person_individualIdNbr,
							item.poaData_poaGranteeList_person_individualIdType,
							item.poaData_poaGranteeList_person_legalIdNbr,
							item.poaData_poaGranteeList_person_legalIdType,
							item.poaData_poaGranteeList_person_legalNature,
							item.poaData_poaGranteeList_person_legalNatureInOtherLang,
							item.poaData_poaGranteeList_person_nationalityCountryCode,
							item.poaData_poaGranteeList_person_personGroupCode,
							item.poaData_poaGranteeList_person_personGroupName,
							item.poaData_poaGranteeList_person_personName,
							item.poaData_poaGranteeList_person_personNameInOtherLang,
							item.poaData_poaGranteeList_person_residenceCountryCode,
							item.poaData_poaGranteeList_person_stateCode,
							item.poaData_poaGranteeList_person_stateName,
							item.poaData_poaGranteeList_person_telephone,
							item.poaData_poaGranteeList_person_zipCode,
							item.poaData_poaGrantor_person_addressStreet,
							item.poaData_poaGrantor_person_addressStreetInOtherLang,
							item.poaData_poaGrantor_person_addressZone,
							item.poaData_poaGrantor_person_agentCode,
							item.poaData_poaGrantor_person_cityCode,
							item.poaData_poaGrantor_person_cityName,
							item.poaData_poaGrantor_person_companyRegisterRegistrationDate,
							item.poaData_poaGrantor_person_companyRegisterRegistrationNbr,
							item.poaData_poaGrantor_person_email,
							item.poaData_poaGrantor_person_individualIdNbr,
							item.poaData_poaGrantor_person_individualIdType,
							item.poaData_poaGrantor_person_legalIdNbr,
							item.poaData_poaGrantor_person_legalIdType,
							item.poaData_poaGrantor_person_legalNature,
							item.poaData_poaGrantor_person_legalNatureInOtherLang,
							item.poaData_poaGrantor_person_nationalityCountryCode,
							item.poaData_poaGrantor_person_personGroupCode,
							item.poaData_poaGrantor_person_personGroupName,
							item.poaData_poaGrantor_person_personName,
							item.poaData_poaGrantor_person_personNameInOtherLang,
							item.poaData_poaGrantor_person_residenceCountryCode,
							item.poaData_poaGrantor_person_stateCode,
							item.poaData_poaGrantor_person_stateName,
							item.poaData_poaGrantor_person_telephone,
							item.poaData_poaGrantor_person_zipCode,
							item.poaData_poaRegNumber,
							item.poaData_scope,
							item.representationData_representativeList_person_addressStreet,
							item.representationData_representativeList_person_addressStreetInOtherLang,
							item.representationData_representativeList_person_addressZone,
							item.representationData_representativeList_person_agentCode,
							item.representationData_representativeList_person_cityCode,
							item.representationData_representativeList_person_cityName,
							item.representationData_representativeList_person_companyRegisterRegistrationDate,
							item.representationData_representativeList_person_companyRegisterRegistrationNbr,
							item.representationData_representativeList_person_email,
							item.representationData_representativeList_person_individualIdNbr,
							item.representationData_representativeList_person_individualIdType,
							item.representationData_representativeList_person_legalIdNbr,
							item.representationData_representativeList_person_legalIdType,
							item.representationData_representativeList_person_legalNature,
							item.representationData_representativeList_person_legalNatureInOtherLang,
							item.representationData_representativeList_person_nationalityCountryCode,
							item.representationData_representativeList_person_personGroupCode,
							item.representationData_representativeList_person_personGroupName,
							item.representationData_representativeList_person_personName,
							item.representationData_representativeList_person_personNameInOtherLang,
							item.representationData_representativeList_person_residenceCountryCode,
							item.representationData_representativeList_person_stateCode,
							item.representationData_representativeList_person_stateName,
							item.representationData_representativeList_person_telephone,
							item.representationData_representativeList_person_zipCode,
							item.representationData_representativeList_representativeType))

class for_id(BaseModel):
	Id:str = ""
@app.post('/sfe/recep_registro', summary="SFE", tags=["Presentación de registro SFE"])
async def sfe_reg_capture(item:for_id):
	full_res = {
			'id':'',
			'fecha':'',
			'formulario_id':'',
			'estado':'',
			'created_at':'',
			'updated_at':'',
			'respuestas':{

			},
			'costo':'',
			'usuario_id':'',
			'deleted_at ':'',
			'codigo':'',
			'firmado_at':'',
			'pagado_at':'',
			'expediente_id':'',
			'pdf_url':'',
			'enviado_at':'',
			'recepcionado_at':'',
			'nom_funcionario':'',
			'pdf':'',
			'expediente_afectado':'',
			'notificacion_id':'',
			'expedientes_autor':'',
			'autorizado_por_id':'',
			'locked_at':'',
			'locked_by_id':''
}
	return(registro_sfe(item.Id))

@app.post('/sfe/recep_renovacion', summary="SFE", tags=["Presentación de renovacion SFE"])
async def sfe_ren_capture(item:for_id):
	full_res = {
			'id':'',
			'fecha':'',
			'formulario_id':'',
			'estado':'',
			'created_at':'',
			'updated_at':'',
			'respuestas':{

			},
			'costo':'',
			'usuario_id':'',
			'deleted_at ':'',
			'codigo':'',
			'firmado_at':'',
			'pagado_at':'',
			'expediente_id':'',
			'pdf_url':'',
			'enviado_at':'',
			'recepcionado_at':'',
			'nom_funcionario':'',
			'pdf':'',
			'expediente_afectado':'',
			'notificacion_id':'',
			'expedientes_autor':'',
			'autorizado_por_id':'',
			'locked_at':'',
			'locked_by_id':''
}
	return(renovacion_sfe(item.ID))

@app.post('/sfe/recep_oposicion', summary="SFE", tags=["Presentación de oposicion SFE"])
async def sfe_opo_capture(item:for_id):
	full_res = {
			'id':'',
			'fecha':'',
			'formulario_id':'',
			'estado':'',
			'created_at':'',
			'updated_at':'',
			'respuestas':{

			},
			'costo':'',
			'usuario_id':'',
			'deleted_at ':'',
			'codigo':'',
			'firmado_at':'',
			'pagado_at':'',
			'expediente_id':'',
			'pdf_url':'',
			'enviado_at':'',
			'recepcionado_at':'',
			'nom_funcionario':'',
			'pdf':'',
			'expediente_afectado':'',
			'notificacion_id':'',
			'expedientes_autor':'',
			'autorizado_por_id':'',
			'locked_at':'',
			'locked_by_id':''
}
	return(oposicion_sfe(item.ID))

@app.post('/sis/test', summary="MEA", tags=["test insert"])
def TEST_MEA(id_tramite):
	create_userdoc = {}
	catch_data = userDocModel()
	catch_data.setData(id_tramite)
	create_userdoc['affectedFileIdList_fileNbr'] = catch_data.affectedFileIdList_fileNbr
	create_userdoc['affectedFileIdList_fileSeq'] = catch_data.affectedFileIdList_fileSeq 
	create_userdoc['affectedFileIdList_fileSeries'] = catch_data.affectedFileIdList_fileSeries 
	create_userdoc['affectedFileIdList_fileType'] = catch_data.affectedFileIdList_fileType 
	create_userdoc['affected_doc_Log'] = catch_data.affected_doc_Log 
	create_userdoc['affected_doc_docNbr'] = catch_data.affected_doc_docNbr 
	create_userdoc['affected_doc_docOrigin'] = catch_data.affected_doc_docOrigin 
	create_userdoc['affected_doc_docSeries'] = catch_data.affected_doc_docSeries 
	create_userdoc['affectedFileSummaryList_disclaimer'] = catch_data.affected_doc_docSeries 
	create_userdoc['affectedFileSummaryList_disclaimerInOtherLang'] = catch_data.affectedFileSummaryList_disclaimerInOtherLang 
	create_userdoc['affectedFileSummaryList_fileNbr'] = catch_data.affectedFileSummaryList_fileNbr 
	create_userdoc['affectedFileSummaryList_fileSeq'] = catch_data.affectedFileSummaryList_fileSeq 
	create_userdoc['affectedFileSummaryList_fileSeries'] = catch_data.affectedFileSummaryList_fileSeries 
	create_userdoc['affectedFileSummaryList_fileType'] = catch_data.affectedFileSummaryList_fileType 
	create_userdoc['affectedFileSummaryList_fileIdAsString'] = catch_data.affectedFileSummaryList_fileIdAsString 
	create_userdoc['affectedFileSummaryList_fileSummaryClasses'] = catch_data.affectedFileSummaryList_fileSummaryClasses 
	create_userdoc['affectedFileSummaryList_fileSummaryCountry'] = catch_data.affectedFileSummaryList_fileSummaryCountry 
	create_userdoc['affectedFileSummaryList_fileSummaryDescription'] = catch_data.affectedFileSummaryList_fileSummaryDescription 
	create_userdoc['affectedFileSummaryList_fileSummaryDescriptionInOtherLang'] = catch_data.affectedFileSummaryList_fileSummaryDescriptionInOtherLang 
	create_userdoc['affectedFileSummaryList_fileSummaryOwner'] = catch_data.affectedFileSummaryList_fileSummaryOwner 
	create_userdoc['affectedFileSummaryList_fileSummaryOwnerInOtherLang'] = catch_data.affectedFileSummaryList_fileSummaryOwnerInOtherLang 
	create_userdoc['affectedFileSummaryList_fileSummaryRepresentative'] = catch_data.affectedFileSummaryList_fileSummaryRepresentative 
	create_userdoc['affectedFileSummaryList_fileSummaryRepresentativeInOtherLang'] = catch_data.affectedFileSummaryList_fileSummaryRepresentativeInOtherLang 
	create_userdoc['affectedFileSummaryList_fileSummaryResponsibleName'] = catch_data.affectedFileSummaryList_fileSummaryResponsibleName 
	create_userdoc['affectedFileSummaryList_fileSummaryStatus'] = catch_data.affectedFileSummaryList_fileSummaryStatus 
	create_userdoc['applicant_applicantNotes'] = catch_data.applicant_applicantNotes 
	create_userdoc['applicant_person_addressStreet'] = catch_data.applicant_person_addressStreet 
	create_userdoc['applicant_person_addressStreetInOtherLang'] = catch_data.applicant_person_addressStreetInOtherLang 
	create_userdoc['applicant_person_addressZone'] = catch_data.applicant_person_addressZone 
	create_userdoc['applicant_person_agentCode'] = catch_data.applicant_person_agentCode 
	create_userdoc['applicant_person_cityCode'] = catch_data.applicant_person_cityCode 
	create_userdoc['applicant_person_cityName'] = catch_data.applicant_person_cityName 
	create_userdoc['applicant_person_companyRegisterRegistrationDate'] = catch_data.applicant_person_companyRegisterRegistrationDate 
	create_userdoc['applicant_person_companyRegisterRegistrationNbr'] = catch_data.applicant_person_companyRegisterRegistrationNbr 
	create_userdoc['applicant_person_email'] = catch_data.applicant_person_email 
	create_userdoc['applicant_person_individualIdNbr'] = catch_data.applicant_person_individualIdNbr 
	create_userdoc['applicant_person_individualIdType'] = catch_data.applicant_person_individualIdType 
	create_userdoc['applicant_person_legalIdNbr'] = catch_data.applicant_person_legalIdNbr 
	create_userdoc['applicant_person_legalIdType'] = catch_data.applicant_person_legalIdType 
	create_userdoc['applicant_person_legalNature'] = catch_data.applicant_person_legalNature 
	create_userdoc['applicant_person_legalNatureInOtherLang'] = catch_data.applicant_person_legalNatureInOtherLang 
	create_userdoc['applicant_person_nationalityCountryCode'] = catch_data.applicant_person_nationalityCountryCode 
	create_userdoc['applicant_person_personGroupCode'] = catch_data.applicant_person_personGroupCode 
	create_userdoc['applicant_person_personGroupName'] = catch_data.applicant_person_personGroupName 
	create_userdoc['applicant_person_personName'] = catch_data.applicant_person_personName 
	create_userdoc['applicant_person_personNameInOtherLang'] = catch_data.applicant_person_personNameInOtherLang 
	create_userdoc['applicant_person_residenceCountryCode'] = catch_data.applicant_person_residenceCountryCode 
	create_userdoc['applicant_person_stateCode'] = catch_data.applicant_person_stateCode 
	create_userdoc['applicant_person_stateName'] = catch_data.applicant_person_stateName 
	create_userdoc['applicant_person_telephone'] = catch_data.applicant_person_telephone 
	create_userdoc['applicant_person_zipCode'] = catch_data.applicant_person_zipCode 
	create_userdoc['documentId_docLog'] = catch_data.documentId_docLog 
	create_userdoc['documentId_docNbr'] = catch_data.documentId_docNbr 
	create_userdoc['documentId_docOrigin'] = catch_data.documentId_docOrigin 
	create_userdoc['documentId_docSeries'] = catch_data.documentId_docSeries 
	create_userdoc['documentId_selected'] = catch_data.documentId_selected 
	create_userdoc['documentSeqId_docSeqName'] = catch_data.documentSeqId_docSeqName 
	create_userdoc['documentSeqId_docSeqNbr'] = catch_data.documentSeqId_docSeqNbr 
	create_userdoc['documentSeqId_docSeqSeries'] = catch_data.documentSeqId_docSeqSeries 
	create_userdoc['documentSeqId_docSeqType'] = catch_data.documentSeqId_docSeqType 
	create_userdoc['filingData_applicationSubtype'] = catch_data.filingData_applicationSubtype 
	create_userdoc['filingData_applicationType'] = catch_data.filingData_applicationType 
	create_userdoc['filingData_captureDate'] = catch_data.filingData_captureDate 
	create_userdoc['filingData_captureUserId'] = catch_data.filingData_captureUserId 
	create_userdoc['filingData_filingDate'] = catch_data.filingData_filingDate 
	create_userdoc['filingData_lawCode'] = catch_data.filingData_lawCode 
	create_userdoc['filingData_novelty1Date'] = catch_data.filingData_novelty1Date 
	create_userdoc['filingData_novelty2Date'] = catch_data.filingData_novelty2Date 
	create_userdoc['filingData_paymentList_currencyName'] = catch_data.filingData_paymentList_currencyName 
	create_userdoc['filingData_paymentList_currencyType'] = catch_data.filingData_paymentList_currencyType 
	create_userdoc['filingData_paymentList_receiptAmount'] = catch_data.filingData_paymentList_receiptAmount 
	create_userdoc['filingData_paymentList_receiptDate'] = catch_data.filingData_paymentList_receiptDate 
	create_userdoc['filingData_paymentList_receiptNbr'] = catch_data.filingData_paymentList_receiptNbr 
	create_userdoc['filingData_paymentList_receiptNotes'] = catch_data.filingData_paymentList_receiptNotes 
	create_userdoc['filingData_paymentList_receiptType'] = catch_data.filingData_paymentList_receiptType 
	create_userdoc['filingData_paymentList_receiptTypeName'] = catch_data.filingData_paymentList_receiptTypeName 
	create_userdoc['filingData_receptionDate'] = catch_data.filingData_receptionDate 
	create_userdoc['filingData_documentId_receptionDocument_docLog'] = catch_data.filingData_documentId_receptionDocument_docLog 
	create_userdoc['filingData_documentId_receptionDocument_docNbr'] = catch_data.filingData_documentId_receptionDocument_docNbr 
	create_userdoc['filingData_documentId_receptionDocument_docOrigin'] = catch_data.filingData_documentId_receptionDocument_docOrigin 
	create_userdoc['filingData_documentId_receptionDocument_docSeries'] = catch_data.filingData_documentId_receptionDocument_docSeries 
	create_userdoc['filingData_documentId_receptionDocument_selected'] = catch_data.filingData_documentId_receptionDocument_selected 
	create_userdoc['filingData_userdocTypeList_userdocName'] = catch_data.filingData_userdocTypeList_userdocName 
	create_userdoc['filingData_userdocTypeList_userdocType'] = catch_data.filingData_userdocTypeList_userdocType 
	create_userdoc['newOwnershipData_ownerList_orderNbr'] = catch_data.newOwnershipData_ownerList_orderNbr 
	create_userdoc['newOwnershipData_ownerList_ownershipNotes'] = catch_data.newOwnershipData_ownerList_ownershipNotes 
	create_userdoc['newOwnershipData_ownerList_person_addressStreet'] = catch_data.newOwnershipData_ownerList_person_addressStreet 
	create_userdoc['newOwnershipData_ownerList_person_addressStreetInOtherLang'] = catch_data.newOwnershipData_ownerList_person_addressStreetInOtherLang 
	create_userdoc['newOwnershipData_ownerList_person_addressZone'] = catch_data.newOwnershipData_ownerList_person_addressZone 
	create_userdoc['newOwnershipData_ownerList_person_agentCode'] = catch_data.newOwnershipData_ownerList_person_agentCode 
	create_userdoc['newOwnershipData_ownerList_person_cityCode'] = catch_data.newOwnershipData_ownerList_person_cityCode 
	create_userdoc['newOwnershipData_ownerList_person_cityName'] = catch_data.newOwnershipData_ownerList_person_cityName 
	create_userdoc['newOwnershipData_ownerList_person_companyRegisterRegistrationDate'] = catch_data.newOwnershipData_ownerList_person_companyRegisterRegistrationDate 
	create_userdoc['newOwnershipData_ownerList_person_companyRegisterRegistrationNbr'] = catch_data.newOwnershipData_ownerList_person_companyRegisterRegistrationNbr 
	create_userdoc['newOwnershipData_ownerList_person_email'] = catch_data.newOwnershipData_ownerList_person_email 
	create_userdoc['newOwnershipData_ownerList_person_individualIdNbr'] = catch_data.newOwnershipData_ownerList_person_individualIdNbr 
	create_userdoc['newOwnershipData_ownerList_person_individualIdType'] = catch_data.newOwnershipData_ownerList_person_individualIdType 
	create_userdoc['newOwnershipData_ownerList_person_legalIdNbr'] = catch_data.newOwnershipData_ownerList_person_legalIdNbr 
	create_userdoc['newOwnershipData_ownerList_person_legalIdType'] = catch_data.newOwnershipData_ownerList_person_legalIdType 
	create_userdoc['newOwnershipData_ownerList_person_legalNature'] = catch_data.newOwnershipData_ownerList_person_legalNature 
	create_userdoc['newOwnershipData_ownerList_person_legalNatureInOtherLang'] = catch_data.newOwnershipData_ownerList_person_legalNatureInOtherLang 
	create_userdoc['newOwnershipData_ownerList_person_nationalityCountryCode'] = catch_data.newOwnershipData_ownerList_person_nationalityCountryCode 
	create_userdoc['newOwnershipData_ownerList_person_personGroupCode'] = catch_data.newOwnershipData_ownerList_person_personGroupCode 
	create_userdoc['newOwnershipData_ownerList_person_personGroupName'] = catch_data.newOwnershipData_ownerList_person_personGroupName 
	create_userdoc['newOwnershipData_ownerList_person_personName'] = catch_data.newOwnershipData_ownerList_person_personName 
	create_userdoc['newOwnershipData_ownerList_person_personNameInOtherLang'] = catch_data.newOwnershipData_ownerList_person_personNameInOtherLang 
	create_userdoc['newOwnershipData_ownerList_person_residenceCountryCode'] = catch_data.newOwnershipData_ownerList_person_residenceCountryCode 
	create_userdoc['newOwnershipData_ownerList_person_stateCode'] = catch_data.newOwnershipData_ownerList_person_stateCode 
	create_userdoc['newOwnershipData_ownerList_person_stateName'] = catch_data.newOwnershipData_ownerList_person_stateName 
	create_userdoc['newOwnershipData_ownerList_person_telephone'] = catch_data.newOwnershipData_ownerList_person_telephone 
	create_userdoc['newOwnershipData_ownerList_person_zipCode'] = catch_data.newOwnershipData_ownerList_person_zipCode 
	create_userdoc['notes'] = catch_data.notes 
	create_userdoc['poaData_poaGranteeList_person_addressStreet'] = "" 
	create_userdoc['poaData_poaGranteeList_person_addressStreetInOtherLang'] = "" 
	create_userdoc['poaData_poaGranteeList_person_addressZone'] = ""
	create_userdoc['poaData_poaGranteeList_person_agentCode'] = "" 
	create_userdoc['poaData_poaGranteeList_person_cityCode'] = "" 
	create_userdoc['poaData_poaGranteeList_person_cityName'] = "" 
	create_userdoc['poaData_poaGranteeList_person_companyRegisterRegistrationDate'] = "" 
	create_userdoc['poaData_poaGranteeList_person_companyRegisterRegistrationNbr'] = "" 
	create_userdoc['poaData_poaGranteeList_person_email'] = "" 
	create_userdoc['poaData_poaGranteeList_person_individualIdNbr'] = "" 
	create_userdoc['poaData_poaGranteeList_person_individualIdType'] = "" 
	create_userdoc['poaData_poaGranteeList_person_legalIdNbr'] = "" 
	create_userdoc['poaData_poaGranteeList_person_legalIdType'] = "" 
	create_userdoc['poaData_poaGranteeList_person_legalNature'] = "" 
	create_userdoc['poaData_poaGranteeList_person_legalNatureInOtherLang'] = "" 
	create_userdoc['poaData_poaGranteeList_person_nationalityCountryCode'] = "" 
	create_userdoc['poaData_poaGranteeList_person_personGroupCode'] = "" 
	create_userdoc['poaData_poaGranteeList_person_personGroupName'] = "" 
	create_userdoc['poaData_poaGranteeList_person_personName'] = "" 
	create_userdoc['poaData_poaGranteeList_person_personNameInOtherLang'] = "" 
	create_userdoc['poaData_poaGranteeList_person_residenceCountryCode'] = "" 
	create_userdoc['poaData_poaGranteeList_person_stateCode'] = "" 
	create_userdoc['poaData_poaGranteeList_person_stateName'] = "" 
	create_userdoc['poaData_poaGranteeList_person_telephone'] = "" 
	create_userdoc['poaData_poaGranteeList_person_zipCode'] = "" 
	create_userdoc['poaData_poaGrantor_person_addressStreet'] = "" 
	create_userdoc['poaData_poaGrantor_person_addressStreetInOtherLang'] = "" 
	create_userdoc['poaData_poaGrantor_person_addressZone'] = "" 
	create_userdoc['poaData_poaGrantor_person_agentCode'] = "" 
	create_userdoc['poaData_poaGrantor_person_cityCode'] = "" 
	create_userdoc['poaData_poaGrantor_person_cityName'] = "" 
	create_userdoc['poaData_poaGrantor_person_companyRegisterRegistrationDate'] = "" 
	create_userdoc['poaData_poaGrantor_person_companyRegisterRegistrationNbr'] = "" 
	create_userdoc['poaData_poaGrantor_person_email'] = "" 
	create_userdoc['poaData_poaGrantor_person_individualIdNbr'] = "" 
	create_userdoc['poaData_poaGrantor_person_individualIdType'] = "" 
	create_userdoc['poaData_poaGrantor_person_legalIdNbr'] = "" 
	create_userdoc['poaData_poaGrantor_person_legalIdType'] = "" 
	create_userdoc['poaData_poaGrantor_person_legalNature'] = "" 
	create_userdoc['poaData_poaGrantor_person_legalNatureInOtherLang'] = "" 
	create_userdoc['poaData_poaGrantor_person_nationalityCountryCode'] = "" 
	create_userdoc['poaData_poaGrantor_person_personGroupCode'] = "" 
	create_userdoc['poaData_poaGrantor_person_personGroupName'] = "" 
	create_userdoc['poaData_poaGrantor_person_personName'] = "" 
	create_userdoc['poaData_poaGrantor_person_personNameInOtherLang'] = "" 
	create_userdoc['poaData_poaGrantor_person_residenceCountryCode'] = "" 
	create_userdoc['poaData_poaGrantor_person_stateCode'] = "" 
	create_userdoc['poaData_poaGrantor_person_stateName'] = "" 
	create_userdoc['poaData_poaGrantor_person_telephone'] = "" 
	create_userdoc['poaData_poaGrantor_person_zipCode'] = "" 
	create_userdoc['poaData_poaRegNumber'] = "" 
	create_userdoc['poaData_scope'] = "" 
	create_userdoc['representationData_representativeList_person_addressStreet'] = catch_data.representationData_representativeList_person_addressStreet 
	create_userdoc['representationData_representativeList_person_addressStreetInOtherLang'] = catch_data.representationData_representativeList_person_addressStreetInOtherLang 
	create_userdoc['representationData_representativeList_person_addressZone'] = catch_data.representationData_representativeList_person_addressZone 
	create_userdoc['representationData_representativeList_person_agentCode'] = catch_data.representationData_representativeList_person_agentCode 
	create_userdoc['representationData_representativeList_person_cityCode'] = catch_data.representationData_representativeList_person_cityCode 
	create_userdoc['representationData_representativeList_person_cityName'] = catch_data.representationData_representativeList_person_cityName 
	create_userdoc['representationData_representativeList_person_companyRegisterRegistrationDate'] = catch_data.representationData_representativeList_person_companyRegisterRegistrationDate 
	create_userdoc['representationData_representativeList_person_companyRegisterRegistrationNbr'] = catch_data.representationData_representativeList_person_companyRegisterRegistrationNbr 
	create_userdoc['representationData_representativeList_person_email'] = catch_data.representationData_representativeList_person_email 
	create_userdoc['representationData_representativeList_person_individualIdNbr'] = catch_data.representationData_representativeList_person_individualIdNbr 
	create_userdoc['representationData_representativeList_person_individualIdType'] = catch_data.representationData_representativeList_person_individualIdType 
	create_userdoc['representationData_representativeList_person_legalIdNbr'] = catch_data.representationData_representativeList_person_legalIdNbr 
	create_userdoc['representationData_representativeList_person_legalIdType'] = catch_data.representationData_representativeList_person_legalIdType 
	create_userdoc['representationData_representativeList_person_legalNature'] = catch_data.representationData_representativeList_person_legalNature 
	create_userdoc['representationData_representativeList_person_legalNatureInOtherLang'] = catch_data.representationData_representativeList_person_legalNatureInOtherLang 
	create_userdoc['representationData_representativeList_person_nationalityCountryCode'] = catch_data.representationData_representativeList_person_nationalityCountryCode 
	create_userdoc['representationData_representativeList_person_personGroupCode'] = catch_data.representationData_representativeList_person_personGroupCode 
	create_userdoc['representationData_representativeList_person_personGroupName'] = catch_data.representationData_representativeList_person_personGroupName 
	create_userdoc['representationData_representativeList_person_personName'] = catch_data.representationData_representativeList_person_personName 
	create_userdoc['representationData_representativeList_person_personNameInOtherLang'] = catch_data.representationData_representativeList_person_personNameInOtherLang 
	create_userdoc['representationData_representativeList_person_residenceCountryCode'] = catch_data.representationData_representativeList_person_residenceCountryCode 
	create_userdoc['representationData_representativeList_person_stateCode'] = catch_data.representationData_representativeList_person_stateCode 
	create_userdoc['representationData_representativeList_person_stateName'] = catch_data.representationData_representativeList_person_stateName 
	create_userdoc['representationData_representativeList_person_telephone'] = catch_data.representationData_representativeList_person_telephone 
	create_userdoc['representationData_representativeList_person_zipCode'] = catch_data.representationData_representativeList_person_zipCode 
	create_userdoc['representationData_representativeList_representativeType'] = catch_data.representationData_representativeList_representativeType 
	return(create_userdoc)
	#return(format_userdoc(id_tramite))

@app.post('/sis/test_reg', summary="MEA", tags=["test insert registro"])
def TEST_MEA_reg(id_tramite):
	create_userdoc = {}
	catch_data = insertRegModel()
	catch_data.setData(id_tramite)
	create_userdoc['file_fileId_fileNbr'] = catch_data.file_fileId_fileNbr
	create_userdoc['file_fileId_fileSeq'] = catch_data.file_fileId_fileSeq
	create_userdoc['file_fileId_fileSeries'] = catch_data.file_fileId_fileSeries
	create_userdoc['file_fileId_fileType'] = catch_data.file_fileId_fileType
	create_userdoc['file_filingData_applicationSubtype'] = catch_data.file_filingData_applicationSubtype
	create_userdoc['file_filingData_applicationType'] = catch_data.file_filingData_applicationType
	create_userdoc['file_filingData_captureUserId'] = catch_data.file_filingData_captureUserId
	create_userdoc['file_filingData_filingDate'] = catch_data.file_filingData_filingDate
	create_userdoc['file_filingData_captureDate'] = catch_data.file_filingData_captureDate
	create_userdoc['file_filingData_lawCode'] = catch_data.file_filingData_lawCode
	create_userdoc['file_filingData_paymentList_currencyType'] = catch_data.file_filingData_paymentList_currencyType
	create_userdoc['file_filingData_paymentList_receiptAmount'] = catch_data.file_filingData_paymentList_receiptAmount
	create_userdoc['file_filingData_paymentList_receiptDate'] = catch_data.file_filingData_paymentList_receiptDate
	create_userdoc['file_filingData_paymentList_receiptNbr'] = catch_data.file_filingData_paymentList_receiptNbr
	create_userdoc['file_filingData_paymentList_receiptNotes'] = catch_data.file_filingData_paymentList_receiptNotes
	create_userdoc['file_filingData_paymentList_receiptType'] = catch_data.file_filingData_paymentList_receiptType
	create_userdoc['file_filingData_receptionUserId'] = catch_data.file_filingData_receptionUserId
	create_userdoc['file_ownershipData_ownerList_person_addressStreet'] = catch_data.file_ownershipData_ownerList_person_addressStreet
	create_userdoc['file_ownershipData_ownerList_person_nationalityCountryCode'] = catch_data.file_ownershipData_ownerList_person_nationalityCountryCode
	create_userdoc['file_ownershipData_ownerList_person_personName'] = catch_data.file_ownershipData_ownerList_person_personName
	create_userdoc['file_ownershipData_ownerList_person_residenceCountryCode'] = catch_data.file_ownershipData_ownerList_person_residenceCountryCode
	create_userdoc['file_rowVersion'] = catch_data.file_rowVersion
	create_userdoc['agentCode'] = catch_data.agentCode
	create_userdoc['file_representationData_representativeList_representativeType'] = catch_data.file_representationData_representativeList_representativeType
	create_userdoc['rowVersion'] = catch_data.rowVersion
	create_userdoc['protectionData_dummy'] = catch_data.protectionData_dummy
	create_userdoc['protectionData_niceClassList_niceClassDescription'] = catch_data.protectionData_niceClassList_niceClassDescription
	create_userdoc['protectionData_niceClassList_niceClassDetailedStatus'] = catch_data.protectionData_niceClassList_niceClassDetailedStatus
	create_userdoc['protectionData_niceClassList_niceClassEdition'] = catch_data.protectionData_niceClassList_niceClassEdition
	create_userdoc['protectionData_niceClassList_niceClassGlobalStatus'] = catch_data.protectionData_niceClassList_niceClassGlobalStatus
	create_userdoc['protectionData_niceClassList_niceClassNbr'] = catch_data.protectionData_niceClassList_niceClassNbr
	create_userdoc['protectionData_niceClassList_niceClassVersion'] = catch_data.protectionData_niceClassList_niceClassVersion
	create_userdoc['logoData'] = catch_data.logoData
	create_userdoc['logoType']= catch_data.logoType
	create_userdoc['signData_markName'] = catch_data.signData_markName
	create_userdoc['signData_signType'] = catch_data.signData_signType
	return(create_userdoc)

@app.post('/sis/test_ren', summary="MEA", tags=["test insert renovacion"])
def TEST_MEA_ren(id_tramite):
	create_userdoc = {}
	catch_data = insertRenModel()
	catch_data.setData(id_tramite)
	create_userdoc['file_fileId_fileNbr'] = catch_data.file_fileId_fileNbr 
	create_userdoc['file_fileId_fileSeq'] = catch_data.file_fileId_fileSeq 
	create_userdoc['file_fileId_fileSeries'] = catch_data.file_fileId_fileSeries 
	create_userdoc['file_fileId_fileType'] = catch_data.file_fileId_fileType 
	create_userdoc['file_filingData_applicationSubtype'] = catch_data.file_filingData_applicationSubtype 
	create_userdoc['file_filingData_applicationType'] = catch_data.file_filingData_applicationType 
	create_userdoc['file_filingData_captureUserId'] = catch_data.file_filingData_captureUserId 
	create_userdoc['file_filingData_captureDate'] = catch_data.file_filingData_captureDate 
	create_userdoc['file_filingData_filingDate'] = catch_data.file_filingData_filingDate 
	create_userdoc['file_filingData_lawCode'] = catch_data.file_filingData_lawCode 
	create_userdoc['file_filingData_paymentList_currencyType'] = catch_data.file_filingData_paymentList_currencyType 
	create_userdoc['file_filingData_paymentList_receiptAmount'] = catch_data.file_filingData_paymentList_receiptAmount 
	create_userdoc['file_filingData_paymentList_receiptDate'] = catch_data.file_filingData_paymentList_receiptDate 
	create_userdoc['file_filingData_paymentList_receiptNbr'] = catch_data.file_filingData_paymentList_receiptNbr 
	create_userdoc['file_filingData_paymentList_receiptNotes'] = catch_data.file_filingData_paymentList_receiptNotes 
	create_userdoc['file_filingData_paymentList_receiptType'] = catch_data.file_filingData_paymentList_receiptType 
	create_userdoc['file_filingData_receptionUserId'] = catch_data.file_filingData_receptionUserId 
	create_userdoc['file_ownershipData_ownerList_person_owneraddressStreet'] = catch_data.file_ownershipData_ownerList_person_owneraddressStreet 
	create_userdoc['file_ownershipData_ownerList_person_ownernationalityCountryCode'] = catch_data.file_ownershipData_ownerList_person_ownernationalityCountryCode 
	create_userdoc['file_ownershipData_ownerList_person_ownerpersonName'] = catch_data.file_ownershipData_ownerList_person_ownerpersonName 
	create_userdoc['file_ownershipData_ownerList_person_ownerresidenceCountryCode'] = catch_data.file_ownershipData_ownerList_person_ownerresidenceCountryCode 
	create_userdoc['file_representationData_representativeList_representativeType'] = catch_data.file_representationData_representativeList_representativeType 
	create_userdoc['agentCode'] = catch_data.agentCode 
	create_userdoc['file_relationshipList_fileId_fileNbr'] = catch_data.file_relationshipList_fileId_fileNbr 
	create_userdoc['file_relationshipList_fileId_fileSeq'] = catch_data.file_relationshipList_fileId_fileSeq 
	create_userdoc['file_relationshipList_fileId_fileSeries'] = catch_data.file_relationshipList_fileId_fileSeries 
	create_userdoc['file_relationshipList_fileId_fileType'] = catch_data.file_relationshipList_fileId_fileType 
	create_userdoc['file_relationshipList_relationshipRole'] = catch_data.file_relationshipList_relationshipRole 
	create_userdoc['file_relationshipList_relationshipType'] = catch_data.file_relationshipList_relationshipType 
	create_userdoc['file_rowVersion'] = catch_data.file_rowVersion 
	create_userdoc['protectionData_dummy'] = catch_data.protectionData_dummy 
	create_userdoc['protectionData_niceClassList_niceClassDescription'] = catch_data.protectionData_niceClassList_niceClassDescription 
	create_userdoc['protectionData_niceClassList_niceClassDetailedStatus'] = catch_data.protectionData_niceClassList_niceClassDetailedStatus 
	create_userdoc['protectionData_niceClassList_niceClassEdition'] = catch_data.protectionData_niceClassList_niceClassEdition 
	create_userdoc['protectionData_niceClassList_niceClassGlobalStatus'] = catch_data.protectionData_niceClassList_niceClassGlobalStatus 
	create_userdoc['protectionData_niceClassList_niceClassNbr'] = catch_data.protectionData_niceClassList_niceClassNbr 
	create_userdoc['protectionData_niceClassList_niceClassVersion'] = catch_data.protectionData_niceClassList_niceClassVersion 
	create_userdoc['rowVersion'] = catch_data.rowVersion 
	create_userdoc['logoData'] = catch_data.logoData 
	create_userdoc['logoType'] = catch_data.logoType 
	create_userdoc['signData_markName'] = catch_data.signData_markName 
	create_userdoc['signData_signType'] = catch_data.signData_signType
	



	return(create_userdoc)

@app.post('/sfe/insert_mea_reg', summary="MEA", tags=["Insert registro de marcas MEA"])
def insert_mea_reg(id_tramite):
	return(insertReg(id_tramite))

@app.post('/sfe/insert_mea_ren', summary="MEA", tags=["Insert renovacion de marcas MEA"])
def insert_mea_ren(id_tramite):
	return(insertRen(id_tramite))

@app.post('/sfe/getTime', summary="MEA", tags=["Tiempo de busqueda para capturar pendientes en tabla tramites en segundos"])
def get_time():
	return(int(MEA_TIEMPO_ACTUALIZACION))

@app.post('/api/getparametros', summary="API", tags=["Lista de parametros"])
def get_params():
	return(get_parametros())

@app.post('/api/getparametros_mea', summary="API", tags=["Lista de parametros MEA"])
def get_params():
	return(get_parametros_mea())

@app.post('/api/reglas', summary="API", tags=["Lista de reglas segun formulario_id"])
def reglas_mea():
	return(reglas_me())

@app.post('/api/getparametro', summary="API", tags=["Devuelve un registro segun su id"])
def get_param(item: for_id):
	return(get_parametro(item.Id))

class update_id(BaseModel):
	param_id:int
	origen:str
	descripcion:str
	valor1:str
	valor2:str
	valor3:str
	valor4:str
	valor5:str
	estado:int
	sistema_id:int
@app.post('/api/updateparametro', summary="API", tags=["editar parametro, respuesta registro editado"])
def update_param(item:update_id):
	return(upDate_parametro(item.param_id,item.origen,item.descripcion,item.valor1,item.valor2,item.valor3,item.valor4,item.valor5,item.estado,item.sistema_id))

class pendientes(BaseModel):
	fecha:str
	ver:str
	pag:str                 
@app.post('/api/pendientes_sfe', summary="API", tags=["Lista de pendientes"])
def pendientes_sfe_m(item:pendientes):
	return(pendientes_sfe(item.fecha,item.ver,item.pag))

class pendientes_full(BaseModel):
	fecha:str
@app.post('/api/pendientes_sfe_full', summary="API", tags=["Lista de pendientes para spi  args( Id - tipo_documento_id )"])
def pendientes_sfe_notPag(item:pendientes_full):
	return(pendientes_sfe_not_pag(item.fecha))

class insert_n_doc(BaseModel):
	arg0:str = ""
	arg1:str = ""
@app.post('/sfe/insert_new_doc', summary="API", tags=["inserta documentos, testigo visual progressBar "])
def auto_insert_mea(item:insert_n_doc):
	return insert_list(item.arg0,item.arg1)

class pendientes_fecha(BaseModel):
	fecha:str              
@app.post('/api/pendientes_sfe_sop', summary="API", tags=["Lista de pendientes para soporte"])
def pendientes_sfe_sop(item:pendientes_fecha):
	return(pendientes_sfe_soporte(item.fecha))

@app.post('/api/pendientes_sfe_not_pag', summary="API", tags=["Lista de pendientes sin paginar"])
def pendientes_sfe_m(item:pendientes_fecha):
	return(pendientes_sfe_not_pag(item.fecha))

class send_mail_ag(BaseModel):
	fileName:str = ""
	ag_mail:str = ""
	affair:str = "" 
@app.post('/sfe/send_mail_ag', summary="SFE", tags=["Envio de correo al agente"])
async def send_pdf_mail_ag(item:send_mail_ag):
	return(enviar(item.fileName,item.ag_mail,item.affair,''))

class pendientes_count(BaseModel):
	fecha:str = ""                
@app.post('/api/pendientes_count', summary="API", tags=["contador pendientes"])
def pendientes_sfe_count(item:pendientes_count):
	return(count_pendiente(item.fecha))

@app.post('/sis/reload', summary="sis", tags=["reload"])
def re_load():
	ObjFichero = open("reload.py",'w')
	msg = "#ReInicio de sistema"
	ObjFichero.write(msg)
	ObjFichero.close()
	ObjFichero2 = open("reload.py")
	TextoFichero = ObjFichero2.read()
	print (TextoFichero)
	ObjFichero2.close()
	return(True)

app.openapi = custom_openapi

