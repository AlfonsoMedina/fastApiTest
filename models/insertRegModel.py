
from asyncio.windows_events import NULL
from dinapi.sfe import pendiente_sfe,code_ag, pago_data, process_day_Nbr, registro_sfe, titulare_reg
from getFileDoc import getFile
from wipo.function_for_reception_in import user_doc_getList_escrito
from wipo.ipas import mark_getlist, personAgente
import tools.connect as connex
import tools.filing_date as captureDate
import tools.connect as connex
from tools.base64Decode import image_url_to_b64


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
	signType:str = ''
	tipo_clase:str = ''
	data:str = ''
	LogData:str = ''
	LogTyp:str = ''
	dir_variant:str = ''
	ownerList:str = ''
	multitu:str = ''
	def __init__(self):
		self.signType = ""
		self.tipo_clase = ""
		self.LogData = ""
		self.LogTyp = ""

	def setData(self,doc_Id):
		
		self.data = registro_sfe(doc_Id) #pendiente_sfe(doc_Id)
		self.multitu = titulare_reg(doc_Id)# TITULARES
		if self.multitu[0]['person']['personName'] == '':
			self.multitu = []


		


		try:
			ag_data = personAgente(code_ag(self.data[0]['usuario_id']))[0]
		except Exception as e:
			print("")
		
		try:
			if self.data['tipo_on'] == "Denominativa": 
				self.signType="N"
				self.LogData = ""
				self.LogTyp = ""
		except Exception as e:
			pass			

		try:
			if self.data['tipo_on'] == "D": 
				self.signType="N"
				self.LogData = ""
				self.LogTyp = ""						
		except Exception as e:
			pass
		try:
			if self.data['tipo_on'] == "Figurativa": 
				self.signType="L"
				self.LogData = image_url_to_b64(self.data['distintivo'])
				self.LogTyp = "JPG"			
		except Exception as e:
			pass
		try:
			if self.data['tipo_on'] == "F": 
				self.signType="L"
				self.LogData = image_url_to_b64(self.data['distintivo'])
				self.LogTyp = "JPG"							
		except Exception as e:
			pass
		try:
			if self.data['tipo_on'] == "Mixta": 
				self.signType="B"
				self.LogData = image_url_to_b64(self.data['distintivo'])
				self.LogTyp = "JPG"				
		except Exception as e:
			pass
		try:
			if self.data['tipo_on'] == "M": 
				self.signType="B"
				self.LogData = image_url_to_b64(self.data['distintivo'])
				self.LogTyp = "JPG"				
		except Exception as e:
			pass
		try:
			if self.data['tipo_on'] == "Tridimensional": 
				self.signType="T"
				self.LogData = image_url_to_b64(self.data['distintivo'])
				self.LogTyp = "JPG"				
		except Exception as e:
			pass
		try:
			if self.data['tipo_on'] == "T": 
				self.signType="T"
				self.LogData = image_url_to_b64(self.data['distintivo'])
				self.LogTyp = "JPG"										
		except Exception as e:
			pass
		try:			
			if self.data['tipo_on'] == "Sonora": 
				self.signType="S"
				self.LogData = ""
				self.LogTyp = ""			
		except Exception as e:
			pass
		try:
			if self.data['tipo_on'] == "S": 
				self.signType="S"
				self.LogData = ""
				self.LogTyp = ""			
		except Exception as e:
			pass
		try:
			if self.data['tipo_on'] == "Olfativa": 
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

		self.file_fileId_fileNbr = str(int(process_day_Nbr())+1)
		self.file_fileId_fileSeq = "PY"
		self.file_fileId_fileSeries = captureDate.capture_year()
		self.file_fileId_fileType = "M"
		self.file_filingData_applicationSubtype = self.tipo_clase
		self.file_filingData_applicationType = "REG"
		self.file_filingData_captureUserId = "4"
		self.file_filingData_filingDate = captureDate.capture_full()
		self.file_filingData_captureDate = captureDate.capture_full()
		self.file_filingData_lawCode = "1.0"
		self.file_filingData_paymentList_currencyType = "GS"
		self.file_filingData_paymentList_receiptAmount = str(pago_data(doc_Id)[1])
		self.file_filingData_paymentList_receiptDate = str(pago_data(doc_Id)[2])[0:10]
		self.file_filingData_paymentList_receiptNbr = str(pago_data(doc_Id)[0])
		self.file_filingData_paymentList_receiptNotes = " Caja MEA"
		self.file_filingData_paymentList_receiptType = "1"
		self.file_filingData_receptionUserId = "4"

		try:
			if self.data['direccion'] == "No definido":
				self.dir_variant = self.data['direccion_dir']
		except Exception as e:
			pass
		try:
			if self.data['direccion_dir'] == "No definido":
				self.dir_variant = self.data['direccion']
		except Exception as e:
			pass


		self.file_ownershipData_ownerList_person_addressStreet = self.data['direccion_dir']




		self.file_ownershipData_ownerList_person_nationalityCountryCode = self.data['pais']
		
		self.file_ownershipData_ownerList_person_personName = self.data['razon_social'] + self.data['nombre_soli']
		self.file_ownershipData_ownerList_person_residenceCountryCode = self.data['pais']


		self.ownerList = self.multitu


		self.file_rowVersion = "1.0"
		self.agentCode = self.data['code_agente']
		self.file_representationData_representativeList_representativeType = "AG"
		self.rowVersion = "1.0"
		self.protectionData_dummy = "false"
		
		self.protectionData_niceClassList_niceClassDescription = self.data['distingue']
		
		self.protectionData_niceClassList_niceClassDetailedStatus = "P"
		self.protectionData_niceClassList_niceClassEdition = "12.0"
		self.protectionData_niceClassList_niceClassGlobalStatus = "P"

		self.protectionData_niceClassList_niceClassNbr = self.data['clase_on']
		
		self.protectionData_niceClassList_niceClassVersion = "2023.01"
		self.logoData = self.LogData
		self.logoType = self.LogTyp
		self.signData_markName = self.data['denominacion_on']
		
		self.signData_signType = self.signType						
		


