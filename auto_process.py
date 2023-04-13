from ast import Break, Pass
from dataclasses import replace
import numbers
from sqlite3 import Time
import string
import time
from time import sleep
from unicodedata import numeric
from models.InsertUserDocModel import userDocModel
from dinapi.sfe import cambio_estado, cambio_estado_soporte, count_pendiente, esc_relation, exp_relation, format_userdoc, pago_id, paymentYeasOrNot, pendiente_sfe, pendientes_sfe, pendientes_sfe_not_pag, process_day_Nbr, process_day_commit_Nbr, reglas_me_ttasa, tasa_id
from getFileDoc import getFile
import tools.filing_date as captureDate
import tools.connect as connex
from wipo.function_for_reception_in import insert_user_doc_escritos, user_doc_getList_escrito, user_doc_read_min
from wipo.ipas import user_doc_afectado, user_doc_receive, user_doc_update
import zeep
import asyncio


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
		
def insert_list(arg0:string,arg1:string):
	
	pago = str(paymentYeasOrNot(arg1)[0]).replace("None","N")
	pago_auth:str = str(pago_id(arg0)).replace("None","sin dato en bancar")
	valid_rules:str = []
	print(' ')
	print(arg0) #tramite ID	
	print(str(arg1)) #TIPO DE DOCUMENTO

	getFile(arg0,str(int(process_day_Nbr())+1))
		
	#CONSULTA SI HAY RELACION DE EXPEDIENTE__________________________________________________________________________________________ 
	if exp_relation(arg1)[0] == 'S': 
		#print('CON EXPEDIENTE RELACIONADO')# CONFIRMA RELACION
		if pendiente_sfe(arg0)[0]['expediente_afectad'] != 'None': 
			#print('relacion expediente Ok!') # insert
			valid_rules.append('Ok')
		else:
			#print('falta expediente relacionado') # estado 99
			valid_rules.append('Error')
			cambio_estado_soporte(arg0)
	else:
		#print('SIN EXPEDIENTE RELACIONADO')# CONFIRMA SIN RELACION
		valid_rules.append('Not')
	#FIN_____________________________________________________________________________________________________________________________ 

	#CONSULTA SI HAY RELACION DE ESCRITO______________________________________________________________________________________________	
	if esc_relation(arg1)[0] == 'S':
		#print('CON ESCRITO RELACIONADO')
		if pendiente_sfe(arg0)[0]['expediente_afectad'] != 'None': 
			#print('relacion de escrito Ok!') # insert
			valid_rules.append('Ok')
		else:
			#print('falta escrito relacionado') # estado 99
			valid_rules.append('Error')
			cambio_estado_soporte(arg0)
	else:
		#print('SIN ESCRITO RELACIONADO')
		valid_rules.append('Not')
	#FIN_____________________________________________________________________________________________________________________________

	#CONSULTA SI EL TIPO ES CON PAGO_____________________________________________________________________________________________________
	if pago == 'S':
			#print('CON PAGO')
			if pago_auth != 'sin dato en bancar': # CONFIRMA EL PAGO EN BANCAR
				#print('Con pago Ok!') # INSERT
				valid_rules.append('Ok')
			else:
				#print(pago_auth) # ESTADO 99
				valid_rules.append('Error')
				cambio_estado_soporte(arg0)
	else:
		#print('SIN PAGO') # INSERT
		valid_rules.append('Not')
	#FIN_____________________________________________________________________________________________________________________________	

	####################################################################################################################################
	####################################################################################################################################
	####################################################################################################################################
	####################################################################################################################################
	####################################################################################################################################

	if valid_rules == ['Ok', 'Not', 'Not']: #con exp - sin esc - sin pago
		#print('ESCRITO CON RELACION')		
		compileAndInsert(arg0,arg1)
		time.sleep(1)
	elif valid_rules == ['Ok', 'Not', 'Ok']: #con exp - sin esc - con pago
		#print('ESCRITO CON RELACION')		
		compileAndInsert(arg0,arg1)
		time.sleep(1)	
	elif valid_rules == ['Not', 'Ok', 'Not']:#sin exp - con esc - sin pago
		#print('ESCRTO A ESCRITO')
		compileAndInsertUserDocUserDoc(arg0,arg1)
		time.sleep(1)
	elif valid_rules == ['Not', 'Ok', 'Ok']:#sin exp - con esc - sin pago
		#print('ESCRTO A ESCRITO')
		compileAndInsertUserDocUserDocPago(arg0,arg1)
		time.sleep(1)
	elif valid_rules == ['Not', 'Not', 'Ok']:#sin exp - sin esc - con pago
		#print('ESCRITO SIN RELACION')		
		compileAndInsert(arg0,arg1)
		time.sleep(1)
	elif valid_rules == ['Not', 'Not', 'Not']:#sin exp - sin esc - sin pago
		#print('ESCRITO SIN RELACION')		
		compileAndInsert(arg0,arg1)
		time.sleep(1)
	else:
		pass		

	#print(valid_rules)

		
#Insert Escritos	
def compileAndInsert(form_Id,typ):

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
			print(str(e))
			cambio_estado_soporte(form_Id)
		
		try:
			exists = str(user_doc_read_min('E',insert_doc.documentId_docNbr,insert_doc.documentId_docOrigin,insert_doc.documentId_docSeries)['documentId']['docNbr']['doubleValue']).replace(".0","") 
			if exists == insert_doc.documentId_docNbr:
				cambio_estado(form_Id,insert_doc.documentId_docNbr)
		except Exception as e:
			cambio_estado_soporte(form_Id)			

#Insert Escrito a Escrito
def compileAndInsertUserDocUserDoc(form_Id,typ):	
		
		escrito_relacionado = userDocModel()
		escrito_relacionado.setData(form_Id)

		try:
			user_doc_receive(
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
						escrito_relacionado.filingData_userdocTypeList_userdocType)
			process_day_commit_Nbr()
		except zeep.exceptions.Fault as e:
			print(str(e))
			cambio_estado_soporte(form_Id)

		time.sleep(1)
	
		sigla_desc = str(escrito_relacionado.filingData_userdocTypeList_userdocName).split("- ")

		try:
			user_doc_update(
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
						escrito_relacionado.representationData_representativeList_person_email)
		except zeep.exceptions.Fault as e:
			print(str(e))
			cambio_estado_soporte(form_Id)

		time.sleep(1)
		
		afferc = user_doc_read_min(escrito_relacionado.affected_doc_Log,escrito_relacionado.affected_doc_docNbr,escrito_relacionado.affected_doc_docOrigin,escrito_relacionado.affected_doc_docSeries)
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

		time.sleep(1)
		
		afferc = str(user_doc_read_min('E',escrito_relacionado.documentId_docNbr,escrito_relacionado.documentId_docOrigin,escrito_relacionado.documentId_docSeries)['documentId']['docNbr']['doubleValue']).replace(".0","") 
		if afferc == escrito_relacionado.documentId_docNbr:
			cambio_estado(form_Id,escrito_relacionado.documentId_docNbr)

		time.sleep(0.5)
		
def compileAndInsertUserDocUserDocPago(form_Id,typ):	
		
		escrito_escrito_pago = userDocModel()
		escrito_escrito_pago.setData(form_Id)
	
		try:
			user_doc_receive(
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
						escrito_escrito_pago.filingData_userdocTypeList_userdocType)
			process_day_commit_Nbr()
		except zeep.exceptions.Fault as e:
			print(str(e))
			cambio_estado_soporte(form_Id)

		time.sleep(1)
		
		sigla_desc = str(escrito_escrito_pago.filingData_userdocTypeList_userdocName).split("- ")
						
		try:
			user_doc_update(
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
						escrito_escrito_pago.representationData_representativeList_person_email)
		except zeep.exceptions.Fault as e:
			print(str(e))
			cambio_estado_soporte(form_Id)		
		
		time.sleep(1)
		
		afferc = user_doc_read_min('E',escrito_escrito_pago.affected_doc_docNbr,escrito_escrito_pago.affected_doc_docOrigin,escrito_escrito_pago.affected_doc_docSeries)
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
		
		time.sleep(1)
		
		afferc = str(user_doc_read_min('E',escrito_escrito_pago.documentId_docNbr,escrito_escrito_pago.documentId_docOrigin,escrito_escrito_pago.documentId_docSeries)['documentId']['docNbr']['doubleValue']).replace(".0","") 
		if afferc == escrito_escrito_pago.documentId_docNbr:
			cambio_estado(form_Id,escrito_escrito_pago.documentId_docNbr)



#if __name__ == "__main__":
listar()


