
from asyncio.windows_events import NULL
from tools.base64Decode import image_url_to_b64
from dinapi.sfe import pago_id, pendiente_sfe,code_ag, pago_data, process_day_Nbr, registro_sfe
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
		typ_signo:str = ''
		desc_serv:str = ''
		logo_url:str = ''
		logo_typ:str = ''
		data = registro_sfe(doc_Id)

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
		
		"""		
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
		"""
		
		if data['tipo_on'] == "Denominativa":
			typ_signo = 'N'
			logo_url = ""
			logo_typ = ""			
		if data['tipo_on'] == "D":
			typ_signo = 'N'
			logo_url = ""
			logo_typ = ""						
		if data['tipo_on'] == "Figurativa":
			typ_signo = 'L'
			logo_url = image_url_to_b64(str(data['distintivo']))
			logo_typ = "JPG"			
		if data['tipo_on'] == "F":
			typ_signo = 'L'
			logo_url = image_url_to_b64(str(data['distintivo']))
			logo_typ = "JPG"			
		if data['tipo_on'] == "Mixta":
			typ_signo = 'B'
			logo_url = image_url_to_b64(str(data['distintivo']))
			logo_typ = "JPG"
		if data['tipo_on'] == "M":
			typ_signo = 'B'
			logo_url = image_url_to_b64(str(data['distintivo']))
			logo_typ = "JPG"	
		if data['tipo_on'] == "Tridimensional":
			typ_signo = 'T'
			logo_url = image_url_to_b64(str(data['distintivo']))
			logo_typ = "JPG"			
		if data['tipo_on'] == "T":
			typ_signo = 'T'
			logo_url = image_url_to_b64(str(data['distintivo']))
			logo_typ = "JPG"
		if data['tipo_on'] == "Sonora":
			typ_signo = 'S'
			logo_url = ""
			logo_typ = ""			
		if data['tipo_on'] == "S":
			typ_signo = 'S'
			logo_url = ""
			logo_typ = ""			
		if data['tipo_on'] == "Olfativa":
			typ_signo = 'O'
			logo_url = ""
			logo_typ = ""			
		if data['tipo_on'] == "O":
			typ_signo = 'O'
			logo_url = ""
			logo_typ = ""												

		if data['clasificacion'] == 'PRODUCTOS':
			desc_serv = 'MP'
		if data['clasificacion'] == 'SERVICIOS':
			desc_serv = 'MS'			


		self.file_fileId_fileNbr = str(int(process_day_Nbr())+1)
		self.file_fileId_fileSeq = "PY"
		self.file_fileId_fileSeries = captureDate.capture_year() 
		self.file_fileId_fileType = "M"		
		self.file_filingData_applicationSubtype = desc_serv
		self.file_filingData_applicationType = "REG"
		self.file_filingData_captureUserId = "4"
		self.file_filingData_filingDate = captureDate.capture_full()
		self.file_filingData_captureDate = captureDate.capture_full()
		self.file_filingData_lawCode = "1.0"
		self.file_filingData_paymentList_currencyType = "GS"
		self.file_filingData_paymentList_receiptAmount = str(pago_data(doc_Id)[1])
		self.file_filingData_paymentList_receiptDate = str(pago_data(doc_Id)[2])
		self.file_filingData_paymentList_receiptNbr = str(pago_data(doc_Id)[0])
		self.file_filingData_paymentList_receiptNotes = "Recibo Sprint MEA"
		self.file_filingData_paymentList_receiptType = "1"
		self.file_filingData_receptionUserId = "4"
		self.file_ownershipData_ownerList_person_addressStreet = data['direccion']
		self.file_ownershipData_ownerList_person_nationalityCountryCode = data['pais']
		self.file_ownershipData_ownerList_person_personName = data['razon_social'] + data['nombre_soli']
		self.file_ownershipData_ownerList_person_residenceCountryCode = data['pais']
		self.file_rowVersion = "1.0"
		self.agentCode = data['code_agente']
		self.file_representationData_representativeList_representativeType = "AG"
		self.rowVersion = "1.0"
		self.protectionData_dummy = "false"
		self.protectionData_niceClassList_niceClassDescription = data['distingue']
		self.protectionData_niceClassList_niceClassDetailedStatus = "P"
		self.protectionData_niceClassList_niceClassEdition = "12.0"
		self.protectionData_niceClassList_niceClassGlobalStatus = "P"
		self.protectionData_niceClassList_niceClassNbr = data['clase_on']
		self.protectionData_niceClassList_niceClassVersion = "2023.01"
		self.logoData = logo_url
		self.logoType = logo_typ
		self.signData_markName = data['denominacion_on']
		self.signData_signType = typ_signo						

		
