"""
Administrador de recepcion MEA
"""
from dataclasses import replace
import numbers
import string
import time
from time import sleep
from unicodedata import numeric
from dinapi.sfe import cambio_estado, cambio_estado_soporte, count_pendiente, esc_relation, exp_relation, format_userdoc, pago_id, paymentYeasOrNot, pendiente_sfe, pendientes_sfe, process_day_Nbr
import tools.connect as connex
from wipo.function_for_reception_in import insert_user_doc_escritos, user_doc_getList_escrito
from wipo.ipas import mark_getlist


list_id = []
def listar():
	#print('crear lista')
	captura_pendientes() # Captura lista pendiente
	time.sleep(int(connex.MEA_TIEMPO_ACTUALIZACION))

def captura_pendientes():
	list_id = []
	today = time.strftime("%Y-%m-%d")
	for i in pendientes_sfe(today,100,0):
		try:
			if i['estado'] == 7:
				list_id.append(str(i['Id'])+"/"+str(i['tool_tip']))
		except Exception as e:
			pass
	print(list_id)
	if list_id != []:
		for i in list_id:
			params = str(i).split('/')
			#print('doc pendiente '+str(params[0]))
			insert_list(str(params[0]),str(params[1]))
			time.sleep(2)
	listar()
		
def insert_list(arg0:string,arg1:string):
	try:
		pago = str(paymentYeasOrNot(arg1)[0]).replace("None","N")
		pago_auth:str = str(pago_id(arg0)).replace("None","sin dato en bancar")
		valid_rules:str = []
		print(' ')	
		print(str(arg1)) #TIPO DE DOCUMENTO
		time.sleep(1)
		#CONSULTA SI HAY RELACION DE EXPEDIENTE__________________________________________________________________________________________ 
		if exp_relation(arg1)[0] == 'S': 
			print('CON EXPEDIENTE RELACIONADO')# CONFIRMA RELACION
			if pendiente_sfe(arg0)[0]['expediente_afectad'] != 'None': 
				print('relacion expediente Ok!') # insert
				valid_rules.append('Ok')
			else:
				print('falta expediente relacionado') # estado 99
				valid_rules.append('Not')
				cambio_estado_soporte(arg0)
		else:
			print('SIN EXPEDIENTE RELACIONADO')# CONFIRMA SIN RELACION
			valid_rules.append('Ok')
		#FIN_____________________________________________________________________________________________________________________________ 

		time.sleep(1)
		#CONSULTA SI HAY RELACION DE ESCRITO______________________________________________________________________________________________	
		if esc_relation(arg1)[0] == 'S':
			print('CON ESCRITO RELACIONADO')
			if pendiente_sfe(arg0)[0]['expediente_afectad'] != 'None': 
				print('relacion de escrito Ok!') # insert
				valid_rules.append('Ok')
			else:
				print('falta escrito relacionado') # estado 99
				valid_rules.append('Not')
				cambio_estado_soporte(arg0)			
		else:
			print('SIN ESCRITO RELACIONADO')
			valid_rules.append('Ok')
		#FIN_____________________________________________________________________________________________________________________________


		time.sleep(1)
		#CONSULTA SI EL TIPO ES CON PAGO_____________________________________________________________________________________________________
		if pago == 'S':
			print('CON PAGO')
			if pago_auth != 'sin dato en bancar': # CONFIRMA EL PAGO EN BANCAR
				print('Con pago Ok!') # INSERT
				valid_rules.append('Ok')
			else:
				print(pago_auth) # ESTADO 99
				valid_rules.append('Not')
				cambio_estado_soporte(arg0)
		else:
			print('SIN PAGO') # INSERT
			valid_rules.append('Ok')
		#FIN_____________________________________________________________________________________________________________________________	

		if valid_rules == ['Ok', 'Ok', 'Ok']:
			print('INSERTAR Y ACTUALIZAR')
			print(compileAndInsert(arg0))
			esc = str(user_doc_getList_escrito(process_day_Nbr())['documentId']['docNbr']['doubleValue']).replace(".0","")
			if int(esc) == process_day_Nbr():
				cambio_estado_soporte(arg0)
			else:
				pass
		else:
			print('NO INSERTAR NI ACTUALIZAR')
			
		#print(valid_rules)

	except Exception as e:
		pass			
	
def compileAndInsert(form_Id):
   item = format_userdoc(form_Id)
   return insert_user_doc_escritos(
					 item['affectedFileIdList_fileNbr'],
					 item['affectedFileIdList_fileSeq'],
					 item['affectedFileIdList_fileSeries'],
					 item['affectedFileIdList_fileType'],
					 item['affectedFileSummaryList_disclaimer'],
					 item['affectedFileSummaryList_disclaimerInOtherLang'],
					 item['affectedFileSummaryList_fileNbr'],
					 item['affectedFileSummaryList_fileSeq'],
					 item['affectedFileSummaryList_fileSeries'],
					 item['affectedFileSummaryList_fileType'],
					 item['affectedFileSummaryList_fileIdAsString'],
					 item['affectedFileSummaryList_fileSummaryClasses'],
					 item['affectedFileSummaryList_fileSummaryCountry'],
					 item['affectedFileSummaryList_fileSummaryDescription'],
					 item['affectedFileSummaryList_fileSummaryDescriptionInOtherLang'],
					 item['affectedFileSummaryList_fileSummaryOwner'],
					 item['affectedFileSummaryList_fileSummaryOwnerInOtherLang'],
					 item['affectedFileSummaryList_fileSummaryRepresentative'],
					 item['affectedFileSummaryList_fileSummaryRepresentativeInOtherLang'],
					 item['affectedFileSummaryList_fileSummaryResponsibleName'],
					 item['affectedFileSummaryList_fileSummaryStatus'],
					 item['applicant_applicantNotes'],
					 item['applicant_person_addressStreet'],
					 item['applicant_person_addressStreetInOtherLang'],
					 item['applicant_person_addressZone'],
					 item['applicant_person_agentCode'],
					 item['applicant_person_cityCode'],
					 item['applicant_person_cityName'],
					 item['applicant_person_companyRegisterRegistrationDate'],
					 item['applicant_person_companyRegisterRegistrationNbr'],
					 item['applicant_person_email'],
					 item['applicant_person_individualIdNbr'],
					 item['applicant_person_individualIdType'],
					 item['applicant_person_legalIdNbr'],
					 item['applicant_person_legalIdType'],
					 item['applicant_person_legalNature'],
					 item['applicant_person_legalNatureInOtherLang'],
					 item['applicant_person_nationalityCountryCode'],
					 item['applicant_person_personGroupCode'],
					 item['applicant_person_personGroupName'],
					 item['applicant_person_personName'],
					 item['applicant_person_personNameInOtherLang'],
					 item['applicant_person_residenceCountryCode'],
					 item['applicant_person_stateCode'],
					 item['applicant_person_stateName'],
					 item['applicant_person_telephone'],
					 item['applicant_person_zipCode'],
					 item['documentId_docLog'],
					 item['documentId_docNbr'],
					 item['documentId_docOrigin'],
					 item['documentId_docSeries'],
					 item['documentId_selected'],
					 item['documentSeqId_docSeqName'],
					 item['documentSeqId_docSeqNbr'],
					 item['documentSeqId_docSeqSeries'],
					 item['documentSeqId_docSeqType'],
					 item['filingData_applicationSubtype'],
					 item['filingData_applicationType'],
					 item['filingData_captureDate'],
					 item['filingData_captureUserId'],
					 item['filingData_filingDate'],
					 item['filingData_lawCode'],
					 item['filingData_novelty1Date'],
					 item['filingData_novelty2Date'],
					 item['filingData_paymentList_currencyName'],
					 item['filingData_paymentList_currencyType'],
					 item['filingData_paymentList_receiptAmount'],
					 item['filingData_paymentList_receiptDate'],
					 item['filingData_paymentList_receiptNbr'],
					 item['filingData_paymentList_receiptNotes'],
					 item['filingData_paymentList_receiptType'],
					 item['filingData_paymentList_receiptTypeName'],
					 item['filingData_receptionDate'],
					 item['filingData_documentId_receptionDocument_docLog'],
					 item['filingData_documentId_receptionDocument_docNbr'],
					 item['filingData_documentId_receptionDocument_docOrigin'],
					 item['filingData_documentId_receptionDocument_docSeries'],
					 item['filingData_documentId_receptionDocument_selected'],
					 item['filingData_userdocTypeList_userdocName'],
					 item['filingData_userdocTypeList_userdocType'],
					 item['newOwnershipData_ownerList_orderNbr'],
					 item['newOwnershipData_ownerList_ownershipNotes'],
					 item['newOwnershipData_ownerList_person_addressStreet'],
					 item['newOwnershipData_ownerList_person_addressStreetInOtherLang'],
					 item['newOwnershipData_ownerList_person_addressZone'],
					 item['newOwnershipData_ownerList_person_agentCode'],
					 item['newOwnershipData_ownerList_person_cityCode'],
					 item['newOwnershipData_ownerList_person_cityName'],
					 item['newOwnershipData_ownerList_person_companyRegisterRegistrationDate'],
					 item['newOwnershipData_ownerList_person_companyRegisterRegistrationNbr'],
					 item['newOwnershipData_ownerList_person_email'],
					 item['newOwnershipData_ownerList_person_individualIdNbr'],
					 item['newOwnershipData_ownerList_person_individualIdType'],
					 item['newOwnershipData_ownerList_person_legalIdNbr'],
					 item['newOwnershipData_ownerList_person_legalIdType'],
					 item['newOwnershipData_ownerList_person_legalNature'],
					 item['newOwnershipData_ownerList_person_legalNatureInOtherLang'],
					 item['newOwnershipData_ownerList_person_nationalityCountryCode'],
					 item['newOwnershipData_ownerList_person_personGroupCode'],
					 item['newOwnershipData_ownerList_person_personGroupName'],
					 item['newOwnershipData_ownerList_person_personName'],
					 item['newOwnershipData_ownerList_person_personNameInOtherLang'],
					 item['newOwnershipData_ownerList_person_residenceCountryCode'],
					 item['newOwnershipData_ownerList_person_stateCode'],
					 item['newOwnershipData_ownerList_person_stateName'],
					 item['newOwnershipData_ownerList_person_telephone'],
					 item['newOwnershipData_ownerList_person_zipCode'],
					 item['notes'],
					 item['poaData_poaGranteeList_person_addressStreet'],
					 item['poaData_poaGranteeList_person_addressStreetInOtherLang'],
					 item['poaData_poaGranteeList_person_addressZone'],
					 item['poaData_poaGranteeList_person_agentCode'],
					 item['poaData_poaGranteeList_person_cityCode'],
					 item['poaData_poaGranteeList_person_cityName'],
					 item['poaData_poaGranteeList_person_companyRegisterRegistrationDate'],
					 item['poaData_poaGranteeList_person_companyRegisterRegistrationNbr'],
					 item['poaData_poaGranteeList_person_email'],
					 item['poaData_poaGranteeList_person_individualIdNbr'],
					 item['poaData_poaGranteeList_person_individualIdType'],
					 item['poaData_poaGranteeList_person_legalIdNbr'],
					 item['poaData_poaGranteeList_person_legalIdType'],
					 item['poaData_poaGranteeList_person_legalNature'],
					 item['poaData_poaGranteeList_person_legalNatureInOtherLang'],
					 item['poaData_poaGranteeList_person_nationalityCountryCode'],
					 item['poaData_poaGranteeList_person_personGroupCode'],
					 item['poaData_poaGranteeList_person_personGroupName'],
					 item['poaData_poaGranteeList_person_personName'],
					 item['poaData_poaGranteeList_person_personNameInOtherLang'],
					 item['poaData_poaGranteeList_person_residenceCountryCode'],
					 item['poaData_poaGranteeList_person_stateCode'],
					 item['poaData_poaGranteeList_person_stateName'],
					 item['poaData_poaGranteeList_person_telephone'],
					 item['poaData_poaGranteeList_person_zipCode'],
					 item['poaData_poaGrantor_person_addressStreet'],
					 item['poaData_poaGrantor_person_addressStreetInOtherLang'],
					 item['poaData_poaGrantor_person_addressZone'],
					 item['poaData_poaGrantor_person_agentCode'],
					 item['poaData_poaGrantor_person_cityCode'],
					 item['poaData_poaGrantor_person_cityName'],
					 item['poaData_poaGrantor_person_companyRegisterRegistrationDate'],
					 item['poaData_poaGrantor_person_companyRegisterRegistrationNbr'],
					 item['poaData_poaGrantor_person_email'],
					 item['poaData_poaGrantor_person_individualIdNbr'],
					 item['poaData_poaGrantor_person_individualIdType'],
					 item['poaData_poaGrantor_person_legalIdNbr'],
					 item['poaData_poaGrantor_person_legalIdType'],
					 item['poaData_poaGrantor_person_legalNature'],
					 item['poaData_poaGrantor_person_legalNatureInOtherLang'],
					 item['poaData_poaGrantor_person_nationalityCountryCode'],
					 item['poaData_poaGrantor_person_personGroupCode'],
					 item['poaData_poaGrantor_person_personGroupName'],
					 item['poaData_poaGrantor_person_personName'],
					 item['poaData_poaGrantor_person_personNameInOtherLang'],
					 item['poaData_poaGrantor_person_residenceCountryCode'],
					 item['poaData_poaGrantor_person_stateCode'],
					 item['poaData_poaGrantor_person_stateName'],
					 item['poaData_poaGrantor_person_telephone'],
					 item['poaData_poaGrantor_person_zipCode'],
					 item['poaData_poaRegNumber'],
					 item['poaData_scope'],
					 item['representationData_representativeList_person_addressStreet'],
					 item['representationData_representativeList_person_addressStreetInOtherLang'],
					 item['representationData_representativeList_person_addressZone'],
					 item['representationData_representativeList_person_agentCode'],
					 item['representationData_representativeList_person_cityCode'],
					 item['representationData_representativeList_person_cityName'],
					 item['representationData_representativeList_person_companyRegisterRegistrationDate'],
					 item['representationData_representativeList_person_companyRegisterRegistrationNbr'],
					 item['representationData_representativeList_person_email'],
					 item['representationData_representativeList_person_individualIdNbr'],
					 item['representationData_representativeList_person_individualIdType'],
					 item['representationData_representativeList_person_legalIdNbr'],
					 item['representationData_representativeList_person_legalIdType'],
					 item['representationData_representativeList_person_legalNature'],
					 item['representationData_representativeList_person_legalNatureInOtherLang'],
					 item['representationData_representativeList_person_nationalityCountryCode'],
					 item['representationData_representativeList_person_personGroupCode'],
					 item['representationData_representativeList_person_personGroupName'],
					 item['representationData_representativeList_person_personName'],
					 item['representationData_representativeList_person_personNameInOtherLang'],
					 item['representationData_representativeList_person_residenceCountryCode'],
					 item['representationData_representativeList_person_stateCode'],
					 item['representationData_representativeList_person_stateName'],
					 item['representationData_representativeList_person_telephone'],
					 item['representationData_representativeList_person_zipCode'],
					 item['representationData_representativeList_representativeType'])

listar()




#Quitar de la lista despues
#list_id.remove(arg0+"/"+arg1)
#print(compileAndInsert('1496','70'))