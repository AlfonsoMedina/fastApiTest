from urllib import request
from fastapi import FastAPI
from pydantic import BaseModel
from tools.base64Decode import image_url_to_b64
from wipo.ipas import  Insert_user_doc, Insert_user_doc_con_recibo_poder, Insert_user_doc_sin_recibo_con_relacion, Insert_user_doc_sin_recibo_relacion, disenio_getlist, disenio_getlist_fecha, disenio_user_doc_getlist_fecha, get_agente, mark_getlist, mark_getlistFecha, mark_getlistReg, mark_insert_reg, patent_getlist_fecha, patent_user_doc_getlist_fecha, personAgente, personAgenteDisenio, personAgentePatent, personTitular, personTitularDisenio, personTitularPatent, user_doc_getlist_fecha, user_doc_receive, user_doc_update #pip install "fastapi[all]"
from wipo.function_for_reception_in import user_doc_read, user_doc_read_disenio, user_doc_read_patent
import zeep

description = """
Version 2023 

## Métodos para consultar e insertar eventos de Mesa de entrada 

las rutas reciben un objeto **JSON** como parametro y retornar un objeto **JSON**.

"""

app = FastAPI(
	title="Api Mesa de Entrada ",
	description=description,
	version="3.0.1",
	openapi_url="/Sprint/v2/openapi.json"
)



class agent_code(BaseModel):
	code:str = ""
@app.post('/api/getAgente_ipas', summary="Marcas", tags=["Consulta nombre de agente   por agent_code"])
def getAgente_ipas(item: agent_code):
	return({"nombre":get_agente(item.code).agentName})

@app.post('/api/getAgente', summary="Marcas", tags=["Consulta datos de agente como persona  por agent_code"])
def consulta_agente(item: agent_code):
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
def consulta_agente_Patent(item: agent_code):
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
def consulta_agente_Disenio(item: agent_code):
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
def consulta_titular(item: gettitular):
	personName = item.nombre					
	return(personTitular(str(personName)))

@app.post('/api/getTitularPatent', summary="Patentes", tags=["Consulta datos de titular como persona de patentes por nombre/denominacion"])
def consulta_titularPatent(item: gettitular):
	personName = item.nombre					
	return(personTitularPatent(str(personName)))

@app.post('/api/getTitularDisenio', summary="Diseño", tags=["Consulta datos de titular como persona de diseño por nombre/denominacion"])
def consulta_titularDisenio(item: gettitular):
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
def procesados_disenios(item: process_fecha):
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
def user_doc_patent(item: process_fecha):
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
def user_doc_disenio(item: process_fecha):
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
def disenio_for_fileNBR(item: for_exp):
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
@app.post('/sfe/insert_userdoc_opo', summary="Marcas", tags=["Escrito de Oposición de marca"])
def insert_user_doc_mde(item: userdoc_insert_OPO):
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
@app.post('/sfe/UserdocUpdate', summary="Marcas", tags=["UpDate para Escrito de marcas"])
def userdoc_update(item: userdoc_upd):
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
def insert_receive(item: receive):
	"""
		**Ej:**\n
			"arg0": "1",
			"arg1": "DAJ1",						**(tipo de documento)**
			"arg3": "true",
			"arg4_offidocNbr": "",
			"arg4_offidocOrigin": "",
			"arg4_offidocSeries": "",
			"arg4_selected": "",
			"arg5_officeDepartmentCode": "",
			"arg5_officeDivisionCode": "",
			"arg5_officeSectionCode": "",
			"arg6": "2023-02-17",					**(fecha del evento)**
			"arg7_currencyType": "",
			"arg7_DReceiptAmount": "",
			"arg7_receiptDate": "",
			"arg7_receiptNbr": "",
			"arg7_receiptType": "",
			"arg8": "298",						**(UserID)**
			"arg9": "SFE test - Aplicante SPRINT",
			"arg10_docLog": "E",					**(escrito relacionado)**
			"arg10_docNbr": "2225891",				**(escrito relacionado)**
			"arg10_docOrigin": "1",					**(escrito relacionado)**
			"arg10_docSeries": "2022",				**(escrito relacionado)**
			"arg10_selected": "",
			"arg11_docSeqName": "",
			"arg11_docSeqNbr": "",
			"arg11_docSeqSeries": "",
			"arg11_docSeqType": "",
			"arg12_docLog": "E",					**(escrito nuevo)**
			"arg12_docNbr": "22102468",				**(escrito nuevo)**
			"arg12_docOrigin": "1",					**(escrito nuevo)**
			"arg12_docSeries": "2022",				**(escrito nuevo)**
			"arg12_selected": "DAJ1"				**(tipo de documento)**

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

class insert_reg(BaseModel):
	fileId_fileId_fileNbr:str = ""
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
	receptionUserId:str = ""
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
def insert_reg(item: insert_reg):
	try:
		if str(item.logoData).count('https:') >= 1:
			imageurltob64 = image_url_to_b64(str(item.logoData))
			return(mark_insert_reg(
								item.fileId_fileId_fileNbr,
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
								item.receptionUserId,
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
								item.fileId_fileId_fileNbr,
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
								item.receptionUserId,
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