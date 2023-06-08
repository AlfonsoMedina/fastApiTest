
import time
from turtle import back
import zeep
from zeep import Client
import psycopg2
from email_pdf_AG import envio_agente_recibido, envio_agente_recibido_reg, envio_agente_recibido_ren, form_id, sigla_id
from email_reg_sfe import envio_agente_reg
from getFileDoc import getFile_reg_and_ren
from sfe_no_presencial_reg_local import registro_pdf_sfe_local
from sfe_no_presencial_ren_local import renovacion_pdf_sfe_local
from tools.base64Decode import decode_img
from models.insertRenModel import insertRenModel
from models.InsertUserDocModel_backUp import userDocModel_test
from dinapi.sfe import COMMIT_NBR, USER_GROUP, cambio_estado_soporte, data_validator, email_receiver, exist_main_mark, exist_notifi, main_State, pago_id, pendiente_sfe, reglas_me_ttasa, renovacion_sfe, rule_notification, status_typ, tasa_id, tipo_form
from models.InsertUserDocModel import userDocModel
from tools.data_format import fecha_barra
import tools.connect as conn_serv
import tools.connect as connex
from wipo.function_for_reception_in import user_doc_getList_escrito, user_doc_read, user_doc_read_min
from wipo.insertGroupProcessMEA import ProcessGroupAddProcess, ProcessGroupGetList, ProcessGroupInsert
from wipo.ipas import daily_log_close, daily_log_open, fetch_all_user_mark, mark_getlist, mark_read
import tools.filing_date as captureDate




try:
	mark_service = conn_serv.MEA_IPAS_DESTINO
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')


def group_today(userNbr,groupName):	
	data = ProcessGroupGetList(userNbr)
	list_data = []
	respuesta = False
	for i in range(1,len(data)):
		if str(groupName) == str(data[i].processGroupName):
			list_data.append(data[i].processGroupName)
			list_data.append(data[i].processGroupId.processGroupCode)
		respuesta = list_data

		if str(groupName) != str(data[i].processGroupName):
			respuesta = False
	return(respuesta)
		
def group_typ(num):
	list = {'1':'[Expediente]','10':'[Escrito+expediente]','11':'[Escrito]'}
	group_name = str(fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00"))+" "+list[str(num)])
	return(group_name)

#EXPEDIENTES DE TIPO REG y REN
def insertar_o_crear_grupo_expediente(user,exp):
	expediente = mark_getlist(exp)
	fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" )) 
	userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
	data = mark_read(
		expediente[0]['fileId']['fileNbr']['doubleValue'], 
		expediente[0]['fileId']['fileSeq'], 
		expediente[0]['fileId']['fileSeries']['doubleValue'], 
		expediente[0]['fileId']['fileType'])
	#####################################################################################################
	group_name = f'{fecha} [Expediente]'
	if group_today(userId, group_name) != False:

		ProcessGroupAddProcess(
			str(group_today(userId, group_name)[1]), 
			userId, 
			data['file']['processId']['processNbr']['doubleValue'],
			data['file']['processId']['processType']
			)
	else:
		pass
	#####################################################################################################
	if group_today(userId, group_name) == False:
		ProcessGroupInsert(
							last_group(userId)+1,
							userId,
							fecha,
							'Creado por M.E.A.',
							'1',
							'1')

		ProcessGroupAddProcess(
							str(group_today(userId, group_name)[1]), 
							userId, 
							data['file']['processId']['processNbr']['doubleValue'],
							data['file']['processId']['processType']
							)
	
	else:
		pass

#ESCRITO RELACINADO CON ESCRITO
def insertar_o_crear_grupo_escrito(user,esc):
	data_doc = user_doc_getList_escrito(esc)
	fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" )) 
	userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
	process = user_doc_read(data_doc['documentId']['docLog'],data_doc['documentId']['docNbr']['doubleValue'],data_doc['documentId']['docOrigin'],data_doc['documentId']['docSeries']['doubleValue'])
	print(process['userdocProcessId']['processNbr']+" "+process['userdocProcessId']['processType'])
	#####################################################################################################
	group_name = f'{fecha} [Escrito]'
	if group_today(userId, group_name) != False:

		ProcessGroupAddProcess(
								str(group_today(userId, group_name)[1]), 
								userId, 
								process['userdocProcessId']['processNbr'],
								process['userdocProcessId']['processType']
								)
	else:
		pass
	#####################################################################################################
	if group_today(userId, group_name) == False:
		ProcessGroupInsert(
							last_group(userId)+1,
							userId,
							fecha,
							'Creado por M.E.A.',
							'1',
							'11')

		ProcessGroupAddProcess(
								str(group_today(userId, group_name)[1]), 
								userId, 
								process['userdocProcessId']['processNbr'],
								process['userdocProcessId']['processType']
								)
	
	else:
		pass

#ESCRITO RELACINADO CON EXPEDIENTE
def insertar_o_crear_grupo_escritoMasExpediente(user,esc):

	data_doc = user_doc_getList_escrito(esc)
	fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" )) 
	userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
	process = user_doc_read(data_doc['documentId']['docLog'],data_doc['documentId']['docNbr']['doubleValue'],data_doc['documentId']['docOrigin'],data_doc['documentId']['docSeries']['doubleValue'])
	print(process['userdocProcessId']['processNbr']+" "+process['userdocProcessId']['processType'])

	#####################################################################################################
	group_name = f'{fecha} [Escrito+expediente]'
	if group_today(userId, group_name) != False:

		ProcessGroupAddProcess(
								str(group_today(userId, group_name)[1]), 
								userId, 
								process['userdocProcessId']['processNbr'],
								process['userdocProcessId']['processType']
								)
	else:
		pass
	#####################################################################################################
	if group_today(userId, group_name) == False:
		ProcessGroupInsert(
							last_group(userId)+1,
							userId,
							fecha,
							'Creado por M.E.A.',
							'1',
							'10')

		ProcessGroupAddProcess(
								str(group_today(userId, group_name)[1]), 
								userId, 
								process['userdocProcessId']['processNbr'],
								process['userdocProcessId']['processType']
								)
	
	else:
		pass


def Insert_Group_Process_reg_ren(fileNbr,user,typ):
	try:
		expediente = mark_getlist(fileNbr)
		fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" )) 
		userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
		data = mark_read(
			expediente[0]['fileId']['fileNbr']['doubleValue'], 
			expediente[0]['fileId']['fileSeq'], 
			expediente[0]['fileId']['fileSeries']['doubleValue'], 
			expediente[0]['fileId']['fileType'])
		group_count = last_group(userId) # cantidad de grupos que tiene el usuario
		if valid_group(userId,group_typ(str(typ)),typ) == False: # no existe el grupo
			print((group_count + 1),userId,group_typ(str(typ)),'descripcion','1',typ)
			ProcessGroupInsert((group_count + 1),userId,fecha,'descripcion','1',typ)
			time.sleep(1) 
			ProcessGroupAddProcess((group_count + 1),userId,data['file']['processId']['processNbr']['doubleValue'],data['file']['processId']['processType'])
			res = 'true'
		else: # existe el grupo
			ProcessGroupAddProcess(group_today(userId,group_typ(str(typ)),typ),userId,data['file']['processId']['processNbr']['doubleValue'],data['file']['processId']['processType'])
			res = 'true'
		return(res)
	except Exception as e:
		return('false')

def valid_group(userNbr,groupName,typ):
	try:
		print(ProcessGroupGetList(userNbr)[0].processGroupName)
		for i in range(len(ProcessGroupGetList(userNbr))):
			processGroupname:bool = False
			data = ProcessGroupGetList(userNbr)[i]
			processGroupname = groupName in data.processGroupName # existe el nombre de grupo
			if str(processGroupname) == 'None':
				resp = False
			if str(processGroupname) == 'True':
				if str(data.processType) == str(typ):
					resp = True
			else:
				resp = False
		return(resp)
	except Exception as e:
		return(False)

def ProcessGroupGetList(userNbr):
	try:
		data = {
					"arg0": {
						"userNbr": {
						"doubleValue":userNbr
						}
					}
				}
		return(clientMark.service.ProcessGroupGetList(**data))
	except zeep.exceptions.Fault as e:
		return(e)

def last_group(userNbr):
	list = []
	list_int = []
	data = ProcessGroupGetList(userNbr)
	for i in range(0,len(data)):
		list.append(data[i].processGroupId.processGroupCode)
	for i in list:
		list_int.append(int(i))
	list_int.sort()
	ultimo = int(len(list_int))-1
	#print(list_int)
	return(list_int[ultimo])

def fileResave(ORIGIN):
	try:
		daily_log_open("2023-05-30")
		data = {
				"arg0": ORIGIN,
				"arg1": "REG",
				"arg2": "MS",

				"arg4": {
					"dateValue": "2023-05-30"
				},
				"arg5": {
					"currencyType": "",
					"DReceiptAmount": "",
					"receiptDate": {
					"dateValue": ""
					},
					"receiptNbr": "",
					"receiptType": ""
				},
				"arg6": {
					"fileNbr": {
					"doubleValue": "23006290"
					},
					"fileSeq": "PY",
					"fileSeries": {
					"doubleValue": "2023"
					},
					"fileType": "M"
				},
				"arg7": {
					"docLog": "E",
					"docNbr": {
					"doubleValue": "23006290"
					},
					"docOrigin": ORIGIN,
					"docSeries": {
					"doubleValue": "2023"
					},
					"selected": ""
				},
				"arg8": "PRUEBA M.E.A."
				}	
		clientMark.service.FileReceive(**data)
		print(daily_log_close("2023-05-30"))
		return(True)
	except zeep.exceptions.Fault as e:
		daily_log_close("2023-05-30")
		return(e)			

def Insert_Group_Process_docs_test(fileNbr,user,typ):
	try:
		data_doc = user_doc_getList_escrito(fileNbr)
		
		fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" )) 

		userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
		
		process = user_doc_read(data_doc['documentId']['docLog'],data_doc['documentId']['docNbr']['doubleValue'],data_doc['documentId']['docOrigin'],data_doc['documentId']['docSeries']['doubleValue'])
		
		print(process['userdocProcessId']['processNbr']+" "+process['userdocProcessId']['processType'])

		group_count = last_group(userId) # cantidad de grupos que tiene el usuario

		print(group_count)

		print(group_typ(typ))

		if valid_group(userId,group_typ(str(typ)),typ) != group_typ(typ): # no existe el grupo

			print('Crear grupo')		
			ProcessGroupInsert((group_count + 1),userId,fecha,'descripcion','1',typ) 
			
			#ProcessGroupAddProcess((group_count + 1),userId,process['userdocProcessId']['processNbr'],process['userdocProcessId']['processType'])
			
			res = 'true'
		
		else: # existe el grupo
			
			ProcessGroupAddProcess(group_today(userId,group_typ(str(typ)),typ), userId, process['userdocProcessId']['processNbr'],process['userdocProcessId']['processType'])
			
			res = 'true'

		return(res)
	except Exception as e:
		return(e)


#captura de error
default_val_e99 = lambda arg: arg if arg != "" else ""
def catch_toError(form_Id):
	print(pendiente_sfe(form_Id))
	getExcept = userDocModel()
	getExcept.setData(form_Id)
	data_list = [getExcept.affectedFileIdList_fileNbr,
	getExcept.affectedFileIdList_fileSeq,
	getExcept.affectedFileIdList_fileSeries,
	getExcept.affectedFileIdList_fileType,
	getExcept.affected_doc_Log,
	getExcept.affected_doc_docNbr,
	getExcept.affected_doc_docOrigin,
	getExcept.affected_doc_docSeries,
	getExcept.affectedFileSummaryList_disclaimer,
	getExcept.affectedFileSummaryList_disclaimerInOtherLang,
	getExcept.affectedFileSummaryList_fileNbr,
	getExcept.affectedFileSummaryList_fileSeq,
	getExcept.affectedFileSummaryList_fileSeries,
	getExcept.affectedFileSummaryList_fileType,
	getExcept.affectedFileSummaryList_fileIdAsString,
	getExcept.affectedFileSummaryList_fileSummaryClasses,
	getExcept.affectedFileSummaryList_fileSummaryCountry,
	getExcept.affectedFileSummaryList_fileSummaryDescription,
	getExcept.affectedFileSummaryList_fileSummaryDescriptionInOtherLang,
	getExcept.affectedFileSummaryList_fileSummaryOwner,
	getExcept.affectedFileSummaryList_fileSummaryOwnerInOtherLang,
	getExcept.affectedFileSummaryList_fileSummaryRepresentative,
	getExcept.affectedFileSummaryList_fileSummaryRepresentativeInOtherLang,
	getExcept.affectedFileSummaryList_fileSummaryResponsibleName,
	getExcept.affectedFileSummaryList_fileSummaryStatus,

	getExcept.applicant_applicantNotes,
	getExcept.applicant_person_addressStreet,
	getExcept.applicant_person_addressStreetInOtherLang,
	getExcept.applicant_person_addressZone,
	getExcept.applicant_person_agentCode,
	getExcept.applicant_person_cityCode,
	getExcept.applicant_person_cityName,
	getExcept.applicant_person_companyRegisterRegistrationDate,
	getExcept.applicant_person_companyRegisterRegistrationNbr,
	getExcept.applicant_person_email,
	getExcept.applicant_person_individualIdNbr,
	getExcept.applicant_person_individualIdType,
	getExcept.applicant_person_legalIdNbr,
	getExcept.applicant_person_legalIdType,
	getExcept.applicant_person_legalNature,
	getExcept.applicant_person_legalNatureInOtherLang,
	default_val_e99(getExcept.applicant_person_nationalityCountryCode),
	getExcept.applicant_person_personGroupCode,
	getExcept.applicant_person_personGroupName,
	default_val_e99(getExcept.applicant_person_personName),
	getExcept.applicant_person_personNameInOtherLang,
	default_val_e99(getExcept.applicant_person_residenceCountryCode),
	getExcept.applicant_person_stateCode,
	getExcept.applicant_person_stateName,
	getExcept.applicant_person_telephone,
	getExcept.applicant_person_zipCode,

	default_val_e99(getExcept.documentId_docLog),
	default_val_e99(getExcept.documentId_docNbr),
	default_val_e99(str(connex.MEA_SFE_FORMULARIOS_ID_Origin)),
	default_val_e99(getExcept.documentId_docSeries),
	getExcept.documentId_selected,
	default_val_e99(getExcept.documentSeqId_docSeqName),
	default_val_e99(getExcept.documentSeqId_docSeqNbr),
	default_val_e99(getExcept.documentSeqId_docSeqSeries),
	default_val_e99(getExcept.documentSeqId_docSeqType),
	getExcept.filingData_applicationSubtype,
	getExcept.filingData_applicationType,
	default_val_e99(getExcept.filingData_captureDate),
	default_val_e99(getExcept.filingData_captureUserId),
	default_val_e99(getExcept.filingData_filingDate),
	getExcept.filingData_lawCode,
	getExcept.filingData_novelty1Date,
	getExcept.filingData_novelty2Date,
	getExcept.filingData_paymentList_currencyName,
	getExcept.filingData_paymentList_currencyType,
	getExcept.filingData_paymentList_receiptAmount,
	getExcept.filingData_paymentList_receiptDate,
	getExcept.filingData_paymentList_receiptNbr,
	getExcept.filingData_paymentList_receiptNotes,
	getExcept.filingData_paymentList_receiptType,
	getExcept.filingData_paymentList_receiptTypeName,
	default_val_e99(getExcept.filingData_receptionDate),
	default_val_e99(getExcept.filingData_documentId_receptionDocument_docLog),
	default_val_e99(getExcept.filingData_documentId_receptionDocument_docNbr),
	default_val_e99(str(connex.MEA_SFE_FORMULARIOS_ID_Origin)),
	default_val_e99(getExcept.filingData_documentId_receptionDocument_docSeries),
	getExcept.filingData_documentId_receptionDocument_selected,
	default_val_e99(getExcept.filingData_userdocTypeList_userdocName),
	default_val_e99(getExcept.filingData_userdocTypeList_userdocType),

	getExcept.newOwnershipData_ownerList_orderNbr,
	getExcept.newOwnershipData_ownerList_ownershipNotes,
	getExcept.newOwnershipData_ownerList_person_addressStreet,
	getExcept.newOwnershipData_ownerList_person_addressStreetInOtherLang,
	getExcept.newOwnershipData_ownerList_person_addressZone,
	default_val_e99(str(getExcept.newOwnershipData_ownerList_person_agentCode)),
	getExcept.newOwnershipData_ownerList_person_cityCode,
	getExcept.newOwnershipData_ownerList_person_cityName,
	getExcept.newOwnershipData_ownerList_person_companyRegisterRegistrationDate,
	getExcept.newOwnershipData_ownerList_person_companyRegisterRegistrationNbr,
	getExcept.newOwnershipData_ownerList_person_email,
	getExcept.newOwnershipData_ownerList_person_individualIdNbr,
	getExcept.newOwnershipData_ownerList_person_individualIdType,
	getExcept.newOwnershipData_ownerList_person_legalIdNbr,
	getExcept.newOwnershipData_ownerList_person_legalIdType,
	getExcept.newOwnershipData_ownerList_person_legalNature,
	getExcept.newOwnershipData_ownerList_person_legalNatureInOtherLang,
	default_val_e99(getExcept.newOwnershipData_ownerList_person_nationalityCountryCode),
	getExcept.newOwnershipData_ownerList_person_personGroupCode,
	getExcept.newOwnershipData_ownerList_person_personGroupName,
	default_val_e99(getExcept.newOwnershipData_ownerList_person_personName),
	getExcept.newOwnershipData_ownerList_person_personNameInOtherLang,
	default_val_e99(getExcept.newOwnershipData_ownerList_person_residenceCountryCode),
	getExcept.newOwnershipData_ownerList_person_stateCode,
	getExcept.newOwnershipData_ownerList_person_stateName,
	getExcept.newOwnershipData_ownerList_person_telephone,
	getExcept.newOwnershipData_ownerList_person_zipCode,

	getExcept.notes,
	getExcept.poaData_poaGranteeList_person_addressStreet,
	getExcept.poaData_poaGranteeList_person_addressStreetInOtherLang,
	getExcept.poaData_poaGranteeList_person_addressZone,
	getExcept.poaData_poaGranteeList_person_agentCode,
	getExcept.poaData_poaGranteeList_person_cityCode,
	getExcept.poaData_poaGranteeList_person_cityName,
	getExcept.poaData_poaGranteeList_person_companyRegisterRegistrationDate,
	getExcept.poaData_poaGranteeList_person_companyRegisterRegistrationNbr,
	getExcept.poaData_poaGranteeList_person_email,
	getExcept.poaData_poaGranteeList_person_individualIdNbr,
	getExcept.poaData_poaGranteeList_person_individualIdType,
	getExcept.poaData_poaGranteeList_person_legalIdNbr,
	getExcept.poaData_poaGranteeList_person_legalIdType,
	getExcept.poaData_poaGranteeList_person_legalNature,
	getExcept.poaData_poaGranteeList_person_legalNatureInOtherLang,
	getExcept.poaData_poaGranteeList_person_nationalityCountryCode,
	getExcept.poaData_poaGranteeList_person_personGroupCode,
	getExcept.poaData_poaGranteeList_person_personGroupName,
	getExcept.poaData_poaGranteeList_person_personName,
	getExcept.poaData_poaGranteeList_person_personNameInOtherLang,
	getExcept.poaData_poaGranteeList_person_residenceCountryCode,
	getExcept.poaData_poaGranteeList_person_stateCode,
	getExcept.poaData_poaGranteeList_person_stateName,
	getExcept.poaData_poaGranteeList_person_telephone,
	getExcept.poaData_poaGranteeList_person_zipCode,
	getExcept.poaData_poaGrantor_person_addressStreet,
	getExcept.poaData_poaGrantor_person_addressStreetInOtherLang,
	getExcept.poaData_poaGrantor_person_addressZone,
	getExcept.poaData_poaGrantor_person_agentCode,
	getExcept.poaData_poaGrantor_person_cityCode,
	getExcept.poaData_poaGrantor_person_cityName,
	getExcept.poaData_poaGrantor_person_companyRegisterRegistrationDate,
	getExcept.poaData_poaGrantor_person_companyRegisterRegistrationNbr,
	getExcept.poaData_poaGrantor_person_email,
	getExcept.poaData_poaGrantor_person_individualIdNbr,
	getExcept.poaData_poaGrantor_person_individualIdType,
	getExcept.poaData_poaGrantor_person_legalIdNbr,
	getExcept.poaData_poaGrantor_person_legalIdType,
	getExcept.poaData_poaGrantor_person_legalNature,
	getExcept.poaData_poaGrantor_person_legalNatureInOtherLang,
	getExcept.poaData_poaGrantor_person_nationalityCountryCode,
	getExcept.poaData_poaGrantor_person_personGroupCode,
	getExcept.poaData_poaGrantor_person_personGroupName,
	getExcept.poaData_poaGrantor_person_personName,
	getExcept.poaData_poaGrantor_person_personNameInOtherLang,
	getExcept.poaData_poaGrantor_person_residenceCountryCode,
	getExcept.poaData_poaGrantor_person_stateCode,
	getExcept.poaData_poaGrantor_person_stateName,
	getExcept.poaData_poaGrantor_person_telephone,
	getExcept.poaData_poaGrantor_person_zipCode,
	getExcept.poaData_poaRegNumber,
	getExcept.poaData_scope,
	default_val_e99(getExcept.representationData_representativeList_person_addressStreet),
	getExcept.representationData_representativeList_person_addressStreetInOtherLang,
	getExcept.representationData_representativeList_person_addressZone,
	default_val_e99(getExcept.representationData_representativeList_person_agentCode),
	getExcept.representationData_representativeList_person_cityCode,
	getExcept.representationData_representativeList_person_cityName,
	getExcept.representationData_representativeList_person_companyRegisterRegistrationDate,
	getExcept.representationData_representativeList_person_companyRegisterRegistrationNbr,
	default_val_e99(getExcept.representationData_representativeList_person_email),
	getExcept.representationData_representativeList_person_individualIdNbr,
	getExcept.representationData_representativeList_person_individualIdType,
	getExcept.representationData_representativeList_person_legalIdNbr,
	getExcept.representationData_representativeList_person_legalIdType,
	getExcept.representationData_representativeList_person_legalNature,
	getExcept.representationData_representativeList_person_legalNatureInOtherLang,
	default_val_e99(getExcept.representationData_representativeList_person_nationalityCountryCode),
	getExcept.representationData_representativeList_person_personGroupCode,
	getExcept.representationData_representativeList_person_personGroupName,
	default_val_e99(getExcept.representationData_representativeList_person_personName),
	getExcept.representationData_representativeList_person_personNameInOtherLang,
	default_val_e99(getExcept.representationData_representativeList_person_residenceCountryCode),
	getExcept.representationData_representativeList_person_stateCode,
	getExcept.representationData_representativeList_person_stateName,
	getExcept.representationData_representativeList_person_telephone,
	getExcept.representationData_representativeList_person_zipCode,
	getExcept.representationData_representativeList_representativeType]

	E99_code = ["affectedFileIdList_fileNbr","affectedFileIdList_fileSeq","affectedFileIdList_fileSeries","affectedFileIdList_fileType","affected_doc_Log","affected_doc_docNbr","affected_doc_docOrigin","affected_doc_docSeries","affectedFileSummaryList_disclaimer","affectedFileSummaryList_disclaimerInOtherLang","affectedFileSummaryList_fileNbr","affectedFileSummaryList_fileSeq","affectedFileSummaryList_fileSeries","affectedFileSummaryList_fileType","affectedFileSummaryList_fileIdAsString","affectedFileSummaryList_fileSummaryClasses","affectedFileSummaryList_fileSummaryCountry","affectedFileSummaryList_fileSummaryDescription","affectedFileSummaryList_fileSummaryDescriptionInOtherLang","affectedFileSummaryList_fileSummaryOwner","affectedFileSummaryList_fileSummaryOwnerInOtherLang","affectedFileSummaryList_fileSummaryRepresentative","affectedFileSummaryList_fileSummaryRepresentativeInOtherLang","affectedFileSummaryList_fileSummaryResponsibleName","affectedFileSummaryList_fileSummaryStatus","applicant_applicantNotes","applicant_person_addressStreet","applicant_person_addressStreetInOtherLang","applicant_person_addressZone","applicant_person_agentCode","applicant_person_cityCode","applicant_person_cityName","applicant_person_companyRegisterRegistrationDate","applicant_person_companyRegisterRegistrationNbr","applicant_person_email","applicant_person_individualIdNbr","applicant_person_individualIdType","applicant_person_legalIdNbr","applicant_person_legalIdType","applicant_person_legalNature","applicant_person_legalNatureInOtherLang","applicant_person_nationalityCountryCode","applicant_person_personGroupCode","applicant_person_personGroupName","applicant_person_personName","applicant_person_personNameInOtherLang","applicant_person_residenceCountryCode","applicant_person_stateCode","applicant_person_stateName","applicant_person_telephone","applicant_person_zipCode","documentId_docLog","documentId_docNbr","documentId_docOrigin","documentId_docSeries","documentId_selected","documentSeqId_docSeqName","documentSeqId_docSeqNbr","documentSeqId_docSeqSeries","documentSeqId_docSeqType","filingData_applicationSubtype","filingData_applicationType","filingData_captureDate","filingData_captureUserId","filingData_filingDate","filingData_lawCode","filingData_novelty1Date","filingData_novelty2Date","filingData_paymentList_currencyName","filingData_paymentList_currencyType","filingData_paymentList_receiptAmount","filingData_paymentList_receiptDate","filingData_paymentList_receiptNbr","filingData_paymentList_receiptNotes","filingData_paymentList_receiptType","filingData_paymentList_receiptTypeName","filingData_receptionDate","filingData_documentId_receptionDocument_docLog","filingData_documentId_receptionDocument_docNbr","filingData_documentId_receptionDocument_docOrigin","filingData_documentId_receptionDocument_docSeries","filingData_documentId_receptionDocument_selected","filingData_userdocTypeList_userdocName","filingData_userdocTypeList_userdocType","newOwnershipData_ownerList_orderNbr","newOwnershipData_ownerList_ownershipNotes","newOwnershipData_ownerList_person_addressStreet","newOwnershipData_ownerList_person_addressStreetInOtherLang","newOwnershipData_ownerList_person_addressZone","newOwnershipData_ownerList_person_agentCode","newOwnershipData_ownerList_person_cityCode","newOwnershipData_ownerList_person_cityName","newOwnershipData_ownerList_person_companyRegisterRegistrationDate","newOwnershipData_ownerList_person_companyRegisterRegistrationNbr","newOwnershipData_ownerList_person_email","newOwnershipData_ownerList_person_individualIdNbr","newOwnershipData_ownerList_person_individualIdType","newOwnershipData_ownerList_person_legalIdNbr","newOwnershipData_ownerList_person_legalIdType","newOwnershipData_ownerList_person_legalNature","newOwnershipData_ownerList_person_legalNatureInOtherLang","newOwnershipData_ownerList_person_nationalityCountryCode","newOwnershipData_ownerList_person_personGroupCode","newOwnershipData_ownerList_person_personGroupName","newOwnershipData_ownerList_person_personName","newOwnershipData_ownerList_person_personNameInOtherLang","newOwnershipData_ownerList_person_residenceCountryCode","newOwnershipData_ownerList_person_stateCode","newOwnershipData_ownerList_person_stateName","newOwnershipData_ownerList_person_telephone","newOwnershipData_ownerList_person_zipCode","notes","poaData_poaGranteeList_person_addressStreet","poaData_poaGranteeList_person_addressStreetInOtherLang","poaData_poaGranteeList_person_addressZone","poaData_poaGranteeList_person_agentCode","poaData_poaGranteeList_person_cityCode","poaData_poaGranteeList_person_cityName","poaData_poaGranteeList_person_companyRegisterRegistrationDate","poaData_poaGranteeList_person_companyRegisterRegistrationNbr","poaData_poaGranteeList_person_email","poaData_poaGranteeList_person_individualIdNbr","poaData_poaGranteeList_person_individualIdType","poaData_poaGranteeList_person_legalIdNbr","poaData_poaGranteeList_person_legalIdType","poaData_poaGranteeList_person_legalNature","poaData_poaGranteeList_person_legalNatureInOtherLang","poaData_poaGranteeList_person_nationalityCountryCode","poaData_poaGranteeList_person_personGroupCode","poaData_poaGranteeList_person_personGroupName","poaData_poaGranteeList_person_personName","poaData_poaGranteeList_person_personNameInOtherLang","poaData_poaGranteeList_person_residenceCountryCode","poaData_poaGranteeList_person_stateCode","poaData_poaGranteeList_person_stateName","poaData_poaGranteeList_person_telephone","poaData_poaGranteeList_person_zipCode","poaData_poaGrantor_person_addressStreet","poaData_poaGrantor_person_addressStreetInOtherLang","poaData_poaGrantor_person_addressZone","poaData_poaGrantor_person_agentCode","poaData_poaGrantor_person_cityCode","poaData_poaGrantor_person_cityName","poaData_poaGrantor_person_companyRegisterRegistrationDate","poaData_poaGrantor_person_companyRegisterRegistrationNbr","poaData_poaGrantor_person_email","poaData_poaGrantor_person_individualIdNbr","poaData_poaGrantor_person_individualIdType","poaData_poaGrantor_person_legalIdNbr","poaData_poaGrantor_person_legalIdType","poaData_poaGrantor_person_legalNature","poaData_poaGrantor_person_legalNatureInOtherLang","poaData_poaGrantor_person_nationalityCountryCode","poaData_poaGrantor_person_personGroupCode","poaData_poaGrantor_person_personGroupName","poaData_poaGrantor_person_personName","poaData_poaGrantor_person_personNameInOtherLang","poaData_poaGrantor_person_residenceCountryCode","poaData_poaGrantor_person_stateCode","poaData_poaGrantor_person_stateName","poaData_poaGrantor_person_telephone","poaData_poaGrantor_person_zipCode","poaData_poaRegNumber","poaData_scope","representationData_representativeList_person_addressStreet","representationData_representativeList_person_addressStreetInOtherLang","representationData_representativeList_person_addressZone","representationData_representativeList_person_agentCode","representationData_representativeList_person_cityCode","representationData_representativeList_person_cityName","representationData_representativeList_person_companyRegisterRegistrationDate","representationData_representativeList_person_companyRegisterRegistrationNbr","representationData_representativeList_person_email","representationData_representativeList_person_individualIdNbr","representationData_representativeList_person_individualIdType","representationData_representativeList_person_legalIdNbr","representationData_representativeList_person_legalIdType","representationData_representativeList_person_legalNature","representationData_representativeList_person_legalNatureInOtherLang","representationData_representativeList_person_nationalityCountryCode","representationData_representativeList_person_personGroupCode","representationData_representativeList_person_personGroupName","representationData_representativeList_person_personName","representationData_representativeList_person_personNameInOtherLang","representationData_representativeList_person_residenceCountryCode","representationData_representativeList_person_stateCode","representationData_representativeList_person_stateName","representationData_representativeList_person_telephone","representationData_representativeList_person_zipCode","representationData_representativeList_representativeType"]
	print(data_list)
	for i in range(0,len(data_list)):
		if data_list[i] == "E99":
			data_validator(f'dato requerido: {E99_code[i]}, tabla tramites ID: {form_Id}','false',form_Id)
			cambio_estado_soporte(form_Id)
			rule_notification('SOP',form_Id)
			return("E99")
		else:
			return("True")

def respuesta_sfe_campo(arg):
	try:
		list_campos = []
		list_valores = {}
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
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
		list_valores['firmado_at'] = str(row[0][11])
		list_valores['pagado_at'] = str(row[0][12])
		list_valores['enviado_at'] = str(row[0][15])
		list_valores['expediente_afectado'] = str(row[0][19])
		list_valores['tipo_documento_id'] = str(row[0][25])
		for i in range(0,len(row[0][6])):
			list_campos.append(row[0][6][i]['campo'])
		
		#print(" ")
		#print('[[[[[[[Lista de campos]]]]]]]]]')
		#print(list_campos)

		#print(" ")
		#print('(((((((((]Lista de valores[)))))))))')

		for item in range(0,len(list_campos)):
			for x in list_campos:
				if row[0][6][item]['campo'] == x:
					try:
						list_valores[x] = row[0][6][item]['valor']
					except Exception as e:
						list_valores[x] = 'sin valor'

	except Exception as e:
		print(e)
	finally:
		conn.close()
	return(list_valores)

model_test = userDocModel_test()

model_test.setData('1613')
"""
print(model_test.affectedFileIdList_fileNbr)
print(model_test.affectedFileIdList_fileSeq)
print(model_test.affectedFileIdList_fileSeries)
print(model_test.affectedFileIdList_fileType)
print(model_test.affected_doc_Log)
print(model_test.affected_doc_docNbr)
print(model_test.affected_doc_docOrigin)
print(model_test.affected_doc_docSeries)
print(model_test.affectedFileSummaryList_disclaimer)
print(model_test.affectedFileSummaryList_disclaimerInOtherLang)
print(model_test.affectedFileSummaryList_fileNbr)
print(model_test.affectedFileSummaryList_fileSeq)
print(model_test.affectedFileSummaryList_fileSeries)
print(model_test.affectedFileSummaryList_fileType)
print(model_test.affectedFileSummaryList_fileIdAsString)
print(model_test.affectedFileSummaryList_fileSummaryClasses)
print(model_test.affectedFileSummaryList_fileSummaryCountry)
print(model_test.affectedFileSummaryList_fileSummaryDescription)
print(model_test.affectedFileSummaryList_fileSummaryDescriptionInOtherLang)
print(model_test.affectedFileSummaryList_fileSummaryOwner)
print(model_test.affectedFileSummaryList_fileSummaryOwnerInOtherLang)
print(model_test.affectedFileSummaryList_fileSummaryRepresentative)
print(model_test.affectedFileSummaryList_fileSummaryRepresentativeInOtherLang)
print(model_test.affectedFileSummaryList_fileSummaryResponsibleName)
print(model_test.affectedFileSummaryList_fileSummaryStatus)
print(model_test.applicant_applicantNotes)
print(model_test.applicant_person_addressStreet)
print(model_test.applicant_person_addressStreetInOtherLang)
print(model_test.applicant_person_addressZone)
print(model_test.applicant_person_agentCode)
print(model_test.applicant_person_cityCode)
print(model_test.applicant_person_cityName)
print(model_test.applicant_person_companyRegisterRegistrationDate)
print(model_test.applicant_person_companyRegisterRegistrationNbr)
print(model_test.applicant_person_email)
print(model_test.applicant_person_individualIdNbr)
print(model_test.applicant_person_individualIdType)
print(model_test.applicant_person_legalIdNbr)
print(model_test.applicant_person_legalIdType)
print(model_test.applicant_person_legalNature)
print(model_test.applicant_person_legalNatureInOtherLang)
print(model_test.applicant_person_nationalityCountryCode)
print(model_test.applicant_person_personGroupCode)
print(model_test.applicant_person_personGroupName)
print(model_test.applicant_person_personName)
print(model_test.applicant_person_personNameInOtherLang)
print(model_test.applicant_person_residenceCountryCode)
print(model_test.applicant_person_stateCode)
print(model_test.applicant_person_stateName)
print(model_test.applicant_person_telephone)
print(model_test.applicant_person_zipCode)
print(model_test.documentId_docLog)
print(model_test.documentId_docNbr)
print(model_test.documentId_docOrigin)
print(model_test.documentId_docSeries)
print(model_test.documentId_selected)
print(model_test.documentSeqId_docSeqName)
print(model_test.documentSeqId_docSeqNbr)
print(model_test.documentSeqId_docSeqSeries)
print(model_test.documentSeqId_docSeqType)
print(model_test.filingData_applicationSubtype)
print(model_test.filingData_applicationType)
print(model_test.filingData_captureDate)
print(model_test.filingData_captureUserId)
print(model_test.filingData_filingDate)
print(model_test.filingData_lawCode)
print(model_test.filingData_novelty1Date)
print(model_test.filingData_novelty2Date)
print(model_test.filingData_paymentList_currencyName)
print(model_test.filingData_paymentList_currencyType)
print(model_test.filingData_paymentList_receiptAmount)
print(model_test.filingData_paymentList_receiptDate)
print(model_test.filingData_paymentList_receiptNbr)
print(model_test.filingData_paymentList_receiptNotes)
print(model_test.filingData_paymentList_receiptType)
print(model_test.filingData_paymentList_receiptTypeName)
print(model_test.filingData_receptionDate)
print(model_test.filingData_documentId_receptionDocument_docLog)
print(model_test.filingData_documentId_receptionDocument_docNbr)
print(model_test.filingData_documentId_receptionDocument_docOrigin)
print(model_test.filingData_documentId_receptionDocument_docSeries)
print(model_test.filingData_documentId_receptionDocument_selected)
print(model_test.filingData_userdocTypeList_userdocName)
print(model_test.filingData_userdocTypeList_userdocType)
print(model_test.newOwnershipData_ownerList_orderNbr)
print(model_test.newOwnershipData_ownerList_ownershipNotes)
print(model_test.newOwnershipData_ownerList_person_addressStreet)
print(model_test.newOwnershipData_ownerList_person_addressStreetInOtherLang)
print(model_test.newOwnershipData_ownerList_person_addressZone)
print(model_test.newOwnershipData_ownerList_person_agentCode)
print(model_test.newOwnershipData_ownerList_person_cityCode)
print(model_test.newOwnershipData_ownerList_person_cityName)
print(model_test.newOwnershipData_ownerList_person_companyRegisterRegistrationDate)
print(model_test.newOwnershipData_ownerList_person_companyRegisterRegistrationNbr)
print(model_test.newOwnershipData_ownerList_person_email)
print(model_test.newOwnershipData_ownerList_person_individualIdNbr)
print(model_test.newOwnershipData_ownerList_person_individualIdType)
print(model_test.newOwnershipData_ownerList_person_legalIdNbr)
print(model_test.newOwnershipData_ownerList_person_legalIdType)
print(model_test.newOwnershipData_ownerList_person_legalNature)
print(model_test.newOwnershipData_ownerList_person_legalNatureInOtherLang)
print(model_test.newOwnershipData_ownerList_person_nationalityCountryCode)
print(model_test.newOwnershipData_ownerList_person_personGroupCode)
print(model_test.newOwnershipData_ownerList_person_personGroupName)
print(model_test.newOwnershipData_ownerList_person_personName)
print(model_test.newOwnershipData_ownerList_person_personNameInOtherLang)
print(model_test.newOwnershipData_ownerList_person_residenceCountryCode)
print(model_test.newOwnershipData_ownerList_person_stateCode)
print(model_test.newOwnershipData_ownerList_person_stateName)
print(model_test.newOwnershipData_ownerList_person_telephone)
print(model_test.newOwnershipData_ownerList_person_zipCode)
print(model_test.notes)
print(model_test.poaData_poaGranteeList_person_addressStreet)
print(model_test.poaData_poaGranteeList_person_addressStreetInOtherLang)
print(model_test.poaData_poaGranteeList_person_addressZone)
print(model_test.poaData_poaGranteeList_person_agentCode)
print(model_test.poaData_poaGranteeList_person_cityCode)
print(model_test.poaData_poaGranteeList_person_cityName)
print(model_test.poaData_poaGranteeList_person_companyRegisterRegistrationDate)
print(model_test.poaData_poaGranteeList_person_companyRegisterRegistrationNbr)
print(model_test.poaData_poaGranteeList_person_email)
print(model_test.poaData_poaGranteeList_person_individualIdNbr)
print(model_test.poaData_poaGranteeList_person_individualIdType)
print(model_test.poaData_poaGranteeList_person_legalIdNbr)
print(model_test.poaData_poaGranteeList_person_legalIdType)
print(model_test.poaData_poaGranteeList_person_legalNature)
print(model_test.poaData_poaGranteeList_person_legalNatureInOtherLang)
print(model_test.poaData_poaGranteeList_person_nationalityCountryCode)
print(model_test.poaData_poaGranteeList_person_personGroupCode)
print(model_test.poaData_poaGranteeList_person_personGroupName)
print(model_test.poaData_poaGranteeList_person_personName)
print(model_test.poaData_poaGranteeList_person_personNameInOtherLang)
print(model_test.poaData_poaGranteeList_person_residenceCountryCode)
print(model_test.poaData_poaGranteeList_person_stateCode)
print(model_test.poaData_poaGranteeList_person_stateName)
print(model_test.poaData_poaGranteeList_person_telephone)
print(model_test.poaData_poaGranteeList_person_zipCode)
print(model_test.poaData_poaGrantor_person_addressStreet)
print(model_test.poaData_poaGrantor_person_addressStreetInOtherLang)
print(model_test.poaData_poaGrantor_person_addressZone)
print(model_test.poaData_poaGrantor_person_agentCode)
print(model_test.poaData_poaGrantor_person_cityCode)
print(model_test.poaData_poaGrantor_person_cityName)
print(model_test.poaData_poaGrantor_person_companyRegisterRegistrationDate)
print(model_test.poaData_poaGrantor_person_companyRegisterRegistrationNbr)
print(model_test.poaData_poaGrantor_person_email)
print(model_test.poaData_poaGrantor_person_individualIdNbr)
print(model_test.poaData_poaGrantor_person_individualIdType)
print(model_test.poaData_poaGrantor_person_legalIdNbr)
print(model_test.poaData_poaGrantor_person_legalIdType)
print(model_test.poaData_poaGrantor_person_legalNature)
print(model_test.poaData_poaGrantor_person_legalNatureInOtherLang)
print(model_test.poaData_poaGrantor_person_nationalityCountryCode)
print(model_test.poaData_poaGrantor_person_personGroupCode)
print(model_test.poaData_poaGrantor_person_personGroupName)
print(model_test.poaData_poaGrantor_person_personName)
print(model_test.poaData_poaGrantor_person_personNameInOtherLang)
print(model_test.poaData_poaGrantor_person_residenceCountryCode)
print(model_test.poaData_poaGrantor_person_stateCode)
print(model_test.poaData_poaGrantor_person_stateName)
print(model_test.poaData_poaGrantor_person_telephone)
print(model_test.poaData_poaGrantor_person_zipCode)
print(model_test.poaData_poaRegNumber)
print(model_test.poaData_scope)
print(model_test.representationData_representativeList_person_addressStreet)
print(model_test.representationData_representativeList_person_addressStreetInOtherLang)
print(model_test.representationData_representativeList_person_addressZone)
print(model_test.representationData_representativeList_person_agentCode)
print(model_test.representationData_representativeList_person_cityCode)
print(model_test.representationData_representativeList_person_cityName)
print(model_test.representationData_representativeList_person_companyRegisterRegistrationDate)
print(model_test.representationData_representativeList_person_companyRegisterRegistrationNbr)
print(model_test.representationData_representativeList_person_email)
print(model_test.representationData_representativeList_person_individualIdNbr)
print(model_test.representationData_representativeList_person_individualIdType)
print(model_test.representationData_representativeList_person_legalIdNbr)
print(model_test.representationData_representativeList_person_legalIdType)
print(model_test.representationData_representativeList_person_legalNature)
print(model_test.representationData_representativeList_person_legalNatureInOtherLang)
print(model_test.representationData_representativeList_person_nationalityCountryCode)
print(model_test.representationData_representativeList_person_personGroupCode)
print(model_test.representationData_representativeList_person_personGroupName)
print(model_test.representationData_representativeList_person_personName)
print(model_test.representationData_representativeList_person_personNameInOtherLang)
print(model_test.representationData_representativeList_person_residenceCountryCode)
print(model_test.representationData_representativeList_person_stateCode)
print(model_test.representationData_representativeList_person_stateName)
print(model_test.representationData_representativeList_person_telephone)
print(model_test.representationData_representativeList_person_zipCode)
print(model_test.representationData_representativeList_representativeType)
"""

def test_renov(arg):
	global_data = {}
	try:
		conn = psycopg2.connect(
					host = '192.168.50.219',
					user= 'user-developer',
					password = 'user-developer--201901',
					database = 'db_sfe_production'
				)
		cursor = conn.cursor()
		cursor.execute("""select t.id,t.fecha,t.formulario_id,f.nombre as nombre_formulario ,t.estado as estado_id,case when t.estado =7 then 'Enviado' when t.estado =8 then 'Recepcionado' end estado_desc,
								to_char(t.created_at,'yyyy-mm-dd hh24:mi:ss')created_at,to_char(t.updated_at,'yyyy-mm-dd hh24:mi:ss')updated_at,t.respuestas,t.costo,t.usuario_id, t.deleted_at,
								t.codigo,t.firmado_at,to_char(t.pagado_at,'yyyy-mm-dd hh24:mi:ss') as pagado_at,t.expediente_id,t.pdf_url,to_char(t.enviado_at,'yyyy-mm-dd hh24:mi:ss') as enviado_at,
								to_char(t.recepcionado_at,'yyyy-mm-dd hh24:mi:ss') as recepcionado_at,t.nom_funcionario,t.pdf,t.expediente_afectado,t.notificacion_id,t.expedientes_autor,t.autorizado_por_id,u.nombre as nombre_agente,pa.numero_agente,
								u.email as email_agente,pa.celular as telefonoAgente,pa.domicilio_agpi,t.nom_funcionario as funcionario_autorizado 
								from tramites t join formularios f on t.formulario_id  = f.id  
								join usuarios u on u.id = t.usuario_id  
								join perfiles_agentes pa on pa.usuario_id = u.id         
								where t.id = {};""".format(int(arg)))
		row=cursor.fetchall()
		#print(row[0][10])
		global_data['fecha_envio'] = str(row[0][17])
		global_data['expediente'] = str(row[0][15])
		global_data['fecha_solicitud'] = str(row[0][18])
		global_data['codigo_barr'] = str(row[0][12])
		global_data['usuario'] = str(row[0][10])
		global_data['code_agente'] = str(row[0][26])
		global_data['nombre_agente'] = str(row[0][25])
		global_data['dir_agente'] = str(row[0][29])
		global_data['TEL_agente'] = str(row[0][28])
		global_data['email_agente'] = str(row[0][27])
		global_data['nombre_formulario'] = str(row[0][3])
		

		for i in row[0][8]:
			try:
				print(i['campo'])
			except Exception as e:
				print("")			
			try:
				print(i['valor'])
			except Exception as e:
				print("")
		return(global_data)
	except Exception as e:
		print(e)
	finally:
		conn.close()	

#print(test_renov('1815'))

"""
ren = insertRenModel()

ren.setData('1795')

print(ren.file_fileId_fileNbr)
print(ren.file_fileId_fileSeq)
print(ren.file_fileId_fileSeries)
print(ren.file_fileId_fileType)
print(ren.file_filingData_applicationSubtype)
print(ren.file_filingData_applicationType)
print(ren.file_filingData_captureUserId)
print(ren.file_filingData_filingDate)
print(ren.file_filingData_captureDate)
print(ren.file_filingData_lawCode)
print(ren.file_filingData_paymentList_currencyType)
print(ren.file_filingData_paymentList_receiptAmount)
print(ren.file_filingData_paymentList_receiptDate)
print(ren.file_filingData_paymentList_receiptNbr)
print(ren.file_filingData_paymentList_receiptNotes)
print(ren.file_filingData_paymentList_receiptType)
print(ren.file_filingData_receptionUserId)
print(ren.file_ownershipData_ownerList_person_owneraddressStreet)
print(ren.file_ownershipData_ownerList_person_ownernationalityCountryCode)
print(ren.file_ownershipData_ownerList_person_ownerpersonName)
print(ren.file_ownershipData_ownerList_person_ownerresidenceCountryCode)
print(ren.file_rowVersion)
print(ren.agentCode)
print(ren.file_relationshipList_fileId_fileNbr)
print(ren.file_relationshipList_fileId_fileSeq)
print(ren.file_relationshipList_fileId_fileSeries)
print(ren.file_relationshipList_fileId_fileType)
print(ren.file_relationshipList_relationshipRole)
print(ren.file_relationshipList_relationshipType)
print(ren.file_representationData_representativeList_representativeType)
print(ren.rowVersion)
print(ren.protectionData_dummy)
print(ren.protectionData_niceClassList_niceClassDescription)
print(ren.protectionData_niceClassList_niceClassDetailedStatus)
print(ren.protectionData_niceClassList_niceClassEdition)
print(ren.protectionData_niceClassList_niceClassGlobalStatus)
print(ren.protectionData_niceClassList_niceClassNbr)
print(ren.protectionData_niceClassList_niceClassVersion)
print(decode_img(ren.logoData))
print(ren.logoType)
print(ren.signData_markName)
print(ren.signData_signType)"""

#exists = str(user_doc_read_min('E','2341453','3','2023')['documentId']['docNbr']['doubleValue']).replace(".0","")

#buscar el nombre de grupo para hoy para [expediente]
#print(group_today('298', '06/06/2023 [Expediente]')) #=> (user, fecha, typ) respuesta: nombre de grupo o  False 

#buscar el nombre de grupo para hoy para [Escrito+expediente]
#print(group_today('298', '06/06/2023', '10')) #=> (user, fecha, typ) respuesta: nombre de grupo o  False 

#buscar el nombre de grupo para hoy para [escrito]
#print(group_today('298', '06/06/2023', '11')) #=> (user, fecha, typ) respuesta: nombre de grupo o  False 


#si existe el nombre => insertar el documento
#ProcessGroupAddProcess(group_today('298', '06/06/2023', '1'), '298', 'processNbr', 'processType')

#si no existe => buscar el ultimo numero de grupo, sumar uno y crear el grupo de hoy => insertar el documento
#buscar el ultimo numero de grupo
#print(last_group('298'))



#CREA GRUPO PARA EXPEDIENTE DE TIPO REN Y REG - (REQUIERE USUSARIO Y EXPEDIENTE)
#insertar_o_crear_grupo_escritoMasExpediente('AMEDINA','2332001')


#envio_agente_reg('23808')

#renovacion_pdf_sfe_local('1814')

#getFile_reg_and_ren('23808','2341236')

#envio_agente_recibido_ren('1815','2341244')

#envio_agente_recibido('1904','2341242')

#Insert_Group_Process_docs_test('2300605','CABENITEZ','11')

#print(respuesta_sfe_campo('1547')['datospersonales_direccion'])

#print(catch_toError('1585'))

#crear grupo
#print(ProcessGroupInsert('1','298','31/05/2023','','1','10'))

#print(COMMIT_NBR())


def filter_user(sig,exp):
	try:
		if exist_main_mark(sig) == 'S':
			status_exp = main_State(exp)
			return(status_exp)
		else:
			return(sig)
	except Exception as e:
		return(sig)

#print(filter_user('CEM','2341306'))

print(USER_GROUP('DAJ1'))

#'23006441'

#EXISTE O NO EL GRUPO USUARIO DE LA FECHA
#print(group_today('298', '06/06/2023', '1'))


#print(group_typ('10'))

#print(Insert_Group_Process_reg_ren('23006295','CABENITEZ','1'))

#print(valid_group('297',group_typ('10'),'10'))

#print(fileResave('3'))

#print(last_group('297'))

#print(Insert_Group_Process('1','2177877','AMEDINA','1'))

#print(USER_GROUP('REN'))





