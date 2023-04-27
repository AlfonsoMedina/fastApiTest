
from asyncio.windows_events import NULL
from tools.base64Decode import image_url_to_b64
from dinapi.sfe import pago_id, pendiente_sfe,code_ag, pago_data, process_day_Nbr, registro_sfe
from getFileDoc import getFile
from wipo.function_for_reception_in import user_doc_getList_escrito
from wipo.ipas import mark_getlist, mark_read, personAgente
import tools.connect as connex
import tools.filing_date as captureDate
import tools.connect as connex


default_val = lambda arg: arg if arg == "null" else "" 
default_val_e99 = lambda arg: arg if arg != "" else ""

class insertRenModel(object):
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
	def __init__(self):
		pass
	
	def exist_split(self,arg0,arg1):
		data = pendiente_sfe(arg0)
		list_splits = {}
		for i in range(0,len(data[0]['respuestas'])):
			list_splits['campo'+str(i)] = data[0]['respuestas'][i]['campo']
		exists = arg1 in list_splits.values()	
		return(exists)

	def setData(self,doc_Id):
		#data = mark_read()
		self.file_fileId_fileNbr = ""
		self.file_fileId_fileSeq = ""
		self.file_fileId_fileSeries = ""
		self.file_fileId_fileType = ""
		self.file_filingData_applicationSubtype = ""
		self.file_filingData_applicationType = ""
		self.file_filingData_captureUserId = ""
		self.file_filingData_captureDate = ""
		self.file_filingData_filingDate = ""
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
		self.file_representationData_representativeList_representativeType = ""
		self.agentCode = ""
		self.file_relationshipList_fileId_fileNbr = ""
		self.file_relationshipList_fileId_fileSeq = ""
		self.file_relationshipList_fileId_fileSeries = ""
		self.file_relationshipList_fileId_fileType = ""
		self.file_relationshipList_relationshipRole = ""
		self.file_relationshipList_relationshipType = ""
		self.file_rowVersion = ""
		self.protectionData_dummy = ""
		self.protectionData_niceClassList_niceClassDescription = ""
		self.protectionData_niceClassList_niceClassDetailedStatus = ""
		self.protectionData_niceClassList_niceClassEdition = ""
		self.protectionData_niceClassList_niceClassGlobalStatus = ""
		self.protectionData_niceClassList_niceClassNbr = ""
		self.protectionData_niceClassList_niceClassVersion = ""
		self.rowVersion = ""
		self.logoData = ""
		self.logoType = ""
		self.signData_markName = ""
		self.signData_signType = ""						

		
