from time import sleep
from urllib import request
from fastapi import FastAPI
from pydantic import BaseModel
from dinapi.sfe import count_pendiente, oposicion_sfe, pendientes_sfe, registro_sfe, renovacion_sfe
from tools.params_seting import  get_parametro, get_parametros, get_parametros_mea, upDate_parametro
from tools.base64Decode import image_url_to_b64
from wipo.ipas import  Insert_user_doc, Insert_user_doc_con_recibo_poder, Insert_user_doc_sin_recibo_con_relacion, Insert_user_doc_sin_recibo_relacion, disenio_getlist, disenio_getlist_fecha, disenio_user_doc_getlist_fecha, get_agente, mark_getlist, mark_getlistFecha, mark_getlistReg, mark_insert_reg, mark_insert_ren, patent_getlist_fecha, patent_user_doc_getlist_fecha, personAgente, personAgenteDisenio, personAgentePatent, personTitular, personTitularDisenio, personTitularPatent, user_doc_getlist_fecha, user_doc_receive, user_doc_update, user_doc_update_sin_recibo #pip install "fastapi[all]"
from wipo.function_for_reception_in import user_doc_read, user_doc_read_disenio, user_doc_read_patent
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
@app.post('/sfe/UserdocUpdate', summary="Marcas", tags=["Escrito con Tipo Documento que afecta a Escritos con costo"])
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



@app.post('/api/getparametros', summary="API", tags=["Lista de parametros"])
def get_params():
	return(get_parametros())

@app.post('/api/getparametros_mea', summary="API", tags=["Lista de parametros MEA"])
def get_params():
	return(get_parametros_mea())

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
	pag:str                 
@app.post('/api/pendientes_sfe', summary="API", tags=["Lista de pendientes"])
def pendientes_sfe_m(item:pendientes):
	return(pendientes_sfe(item.fecha,item.pag))

class pendientes_count(BaseModel):
	fecha:str = ""                
@app.post('/api/pendientes_count', summary="API", tags=["contador pendientes"])
def pendientes_sfe_count(item:pendientes_count):
	return(count_pendiente(item.fecha))










app.openapi = custom_openapi


