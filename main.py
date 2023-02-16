from urllib import request
from fastapi import FastAPI
from pydantic import BaseModel
from wipo.ipas import  Insert_user_doc, Insert_user_doc_con_recibo_poder, Insert_user_doc_sin_recibo_con_relacion, Insert_user_doc_sin_recibo_relacion, disenio_getlist, disenio_getlist_fecha, disenio_user_doc_getlist_fecha, get_agente, mark_getlist, mark_getlistFecha, mark_getlistReg, patent_getlist_fecha, patent_user_doc_getlist_fecha, personAgente, personAgenteDisenio, personAgentePatent, personTitular, personTitularDisenio, personTitularPatent, user_doc_getlist_fecha #pip install "fastapi[all]"
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



class userdoc_insert_uno(BaseModel):
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
@app.post('/api/insert_userdoc_opo', summary="Marcas", tags=["Escrito de Oposición de marca"])
def insert_user_doc_mde(item: userdoc_insert_uno):
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

