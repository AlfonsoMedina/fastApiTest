
from asyncio.windows_events import NULL
from dinapi.sfe import pendiente_sfe,code_ag, pago_data, process_day_Nbr, registro_sfe
from getFileDoc import getFile
from wipo.function_for_reception_in import user_doc_getList_escrito
from wipo.ipas import mark_getlist, personAgente
import tools.connect as connex
import tools.filing_date as captureDate
import tools.connect as connex


default_val = lambda arg: arg if arg == "null" else "" 
default_val_e99 = lambda arg: arg if arg != "" else ""

class insertRegModel(object):
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
		data = pendiente_sfe(doc_Id) #registro_sfe(doc_Id)
		
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
		
		self.file_fileId_fileNbr = "" 		# dia proceso
		self.file_fileId_fileSeq = ""		# PY
		self.file_fileId_fileSeries = "" 	# año
		self.file_fileId_fileType = ""		# M
		self.file_filingData_applicationSubtype = ""
		self.file_filingData_applicationType = "REG"
		self.file_filingData_captureUserId = ""
		self.file_filingData_filingDate = ""
		self.file_filingData_captureDate = ""
		self.file_filingData_lawCode = ""
		self.file_filingData_paymentList_currencyType = ""
		self.file_filingData_paymentList_receiptAmount = ""
		self.file_filingData_paymentList_receiptDate = ""
		self.file_filingData_paymentList_receiptNbr = ""
		self.file_filingData_paymentList_receiptNotes = ""
		self.file_filingData_paymentList_receiptType = ""
		self.file_filingData_receptionUserId = ""
		self.file_ownershipData_ownerList_person_addressStreet = ""
		self.file_ownershipData_ownerList_person_nationalityCountryCode = ""
		self.file_ownershipData_ownerList_person_personName = ""
		self.file_ownershipData_ownerList_person_residenceCountryCode = ""
		self.file_rowVersion = "1.0"
		self.agentCode = ""
		self.file_representationData_representativeList_representativeType = ""
		self.rowVersion = ""
		self.protectionData_dummy = "false"
		self.protectionData_niceClassList_niceClassDescription = ""
		self.protectionData_niceClassList_niceClassDetailedStatus = ""
		self.protectionData_niceClassList_niceClassEdition = "12"
		self.protectionData_niceClassList_niceClassGlobalStatus = "P"
		self.protectionData_niceClassList_niceClassNbr = data.clase_on
		self.protectionData_niceClassList_niceClassVersion = "2023.01"
		self.logoData = ""
		self.logoType = ""
		self.signData_markName = "LOMITA"
		self.signData_signType = "B"						

		



