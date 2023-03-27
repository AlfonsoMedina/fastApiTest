"""
Administrador de recepcion MEA
"""
import string
import time
from time import sleep
from dinapi.sfe import cambio_estado, count_pendiente, format_userdoc, paymentYeasOrNot, pendiente_sfe, pendientes_sfe
import tools.connect as connex
from wipo.function_for_reception_in import insert_user_doc_escritos


"""
def timer(step):
	print('M.E.A Online............')
	i = 0
	while i < step:
		for i in range(step):
			check_date()
			#print('.')
			if(i == 10):
				i=0
		sleep(int(connex.MEA_TIEMPO_ACTUALIZACION))		

def check_date(): # Captura lista pendiente
	today = time.strftime("%Y-%m-%d")
	for i in pendientes_sfe(today,0):
		try:
			if i['estado'] == 7:
				list_id.append(str(i['Id'])+"-"+str(i['tip_doc']))
		except Exception as e:
			pass
	if list_id != []:
		for n in list_id:
			params = str(n).split('-')
			insert_list(params[0],params[1])


"""

list_id = []
def listar():
	print('crear lista')
	check_date() # Captura lista pendiente
	time.sleep(int(connex.MEA_TIEMPO_ACTUALIZACION))
	insertar()

def insertar():
	time.sleep(int(connex.MEA_TIEMPO_ACTUALIZACION)/2)
	print('ordenar lista')
	time.sleep(1)
	list_id.sort()
	#print(list_id)
	if list_id != []:
		for i in list_id:
			params = str(i).split('-')
			print('insertar docs '+str(params[0]))
			insert_list(str(params[0]),str(params[1]))
		time.sleep(2)
	listar()

def check_date(): # Captura lista pendiente
	today = time.strftime("%Y-%m-%d")
	for i in pendientes_sfe(today,100,0):
		try:
			if i['estado'] == 7:
				list_id.append(str(i['Id'])+"-"+str(i['tool_tip']))
			print(list_id)
		except Exception as e:
			pass

def insert_list(arg0:string,arg1:string): # Insercion segun tipo de formulario
	if arg1 == "68":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		
		cambio_estado(arg0)

	if arg1 == "70":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)

		cambio_estado(arg0)

	if arg1 == "69":
		print(arg0 + " Procesado...") 
		list_id.remove(arg0+"-"+arg1)

		cambio_estado(arg0)

	if arg1 == "36":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)

		cambio_estado(arg0)

	if arg1 == "39":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

	if arg1 == "42":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

	if arg1 == "95":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

	if arg1 == "3":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

	if arg1 == "4":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

	if arg1 == "27":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

#listar()


print(paymentYeasOrNot('DTM - Duplicado de Títulos Marcas'))



def compileAndInsert(form_Id,typ):
	item = format_userdoc(form_Id,typ)
	return insert_user_doc_escritos(item['affectedFileIdList_fileNbr'],
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


#print(compileAndInsert('1496','70'))