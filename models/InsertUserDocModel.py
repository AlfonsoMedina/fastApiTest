
from asyncio.windows_events import NULL
from dinapi.sfe import pendiente_sfe,code_ag, pago_data, process_day_Nbr
from getFileDoc import getFile
from wipo.function_for_reception_in import user_doc_getList_escrito
from wipo.ipas import mark_getlist, personAgente
import tools.connect as connex
import tools.filing_date as captureDate
import tools.connect as connex


default_val = lambda arg: arg if arg == "null" else "" 
default_val_e99 = lambda arg: arg if arg != "" else ""

class userDocModel(object):
	affectedFileIdList_fileNbr:str = ""
	affectedFileIdList_fileSeq:str = ""
	affectedFileIdList_fileSeries:str = ""
	affectedFileIdList_fileType:str = ""
	affected_doc_Log:str = ""
	affected_doc_docNbr:str = ""
	affected_doc_docOrigin:str = ""
	affected_doc_docSeries:str = ""
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
	def __init__(self):
		pass
	
	def exist_split(self,arg0,arg1):
		data = pendiente_sfe(arg0)
		list_splits = {}
		for i in range(0,len(data[0]['respuestas'])):
			list_splits['campo'+str(i)] = data[0]['respuestas'][i]['campo']
		exists = arg1 in list_splits.values()	
		return(exists)


	#Adjunto requerido 
	
	#actualizacion de front durante proceso

	def setData(self,doc_Id):
		ruc_Typ:str = ''
		ci_Typ:str = ''	
		ruc_Nbr:str = "E99"
		ci_Nbr:str = "E99"
		data = pendiente_sfe(doc_Id)
		
		try:
			ag_data = personAgente(code_ag(data[0]['usuario_id']))[0]
		except Exception as e:
			print("")

		try:
			if self.exist_split(doc_Id,'datospersonales_tipo') == True:  		
				for i in range(0,len(data[0]['respuestas'])):
					if data[0]['respuestas'][i]['campo'] == 'datospersonales_tipo':	
						if str(data[0]['respuestas'][i]['valor']) == 'Persona Jurídica':
							ruc_Typ = 'RUC'
						
						if str(data[0]['respuestas'][i]['valor']) == 'Persona Física':
							ci_Typ = 'CED'
		except Exception as e:
				pass
		
		
		if ruc_Typ == 'RUC': 
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_documento':
					ruc_Nbr = str(data[0]['respuestas'][i]['valor'])
					ci_Nbr = ""				
		elif ci_Typ == 'CED': 
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_documento':	
					ci_Nbr = str(data[0]['respuestas'][i]['valor'])
					ruc_Nbr = ""				
		else:
			pass
						

		try:
			if str(data[0]['expediente_afectad']) != "None":
				if user_doc_getList_escrito(data[0]['expediente_afectad']) != []:
					self.affected_doc_Log = "E"
					self.affected_doc_docNbr = str(user_doc_getList_escrito(data[0]['expediente_afectad'])['documentId']['docNbr']['doubleValue'])
					self.affected_doc_docOrigin = str(user_doc_getList_escrito(data[0]['expediente_afectad'])['documentId']['docOrigin'])
					self.affected_doc_docSeries = str(user_doc_getList_escrito(data[0]['expediente_afectad'])['documentId']['docSeries']['doubleValue'])
				else:
					self.affected_doc_Log = ""
					self.affected_doc_docNbr = ""
					self.affected_doc_docOrigin = ""
					self.affected_doc_docSeries = ""					
			else:
				self.affected_doc_Log = ""
				self.affected_doc_docNbr = ""
				self.affected_doc_docOrigin = ""
				self.affected_doc_docSeries = ""
		except Exception as e:
			self.affected_doc_Log = ""
			self.affected_doc_docNbr = ""
			self.affected_doc_docOrigin = ""
			self.affected_doc_docSeries = ""

		try:
			if str(data[0]['expediente_afectad']) != "None":
				if mark_getlist(data[0]['expediente_afectad']) != []:
					self.affectedFileIdList_fileNbr:str = mark_getlist(data[0]['expediente_afectad'])[0]['fileId']['fileNbr']['doubleValue']
					self.affectedFileIdList_fileSeq:str = mark_getlist(data[0]['expediente_afectad'])[0]['fileId']['fileSeq']
					self.affectedFileIdList_fileSeries:str = mark_getlist(data[0]['expediente_afectad'])[0]['fileId']['fileSeries']['doubleValue']
					self.affectedFileIdList_fileType:str = mark_getlist(data[0]['expediente_afectad'])[0]['fileId']['fileType']
				else:
					self.affectedFileIdList_fileNbr:str = ""
					self.affectedFileIdList_fileSeq:str = ""
					self.affectedFileIdList_fileSeries:str = ""
					self.affectedFileIdList_fileType:str = ""
			else:
				self.affectedFileIdList_fileNbr:str = ""
				self.affectedFileIdList_fileSeq:str = ""
				self.affectedFileIdList_fileSeries:str = ""
				self.affectedFileIdList_fileType:str = ""
		except Exception as e:
			self.affectedFileIdList_fileNbr:str = ""
			self.affectedFileIdList_fileSeq:str = ""
			self.affectedFileIdList_fileSeries:str = ""
			self.affectedFileIdList_fileType:str = ""


		self.affectedFileSummaryList_disclaimer= ""
		self.affectedFileSummaryList_disclaimerInOtherLang= ""
		self.affectedFileSummaryList_fileNbr= ""
		self.affectedFileSummaryList_fileSeq= ""
		self.affectedFileSummaryList_fileSeries= ""
		self.affectedFileSummaryList_fileType= ""
		self.affectedFileSummaryList_fileIdAsString= ""
		self.affectedFileSummaryList_fileSummaryClasses= ""
		self.affectedFileSummaryList_fileSummaryCountry= ""
		self.affectedFileSummaryList_fileSummaryDescription= ""
		self.affectedFileSummaryList_fileSummaryDescriptionInOtherLang= ""
		self.affectedFileSummaryList_fileSummaryOwner= ""
		self.affectedFileSummaryList_fileSummaryOwnerInOtherLang= ""
		self.affectedFileSummaryList_fileSummaryRepresentative= ""
		self.affectedFileSummaryList_fileSummaryRepresentativeInOtherLang= ""
		self.affectedFileSummaryList_fileSummaryResponsibleName= ""
		self.affectedFileSummaryList_fileSummaryStatus= ""
		self.applicant_applicantNotes = "Aplicante SPRINT M.E.A."
		
		######( expedienteoescrito_denominacion )####### verificar nombre razon social

		if self.exist_split(doc_Id,'datospersonales_direccion') == True:   		
			try:
				for i in range(0,len(data[0]['respuestas'])):
					if data[0]['respuestas'][i]['campo'] == 'datospersonales_direccion':				
						self.applicant_person_addressStreet = str(data[0]['respuestas'][i]['valor'])
			except Exception as e:
				self.applicant_person_addressStreet= ""
		else:
			self.applicant_person_addressStreet= "E99"

		
		self.applicant_person_addressStreetInOtherLang= ""
		self.applicant_person_addressZone= ""
		self.applicant_person_agentCode= ""
		self.applicant_person_cityCode= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_ciudad':			
					self.applicant_person_cityName = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.applicant_person_cityName = ""
		
		self.applicant_person_companyRegisterRegistrationDate= ""
		self.applicant_person_companyRegisterRegistrationNbr= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_correoelectronico':			
					self.applicant_person_email = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.applicant_person_email= ""
		
		self.applicant_person_individualIdNbr = ci_Nbr
		
		self.applicant_person_individualIdType = ci_Typ
		
		self.applicant_person_legalIdNbr = ruc_Nbr
		self.applicant_person_legalIdType = ruc_Typ		
		
		self.applicant_person_legalNature= ""
		self.applicant_person_legalNatureInOtherLang= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_pais':
					self.applicant_person_nationalityCountryCode = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.applicant_person_nationalityCountryCode= ""
		
		self.applicant_person_personGroupCode= ""
		self.applicant_person_personGroupName= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_nombresrazon':
					self.applicant_person_personName = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.applicant_person_personName= ""
		
		self.applicant_person_personNameInOtherLang= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_pais':
					self.applicant_person_residenceCountryCode = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.applicant_person_residenceCountryCode= "" 
		
		self.applicant_person_stateCode= ""
		self.applicant_person_stateName= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_telefono':
					self.applicant_person_telephone = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.applicant_person_telephone= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_codigopostal':
					self.applicant_person_zipCode = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.applicant_person_zipCode= ""
				
		try:
			self.documentId_docLog = "E"
		except Exception as e:
			self.documentId_docLog= ""
		
		try:
			self.documentId_docNbr = str(int(process_day_Nbr())+1)
		except Exception as e:
			self.documentId_docNbr= ""	
		
		try:
			self.documentId_docOrigin = str(connex.MEA_SFE_FORMULARIOS_ID_Origin)
		except Exception as e:
			self.documentId_docOrigin= ""	
		
		try:
			self.documentId_docSeries = captureDate.capture_year()
		except Exception as e:
			self.documentId_docSeries= ""	
		
		try:
			self.documentId_selected= ""
		except Exception as e:
			self.documentId_selected= ""	
		
		try:	
			self.documentSeqId_docSeqName = "Documentos"
		except Exception as e:
			self.documentSeqId_docSeqName= ""	
		
		try:	
			self.documentSeqId_docSeqNbr = str(int(process_day_Nbr())+1)
		except Exception as e:
			self.documentSeqId_docSeqNbr= ""	
		
		try:	
			self.documentSeqId_docSeqSeries = captureDate.capture_year()
		except Exception as e:
			self.documentSeqId_docSeqSeries= ""	
		
		try:
			self.documentSeqId_docSeqType = "PY"
		except Exception as e:
			self.documentSeqId_docSeqType= ""	
		
		
		self.filingData_applicationSubtype= ""
		self.filingData_applicationType= ""
		self.filingData_captureDate = captureDate.capture_full()
		self.filingData_captureUserId = connex.MEA_PERIODO_RECEPCION_userId
		self.filingData_filingDate = captureDate.capture_full()
		self.filingData_lawCode= ""
		self.filingData_novelty1Date= ""
		self.filingData_novelty2Date= ""
		self.filingData_paymentList_currencyName = "Guaraníes"
		self.filingData_paymentList_currencyType = "GS"
		
		try:
			self.filingData_paymentList_receiptAmount = str(pago_data(doc_Id)[1])
		except Exception as e:
			self.filingData_paymentList_receiptAmount= ""
		
		try:	
			self.filingData_paymentList_receiptDate = str(pago_data(doc_Id)[2])[0:10]
		except Exception as e:
			self.filingData_paymentList_receiptDate= ""		
		
		try:
			self.filingData_paymentList_receiptNbr = str(pago_data(doc_Id)[0])
		except Exception as e:
			self.filingData_paymentList_receiptNbr= ""		
		
		self.filingData_paymentList_receiptNotes = " Caja MEA"
		self.filingData_paymentList_receiptType = str(data[0]['tasa_id'])
		self.filingData_paymentList_receiptTypeName = str(data[0]['tasa_desc'])
		self.filingData_receptionDate = captureDate.capture_full()
		self.filingData_documentId_receptionDocument_docLog = "E"
		self.filingData_documentId_receptionDocument_docNbr = str(int(process_day_Nbr())+1)
		self.filingData_documentId_receptionDocument_docOrigin = str(connex.MEA_SFE_FORMULARIOS_ID_Origin)
		self.filingData_documentId_receptionDocument_docSeries = captureDate.capture_year()
		self.filingData_documentId_receptionDocument_selected= ""
		self.filingData_userdocTypeList_userdocName = str(data[0]['tool_tip'])
		self.filingData_userdocTypeList_userdocType = str(data[0]['tipo_documento_id'])
		
		
		self.newOwnershipData_ownerList_orderNbr= ""
		self.newOwnershipData_ownerList_ownershipNotes= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_direccion':	
					self.newOwnershipData_ownerList_person_addressStreet = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.newOwnershipData_ownerList_person_addressStreet= ""
		
		self.newOwnershipData_ownerList_person_addressStreetInOtherLang= ""
		self.newOwnershipData_ownerList_person_addressZone= ""
		self.newOwnershipData_ownerList_person_agentCode= ""
		self.newOwnershipData_ownerList_person_cityCode= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_ciudad':			
					self.newOwnershipData_ownerList_person_cityName = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.newOwnershipData_ownerList_person_cityName = ""
		
		self.newOwnershipData_ownerList_person_companyRegisterRegistrationDate= ""
		self.newOwnershipData_ownerList_person_companyRegisterRegistrationNbr= ""
		self.newOwnershipData_ownerList_person_email= ""
		self.newOwnershipData_ownerList_person_individualIdNbr = ci_Nbr
		self.newOwnershipData_ownerList_person_individualIdType = ci_Typ
		self.newOwnershipData_ownerList_person_legalIdNbr = ruc_Nbr
		self.newOwnershipData_ownerList_person_legalIdType = ruc_Typ
		self.newOwnershipData_ownerList_person_legalNature = ""
		self.newOwnershipData_ownerList_person_legalNatureInOtherLang = ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_pais':
					self.newOwnershipData_ownerList_person_nationalityCountryCode = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.newOwnershipData_ownerList_person_nationalityCountryCode= "" 
		
		self.newOwnershipData_ownerList_person_personGroupCode= ""
		self.newOwnershipData_ownerList_person_personGroupName= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_nombresrazon':
					self.newOwnershipData_ownerList_person_personName = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.newOwnershipData_ownerList_person_personName= ""
		
		self.newOwnershipData_ownerList_person_personNameInOtherLang= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_pais':
					self.newOwnershipData_ownerList_person_residenceCountryCode = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.newOwnershipData_ownerList_person_residenceCountryCode= ""
		
		self.newOwnershipData_ownerList_person_stateCode= ""
		self.newOwnershipData_ownerList_person_stateName= ""
		
		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_telefono':
					self.newOwnershipData_ownerList_person_telephone = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			self.newOwnershipData_ownerList_person_telephone= ""	
		
		self.newOwnershipData_ownerList_person_zipCode= ""
		self.notes= ""
		self.poaData_poaGranteeList_person_addressStreet= ""
		self.poaData_poaGranteeList_person_addressStreetInOtherLang= ""
		self.poaData_poaGranteeList_person_addressZone= ""
		self.poaData_poaGranteeList_person_agentCode= ""
		self.poaData_poaGranteeList_person_cityCode= ""
		self.poaData_poaGranteeList_person_cityName= ""
		self.poaData_poaGranteeList_person_companyRegisterRegistrationDate= ""
		self.poaData_poaGranteeList_person_companyRegisterRegistrationNbr= ""
		self.poaData_poaGranteeList_person_email= ""
		self.poaData_poaGranteeList_person_individualIdNbr= ""
		self.poaData_poaGranteeList_person_individualIdType= ""
		self.poaData_poaGranteeList_person_legalIdNbr= ""
		self.poaData_poaGranteeList_person_legalIdType= ""
		self.poaData_poaGranteeList_person_legalNature= ""
		self.poaData_poaGranteeList_person_legalNatureInOtherLang= ""
		self.poaData_poaGranteeList_person_nationalityCountryCode= ""
		self.poaData_poaGranteeList_person_personGroupCode= ""
		self.poaData_poaGranteeList_person_personGroupName= ""
		self.poaData_poaGranteeList_person_personName= ""
		self.poaData_poaGranteeList_person_personNameInOtherLang= ""
		self.poaData_poaGranteeList_person_residenceCountryCode= ""
		self.poaData_poaGranteeList_person_stateCode= ""
		self.poaData_poaGranteeList_person_stateName= ""
		self.poaData_poaGranteeList_person_telephone= ""
		self.poaData_poaGranteeList_person_zipCode= ""
		self.poaData_poaGrantor_person_addressStreet= ""
		self.poaData_poaGrantor_person_addressStreetInOtherLang= ""
		self.poaData_poaGrantor_person_addressZone= ""
		self.poaData_poaGrantor_person_agentCode= ""
		self.poaData_poaGrantor_person_cityCode= ""
		self.poaData_poaGrantor_person_cityName= ""
		self.poaData_poaGrantor_person_companyRegisterRegistrationDate= ""
		self.poaData_poaGrantor_person_companyRegisterRegistrationNbr= ""
		self.poaData_poaGrantor_person_email= ""
		self.poaData_poaGrantor_person_individualIdNbr= ""
		self.poaData_poaGrantor_person_individualIdType= ""
		self.poaData_poaGrantor_person_legalIdNbr= ""
		self.poaData_poaGrantor_person_legalIdType= ""
		self.poaData_poaGrantor_person_legalNature= ""
		self.poaData_poaGrantor_person_legalNatureInOtherLang= ""
		self.poaData_poaGrantor_person_nationalityCountryCode= ""
		self.poaData_poaGrantor_person_personGroupCode= ""
		self.poaData_poaGrantor_person_personGroupName= ""
		self.poaData_poaGrantor_person_personName= ""
		self.poaData_poaGrantor_person_personNameInOtherLang= ""
		self.poaData_poaGrantor_person_residenceCountryCode= ""
		self.poaData_poaGrantor_person_stateCode= ""
		self.poaData_poaGrantor_person_stateName= ""
		self.poaData_poaGrantor_person_telephone= ""
		self.poaData_poaGrantor_person_zipCode= ""
		self.poaData_poaRegNumber= ""
		self.poaData_scope= ""
		
		
		try:
			self.representationData_representativeList_person_addressStreet = ag_data['addressStreet']
		except Exception as e:
			self.representationData_representativeList_person_addressStreet= ""
		try:	
			self.representationData_representativeList_person_addressStreetInOtherLang= ""
		except Exception as e:
			self.representationData_representativeList_person_addressStreetInOtherLang= ""	
		try:
			self.representationData_representativeList_person_addressZone = default_val(ag_data['addressZone'])
		except Exception as e:
			self.representationData_representativeList_person_addressZone= ""	
		try:
			self.representationData_representativeList_person_agentCode = str(int(ag_data['agentCode']['doubleValue']))
		except Exception as e:
			self.representationData_representativeList_person_agentCode= ""	
		try:
			self.representationData_representativeList_person_cityCode =  default_val(ag_data['cityCode'])
		except Exception as e:
			self.representationData_representativeList_person_cityCode= ""	
		try:	
			self.representationData_representativeList_person_cityName = default_val(ag_data['cityName'])
		except Exception as e:
			self.representationData_representativeList_person_cityName= ""	
		try:	
			self.representationData_representativeList_person_companyRegisterRegistrationDate= ""
		except Exception as e:
			self.representationData_representativeList_person_companyRegisterRegistrationDate= ""	
		try:	
			self.representationData_representativeList_person_companyRegisterRegistrationNbr= ""
		except Exception as e:
			self.representationData_representativeList_person_companyRegisterRegistrationNbr= ""		
		try:		
			self.representationData_representativeList_person_email = ag_data['email']
		except Exception as e:
			self.representationData_representativeList_person_email= ""		
		try:		
			self.representationData_representativeList_person_individualIdNbr= ""	
		except Exception as e:
			self.representationData_representativeList_person_individualIdNbr= ""		
		try:		
			self.representationData_representativeList_person_individualIdType= ""
		except Exception as e:
			self.representationData_representativeList_person_individualIdType= ""		
		try:		
			self.representationData_representativeList_person_legalIdNbr= ""
		except Exception as e:
			self.representationData_representativeList_person_legalIdNbr= ""		
		try:		
			self.representationData_representativeList_person_legalIdType= ""
		except Exception as e:
			self.representationData_representativeList_person_legalIdType= ""		
		try:		
			self.representationData_representativeList_person_legalNature= ""
		except Exception as e:
			self.representationData_representativeList_person_legalNature= ""		
		try:		
			self.representationData_representativeList_person_legalNatureInOtherLang= ""
		except Exception as e:
			self.representationData_representativeList_person_legalNatureInOtherLang= ""		
		try:		
			self.representationData_representativeList_person_nationalityCountryCode = ag_data['nationalityCountryCode']
		except Exception as e:
			self.representationData_representativeList_person_nationalityCountryCode= ""		
		try:		
			self.representationData_representativeList_person_personGroupCode= ""
		except Exception as e:
			self.representationData_representativeList_person_personGroupCode= ""		
		try:		
			self.representationData_representativeList_person_personGroupName= ""
		except Exception as e:
			self.representationData_representativeList_person_personGroupName= ""		
		try:		
			self.representationData_representativeList_person_personName = ag_data['personName']
		except Exception as e:
			self.representationData_representativeList_person_personName= ""		
		try:		
			self.representationData_representativeList_person_personNameInOtherLang= ""
		except Exception as e:
			self.representationData_representativeList_person_personNameInOtherLang= ""		
		try:		
			self.representationData_representativeList_person_residenceCountryCode = ag_data['residenceCountryCode']
		except Exception as e:
			self.representationData_representativeList_person_residenceCountryCode= ""
		try:		
			self.representationData_representativeList_person_stateCode = ""
		except Exception as e:
			self.representationData_representativeList_person_stateCode= ""
		try:		
			self.representationData_representativeList_person_stateName= ""
		except Exception as e:
			self.representationData_representativeList_person_stateName= ""
		try:		
			self.representationData_representativeList_person_telephone = ag_data['telephone']
		except Exception as e:
			self.representationData_representativeList_person_telephone= ""		
		try:		
			self.representationData_representativeList_person_zipCode = ag_data['zipCode']
		except Exception as e:
			self.representationData_representativeList_person_zipCode= ""	
		try:
			self.representationData_representativeList_representativeType = ag_data['representativeType']
		except Exception as e:
			self.representationData_representativeList_representativeType = "AG"



