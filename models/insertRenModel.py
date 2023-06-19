import base64
from dinapi.sfe import pendiente_sfe,code_ag, pago_data, process_day_Nbr, registro_sfe, renovacion_sfe
from getFileDoc import getFile
from respuesta_map import dir_titu, nom_titu
from wipo.function_for_reception_in import user_doc_getList_escrito
from wipo.ipas import mark_getlist, mark_getlistReg, mark_read, mark_readlogo, personAgente
import tools.connect as connex
import tools.filing_date as captureDate
import tools.connect as connex
from tools.base64Decode import decode_img, image_url_to_b64


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
	file_ownershipData_ownerList_person_owneraddressStreet:str = ""
	file_ownershipData_ownerList_person_ownernationalityCountryCode:str = ""
	file_ownershipData_ownerList_person_ownerpersonName:str = ""
	file_ownershipData_ownerList_person_ownerresidenceCountryCode:str = ""
	file_rowVersion:str = ""
	agentCode:str = ""

	file_relationshipList_fileId_fileNbr:str = ""
	file_relationshipList_fileId_fileSeq:str = ""
	file_relationshipList_fileId_fileSeries:str = ""
	file_relationshipList_fileId_fileType:str = ""
	file_relationshipList_relationshipRole:str = ""
	file_relationshipList_relationshipType:str = ""

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
	signType:str = ''
	tipo_clase:str = ''
	data:str = ''
	LogData:str = ''
	LogDataUri:str = ''
	LogTyp:str = ''
	relacion:str = ''
	dir_owner:str = ''
	thisName:str = ''
	fileNbr:str = ''
	fileSeq:str = ''
	fileSeries:str = ''
	fileId:str = ''
	ag_email:str = ''
	def __init__(self):
		self.signType = ""
		self.tipo_clase = ""
		self.LogData = ""
		self.LogTyp = ""

	def setData(self,doc_Id):
		
		self.data = renovacion_sfe(doc_Id) 

		self.ag_email = self.data['email_agente']
	
		#print(self.data)

		#print('----------------------------------------------')

		try:
			if self.data['distintivo'] == "No definido":
				self.LogDataUri = self.data['distintivoAct']
			elif self.data['distintivoAct'] == "No definido":
				self.LogDataUri = self.data['distintivo']
			else:
				self.LogDataUri = ""
		except Exception as e:
			self.LogDataUri = ""	

		#print(self.LogDataUri)

		get_List = mark_getlistReg(self.data['registro_nbr'])
		
		get_data_mark = mark_read(
			get_List[0].fileId.fileNbr.doubleValue, 
			get_List[0].fileId.fileSeq, 
			get_List[0].fileId.fileSeries.doubleValue, 
			get_List[0].fileId.fileType
			)

		try:	
			if self.data['tipo_guion'] == "Sonora": 
				self.signType="S"
				self.LogData = ""
				self.LogTyp = ""			
		except Exception as e:
			pass
		
		try:
			if self.data['tipo_guion'] == "S": 
				self.signType="S"
				self.LogData = ""
				self.LogTyp = ""			
		except Exception as e:
			pass
		
		try:
			if self.data['tipo_guion'] == "Olfativa": 
				self.signType="O"
				self.LogData = ""
				self.LogTyp = ""				
		except Exception as e:
			pass
								
		try:
			if self.data['clasificacion'] == 'PRODUCTO':
				self.tipo_clase = "MP"
		except Exception as e:
			pass
								
		try:
			if self.data['clasificacion'] == 'SERVICIO':
				self.tipo_clase = 'MS'
		except Exception as e:
			pass
								
		try:
			if self.data['clasificacion'] == 'PRODUCTOS':
				self.tipo_clase = "MP"
		except Exception as e:
			pass
								
		try:				
			if self.data['clasificacion'] == 'SERVICIOS':
				self.tipo_clase = 'MS'
		except Exception as e:
			pass



		self.file_fileId_fileNbr = str(get_data_mark.file.fileId.fileNbr.doubleValue)
		self.file_fileId_fileSeq = get_data_mark.file.fileId.fileSeq
		self.file_fileId_fileSeries = str(captureDate.capture_year())
		self.file_fileId_fileType = get_data_mark.file.fileId.fileType
		self.file_filingData_applicationSubtype = self.tipo_clase
		self.file_filingData_applicationType = get_data_mark.file.filingData.applicationType
		self.file_filingData_captureUserId = str(get_data_mark.file.filingData.captureUserId.doubleValue)
		self.file_filingData_filingDate = str(captureDate.capture_full())
		self.file_filingData_captureDate = str(captureDate.capture_full())
		self.file_filingData_lawCode = str(get_data_mark.file.filingData.lawCode.doubleValue)
		try:
			self.file_filingData_paymentList_currencyType = "GS"
			self.file_filingData_paymentList_receiptAmount = str(pago_data(doc_Id)[1])
			self.file_filingData_paymentList_receiptDate = str(pago_data(doc_Id)[2])[0:10]
			self.file_filingData_paymentList_receiptNbr = str(pago_data(doc_Id)[0])
			self.file_filingData_paymentList_receiptNotes = "Caja MEA"
			self.file_filingData_paymentList_receiptType = "1"
		except Exception as e:
			self.file_filingData_paymentList_currencyType = ""
			self.file_filingData_paymentList_receiptAmount = ""
			self.file_filingData_paymentList_receiptDate = ""
			self.file_filingData_paymentList_receiptNbr = ""
			self.file_filingData_paymentList_receiptNotes = ""
			self.file_filingData_paymentList_receiptType = ""			
		self.file_filingData_receptionUserId = str("4")
		self.file_ownershipData_ownerList_person_owneraddressStreet = get_data_mark.file.ownershipData.ownerList[0].person.addressStreet
		self.file_ownershipData_ownerList_person_ownernationalityCountryCode = get_data_mark.file.ownershipData.ownerList[0].person.nationalityCountryCode
		self.file_ownershipData_ownerList_person_ownerpersonName = get_data_mark.file.ownershipData.ownerList[0].person.personName
		self.file_ownershipData_ownerList_person_ownerresidenceCountryCode = get_data_mark.file.ownershipData.ownerList[0].person.residenceCountryCode
		self.file_rowVersion = "1.0"
		self.agentCode = self.data['code_agente']

		self.file_relationshipList_fileId_fileNbr = str(get_data_mark.file.fileId.fileNbr.doubleValue)
		self.file_relationshipList_fileId_fileSeq = get_data_mark.file.fileId.fileSeq
		self.file_relationshipList_fileId_fileSeries = str(get_data_mark.file.fileId.fileSeries.doubleValue)
		self.file_relationshipList_fileId_fileType = get_data_mark.file.fileId.fileType
		self.file_relationshipList_relationshipRole = '2'
		self.file_relationshipList_relationshipType = 'REN'

		self.file_representationData_representativeList_representativeType = get_data_mark.file.representationData.representativeList[0].representativeType
		self.rowVersion = "1.0"
		self.protectionData_dummy = str(get_data_mark.protectionData.dummy)
		self.protectionData_niceClassList_niceClassDescription = get_data_mark.protectionData.niceClassList[0].niceClassDescription
		self.protectionData_niceClassList_niceClassDetailedStatus = "P"
		self.protectionData_niceClassList_niceClassEdition = "12.0"
		self.protectionData_niceClassList_niceClassGlobalStatus = "P"
		self.protectionData_niceClassList_niceClassNbr = str(get_data_mark.protectionData.niceClassList[0].niceClassNbr.doubleValue)
		self.protectionData_niceClassList_niceClassVersion = "2023.01"
		self.logoData = base64.b64encode(get_data_mark.signData.logo.logoData).decode("UTF-8")
		self.logoType = str(get_data_mark.signData.logo.logoType)
		self.signData_markName = get_data_mark.signData.markName
		self.signData_signType = str(get_data_mark.signData.signType)
		self.signType = "-"
		self.tipo_clase = "-"
		self.data = "-"
		self.LogData = ""
		self.LogTyp = ""
		self.relacion = "-"
		self.dir_owner = "-"
		self.thisName = "-"
		self.fileNbr = "-"
		self.fileSeq = "-"
		self.fileSeries = "-"
		self.fileId = "-"




