from ast import Break, Pass
from dataclasses import replace
import numbers
from sqlite3 import Time
import string
import time
from time import sleep
from email_pdf_AG import  envio_agente_recibido
from models.InsertUserDocModel import userDocModel
from dinapi.sfe import cambio_estado, cambio_estado_soporte, count_pendiente, data_validator, esc_relation, exp_relation, format_userdoc, pago_id, paymentYeasOrNot, pendiente_sfe, pendientes_sfe, pendientes_sfe_not_pag, process_day_Nbr, process_day_commit_Nbr, reglas_me_ttasa, tasa_id
from getFileDoc import getFile
from tools.send_mail import delete_file, enviar
import tools.filing_date as captureDate
import tools.connect as connex
from wipo.function_for_reception_in import insert_user_doc_escritos, user_doc_getList_escrito, user_doc_read_min
from wipo.ipas import user_doc_afectado, user_doc_receive, user_doc_update
import zeep
import asyncio
import threading

default_val_e99 = lambda arg: arg if arg != "" else "E99"
list_id = []
sigla:string = ''
def listar():
	#print('............................................................................')
	captura_pendientes() # Captura lista pendiente
	time.sleep(int(connex.MEA_TIEMPO_ACTUALIZACION))#int(connex.MEA_TIEMPO_ACTUALIZACION)
	listar()

def captura_pendientes():
	list_id = []
	today = time.strftime("%Y-%m-%d")
	for i in pendientes_sfe_not_pag(today):
		try:
			sigla_doc = str(i['tool_tip']).split("-")
			if i['estado'] == 7:
				list_id.append(str(i['Id'])+"/"+str(sigla_doc[0]))
		except Exception as e:
			pass
	#print(list_id)
	if list_id != []:
		for i in list_id:
			params = str(i).split('/')
			#print('doc pendiente '+str(params[0]))
			insert_list(str(params[0]),str(params[1]))
			time.sleep(1)

#arg0 id and arg1 sigla in state 7
def insert_list(arg0:string,arg1:string):
	
	pago = str(paymentYeasOrNot(arg1)[0]).replace("None","N")
	pago_auth:str = str(pago_id(arg0)).replace("None","sin dato en bancar")
	valid_rules:str = []
	#print(' ')
	#print(arg0) #tramite ID	
	#print(str(arg1)) #TIPO DE DOCUMENTO

	#////////////////////////////////////////||||||||||||||||||||||||||||||||||||||||///////////////////////////////////////#
	exceptions = userDocModel()
	if exceptions.exist_split(arg0,'observacion_documentos') == False:
		data_validator(f'No existe documento adjunto, tabla tramites ID: {arg0}')
		cambio_estado_soporte(arg0)
		#listar()
		return("E99")

	getFile(arg0,str(int(process_day_Nbr())+1))
		
	#CONSULTA SI HAY RELACION DE EXPEDIENTE__________________________________________________________________________________________ 
	if exp_relation(arg1)[0] == 'S': 
		if pendiente_sfe(arg0)[0]['expediente_afectad'] != 'None': 
			valid_rules.append('Ok')
		else:
			data_validator(f'El expediente relacionado es requerido, tabla tramites ID: {arg0}')
			valid_rules.append('Error')
			cambio_estado_soporte(arg0)
	else:
		valid_rules.append('Not')
	#FIN_____________________________________________________________________________________________________________________________ 

	#CONSULTA SI HAY RELACION DE ESCRITO______________________________________________________________________________________________	
	if esc_relation(arg1)[0] == 'S':
		if pendiente_sfe(arg0)[0]['expediente_afectad'] != 'None': 
			valid_rules.append('Ok')
		else:
			data_validator(f'El escrito relacionado es requerido, tabla tramites ID: {arg0}')
			valid_rules.append('Error')
			cambio_estado_soporte(arg0)
	else:
		valid_rules.append('Not')
	#FIN_____________________________________________________________________________________________________________________________

	#CONSULTA SI EL TIPO ES CON PAGO_____________________________________________________________________________________________________
	if pago == 'S':
			if pago_auth != 'sin dato en bancar':
				valid_rules.append('Ok')
			else:
				data_validator(f'Confirmar relacion con pago (bancard transactions), tabla tramites ID: {arg0}')
				valid_rules.append('Error')
				cambio_estado_soporte(arg0)
	else:
		valid_rules.append('Not')
	#FIN_____________________________________________________________________________________________________________________________	

	####################################################################################################################################
	####################################################################################################################################
	####################################################################################################################################
	####################################################################################################################################
	####################################################################################################################################

	if valid_rules == ['Ok', 'Not', 'Not']: 
		#print('ESCRITO CON RELACION')		
		compileAndInsert(arg0,arg1)
		time.sleep(1)
	elif valid_rules == ['Ok', 'Not', 'Ok']:
		#print('ESCRITO CON RELACION')		
		compileAndInsert(arg0,arg1)
		time.sleep(1)	
	elif valid_rules == ['Not', 'Ok', 'Not']:
		#print('ESCRTO A ESCRITO')
		compileAndInsertUserDocUserDoc(arg0,arg1)
		time.sleep(1)
	elif valid_rules == ['Not', 'Ok', 'Ok']:
		#print('ESCRTO A ESCRITO')
		compileAndInsertUserDocUserDocPago(arg0,arg1)
		time.sleep(1)
	elif valid_rules == ['Not', 'Not', 'Ok']:
		#print('ESCRITO SIN RELACION')		
		compileAndInsert(arg0,arg1)
		time.sleep(1)
	elif valid_rules == ['Not', 'Not', 'Not']:
		#print('ESCRITO SIN RELACION')		
		compileAndInsert(arg0,arg1)
		time.sleep(1)
	else:
		pass

	return("Ok")		

def compileAndInsert(form_Id,typ):
		catch_toError(form_Id)

		insert_doc = userDocModel()
		insert_doc.setData(form_Id)
		
		try:
			insert_user_doc_escritos(
						insert_doc.affectedFileIdList_fileNbr,
						insert_doc.affectedFileIdList_fileSeq,
						insert_doc.affectedFileIdList_fileSeries,
						insert_doc.affectedFileIdList_fileType,
						insert_doc.affectedFileSummaryList_disclaimer,
						insert_doc.affectedFileSummaryList_disclaimerInOtherLang,
						insert_doc.affectedFileSummaryList_fileNbr,
						insert_doc.affectedFileSummaryList_fileSeq,
						insert_doc.affectedFileSummaryList_fileSeries,
						insert_doc.affectedFileSummaryList_fileType,
						insert_doc.affectedFileSummaryList_fileIdAsString,
						insert_doc.affectedFileSummaryList_fileSummaryClasses,
						insert_doc.affectedFileSummaryList_fileSummaryCountry,
						insert_doc.affectedFileSummaryList_fileSummaryDescription,
						insert_doc.affectedFileSummaryList_fileSummaryDescriptionInOtherLang,
						insert_doc.affectedFileSummaryList_fileSummaryOwner,
						insert_doc.affectedFileSummaryList_fileSummaryOwnerInOtherLang,
						insert_doc.affectedFileSummaryList_fileSummaryRepresentative,
						insert_doc.affectedFileSummaryList_fileSummaryRepresentativeInOtherLang,
						insert_doc.affectedFileSummaryList_fileSummaryResponsibleName,
						insert_doc.affectedFileSummaryList_fileSummaryStatus,
						insert_doc.applicant_applicantNotes,
						insert_doc.applicant_person_addressStreet,
						insert_doc.applicant_person_addressStreetInOtherLang,
						insert_doc.applicant_person_addressZone,
						insert_doc.applicant_person_agentCode,
						insert_doc.applicant_person_cityCode,
						insert_doc.applicant_person_cityName,
						insert_doc.applicant_person_companyRegisterRegistrationDate,
						insert_doc.applicant_person_companyRegisterRegistrationNbr,
						insert_doc.applicant_person_email,
						insert_doc.applicant_person_individualIdNbr,
						insert_doc.applicant_person_individualIdType,
						insert_doc.applicant_person_legalIdNbr,
						insert_doc.applicant_person_legalIdType,
						insert_doc.applicant_person_legalNature,
						insert_doc.applicant_person_legalNatureInOtherLang,
						insert_doc.applicant_person_nationalityCountryCode,
						insert_doc.applicant_person_personGroupCode,
						insert_doc.applicant_person_personGroupName,
						insert_doc.applicant_person_personName,
						insert_doc.applicant_person_personNameInOtherLang,
						insert_doc.applicant_person_residenceCountryCode,
						insert_doc.applicant_person_stateCode,
						insert_doc.applicant_person_stateName,
						insert_doc.applicant_person_telephone,
						insert_doc.applicant_person_zipCode,
						insert_doc.documentId_docLog,
						insert_doc.documentId_docNbr,
						insert_doc.documentId_docOrigin,
						insert_doc.documentId_docSeries,
						insert_doc.documentId_selected,
						insert_doc.documentSeqId_docSeqName,
						insert_doc.documentSeqId_docSeqNbr,
						insert_doc.documentSeqId_docSeqSeries,
						insert_doc.documentSeqId_docSeqType,
						insert_doc.filingData_applicationSubtype,
						insert_doc.filingData_applicationType,
						insert_doc.filingData_captureDate,
						connex.MEA_PERIODO_RECEPCION_userId, #insert_doc.filingData_captureUserId
						insert_doc.filingData_filingDate,
						insert_doc.filingData_lawCode,
						insert_doc.filingData_novelty1Date,
						insert_doc.filingData_novelty2Date,
						insert_doc.filingData_paymentList_currencyName,
						insert_doc.filingData_paymentList_currencyType,
						insert_doc.filingData_paymentList_receiptAmount,
						insert_doc.filingData_paymentList_receiptDate,
						insert_doc.filingData_paymentList_receiptNbr,
						insert_doc.filingData_paymentList_receiptNotes,
						insert_doc.filingData_paymentList_receiptType,
						insert_doc.filingData_paymentList_receiptTypeName,
						insert_doc.filingData_receptionDate,
						insert_doc.filingData_documentId_receptionDocument_docLog,
						insert_doc.filingData_documentId_receptionDocument_docNbr,
						insert_doc.filingData_documentId_receptionDocument_docOrigin,
						insert_doc.filingData_documentId_receptionDocument_docSeries,
						insert_doc.filingData_documentId_receptionDocument_selected,
						insert_doc.filingData_userdocTypeList_userdocName,
						insert_doc.filingData_userdocTypeList_userdocType,
						insert_doc.newOwnershipData_ownerList_orderNbr,
						insert_doc.newOwnershipData_ownerList_ownershipNotes,
						insert_doc.newOwnershipData_ownerList_person_addressStreet,
						insert_doc.newOwnershipData_ownerList_person_addressStreetInOtherLang,
						insert_doc.newOwnershipData_ownerList_person_addressZone,
						insert_doc.newOwnershipData_ownerList_person_agentCode,
						insert_doc.newOwnershipData_ownerList_person_cityCode,
						insert_doc.newOwnershipData_ownerList_person_cityName,
						insert_doc.newOwnershipData_ownerList_person_companyRegisterRegistrationDate,
						insert_doc.newOwnershipData_ownerList_person_companyRegisterRegistrationNbr,
						insert_doc.newOwnershipData_ownerList_person_email,
						insert_doc.newOwnershipData_ownerList_person_individualIdNbr,
						insert_doc.newOwnershipData_ownerList_person_individualIdType,
						insert_doc.newOwnershipData_ownerList_person_legalIdNbr,
						insert_doc.newOwnershipData_ownerList_person_legalIdType,
						insert_doc.newOwnershipData_ownerList_person_legalNature,
						insert_doc.newOwnershipData_ownerList_person_legalNatureInOtherLang,
						insert_doc.newOwnershipData_ownerList_person_nationalityCountryCode,
						insert_doc.newOwnershipData_ownerList_person_personGroupCode,
						insert_doc.newOwnershipData_ownerList_person_personGroupName,
						insert_doc.newOwnershipData_ownerList_person_personName,
						insert_doc.newOwnershipData_ownerList_person_personNameInOtherLang,
						insert_doc.newOwnershipData_ownerList_person_residenceCountryCode,
						insert_doc.newOwnershipData_ownerList_person_stateCode,
						insert_doc.newOwnershipData_ownerList_person_stateName,
						insert_doc.newOwnershipData_ownerList_person_telephone,
						insert_doc.newOwnershipData_ownerList_person_zipCode,
						insert_doc.notes,
						insert_doc.poaData_poaGranteeList_person_addressStreet,
						insert_doc.poaData_poaGranteeList_person_addressStreetInOtherLang,
						insert_doc.poaData_poaGranteeList_person_addressZone,
						insert_doc.poaData_poaGranteeList_person_agentCode,
						insert_doc.poaData_poaGranteeList_person_cityCode,
						insert_doc.poaData_poaGranteeList_person_cityName,
						insert_doc.poaData_poaGranteeList_person_companyRegisterRegistrationDate,
						insert_doc.poaData_poaGranteeList_person_companyRegisterRegistrationNbr,
						insert_doc.poaData_poaGranteeList_person_email,
						insert_doc.poaData_poaGranteeList_person_individualIdNbr,
						insert_doc.poaData_poaGranteeList_person_individualIdType,
						insert_doc.poaData_poaGranteeList_person_legalIdNbr,
						insert_doc.poaData_poaGranteeList_person_legalIdType,
						insert_doc.poaData_poaGranteeList_person_legalNature,
						insert_doc.poaData_poaGranteeList_person_legalNatureInOtherLang,
						insert_doc.poaData_poaGranteeList_person_nationalityCountryCode,
						insert_doc.poaData_poaGranteeList_person_personGroupCode,
						insert_doc.poaData_poaGranteeList_person_personGroupName,
						insert_doc.poaData_poaGranteeList_person_personName,
						insert_doc.poaData_poaGranteeList_person_personNameInOtherLang,
						insert_doc.poaData_poaGranteeList_person_residenceCountryCode,
						insert_doc.poaData_poaGranteeList_person_stateCode,
						insert_doc.poaData_poaGranteeList_person_stateName,
						insert_doc.poaData_poaGranteeList_person_telephone,
						insert_doc.poaData_poaGranteeList_person_zipCode,
						insert_doc.poaData_poaGrantor_person_addressStreet,
						insert_doc.poaData_poaGrantor_person_addressStreetInOtherLang,
						insert_doc.poaData_poaGrantor_person_addressZone,
						insert_doc.poaData_poaGrantor_person_agentCode,
						insert_doc.poaData_poaGrantor_person_cityCode,
						insert_doc.poaData_poaGrantor_person_cityName,
						insert_doc.poaData_poaGrantor_person_companyRegisterRegistrationDate,
						insert_doc.poaData_poaGrantor_person_companyRegisterRegistrationNbr,
						insert_doc.poaData_poaGrantor_person_email,
						insert_doc.poaData_poaGrantor_person_individualIdNbr,
						insert_doc.poaData_poaGrantor_person_individualIdType,
						insert_doc.poaData_poaGrantor_person_legalIdNbr,
						insert_doc.poaData_poaGrantor_person_legalIdType,
						insert_doc.poaData_poaGrantor_person_legalNature,
						insert_doc.poaData_poaGrantor_person_legalNatureInOtherLang,
						insert_doc.poaData_poaGrantor_person_nationalityCountryCode,
						insert_doc.poaData_poaGrantor_person_personGroupCode,
						insert_doc.poaData_poaGrantor_person_personGroupName,
						insert_doc.poaData_poaGrantor_person_personName,
						insert_doc.poaData_poaGrantor_person_personNameInOtherLang,
						insert_doc.poaData_poaGrantor_person_residenceCountryCode,
						insert_doc.poaData_poaGrantor_person_stateCode,
						insert_doc.poaData_poaGrantor_person_stateName,
						insert_doc.poaData_poaGrantor_person_telephone,
						insert_doc.poaData_poaGrantor_person_zipCode,
						insert_doc.poaData_poaRegNumber,
						insert_doc.poaData_scope,
						insert_doc.representationData_representativeList_person_addressStreet,
						insert_doc.representationData_representativeList_person_addressStreetInOtherLang,
						insert_doc.representationData_representativeList_person_addressZone,
						insert_doc.representationData_representativeList_person_agentCode,
						insert_doc.representationData_representativeList_person_cityCode,
						insert_doc.representationData_representativeList_person_cityName,
						insert_doc.representationData_representativeList_person_companyRegisterRegistrationDate,
						insert_doc.representationData_representativeList_person_companyRegisterRegistrationNbr,
						insert_doc.representationData_representativeList_person_email,
						insert_doc.representationData_representativeList_person_individualIdNbr,
						insert_doc.representationData_representativeList_person_individualIdType,
						insert_doc.representationData_representativeList_person_legalIdNbr,
						insert_doc.representationData_representativeList_person_legalIdType,
						insert_doc.representationData_representativeList_person_legalNature,
						insert_doc.representationData_representativeList_person_legalNatureInOtherLang,
						insert_doc.representationData_representativeList_person_nationalityCountryCode,
						insert_doc.representationData_representativeList_person_personGroupCode,
						insert_doc.representationData_representativeList_person_personGroupName,
						insert_doc.representationData_representativeList_person_personName,
						insert_doc.representationData_representativeList_person_personNameInOtherLang,
						insert_doc.representationData_representativeList_person_residenceCountryCode,
						insert_doc.representationData_representativeList_person_stateCode,
						insert_doc.representationData_representativeList_person_stateName,
						insert_doc.representationData_representativeList_person_telephone,
						insert_doc.representationData_representativeList_person_zipCode,
						insert_doc.representationData_representativeList_representativeType)
			process_day_commit_Nbr()
		except zeep.exceptions.Fault as e:
			data_validator(f'Error de IPAS => {str(e)}, tabla tramites ID: {form_Id}')
			cambio_estado_soporte(form_Id)
		
		try:
			exists = str(user_doc_read_min('E',insert_doc.documentId_docNbr,insert_doc.documentId_docOrigin,insert_doc.documentId_docSeries)['documentId']['docNbr']['doubleValue']).replace(".0","") 
			if exists == insert_doc.documentId_docNbr:
				cambio_estado(form_Id,insert_doc.documentId_docNbr)
				time.sleep(1)
				envio_agente_recibido(form_Id,insert_doc.documentId_docNbr)	#Crear PDF
				time.sleep(1)
				delete_file(enviar('notificacion-DINAPI.pdf',insert_doc.representationData_representativeList_person_email,'M.E.A',''))	#Enviar Correo Electronico				
		except Exception as e:
			data_validator(f'Error al cambiar estado de esc. N° {insert_doc.documentId_docNbr}, tabla tramites ID: {form_Id}')
			cambio_estado_soporte(form_Id)			

def compileAndInsertUserDocUserDoc(form_Id,typ):	
		catch_toError(form_Id)
		escrito_relacionado = userDocModel()
		escrito_relacionado.setData(form_Id)

		try:
			print(user_doc_receive(
						"1",
						escrito_relacionado.filingData_userdocTypeList_userdocType,
						"true",
						"",
						"",
						"",
						"",
						"",
						"",
						"",
						str(captureDate.capture_day()),
						"",
						"",
						"",
						"",
						"",
						escrito_relacionado.filingData_captureUserId,#item['filingData_captureUserId']
						"SFE test - Aplicante M.E.A",
						escrito_relacionado.affected_doc_Log,
						escrito_relacionado.affected_doc_docNbr,
						escrito_relacionado.affected_doc_docOrigin, 
						escrito_relacionado.affected_doc_docSeries,
						"",
						"",
						"",
						"",
						"",
						escrito_relacionado.documentId_docLog,
						escrito_relacionado.documentId_docNbr,
						escrito_relacionado.documentId_docOrigin,
						escrito_relacionado.documentId_docSeries,
						escrito_relacionado.filingData_userdocTypeList_userdocType))
			process_day_commit_Nbr()
		except zeep.exceptions.Fault as e:
			data_validator(f'Error de IPAS receive => {str(e)}, tabla tramites ID: {form_Id}')
			cambio_estado_soporte(form_Id)

		time.sleep(1)
	
		sigla_desc = str(escrito_relacionado.filingData_userdocTypeList_userdocName).split("- ")

		try:
			print(user_doc_update(
						escrito_relacionado.affected_doc_Log,
						escrito_relacionado.affected_doc_docNbr,
						escrito_relacionado.affected_doc_docOrigin, 
						escrito_relacionado.affected_doc_docSeries,
						escrito_relacionado.applicant_applicantNotes,
						escrito_relacionado.applicant_person_addressStreet,
						escrito_relacionado.applicant_person_cityName,
						escrito_relacionado.applicant_person_email,
						escrito_relacionado.applicant_person_nationalityCountryCode,
						escrito_relacionado.applicant_person_personName,
						escrito_relacionado.applicant_person_residenceCountryCode,
						escrito_relacionado.applicant_person_telephone,
						escrito_relacionado.applicant_person_zipCode,
						escrito_relacionado.documentId_docLog,
						escrito_relacionado.documentId_docNbr,
						escrito_relacionado.documentId_docOrigin,
						escrito_relacionado.documentId_docSeries,
						escrito_relacionado.documentSeqId_docSeqNbr,
						escrito_relacionado.documentSeqId_docSeqSeries,
						escrito_relacionado.documentSeqId_docSeqType,
						escrito_relacionado.filingData_captureDate,
						escrito_relacionado.filingData_captureUserId,
						escrito_relacionado.filingData_filingDate,
						escrito_relacionado.filingData_receptionDate,
						escrito_relacionado.filingData_paymentList_currencyName,
						escrito_relacionado.filingData_paymentList_currencyType,
						escrito_relacionado.filingData_paymentList_receiptAmount,
						escrito_relacionado.filingData_paymentList_receiptDate,
						escrito_relacionado.filingData_paymentList_receiptNbr,
						escrito_relacionado.filingData_paymentList_receiptNotes,
						escrito_relacionado.filingData_paymentList_receiptType,
						escrito_relacionado.filingData_paymentList_receiptTypeName,		
						escrito_relacionado.filingData_documentId_receptionDocument_docNbr,
						escrito_relacionado.filingData_documentId_receptionDocument_docOrigin,
						escrito_relacionado.filingData_documentId_receptionDocument_docSeries,
						sigla_desc[1],
						escrito_relacionado.filingData_userdocTypeList_userdocType,					
						"1",
						escrito_relacionado.newOwnershipData_ownerList_ownershipNotes,
						escrito_relacionado.newOwnershipData_ownerList_person_addressStreet,
						escrito_relacionado.newOwnershipData_ownerList_person_cityName,
						escrito_relacionado.newOwnershipData_ownerList_person_email,
						escrito_relacionado.newOwnershipData_ownerList_person_nationalityCountryCode,
						escrito_relacionado.newOwnershipData_ownerList_person_personName,
						escrito_relacionado.newOwnershipData_ownerList_person_residenceCountryCode,
						escrito_relacionado.newOwnershipData_ownerList_person_telephone,
						escrito_relacionado.newOwnershipData_ownerList_person_zipCode,
						escrito_relacionado.notes,
						escrito_relacionado.representationData_representativeList_person_addressStreet,
						escrito_relacionado.representationData_representativeList_person_addressZone,
						escrito_relacionado.representationData_representativeList_person_agentCode,
						escrito_relacionado.representationData_representativeList_person_cityName,
						escrito_relacionado.representationData_representativeList_person_individualIdNbr,
						escrito_relacionado.representationData_representativeList_person_individualIdType,
						escrito_relacionado.representationData_representativeList_person_legalIdNbr,
						escrito_relacionado.representationData_representativeList_person_legalIdType,
						escrito_relacionado.representationData_representativeList_person_legalNature,					
						escrito_relacionado.representationData_representativeList_person_nationalityCountryCode,
						escrito_relacionado.representationData_representativeList_person_personName,
						escrito_relacionado.representationData_representativeList_person_personNameInOtherLang,
						escrito_relacionado.representationData_representativeList_person_residenceCountryCode,
						escrito_relacionado.representationData_representativeList_person_telephone,
						escrito_relacionado.representationData_representativeList_person_zipCode,
						escrito_relacionado.representationData_representativeList_representativeType,
						escrito_relacionado.representationData_representativeList_person_email))
		except zeep.exceptions.Fault as e:
			data_validator(f'Error de IPAS update => {str(e)}, tabla tramites ID: {form_Id}')
			cambio_estado_soporte(form_Id)

		time.sleep(1)
		
		afferc = user_doc_read_min(escrito_relacionado.affected_doc_Log,escrito_relacionado.affected_doc_docNbr,escrito_relacionado.affected_doc_docOrigin,escrito_relacionado.affected_doc_docSeries)
		#print(afferc)
		try:
			if afferc['affectedFileIdList'][0]['fileSeq'] == 'PY':
				user_doc_afectado(
									escrito_relacionado.documentId_docLog,
									escrito_relacionado.documentId_docNbr,
									escrito_relacionado.documentId_docOrigin,
									escrito_relacionado.documentId_docSeries,
									afferc['affectedFileIdList'][0]['fileNbr']['doubleValue'],
									afferc['affectedFileIdList'][0]['fileSeq'],
									afferc['affectedFileIdList'][0]['fileSeries']['doubleValue'],
									afferc['affectedFileIdList'][0]['fileType'])
			else:
				pass
		except Exception as e:
				pass
				#data_validator(f'Error de IPAS affectedFileIdList => {str(e)}, tabla tramites ID: {form_Id}')
				#cambio_estado_soporte(form_Id)

		time.sleep(1)
		
		newDoc = str(user_doc_read_min('E',escrito_relacionado.documentId_docNbr,escrito_relacionado.documentId_docOrigin,escrito_relacionado.documentId_docSeries)['documentId']['docNbr']['doubleValue']).replace(".0","") 
		if newDoc == escrito_relacionado.documentId_docNbr:
			cambio_estado(form_Id,escrito_relacionado.documentId_docNbr)
			time.sleep(1)
			envio_agente_recibido(form_Id,escrito_relacionado.documentId_docNbr)		#Crear PDF
			time.sleep(1)
			delete_file(enviar('notificacion-DINAPI.pdf',escrito_relacionado.representationData_representativeList_person_email,'M.E.A',''))	#Enviar Correo Electronico
		else:
			data_validator(f'Error al cambiar estado de esc. N° {escrito_relacionado.documentId_docNbr}, tabla tramites ID: {form_Id}')
			cambio_estado_soporte(form_Id)

		time.sleep(0.5)
		
def compileAndInsertUserDocUserDocPago(form_Id,typ):	
		catch_toError(form_Id)
		escrito_escrito_pago = userDocModel()
		escrito_escrito_pago.setData(form_Id)

		try:
			print(user_doc_receive(
						"1",
						escrito_escrito_pago.filingData_userdocTypeList_userdocType,
						"true",
						"",
						"",
						"",
						"",
						"",
						"",
						"",
						str(captureDate.capture_day()),
						"",
						"",
						"",
						"",
						"",
						escrito_escrito_pago.filingData_captureUserId,
						"SFE test - Aplicante M.E.A",
						escrito_escrito_pago.affected_doc_Log,
						escrito_escrito_pago.affected_doc_docNbr,
						escrito_escrito_pago.affected_doc_docOrigin, 
						escrito_escrito_pago.affected_doc_docSeries,
						"",
						"",
						"",
						"",
						"",
						escrito_escrito_pago.documentId_docLog,
						escrito_escrito_pago.documentId_docNbr,
						escrito_escrito_pago.documentId_docOrigin,
						escrito_escrito_pago.documentId_docSeries,
						escrito_escrito_pago.filingData_userdocTypeList_userdocType))
			process_day_commit_Nbr()
		except zeep.exceptions.Fault as e:
			data_validator(f'Error de IPAS receive => {str(e)}, tabla tramites ID: {form_Id}')
			cambio_estado_soporte(form_Id)

		time.sleep(1)
		
		sigla_desc = str(escrito_escrito_pago.filingData_userdocTypeList_userdocName).split("- ")				
		try:
			print(user_doc_update(
						escrito_escrito_pago.affected_doc_Log,
						escrito_escrito_pago.affected_doc_docNbr,
						escrito_escrito_pago.affected_doc_docOrigin, 
						escrito_escrito_pago.affected_doc_docSeries,
						escrito_escrito_pago.applicant_applicantNotes,
						escrito_escrito_pago.applicant_person_addressStreet,
						escrito_escrito_pago.applicant_person_cityName,
						escrito_escrito_pago.applicant_person_email,
						escrito_escrito_pago.applicant_person_nationalityCountryCode,
						escrito_escrito_pago.applicant_person_personName,
						escrito_escrito_pago.applicant_person_residenceCountryCode,
						escrito_escrito_pago.applicant_person_telephone,
						escrito_escrito_pago.applicant_person_zipCode,
						escrito_escrito_pago.documentId_docLog,
						escrito_escrito_pago.documentId_docNbr,
						escrito_escrito_pago.documentId_docOrigin,
						escrito_escrito_pago.documentId_docSeries,
						escrito_escrito_pago.documentSeqId_docSeqNbr,
						escrito_escrito_pago.documentSeqId_docSeqSeries,
						escrito_escrito_pago.documentSeqId_docSeqType,
						escrito_escrito_pago.filingData_captureDate,
						escrito_escrito_pago.filingData_captureUserId,
						escrito_escrito_pago.filingData_filingDate,
						escrito_escrito_pago.filingData_receptionDate,
						escrito_escrito_pago.filingData_paymentList_currencyName,
						escrito_escrito_pago.filingData_paymentList_currencyType,
						escrito_escrito_pago.filingData_paymentList_receiptAmount,
						escrito_escrito_pago.filingData_paymentList_receiptDate,
						escrito_escrito_pago.filingData_paymentList_receiptNbr,
						escrito_escrito_pago.filingData_paymentList_receiptNotes,
						escrito_escrito_pago.filingData_paymentList_receiptType,
						escrito_escrito_pago.filingData_paymentList_receiptTypeName,		
						escrito_escrito_pago.filingData_documentId_receptionDocument_docNbr,
						escrito_escrito_pago.filingData_documentId_receptionDocument_docOrigin,
						escrito_escrito_pago.filingData_documentId_receptionDocument_docSeries,
						sigla_desc[1],
						escrito_escrito_pago.filingData_userdocTypeList_userdocType,					
						"1",
						escrito_escrito_pago.newOwnershipData_ownerList_ownershipNotes,
						escrito_escrito_pago.newOwnershipData_ownerList_person_addressStreet,
						escrito_escrito_pago.newOwnershipData_ownerList_person_cityName,
						escrito_escrito_pago.newOwnershipData_ownerList_person_email,
						escrito_escrito_pago.newOwnershipData_ownerList_person_nationalityCountryCode,
						escrito_escrito_pago.newOwnershipData_ownerList_person_personName,
						escrito_escrito_pago.newOwnershipData_ownerList_person_residenceCountryCode,
						escrito_escrito_pago.newOwnershipData_ownerList_person_telephone,
						escrito_escrito_pago.newOwnershipData_ownerList_person_zipCode,
						escrito_escrito_pago.notes,
						escrito_escrito_pago.representationData_representativeList_person_addressStreet,
						escrito_escrito_pago.representationData_representativeList_person_addressZone,
						escrito_escrito_pago.representationData_representativeList_person_agentCode,
						escrito_escrito_pago.representationData_representativeList_person_cityName,
						escrito_escrito_pago.representationData_representativeList_person_individualIdNbr,
						escrito_escrito_pago.representationData_representativeList_person_individualIdType,
						escrito_escrito_pago.representationData_representativeList_person_legalIdNbr,
						escrito_escrito_pago.representationData_representativeList_person_legalIdType,
						escrito_escrito_pago.representationData_representativeList_person_legalNature,					
						escrito_escrito_pago.representationData_representativeList_person_nationalityCountryCode,
						escrito_escrito_pago.representationData_representativeList_person_personName,
						escrito_escrito_pago.representationData_representativeList_person_personNameInOtherLang,
						escrito_escrito_pago.representationData_representativeList_person_residenceCountryCode,
						escrito_escrito_pago.representationData_representativeList_person_telephone,
						escrito_escrito_pago.representationData_representativeList_person_zipCode,
						escrito_escrito_pago.representationData_representativeList_representativeType,
						escrito_escrito_pago.representationData_representativeList_person_email))
		except zeep.exceptions.Fault as e:
			data_validator(f'Error de IPAS update => {str(e)}, tabla tramites ID: {form_Id}')
			cambio_estado_soporte(form_Id)		
		
		time.sleep(1)
		
		afferc = user_doc_read_min('E',escrito_escrito_pago.affected_doc_docNbr,escrito_escrito_pago.affected_doc_docOrigin,escrito_escrito_pago.affected_doc_docSeries)
		#print(afferc)
		try:
			if afferc['affectedFileIdList'][0]['fileSeq'] == 'PY':
				user_doc_afectado(escrito_escrito_pago.documentId_docLog,
									escrito_escrito_pago.documentId_docNbr,
									escrito_escrito_pago.documentId_docOrigin,
									escrito_escrito_pago.documentId_docSeries,
									afferc['affectedFileIdList'][0]['fileNbr']['doubleValue'],
									afferc['affectedFileIdList'][0]['fileSeq'],
									afferc['affectedFileIdList'][0]['fileSeries']['doubleValue'],
									afferc['affectedFileIdList'][0]['fileType'])
			else:
				pass
		except Exception as e:
				pass
				#data_validator(f'Error de IPAS affectedFileIdList => {str(e)}, tabla tramites ID: {form_Id}')
				#cambio_estado_soporte(form_Id)
		
		time.sleep(1)
		
		newDoc = str(user_doc_read_min('E',escrito_escrito_pago.documentId_docNbr,escrito_escrito_pago.documentId_docOrigin,escrito_escrito_pago.documentId_docSeries)['documentId']['docNbr']['doubleValue']).replace(".0","") 
		if newDoc == escrito_escrito_pago.documentId_docNbr:
			cambio_estado(form_Id,escrito_escrito_pago.documentId_docNbr)
			time.sleep(1)
			envio_agente_recibido(form_Id,escrito_escrito_pago.documentId_docNbr)#Crear PDF
			time.sleep(1)
			delete_file(enviar(
			'notificacion-DINAPI.pdf',
			escrito_escrito_pago.representationData_representativeList_person_email,
			'M.E.A',
			''))#Enviar Correo Electronico			
		else:
			data_validator(f'Error al cambiar estado de esc. N° {escrito_escrito_pago.documentId_docNbr}, tabla tramites ID: {form_Id}')
			cambio_estado_soporte(form_Id)

def catch_toError(form_Id):
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
	getExcept.applicant_person_nationalityCountryCode,
	getExcept.applicant_person_personGroupCode,
	getExcept.applicant_person_personGroupName,
	getExcept.applicant_person_personName,
	getExcept.applicant_person_personNameInOtherLang,
	getExcept.applicant_person_residenceCountryCode,
	getExcept.applicant_person_stateCode,
	getExcept.applicant_person_stateName,
	getExcept.applicant_person_telephone,
	getExcept.applicant_person_zipCode,

	default_val_e99(getExcept.documentId_docLog),
	default_val_e99(getExcept.documentId_docNbr),
	default_val_e99(getExcept.documentId_docOrigin),
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
	default_val_e99(getExcept.filingData_documentId_receptionDocument_docOrigin),
	default_val_e99(getExcept.filingData_documentId_receptionDocument_docSeries),
	getExcept.filingData_documentId_receptionDocument_selected,
	default_val_e99(getExcept.filingData_userdocTypeList_userdocName),
	default_val_e99(getExcept.filingData_userdocTypeList_userdocType),

	getExcept.newOwnershipData_ownerList_orderNbr,
	getExcept.newOwnershipData_ownerList_ownershipNotes,
	getExcept.newOwnershipData_ownerList_person_addressStreet,
	getExcept.newOwnershipData_ownerList_person_addressStreetInOtherLang,
	getExcept.newOwnershipData_ownerList_person_addressZone,
	getExcept.newOwnershipData_ownerList_person_agentCode,
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
	getExcept.newOwnershipData_ownerList_person_nationalityCountryCode,
	getExcept.newOwnershipData_ownerList_person_personGroupCode,
	getExcept.newOwnershipData_ownerList_person_personGroupName,
	getExcept.newOwnershipData_ownerList_person_personName,
	getExcept.newOwnershipData_ownerList_person_personNameInOtherLang,
	getExcept.newOwnershipData_ownerList_person_residenceCountryCode,
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
	for i in range(0,len(data_list)):
		if data_list[i] == "E99":
			data_validator(f'dato requerido: {E99_code[i]}, tabla tramites ID: {form_Id}')
			cambio_estado_soporte(form_Id)
			return("E99")


#envio_agente_recibido('1547','2277877')

















"""
data = pendiente_sfe('1551')
for i in range(0,len(data[0]['respuestas'])):
	try:
		print(data[0]['respuestas'][i]['descripcion'])
	except Exception as e:
		print("sin descripcion")
	#print("")		
	try:
		print(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		print("no existe etiqueta (valor) en el bloque")
	print("----------------------------------------------------------------")

"""