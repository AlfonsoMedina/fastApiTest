from ast import Return
from base64 import encode
import base64
from datetime import date, timedelta
from dis import code_info
import json
import pickle
from time import sleep
from click import File
from zeep import Client
from io import BytesIO, FileIO
from flask import jsonify
import psycopg2
import zeep
from io import open
import tools.connect as conn_serv
from tools.service_system import config_parametro
import pymssql
import datetime
import sys
import tools.connect as connex

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
try:
	mark_service = conn_serv.MEA_IPAS_DESTINO
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')

try:
	Patents_service = conn_serv.ipas_produccion_patent
	wsdlPatente = Patents_service + "/IpasServices/IpasServices?wsdl"
	clientPatents = Client(wsdlPatente)
except Exception as e:
	print('Error de coneccion  IPAS Patentes!!')

try:
	disenio_service = conn_serv.ipas_produccion_disenio 
	wsdlDisenio = disenio_service + "/IpasServices/IpasServices?wsdl"
	clientDisenio = Client(wsdlDisenio)
except Exception as e:
	print('Error de coneccion  IPAS Diseño!!')

print(sys.version)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#---------------------------------------------------------------Marcas--------------------------------------------------------------------------------------------------
# Envio => POST = "21107702" 
def mark_getlist(fileNbr):
	try:
		MarkGetList = {'arg0': {'criteriaFileId': {'fileNbrFrom': {'doubleValue':fileNbr,},'fileNbrTo': {'doubleValue':fileNbr}},},}
		return clientMark.service.MarkGetList(**MarkGetList)
	except zeep.exceptions.Fault as e:
		return([])		

def mark_getlistReg(solidNbr):
	MarkGetListReg = {'arg0': {'criteriaRegistrationData': {'registrationNbrFrom': {'doubleValue':solidNbr,},'registrationNbrTo': {'doubleValue':solidNbr}},},}
	return clientMark.service.MarkGetList(**MarkGetListReg)

#consulta registro de poder
def getPoder(registro):
	try:
		data = {"arg0": {
					"criteriaExtraData": {
					"dataNbr1": {
						"doubleValue": registro
					}}}}
		find_data = clientMark.service.UserdocGetList(**data)
		if find_data != []:
			return True
		else:
			return False	
	except zeep.exceptions.Fault as e:
		return False
				
# Envio => POST = {"arg0": {"fileNbr":  "2017020","fileSeq": "PY","fileSeries": "2020","fileType": "M"},"arg1": "","arg2": ""}
def mark_readlogo(fileNbr, fileSeq, fileSeries, fileType): #{'doubleValue': '2177877',},'fileSeq': 'PY','fileSeries': {'doubleValue': '2021', },'fileType': 'M',
	MarkReadLogo = {'arg0': {'fileNbr': {'doubleValue': fileNbr,},'fileSeq': fileSeq,'fileSeries': {'doubleValue': fileSeries, },'fileType': fileType, },	}
	return clientMark.service.MarkReadLogo(**MarkReadLogo) 

#ProcessReadAction PROBAR 
def Process_Read_Action(action,processNbr,processType):
	Read_Action = {	"arg0": {"actionNbr": {	"doubleValue": action},"processId": {"processNbr": {"doubleValue": processNbr},"processType": processType}}}
	return(clientMark.service.ProcessReadAction(**Read_Action))

#Lista de procesos o eventos
def Process_Read_EventList(processNbr,processType):
	eventList = {"arg0": {"processNbr": {"doubleValue": processNbr},"processType": processType}}
	return(clientMark.service.ProcessReadEventList(**eventList))

# Envio => POST = {"arg0": {"fileNbr":  "2017020","fileSeq": "PY","fileSeries": "2020","fileType": "M"},"arg1": "","arg2": ""}
def process_read(processNbr, processType): #{"arg0": {"processNbr": {"doubleValue": processNbr }, "processType": processType },"arg1": "","arg2": ""}
	Process_Read = {"arg0": {"processNbr": {"doubleValue": processNbr }, "processType": processType },"arg1": "","arg2": ""}
	return clientMark.service.ProcessRead(**Process_Read)

def Process_Get_Possible_Option_List(actionType):
	pgpol = {
			"arg0": {
				"actionType": str(actionType)
			},
			"arg1": "",
			"arg2": "",
			"arg3": {
				"doubleValue": ""
			},
			"arg4": ""
			}
	return clientMark.service.ProcessGetPossibleOptionList(**pgpol)        

#Lista de expediente por fecha
def mark_getlistFecha(filingDateFrom, filingDateTo):
	MarkGetListFecha = {
		'arg0':{
			'criteriaFilingData': {
				'filingDateFrom': {
					'dateValue':filingDateFrom+'T00:00:00-04:00',
					},
					'filingDateTo': {
						'dateValue':filingDateTo+'T23:59:59-04:00'
						}
					},},}
	return clientMark.service.MarkGetList(**MarkGetListFecha)

# Envio => POST = {"arg0": {"fileNbr":  "2017020","fileSeq": "PY","fileSeries": "2020","fileType": "M"},"arg1": "","arg2": ""}
def mark_read(fileNbr, fileSeq, fileSeries, fileType):
	MarkRead = {'arg0': {'fileNbr': {'doubleValue': fileNbr,},'fileSeq': fileSeq,'fileSeries': {'doubleValue': fileSeries, },'fileType': fileType, }, 'arg1':'?', 'arg2':'?',	}
	#print(clientMark.service.MarkRead(**MarkRead))
	return clientMark.service.MarkRead(**MarkRead)

# Envio => POST = {"arg0": {"fileNbr":  "2017020","fileSeq": "PY","fileSeries": "2020","fileType": "M"},"arg1": "","arg2": ""}
def file_read(fileNbr, fileSeq, fileSeries, fileType):
	FileRead = {'arg0': {'fileNbr': {'doubleValue': fileNbr,},'fileSeq': fileSeq,'fileSeries': {'doubleValue': fileSeries, },'fileType': fileType, }, 'arg1':'?', 'arg2':'?',	}
	return clientMark.service.FileRead(**FileRead)

#FetchAll para gestion de usuario
def fetch_all_user(login):
	query = {
	"arg0": "SELECT * FROM MARCAS_PY.ADMIN.IP_USER iu where LOGIN='"+login+"'",
	"arg1": {
			"sqlColumnList":[
							{"sqlColumnType": "String", "sqlColumnValue":"FULL_NAME"},
							{"sqlColumnType": "String", "sqlColumnValue":"LOGIN"},
							{"sqlColumnType": "String", "sqlColumnValue":"USER_ID"},
							{"sqlColumnType": "String", "sqlColumnValue":"USER_NAME"},
							{"sqlColumnType": "String", "sqlColumnValue":"lOGIN_PASSWORD"},
							{"sqlColumnType": "String", "sqlColumnValue":"OFFICE_DIVISION_CODE"},
							{"sqlColumnType": "String", "sqlColumnValue":"OFFICE_DEPARTMENT_CODE"},
							{"sqlColumnType": "String", "sqlColumnValue":"OFFICE_SECTION_CODE"},
							{"sqlColumnType": "String", "sqlColumnValue":"SIGNATURE_DATA"},
							{"sqlColumnType": "String", "sqlColumnValue":"IND_INACTIVE"}]
	}
  }
	return(clientMark.service.SqlFetchAll(**query))

#FetchAll para gestion de usuario
def fetch_all_LOG_Read(fecha):
	query = {
	"arg0": "SELECT DAILY_LOG_DATE, IND_OPEN, IND_CLOSED, DOC_ORI, DOC_LOG FROM IP_DAILY_LOG idl WHERE DAILY_LOG_DATE BETWEEN '30/11/2022' AND '30/11/2022'",
	"arg1": {
			"sqlColumnList":[
							{"sqlColumnType": "String", "sqlColumnValue":"DAILY_LOG_DATE"},
							{"sqlColumnType": "String", "sqlColumnValue":"IND_OPEN"},
							{"sqlColumnType": "String", "sqlColumnValue":"IND_CLOSED"},
							{"sqlColumnType": "String", "sqlColumnValue":"DOC_ORI"},
							{"sqlColumnType": "String", "sqlColumnValue":"DOC_LOG"},
							]
	}
  }
	return(clientMark.service.SqlFetchAll(**query))

#mostrar documento por su process number
def fetch_all_officdoc(PROC_NBR):
	try:
		query = {
				  "arg0": "select CONTENT_DATA from IP_OFFIDOC where PROC_NBR  = "+PROC_NBR+" and CONTENT_TYPE = 'PDF'", # 61792 51014 6232
				  "arg1": {
					"rowNum": {
					  "doubleValue": 1
					},
					  "sqlColumnList": {"columnNum": {"doubleValue": 1},
					  "sqlColumnType": "String", "sqlColumnValue": "CONTENT_DATA"
					}
				  }
				}
		return(clientMark.service.SqlFetchAll(**query)[0].sqlColumnList[0].sqlColumnValue)
	except Exception as e:
		return('false')

#Offic_Nbr desde IP_OFFICDOC
def fetch_all_officdoc_nuxeo(PROC_NBR:str):
	try:
		query = {
				  "arg0": "SELECT OFFIDOC_NBR,ACTION_USER_ID,OFFIDOC_TYP FROM MARCAS_PY.ADMIN.IP_OFFIDOC WHERE CONTENT_TYPE is null and PROC_NBR ='"+PROC_NBR+"'", 
				  "arg1": {
							"sqlColumnList":[
											{"sqlColumnType": "String", "sqlColumnValue":"OFFIDOC_NBR"},
											{"sqlColumnType": "String", "sqlColumnValue":"ACTION_USER_ID"},
											{"sqlColumnType": "String", "sqlColumnValue":"OFFIDOC_TYP"},
											]
				  }
				}
		return(clientMark.service.SqlFetchAll(**query))
	except Exception as e:
		return(e)	

def fetch_all_do_edoc_nuxeo(EDOC_NBR:str):
	try:
		query = {
				  "arg0": "SELECT * FROM MARCAS_PY.ADMIN.DO_EDOC WHERE EDOC_NBR = '"+EDOC_NBR+"' AND EDOC_IMAGE_CERTIF_USER = 4;", 
				  "arg1": {
							"sqlColumnList":[
											{"sqlColumnType": "String", "sqlColumnValue":"EDOC_ID"},
											{"sqlColumnType": "String", "sqlColumnValue":"EDOC_TYP"},
											{"sqlColumnType": "String", "sqlColumnValue":"EDOC_DATE"},
											
											{"sqlColumnType": "String", "sqlColumnValue":"EDOC_SEQ"},
											{"sqlColumnType": "String", "sqlColumnValue":"EDOC_SER"},
											{"sqlColumnType": "String", "sqlColumnValue":"EDOC_NBR"},

											{"sqlColumnType": "String", "sqlColumnValue":"EDOC_IMAGE_LINKING_DATE"},
											{"sqlColumnType": "String", "sqlColumnValue":"EDOC_IMAGE_LINKING_USER"},
											{"sqlColumnType": "String", "sqlColumnValue":"ROW_VERSION"},

											{"sqlColumnType": "String", "sqlColumnValue":"EFOLDER_ID"},
											{"sqlColumnType": "String", "sqlColumnValue":"EDOC_IMAGE_CERTIF_DATE"},
											{"sqlColumnType": "String", "sqlColumnValue":"EDOC_IMAGE_CERTIF_USER"},
											]
				  }
				}
		return(clientMark.service.SqlFetchAll(**query))
	except Exception as e:
		return(e)

#buscar documentos por process number
def fetch_all_list_proc_nbr(PROC_NBR):
	try:
		query = {
				  "arg0": "SELECT PROC_NBR,OFFIDOC_TYP FROM MARCAS_PY.ADMIN.IP_OFFIDOC WHERE CONTENT_TYPE = 'PDF' AND  PROC_NBR  ="+PROC_NBR,
				  "arg1": {
					  "sqlColumnList":[
											{"sqlColumnType": "String", "sqlColumnValue":"PROC_NBR"},
											{"sqlColumnType": "String", "sqlColumnValue":"OFFIDOC_TYP"}
											]
				  }
				}
		proc_nbr_list=[]
		for i in clientMark.service.SqlFetchAll(**query):
			proc_nbr_list.append({"proc_nbr":i.sqlColumnList[0].sqlColumnValue,"doc":i.sqlColumnList[1].sqlColumnValue})            
		return(proc_nbr_list)
	except Exception as e:
		return('false')

#mostrar documento por su OFFIDOC_PROC_NBR
def fetch_all_offic_doc_OFFIDOC_PROC_NBR(PROC_NBR):
	try:
		query = {
				  "arg0": "SELECT top 1 CONTENT_DATA FROM MARCAS_PY.ADMIN.IP_OFFIDOC WHERE OFFIDOC_TYP = 'ORD_PUBL' and PROC_NBR = "+PROC_NBR,
				  "arg1": {
					"rowNum": {
					  "doubleValue": 1
					},
					  "sqlColumnList": {"columnNum": {"doubleValue": 1},
					  "sqlColumnType": "String", "sqlColumnValue": "CONTENT_DATA"
					}
				  }
				}
		return(clientMark.service.SqlFetchAll(**query)[0].sqlColumnList[0].sqlColumnValue)
	except zeep.exceptions.Fault as e:
		return(str(e))

#FetchAll para Orden de Publicacion por fecha
def fetch_all(desde, hasta):
	fecha = str(str(desde)+' 00:00:00')
	fecha2 = str(str(desde)+' 23:59:00')
	query_sqls_fecha = {
		"arg0":'''
				SELECT  mar.FILE_NBR, pro.PROC_NBR, mar.FILING_DATE, typ.APPL_TYPE_NAME, 
						mar.SIGN_WCODE, mar.NICE_CLASS_TXT, den.MARK_NAME, per1.PERSON_NAME, 
						dir.ADDR_STREET, per2.AGENT_CODE , per2.PERSON_NAME as PERSON_NAME2, logo.LOGO_DATA, 
						act.ACTION_DATE, act.ACTION_TYP, desact.ACTION_TYPE_NAME, 
						cldes.NICE_CLASS_DESCRIPTION, usu.USER_NAME, usu.[LOGIN] uslog, usu.USER_ID
				FROM ADMIN.IP_MARK mar
				LEFT JOIN ADMIN.IP_PROC pro ON pro.FILE_NBR = mar.FILE_NBR
				LEFT JOIN ADMIN.IP_ACTION act ON act.PROC_NBR = pro.PROC_NBR and act.PROC_TYP = pro.PROC_TYP 
				LEFT JOIN ADMIN.IP_NAME den ON den.MARK_CODE = mar.MARK_CODE 
				LEFT JOIN ADMIN.IP_PERSON per1 ON per1.PERSON_NBR = mar.MAIN_OWNER_PERSON_NBR
				LEFT JOIN ADMIN.IP_MARK_OWNERS owner ON owner.FILE_NBR = mar.FILE_NBR and owner.PERSON_NBR = per1.PERSON_NBR
				LEFT JOIN ADMIN.IP_PERSON_ADDRESSES dir ON dir.PERSON_NBR = per1.PERSON_NBR and dir.ADDR_NBR = owner.ADDR_NBR
				LEFT JOIN ADMIN.IP_PERSON per2 ON per2.PERSON_NBR  = mar.SERVICE_PERSON_NBR 
				LEFT JOIN ADMIN.CF_APPLICATION_TYPE typ ON typ.APPL_TYP = mar.APPL_TYP
				LEFT JOIN ADMIN.IP_LOGO logo ON logo.FILE_NBR = mar.FILE_NBR
				LEFT JOIN ADMIN.CF_ACTION_TYPE desact ON desact.ACTION_TYP = act.ACTION_TYP 
				LEFT JOIN ADMIN.IP_MARK_NICE_CLASSES cldes ON cldes.FILE_NBR = mar.FILE_NBR
				LEFT JOIN ADMIN.IP_USER usu1 ON usu1.USER_ID = mar.CAPTURE_USER_ID 
				LEFT JOIN ADMIN.IP_USER usu ON usu.USER_ID = act.CAPTURE_USER_ID and usu.USER_ID = AUTHORISING_USER_ID
				WHERE act.ACTION_DATE BETWEEN CONVERT( DATETIME, N'{}', 121) 
				AND CONVERT( DATETIME, N'{}', 121) AND (act.ACTION_TYP = '549' or act.ACTION_TYP = '550' or act.ACTION_TYP = '560') AND act.IND_DELETED IS NULL
			'''.format(fecha,fecha2),

		"arg1":{
			"sqlColumnList":[
				{"sqlColumnType": "String", "sqlColumnValue":"FILE_NBR"},
				{"sqlColumnType": "String", "sqlColumnValue":"PROC_NBR"},
				{"sqlColumnType": "String", "sqlColumnValue":"FILING_DATE"},
				{"sqlColumnType": "String", "sqlColumnValue":"APPL_TYPE_NAME"},
				{"sqlColumnType": "String", "sqlColumnValue":"SIGN_WCODE"},
				{"sqlColumnType": "String", "sqlColumnValue":"NICE_CLASS_TXT"},
				{"sqlColumnType": "String", "sqlColumnValue":"MARK_NAME"},
				{"sqlColumnType": "String", "sqlColumnValue":"PERSON_NAME"},
				{"sqlColumnType": "String", "sqlColumnValue":"ADDR_STREET"},
				{"sqlColumnType": "String", "sqlColumnValue":"AGENT_CODE"},
				{"sqlColumnType": "String", "sqlColumnValue":"PERSON_NAME2"},
				{"sqlColumnType": "String", "sqlColumnValue":"LOGO_DATA"},
				{"sqlColumnType": "String", "sqlColumnValue":"ACTION_DATE"},
				{"sqlColumnType": "String", "sqlColumnValue":"ACTION_TYP"},
				{"sqlColumnType": "String", "sqlColumnValue":"ACTION_TYPE_NAME"},
				{"sqlColumnType": "String", "sqlColumnValue":"NICE_CLASS_DESCRIPTION"},
				{"sqlColumnType": "String", "sqlColumnValue":"USER_NAME"},
				{"sqlColumnType": "String", "sqlColumnValue":"uslog"},
				{"sqlColumnType": "String", "sqlColumnValue":"USER_ID"}
			]
		}
	}
	return(clientMark.service.SqlFetchAll(**query_sqls_fecha))

#FechAll para Orden de Publicacion por expediente
def Fech_All_Exp(exp):
	query_sqls = {
		"arg0":'''
				SELECT  mar.FILE_NBR, pro.PROC_NBR, mar.FILING_DATE, typ.APPL_TYPE_NAME, 
						mar.SIGN_WCODE, mar.NICE_CLASS_TXT, den.MARK_NAME, per1.PERSON_NAME, 
						dir.ADDR_STREET, per2.AGENT_CODE , per2.PERSON_NAME as PERSON_NAME2, logo.LOGO_DATA, 
						act.ACTION_DATE, act.ACTION_TYP, desact.ACTION_TYPE_NAME, 
						cldes.NICE_CLASS_DESCRIPTION, usu.USER_NAME, usu.[LOGIN] uslog, usu.USER_ID
				FROM ADMIN.IP_MARK mar
				LEFT JOIN ADMIN.IP_PROC pro ON pro.FILE_NBR = mar.FILE_NBR
				LEFT JOIN ADMIN.IP_ACTION act ON act.PROC_NBR = pro.PROC_NBR and act.PROC_TYP = pro.PROC_TYP 
				LEFT JOIN ADMIN.IP_NAME den ON den.MARK_CODE = mar.MARK_CODE 
				LEFT JOIN ADMIN.IP_PERSON per1 ON per1.PERSON_NBR = mar.MAIN_OWNER_PERSON_NBR
				LEFT JOIN ADMIN.IP_MARK_OWNERS owner ON owner.FILE_NBR = mar.FILE_NBR and owner.PERSON_NBR = per1.PERSON_NBR
				LEFT JOIN ADMIN.IP_PERSON_ADDRESSES dir ON dir.PERSON_NBR = per1.PERSON_NBR and dir.ADDR_NBR = owner.ADDR_NBR
				LEFT JOIN ADMIN.IP_PERSON per2 ON per2.PERSON_NBR  = mar.SERVICE_PERSON_NBR 
				LEFT JOIN ADMIN.CF_APPLICATION_TYPE typ ON typ.APPL_TYP = mar.APPL_TYP
				LEFT JOIN ADMIN.IP_LOGO logo ON logo.FILE_NBR = mar.FILE_NBR
				LEFT JOIN ADMIN.CF_ACTION_TYPE desact ON desact.ACTION_TYP = act.ACTION_TYP 
				LEFT JOIN ADMIN.IP_MARK_NICE_CLASSES cldes ON cldes.FILE_NBR = mar.FILE_NBR
				LEFT JOIN ADMIN.IP_USER usu1 ON usu1.USER_ID = mar.CAPTURE_USER_ID 
				LEFT JOIN ADMIN.IP_USER usu ON usu.USER_ID = act.CAPTURE_USER_ID and usu.USER_ID = AUTHORISING_USER_ID
				WHERE mar.FILE_NBR = {} AND     (act.ACTION_TYP = '549' or act.ACTION_TYP = '550' or act.ACTION_TYP = '560') AND act.IND_DELETED IS NULL
			'''.format(exp),

		"arg1":{
			"sqlColumnList":[
				{"sqlColumnType": "String", "sqlColumnValue":"FILE_NBR"},
				{"sqlColumnType": "String", "sqlColumnValue":"PROC_NBR"},
				{"sqlColumnType": "String", "sqlColumnValue":"FILING_DATE"},
				{"sqlColumnType": "String", "sqlColumnValue":"APPL_TYPE_NAME"},
				{"sqlColumnType": "String", "sqlColumnValue":"SIGN_WCODE"},
				{"sqlColumnType": "String", "sqlColumnValue":"NICE_CLASS_TXT"},
				{"sqlColumnType": "String", "sqlColumnValue":"MARK_NAME"},
				{"sqlColumnType": "String", "sqlColumnValue":"PERSON_NAME"},
				{"sqlColumnType": "String", "sqlColumnValue":"ADDR_STREET"},
				{"sqlColumnType": "String", "sqlColumnValue":"AGENT_CODE"},
				{"sqlColumnType": "String", "sqlColumnValue":"PERSON_NAME2"},
				{"sqlColumnType": "String", "sqlColumnValue":"LOGO_DATA"},
				{"sqlColumnType": "String", "sqlColumnValue":"ACTION_DATE"},
				{"sqlColumnType": "String", "sqlColumnValue":"ACTION_TYP"},
				{"sqlColumnType": "String", "sqlColumnValue":"ACTION_TYPE_NAME"},
				{"sqlColumnType": "String", "sqlColumnValue":"NICE_CLASS_DESCRIPTION"},
				{"sqlColumnType": "String", "sqlColumnValue":"USER_NAME"},
				{"sqlColumnType": "String", "sqlColumnValue":"uslog"},
				{"sqlColumnType": "String", "sqlColumnValue":"USER_ID"}
			]
		}
	}
	return(clientMark.service.SqlFetchAll(**query_sqls))    

def Fech_All_Exp_titulares(exp):
	query_sqls = {
		"arg0":'''
					select rtrim(ip1.PERSON_NAME) as res, ltrim(dir.ADDR_STREET)  as dir, dir.RESIDENCE_COUNTRY_CODE, pais.COUNTRY_NAME 
					from ADMIN.IP_PERSON ip1 
					left join ADMIN.IP_PERSON_ADDRESSES dir on dir.PERSON_NBR = ip1.PERSON_NBR  
					left join ADMIN.IP_MARK_OWNERS ip2 on ip2.PERSON_NBR = ip1.PERSON_NBR and ip2.ADDR_NBR = dir.ADDR_NBR  
					left join ADMIN.CF_GEO_COUNTRY pais on pais.COUNTRY_CODE = dir.RESIDENCE_COUNTRY_CODE
					where ip2.FILE_NBR = {}
			'''.format(exp),

		"arg1":{
			"sqlColumnList":[
				{"sqlColumnType": "String", "sqlColumnValue":"res"},
				{"sqlColumnType": "String", "sqlColumnValue":"dir"},
				{"sqlColumnType": "String", "sqlColumnValue":"RESIDENCE_COUNTRY_CODE"},
				{"sqlColumnType": "String", "sqlColumnValue":"COUNTRY_NAME"},
			]
		}
	}
	return(clientMark.service.SqlFetchAll(**query_sqls))  

def Fech_All_Exp_pais():
	query_sqls_pais = {
		"arg0":'''select COD_PAIS,NOM_PAIS from ADMIN.PAIS pais ''',

		"arg1":{
			"sqlColumnList":[
				{"sqlColumnType": "String", "sqlColumnValue":"COD_PAIS"},
				{"sqlColumnType": "String", "sqlColumnValue":"NOM_PAIS"},
			]
		}
	}
	return(clientMark.service.SqlFetchAll(**query_sqls_pais))

def Fech_All_Exp_pais_code(code):
	query_sqls_pais = {
		"arg0":"select COD_PAIS,NOM_PAIS from ADMIN.PAIS pais WHERE COD_PAIS = '"+code+"' ",

		"arg1":{
			"sqlColumnList":[
				{"sqlColumnType": "String", "sqlColumnValue":"COD_PAIS"},
				{"sqlColumnType": "String", "sqlColumnValue":"NOM_PAIS"},
			]
		}
	}
	return(clientMark.service.SqlFetchAll(**query_sqls_pais))

#FetchAll consulta lista tipo documento 
def Fech_All_tipo_doc():
	res = []
	try:
		FechAlltipodoc = {
			"arg0":'''SELECT TD.USERDOC_TYP,TD.USERDOC_NAME FROM CF_USERDOC_TYPE TD ORDER BY TD.USERDOC_TYP ''',

			"arg1":{
				"sqlColumnList":[
					{"sqlColumnType": "String", "sqlColumnValue":"USERDOC_TYP"},
					{"sqlColumnType": "String", "sqlColumnValue":"USERDOC_NAME"},
				]
			}
		}
		data = clientMark.service.SqlFetchAll(**FechAlltipodoc)
		for i in range(0,len(data)):
			res.append({
						"code":data[i].sqlColumnList[0].sqlColumnValue,
						"desc":data[i].sqlColumnList[1].sqlColumnValue
						})
		return(res)
	except Exception as e:
		pass

#////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Agente por codilgo Marcas
def personAgente(agent):
	agentCode = {"arg0": {"agentCode": {"doubleValue": str(agent)}}}
	return clientMark.service.PersonGetList(**agentCode)
#Agente por codilgo Patente
def personAgentePatent(agent):
	agentCode = {"arg0": {"agentCode": {"doubleValue": str(agent)}}}
	return clientPatents.service.PersonGetList(**agentCode)
#Agente por codilgo Diseño
def personAgenteDisenio(agent):
	agentCode = {"arg0": {"agentCode": {"doubleValue": str(agent)}}}
	return clientDisenio.service.PersonGetList(**agentCode)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Titular por nombre Marcas
def personTitular(nombre):
	data=[]
	nombre = { "arg0": { "personNameContainsWords": str(nombre) }}
	res = clientMark.service.PersonGetList(**nombre)
	for i in range(0,len(res)):
		data.append({
			"addressStreet": str(res[i].addressStreet).replace("'","\'"),
			"addressStreetInOtherLang": str(res[i].addressStreetInOtherLang).replace("'","\'"),
			"addressZone": str(res[i].addressZone).replace("'","\'"),
			"agentCode": "",
			"cityCode": str(res[i].cityCode).replace("'","\'"),
			"cityName": str(res[i].cityName).replace("'","\'"),
			"companyRegisterRegistrationDate": str(res[i].companyRegisterRegistrationDate).replace("'","\'"),
			"companyRegisterRegistrationNbr": str(res[i].companyRegisterRegistrationNbr).replace("'","\'"),
			"email": str(res[i].email).replace("'","\'"),
			"indCompany": str(res[i].indCompany).replace("'","\'").replace("False","false").replace("True","true"),
			"individualIdNbr": str(res[i].individualIdNbr).replace("'","\'"),
			"individualIdType": str(res[i].individualIdType).replace("'","\'"),
			"legalIdNbr": str(res[i].legalIdNbr).replace("'","\'"),
			"legalIdType": str(res[i].legalIdType).replace("'","\'"),
			"legalNature": str(res[i].legalNature).replace("'","\'"),
			"legalNatureInOtherLang": str(res[i].legalNatureInOtherLang).replace("'","\'"),
			"nationalityCountryCode": str(res[i].nationalityCountryCode).replace("'","\'"),
			"personGroupCode": str(res[i].personGroupCode).replace("'","\'"),
			"personGroupName": str(res[i].personGroupName).replace("'","\'"),
			"personName": str(res[i].personName).replace("'","\'"),
			"personNameInOtherLang": str(res[i].personNameInOtherLang).replace("'","\'"),
			"residenceCountryCode": str(res[i].residenceCountryCode).replace("'","\'"),
			"stateCode": str(res[i].stateCode).replace("'","\'"),
			"stateName": str(res[i].stateName).replace("'","\'"),
			"telephone": str(res[i].telephone).replace("'","\'"),
			"zipCode": str(res[i].zipCode).replace("'","\'")
		})
	return data
#Titular por nombre Patentes
def personTitularPatent(nombre):
	data=[]
	nombre = { "arg0": { "personNameContainsWords": str(nombre) }}	
	res = clientPatents.service.PersonGetList(**nombre)
	for i in range(0,len(res)):
		data.append({
			"addressStreet": str(res[i].addressStreet).replace("'","\'"),
			"addressStreetInOtherLang": str(res[i].addressStreetInOtherLang).replace("'","\'"),
			"addressZone": str(res[i].addressZone).replace("'","\'"),
			"agentCode": "",
			"cityCode": str(res[i].cityCode).replace("'","\'"),
			"cityName": str(res[i].cityName).replace("'","\'"),
			"companyRegisterRegistrationDate": str(res[i].companyRegisterRegistrationDate).replace("'","\'"),
			"companyRegisterRegistrationNbr": str(res[i].companyRegisterRegistrationNbr).replace("'","\'"),
			"email": str(res[i].email).replace("'","\'"),
			"indCompany": str(res[i].indCompany).replace("'","\'").replace("False","false").replace("True","true"),
			"individualIdNbr": str(res[i].individualIdNbr).replace("'","\'"),
			"individualIdType": str(res[i].individualIdType).replace("'","\'"),
			"legalIdNbr": str(res[i].legalIdNbr).replace("'","\'"),
			"legalIdType": str(res[i].legalIdType).replace("'","\'"),
			"legalNature": str(res[i].legalNature).replace("'","\'"),
			"legalNatureInOtherLang": str(res[i].legalNatureInOtherLang).replace("'","\'"),
			"nationalityCountryCode": str(res[i].nationalityCountryCode).replace("'","\'"),
			"personGroupCode": str(res[i].personGroupCode).replace("'","\'"),
			"personGroupName": str(res[i].personGroupName).replace("'","\'"),
			"personName": str(res[i].personName).replace("'","\'"),
			"personNameInOtherLang": str(res[i].personNameInOtherLang).replace("'","\'"),
			"residenceCountryCode": str(res[i].residenceCountryCode).replace("'","\'"),
			"stateCode": str(res[i].stateCode).replace("'","\'"),
			"stateName": str(res[i].stateName).replace("'","\'"),
			"telephone": str(res[i].telephone).replace("'","\'"),
			"zipCode": str(res[i].zipCode).replace("'","\'")
		})
	return data
#Titular por nombre Diseño
def personTitularDisenio(nombre):
	data=[]
	nombre = { "arg0": { "personNameContainsWords": str(nombre) }}	
	res = clientDisenio.service.PersonGetList(**nombre)
	for i in range(0,len(res)):
		data.append({
			"addressStreet": str(res[i].addressStreet).replace("'","\'"),
			"addressStreetInOtherLang": str(res[i].addressStreetInOtherLang).replace("'","\'"),
			"addressZone": str(res[i].addressZone).replace("'","\'"),
			"agentCode": "",
			"cityCode": str(res[i].cityCode).replace("'","\'"),
			"cityName": str(res[i].cityName).replace("'","\'"),
			"companyRegisterRegistrationDate": str(res[i].companyRegisterRegistrationDate).replace("'","\'"),
			"companyRegisterRegistrationNbr": str(res[i].companyRegisterRegistrationNbr).replace("'","\'"),
			"email": str(res[i].email).replace("'","\'"),
			"indCompany": str(res[i].indCompany).replace("'","\'").replace("False","false").replace("True","true"),
			"individualIdNbr": str(res[i].individualIdNbr).replace("'","\'"),
			"individualIdType": str(res[i].individualIdType).replace("'","\'"),
			"legalIdNbr": str(res[i].legalIdNbr).replace("'","\'"),
			"legalIdType": str(res[i].legalIdType).replace("'","\'"),
			"legalNature": str(res[i].legalNature).replace("'","\'"),
			"legalNatureInOtherLang": str(res[i].legalNatureInOtherLang).replace("'","\'"),
			"nationalityCountryCode": str(res[i].nationalityCountryCode).replace("'","\'"),
			"personGroupCode": str(res[i].personGroupCode).replace("'","\'"),
			"personGroupName": str(res[i].personGroupName).replace("'","\'"),
			"personName": str(res[i].personName).replace("'","\'"),
			"personNameInOtherLang": str(res[i].personNameInOtherLang).replace("'","\'"),
			"residenceCountryCode": str(res[i].residenceCountryCode).replace("'","\'"),
			"stateCode": str(res[i].stateCode).replace("'","\'"),
			"stateName": str(res[i].stateName).replace("'","\'"),
			"telephone": str(res[i].telephone).replace("'","\'"),
			"zipCode": str(res[i].zipCode).replace("'","\'")
		})
	return data
#////////////////////////////////////////////////////////////////////////////////////////////////////////////

#UserDocGetList por fecha (Marcas)
def user_doc_getlist_fecha(filingDateFrom,filingDateTo):
	udgf = {
			"arg0": {
				"criteriaUserdocFilingData": {
				"filingDateFrom": {
					"dateValue": filingDateFrom+"T00:00:00-04:00"
				},
				"filingDateTo": {
					"dateValue": filingDateTo+"T23:59:59-04:00"
				}
				}
			}
			}
	return clientMark.service.UserdocGetList(**udgf)

#Documento
def office_doc_read():
	params = {"arg0": {"offidocNbr": {"doubleValue": 51014},
						"offidocOrigin": 1,
						"offidocSeries": {"doubleValue": 2022},
						"selected": ""}
						}
	return(clientMark.service.OfficedocRead(**params))

def mark_insert_reg(
					fileId_fileId_fileNbr,
					file_fileId_fileSeq,
					file_fileId_fileSeries,
					file_fileId_fileType,
					file_filingData_applicationSubtype,
					file_filingData_applicationType,
					file_filingData_captureUserId,
					file_filingData_filingDate,
					file_filingData_captureDate,
					file_filingData_lawCode,
					file_filingData_paymentList_currencyType,
					file_filingData_paymentList_receiptAmount,
					file_filingData_paymentList_receiptDate,
					file_filingData_paymentList_receiptNbr,
					file_filingData_paymentList_receiptNotes,
					file_filingData_paymentList_receiptType,
					file_filingData_receptionUserId,
					file_ownershipData_ownerList_person_telephone,
					file_ownershipData_ownerList_person_zipCode, 
					file_ownershipData_ownerList_person_email, 
					file_ownershipData_ownerList_person_individualIdType, 
					file_ownershipData_ownerList_person_individualIdNbr, 
					file_ownershipData_ownerList_person_legalIdType, 
					file_ownershipData_ownerList_person_legalIdNbr, 
					file_ownershipData_ownerList_person_cityName, 
					file_ownershipData_ownerList_person_addressZone,
					file_ownershipData_ownerList_person_addressStreet,
					file_ownershipData_ownerList_person_nationalityCountryCode,
					file_ownershipData_ownerList_person_personName,
					file_ownershipData_ownerList_person_residenceCountryCode,
					file_rowVersion,
					agentCode,
					file_representationData_representativeList_representativeType,
					rowVersion,
					protectionData_dummy,
					protectionData_niceClassList_niceClassDescription,
					protectionData_niceClassList_niceClassDetailedStatus,
					protectionData_niceClassList_niceClassEdition,
					protectionData_niceClassList_niceClassGlobalStatus,
					protectionData_niceClassList_niceClassNbr,
					protectionData_niceClassList_niceClassVersion,
					documentId_PowerOfAttorneyRegister_docLog,
					documentId_PowerOfAttorneyRegister_docNbr,
					documentId_PowerOfAttorneyRegister_docOrigin,
					documentId_PowerOfAttorneyRegister_docSeries,
					limitationData_disclaimer,
					logoData,
					logoType,
					logo_colourDescription,
					signData_markName,
					signData_signType,
					ownerList):
  try:
    logo = logoData
    if ownerList == "":
      markinsertreg = { 
      'arg0': {
        'file': {
          'fileId': {
            'fileNbr': {
            'doubleValue': fileId_fileId_fileNbr
            },
            'fileSeq': file_fileId_fileSeq,
            'fileSeries': {
            'doubleValue': file_fileId_fileSeries,
            },
            'fileType': file_fileId_fileType
          },
          'filingData': {
            'applicationSubtype': file_filingData_applicationSubtype,
            'applicationType': file_filingData_applicationType,
            'captureUserId': {
            'doubleValue': file_filingData_captureUserId
            },
            'filingDate': {
            'dateValue': file_filingData_filingDate    ########################################
            },
            'captureDate': {
              'dateValue': file_filingData_captureDate  ################### problemas con fecha futura
            },
            'lawCode': {
            'doubleValue': file_filingData_lawCode
            },
            'paymentList': {
            'currencyType': file_filingData_paymentList_currencyType,
            'receiptAmount': file_filingData_paymentList_receiptAmount,
            'receiptDate': {
              'dateValue': file_filingData_paymentList_receiptDate
            },
            'receiptNbr': file_filingData_paymentList_receiptNbr,
            'receiptNotes': file_filingData_paymentList_receiptNotes,
            'receiptType': file_filingData_paymentList_receiptType
            },
            'receptionUserId': {
            'doubleValue': file_filingData_receptionUserId
            },
              "receptionDocument": {
                "documentId": {
                "docLog": "E",
                "docNbr": {
                  "doubleValue": ""
                },
                "docOrigin": str(connex.MEA_SFE_FORMULARIOS_ID_Origin),
                "docSeries": {
                  "doubleValue": file_fileId_fileSeries
                },
                "selected": ""
                },
                "documentSeqId": {
                "docSeqName": "",
                "docSeqNbr": {
                  "doubleValue": ""
                },
                "docSeqSeries": {
                  "doubleValue": file_fileId_fileSeries
                },
              "docSeqType": ""
            }
          }
        },
          'ownershipData': {
            'ownerList': {
              'person': {
						'telephone': file_ownershipData_ownerList_person_telephone, 
						'zipCode': file_ownershipData_ownerList_person_zipCode, 
						'email': file_ownershipData_ownerList_person_email, 
						'individualIdType': file_ownershipData_ownerList_person_individualIdType, 
						'individualIdNbr': file_ownershipData_ownerList_person_individualIdNbr, 
						'legalIdType': file_ownershipData_ownerList_person_legalIdType, 
						'legalIdNbr': file_ownershipData_ownerList_person_legalIdNbr, 
						'cityName': file_ownershipData_ownerList_person_cityName, 
						'addressZone': file_ownershipData_ownerList_person_addressZone,
						'addressStreet': file_ownershipData_ownerList_person_addressStreet,
						'nationalityCountryCode': file_ownershipData_ownerList_person_nationalityCountryCode,
						'personName': file_ownershipData_ownerList_person_personName,
						'residenceCountryCode': file_ownershipData_ownerList_person_residenceCountryCode
					},
            },
     
          },
          'representationData': {
			"documentId_PowerOfAttorneyRegister": {
				"docLog": documentId_PowerOfAttorneyRegister_docLog,
				"docNbr": {
				"doubleValue": documentId_PowerOfAttorneyRegister_docNbr
				},
				"docOrigin": documentId_PowerOfAttorneyRegister_docOrigin,
				"docSeries": {
				"doubleValue": documentId_PowerOfAttorneyRegister_docSeries
				},
				"selected": ""
			},
            'representativeList': {
            'indService': "",
                'person': {
                    'addressStreet': str(personAgente(agentCode)[0].addressStreet).replace("None",""),
                    'addressStreetInOtherLang': str(personAgente(agentCode)[0].addressStreetInOtherLang).replace("None",""),
                    'addressZone': str(personAgente(agentCode)[0].addressZone).replace("None",""),
                    'agentCode': {
                    'doubleValue':str(personAgente(agentCode)[0].agentCode.doubleValue).replace("None","")
                    },
                    'cityCode': str(personAgente(agentCode)[0].cityCode).replace("None",""),
                    'cityName': str(personAgente(agentCode)[0].cityName).replace("None",""),
                    'companyRegisterRegistrationDate': str(personAgente(agentCode)[0].companyRegisterRegistrationDate).replace("None",""),
                    'companyRegisterRegistrationNbr': str(personAgente(agentCode)[0].companyRegisterRegistrationNbr).replace("None",""),
                    'email': str(personAgente(agentCode)[0].email).replace("None",""),
                    'indCompany': str(personAgente(str(agentCode))[0].indCompany),
                    'individualIdNbr': str(personAgente(agentCode)[0].individualIdNbr).replace("None",""),
                    'individualIdType': str(personAgente(agentCode)[0].individualIdType).replace("None",""),
                    'legalIdNbr': str(personAgente(agentCode)[0].legalIdNbr).replace("None",""),
                    'legalIdType': str(personAgente(agentCode)[0].legalIdType).replace("None",""),
                    'legalNature': str(personAgente(agentCode)[0].legalNature).replace("None",""),
                    'legalNatureInOtherLang': str(personAgente(agentCode)[0].legalNatureInOtherLang).replace("None",""),
                    'nationalityCountryCode': str(personAgente(agentCode)[0].nationalityCountryCode).replace("None",""),
                    'personGroupCode': "",
                    'personGroupName': str(personAgente(agentCode)[0].personGroupName).replace("None",""),
                    'personName': str(personAgente(agentCode)[0].personName).replace("None",""),
                    'personNameInOtherLang': str(personAgente(agentCode)[0].personNameInOtherLang).replace("None",""),
                    'residenceCountryCode': str(personAgente(agentCode)[0].residenceCountryCode).replace("None",""),
                    'stateCode': str(personAgente(agentCode)[0].stateCode).replace("None",""),
                    'stateName': str(personAgente(agentCode)[0].stateName).replace("None",""),
                    'telephone': str(personAgente(agentCode)[0].telephone).replace("None",""),
                    'zipCode': str(personAgente(agentCode)[0].zipCode).replace("None","")
                    },
            'representativeType': file_representationData_representativeList_representativeType
            }
          },
          'rowVersion': {
            'doubleValue': file_rowVersion
          }
        },
		"limitationData": {
			"byConsent": "not data",
			"disclaimer": limitationData_disclaimer,
			"disclaimerInOtherLang": "not data",
			"regulations": "not data"
		},		
        'protectionData': {
          'dummy': protectionData_dummy,
          'niceClassList': {
            'niceClassDescription': protectionData_niceClassList_niceClassDescription,
            'niceClassDetailedStatus': protectionData_niceClassList_niceClassDetailedStatus,
            'niceClassEdition': {
            'doubleValue': protectionData_niceClassList_niceClassEdition
            },
            'niceClassGlobalStatus': protectionData_niceClassList_niceClassGlobalStatus,
            'niceClassNbr': {
            'doubleValue': protectionData_niceClassList_niceClassNbr
            },
            'niceClassVersion': protectionData_niceClassList_niceClassVersion
          }
        },
        'rowVersion': {
          'doubleValue': rowVersion
        },
        'signData': {
          'logo': {
              'colourDescription': logo_colourDescription,
              'colourDescriptionInOtherLang': '',
              'logoData':base64.b64decode(logo),  #Convertir cadena en bytes
              'logoType': logoType,
            },
          'markName': signData_markName,
          'signType': signData_signType
        }
      } }
    else:
      markinsertreg = { 
      'arg0': {
        'file': {
          'fileId': {
            'fileNbr': {
            'doubleValue': fileId_fileId_fileNbr
            },
            'fileSeq': file_fileId_fileSeq,
            'fileSeries': {
            'doubleValue': file_fileId_fileSeries,
            },
            'fileType': file_fileId_fileType
          },
          'filingData': {
            'applicationSubtype': file_filingData_applicationSubtype,
            'applicationType': file_filingData_applicationType,
            'captureUserId': {
            'doubleValue': file_filingData_captureUserId
            },
            'filingDate': {
            'dateValue': file_filingData_filingDate    ########################################
            },
            'captureDate': {
              'dateValue': file_filingData_captureDate  ################### problemas con fecha futura
            },
            'lawCode': {
            'doubleValue': file_filingData_lawCode
            },
            'paymentList': {
            'currencyType': file_filingData_paymentList_currencyType,
            'receiptAmount': file_filingData_paymentList_receiptAmount,
            'receiptDate': {
              'dateValue': file_filingData_paymentList_receiptDate
            },
            'receiptNbr': file_filingData_paymentList_receiptNbr,
            'receiptNotes': file_filingData_paymentList_receiptNotes,
            'receiptType': file_filingData_paymentList_receiptType
            },
            'receptionUserId': {
            'doubleValue': file_filingData_receptionUserId
            },              
            "receptionDocument": {
                "documentId": {
                "docLog": "E",
                "docNbr": {
                  "doubleValue": ""
                },
                "docOrigin": str(connex.MEA_SFE_FORMULARIOS_ID_Origin),
                "docSeries": {
                  "doubleValue": file_fileId_fileSeries
                },
                "selected": ""
                },
                "documentSeqId": {
                "docSeqName": "",
                "docSeqNbr": {
                  "doubleValue": ""
                },
                "docSeqSeries": {
                  "doubleValue": file_fileId_fileSeries
                },
              "docSeqType": ""
            }
          }
          },
          'ownershipData': {
            'ownerList': {
              'person': {
                'addressStreet': file_ownershipData_ownerList_person_addressStreet,
                'nationalityCountryCode': file_ownershipData_ownerList_person_nationalityCountryCode,
                'personName': file_ownershipData_ownerList_person_personName,
                'residenceCountryCode': file_ownershipData_ownerList_person_residenceCountryCode
              },
              
              
            },
            "ownerList": ownerList
   
          },
          'representationData': {
				"documentId_PowerOfAttorneyRegister": {
					"docLog": documentId_PowerOfAttorneyRegister_docLog,
					"docNbr": {
					"doubleValue": documentId_PowerOfAttorneyRegister_docNbr
					},
					"docOrigin": documentId_PowerOfAttorneyRegister_docOrigin,
					"docSeries": {
					"doubleValue": documentId_PowerOfAttorneyRegister_docSeries
					},
					"selected": ""
				},			  
            'representativeList': {
            'indService': "",
                'person': {
                    'addressStreet': str(personAgente(agentCode)[0].addressStreet).replace("None",""),
                    'addressStreetInOtherLang': str(personAgente(agentCode)[0].addressStreetInOtherLang).replace("None",""),
                    'addressZone': str(personAgente(agentCode)[0].addressZone).replace("None",""),
                    'agentCode': {
                    'doubleValue':str(personAgente(agentCode)[0].agentCode.doubleValue).replace("None","")
                    },
                    'cityCode': str(personAgente(agentCode)[0].cityCode).replace("None",""),
                    'cityName': str(personAgente(agentCode)[0].cityName).replace("None",""),
                    'companyRegisterRegistrationDate': str(personAgente(agentCode)[0].companyRegisterRegistrationDate).replace("None",""),
                    'companyRegisterRegistrationNbr': str(personAgente(agentCode)[0].companyRegisterRegistrationNbr).replace("None",""),
                    'email': str(personAgente(agentCode)[0].email).replace("None",""),
                    'indCompany': str(personAgente(str(agentCode))[0].indCompany),
                    'individualIdNbr': str(personAgente(agentCode)[0].individualIdNbr).replace("None",""),
                    'individualIdType': str(personAgente(agentCode)[0].individualIdType).replace("None",""),
                    'legalIdNbr': str(personAgente(agentCode)[0].legalIdNbr).replace("None",""),
                    'legalIdType': str(personAgente(agentCode)[0].legalIdType).replace("None",""),
                    'legalNature': str(personAgente(agentCode)[0].legalNature).replace("None",""),
                    'legalNatureInOtherLang': str(personAgente(agentCode)[0].legalNatureInOtherLang).replace("None",""),
                    'nationalityCountryCode': str(personAgente(agentCode)[0].nationalityCountryCode).replace("None",""),
                    'personGroupCode': "",
                    'personGroupName': str(personAgente(agentCode)[0].personGroupName).replace("None",""),
                    'personName': str(personAgente(agentCode)[0].personName).replace("None",""),
                    'personNameInOtherLang': str(personAgente(agentCode)[0].personNameInOtherLang).replace("None",""),
                    'residenceCountryCode': str(personAgente(agentCode)[0].residenceCountryCode).replace("None",""),
                    'stateCode': str(personAgente(agentCode)[0].stateCode).replace("None",""),
                    'stateName': str(personAgente(agentCode)[0].stateName).replace("None",""),
                    'telephone': str(personAgente(agentCode)[0].telephone).replace("None",""),
                    'zipCode': str(personAgente(agentCode)[0].zipCode).replace("None","")
                    },
            'representativeType': file_representationData_representativeList_representativeType
            }
          },
          'rowVersion': {
            'doubleValue': file_rowVersion
          }
        },
		"limitationData": {
			"byConsent": "not data",
			"disclaimer": limitationData_disclaimer,
			"disclaimerInOtherLang": "not data",
			"regulations": "not data"
		},		
        'protectionData': {
          'dummy': protectionData_dummy,
          'niceClassList': {
            'niceClassDescription': protectionData_niceClassList_niceClassDescription,
            'niceClassDetailedStatus': protectionData_niceClassList_niceClassDetailedStatus,
            'niceClassEdition': {
            'doubleValue': protectionData_niceClassList_niceClassEdition
            },
            'niceClassGlobalStatus': protectionData_niceClassList_niceClassGlobalStatus,
            'niceClassNbr': {
            'doubleValue': protectionData_niceClassList_niceClassNbr
            },
            'niceClassVersion': protectionData_niceClassList_niceClassVersion
          }
        },
        'rowVersion': {
          'doubleValue': rowVersion
        },
        'signData': {
          'logo': {
              'colourDescription': logo_colourDescription,
              'colourDescriptionInOtherLang': '',
              'logoData':base64.b64decode(logo),  #Convertir cadena en bytes
              'logoType': logoType,
            },
          'markName': signData_markName,
          'signType': signData_signType
        }
      } }
    clientMark.service.MarkInsert(**markinsertreg)
    return "true"
  except zeep.exceptions.Fault as e:
    return(str(e))
		
def mark_insert_ren(
					file_fileId_fileNbr,
					file_fileId_fileSeq,
					file_fileId_fileSeries,
					file_fileId_fileType,
					file_filingData_applicationSubtype,
					file_filingData_applicationType,
					file_filingData_captureUserId,
					file_filingData_captureDate,
					file_filingData_filingDate,
					file_filingData_lawCode,
					file_filingData_paymentList_currencyType,
					file_filingData_paymentList_receiptAmount,
					file_filingData_paymentList_receiptDate,
					file_filingData_paymentList_receiptNbr,
					file_filingData_paymentList_receiptNotes,
					file_filingData_paymentList_receiptType,
					file_filingData_receptionUserId,
					file_ownershipData_ownerList_person_owneraddressStreet,
					file_ownershipData_ownerList_person_ownernationalityCountryCode,
					file_ownershipData_ownerList_person_ownerpersonName,
					file_ownershipData_ownerList_person_ownerresidenceCountryCode,
					file_representationData_representativeList_representativeType,
					agentCode,
					file_relationshipList_fileId_fileNbr,
					file_relationshipList_fileId_fileSeq,
					file_relationshipList_fileId_fileSeries,
					file_relationshipList_fileId_fileType,
					file_relationshipList_relationshipRole,
					file_relationshipList_relationshipType,
					file_rowVersion,
					protectionData_dummy,
					protectionData_niceClassList_niceClassDescription,
					protectionData_niceClassList_niceClassDetailedStatus,
					protectionData_niceClassList_niceClassEdition,
					protectionData_niceClassList_niceClassGlobalStatus,
					protectionData_niceClassList_niceClassNbr,
					protectionData_niceClassList_niceClassVersion,
					rowVersion,
					logoData,
					logoType,
					signData_markName,
					signData_signType):
	try:
		logo = logoData
		markinsertren = { 
			'arg0': {
				'file': {
					'fileId': {
						'fileNbr': {
						'doubleValue': file_fileId_fileNbr
						},
						'fileSeq': file_fileId_fileSeq,
						'fileSeries': {
						'doubleValue': file_fileId_fileSeries,
						},
						'fileType': file_fileId_fileType
					},
					'filingData': {
						'applicationSubtype': file_filingData_applicationSubtype,
						'applicationType': file_filingData_applicationType,
						'captureUserId': {
						'doubleValue': file_filingData_captureUserId
						},
						'captureDate': {
							'dateValue': file_filingData_captureDate
						},
						'filingDate': {
						'dateValue': file_filingData_filingDate
						},
						'lawCode': {
						'doubleValue': file_filingData_lawCode
						},
						'paymentList': {
						'currencyType': file_filingData_paymentList_currencyType,
						'receiptAmount': file_filingData_paymentList_receiptAmount,
						'receiptDate': {
							'dateValue': file_filingData_paymentList_receiptDate
						},
						'receiptNbr': file_filingData_paymentList_receiptNbr,
						'receiptNotes': file_filingData_paymentList_receiptNotes,
						'receiptType': file_filingData_paymentList_receiptType
						},
						'receptionUserId': {
							'doubleValue': file_filingData_receptionUserId
						},
						"receptionDocument": {
								"documentId": {
								"docLog": "E",
								"docNbr": {
									"doubleValue": ""
								},
								"docOrigin": str(connex.MEA_SFE_FORMULARIOS_ID_Origin),
								"docSeries": {
									"doubleValue": file_fileId_fileSeries
								},
								"selected": ""
								},
								"documentSeqId": {
								"docSeqName": "",
								"docSeqNbr": {
									"doubleValue": ""
								},
								"docSeqSeries": {
									"doubleValue": file_fileId_fileSeries
								},
							"docSeqType": ""
						}
					}
					},
					'ownershipData': {
						'ownerList': {
							'person': {
								'addressStreet': file_ownershipData_ownerList_person_owneraddressStreet,
								'nationalityCountryCode': file_ownershipData_ownerList_person_ownernationalityCountryCode,
								'personName': file_ownershipData_ownerList_person_ownerpersonName,
								'residenceCountryCode': file_ownershipData_ownerList_person_ownerresidenceCountryCode
							}
						}
					},
					'representationData': {
						'representativeList': {
						'indService': '',
						'person': {
								'addressStreet': str(personAgente(agentCode)[0].addressStreet).replace("None",""),
								'addressStreetInOtherLang': str(personAgente(agentCode)[0].addressStreetInOtherLang).replace("None",""),
								'addressZone': str(personAgente(agentCode)[0].addressZone).replace("None",""),
								'agentCode': {
								'doubleValue':str(personAgente(agentCode)[0].agentCode.doubleValue).replace("None","")
								},
								'cityCode': str(personAgente(agentCode)[0].cityCode).replace("None",""),
								'cityName': str(personAgente(agentCode)[0].cityName).replace("None",""),
								'companyRegisterRegistrationDate': str(personAgente(agentCode)[0].companyRegisterRegistrationDate).replace("None",""),
								'companyRegisterRegistrationNbr': str(personAgente(agentCode)[0].companyRegisterRegistrationNbr).replace("None",""),
								'email': str(personAgente(agentCode)[0].email).replace("None",""),
								'indCompany': str(personAgente(str(agentCode))[0].indCompany),
								'individualIdNbr': str(personAgente(agentCode)[0].individualIdNbr).replace("None",""),
								'individualIdType': str(personAgente(agentCode)[0].individualIdType).replace("None",""),
								'legalIdNbr': str(personAgente(agentCode)[0].legalIdNbr).replace("None",""),
								'legalIdType': str(personAgente(agentCode)[0].legalIdType).replace("None",""),
								'legalNature': str(personAgente(agentCode)[0].legalNature).replace("None",""),
								'legalNatureInOtherLang': str(personAgente(agentCode)[0].legalNatureInOtherLang).replace("None",""),
								'nationalityCountryCode': str(personAgente(agentCode)[0].nationalityCountryCode).replace("None",""),
								'personGroupCode': "",
								'personGroupName': str(personAgente(agentCode)[0].personGroupName).replace("None",""),
								'personName': str(personAgente(agentCode)[0].personName).replace("None",""),
								'personNameInOtherLang': str(personAgente(agentCode)[0].personNameInOtherLang).replace("None",""),
								'residenceCountryCode': str(personAgente(agentCode)[0].residenceCountryCode).replace("None",""),
								'stateCode': str(personAgente(agentCode)[0].stateCode).replace("None",""),
								'stateName': str(personAgente(agentCode)[0].stateName).replace("None",""),
								'telephone': str(personAgente(agentCode)[0].telephone).replace("None",""),
								'zipCode': str(personAgente(agentCode)[0].zipCode).replace("None","")
								},
						'representativeType': file_representationData_representativeList_representativeType
						}
					},
					"relationshipList":{
						'fileId': {
							'fileNbr': {
								'doubleValue': file_relationshipList_fileId_fileNbr
							},
							'fileSeq': file_relationshipList_fileId_fileSeq,
							'fileSeries': {
								'doubleValue': file_relationshipList_fileId_fileSeries,
							},
							'fileType': file_relationshipList_fileId_fileType
						},
						'relationshipRole': file_relationshipList_relationshipRole,
						'relationshipType': file_relationshipList_relationshipType
					},
					'rowVersion': {
						'doubleValue': file_rowVersion
					}
				},
				'protectionData': {
					'dummy': protectionData_dummy,
					'niceClassList': {
						'niceClassDescription': protectionData_niceClassList_niceClassDescription,
						'niceClassDetailedStatus': protectionData_niceClassList_niceClassDetailedStatus,
						'niceClassEdition': {
							'doubleValue': protectionData_niceClassList_niceClassEdition
						},
						'niceClassGlobalStatus': protectionData_niceClassList_niceClassGlobalStatus,
						'niceClassNbr': {
							'doubleValue': protectionData_niceClassList_niceClassNbr
						},
						'niceClassVersion': protectionData_niceClassList_niceClassVersion
					}
				},
				'rowVersion': {
					'doubleValue': rowVersion
				},
				'signData': {
					'logo': {
						'logoData':base64.b64decode(logo), #Convertir cadena en bytes
						'logoType': logoType
					},
					'markName': signData_markName,
					'signType': signData_signType
				}
			} }
		clientMark.service.MarkInsert(**markinsertren)
		return "true"
	except zeep.exceptions.Fault as e:
		return(str(e))

#insert IPAS
def Insert_Action(exp,pago,userid,nota,evento): # {"exp":"","pago":"","userid":"","nota":"","evento":"554","inicio":"","fin":""}
	try:
		today = date.today()#Día actual
		today_date = date.today()
		td = timedelta(3) # tres dias adelante
		pub_tres = today_date + td
		td_mañana = timedelta(1) # Fecha mañana inicio 
		pub_uno = today + td_mañana
		inicio = ''
		fin = ''
		f_inicio = ''
		f_fin = ''

		ultimo = int(len(mark_getlist(exp)))-1
		expediente = mark_getlist(exp)[ultimo]
		data = mark_read(expediente.fileId.fileNbr.doubleValue,expediente.fileId.fileSeq,expediente.fileId.fileSeries.doubleValue,expediente.fileId.fileType)

		if evento == '573':
			if data.file.filingData.applicationType == 'REG':
				inicio = str(pub_uno).split('-')
				fin = str(pub_tres).split('-')
				f_inicio = inicio[2]+'/'+inicio[1]+'/'+inicio[0]
				f_fin = fin[2]+'/'+fin[1]+'/'+fin[0]

			if data.file.filingData.applicationType == 'REN':
				inicio = str(pub_uno).split('-')
				fin = str(pub_uno).split('-')
				f_inicio = inicio[2]+'/'+inicio[1]+'/'+inicio[0]
				f_fin = fin[2]+'/'+fin[1]+'/'+fin[0]

		ProcessInsertAction = {
								"arg0": {
									"processNbr": { 
											"doubleValue": str(data.file.processId.processNbr.doubleValue) },
											"processType": str(data.file.processId.processType) },
								"arg1": {
									"actionType": str(evento)
									},
								"arg2": {
									"dateValue": ""
									},
								"arg3": {
									"dateValue": ""
									},
								"arg4": {
									"userNbr": {
										"doubleValue": str(userid)
										}
										},
								"arg6": str(nota),
								"arg7": str(f_inicio),
								"arg8": str(f_fin),
								"arg9": "",
								"arg10": "",
								"arg11": "",
								"arg14": {
									"userNbr": {
									"doubleValue": str(userid)
									}
								},
								"arg15": {
									"doubleValue": 0
								}
							}
		return clientMark.service.ProcessInsertAction(**ProcessInsertAction)
	except zeep.exceptions.Fault as e:
		return(str(e))

#Insert 573 event REDPI with date pay set user date (config for suport )
def Insert_Action_soporte(exp,pago,userid,nota,evento): # {"exp":"","pago":"","userid":"","nota":"","evento":"554","inicio":"","fin":""}
	try:
		beta2 = str(pago).split('-') # divide fecha
		format_beta = datetime.datetime(int(beta2[0]),int(beta2[1]),int(beta2[2]))
		print(format_beta)
		today = format_beta
		today_date = format_beta
		td = timedelta(3) # tres dias adelante
		pub_tres = today_date + td
		td_mañana = timedelta(1) # Fecha mañana inicio 
		pub_uno = today + td_mañana
		inicio = ''
		fin = ''
		f_inicio = ''
		f_fin = ''
		print(str(pub_uno).replace(" 00:00:00",""))
		print(str(pub_tres).replace(" 00:00:00",""))

		ultimo = int(len(mark_getlist(exp)))-1
		expediente = mark_getlist(exp)[ultimo]
		data = mark_read(expediente.fileId.fileNbr.doubleValue,expediente.fileId.fileSeq,expediente.fileId.fileSeries.doubleValue,expediente.fileId.fileType)

		if evento == '573':
			if data.file.filingData.applicationType == 'REG':
				inicio = str(pub_uno).replace(" 00:00:00","").split('-')
				fin = str(pub_tres).replace(" 00:00:00","").split('-')
				f_inicio = inicio[2]+'/'+inicio[1]+'/'+inicio[0]
				f_fin = fin[2]+'/'+fin[1]+'/'+fin[0]

			if data.file.filingData.applicationType == 'REN':
				inicio = str(pub_uno).replace(" 00:00:00","").split('-')
				fin = str(pub_uno).replace(" 00:00:00","").split('-')
				f_inicio = inicio[2]+'/'+inicio[1]+'/'+inicio[0]
				f_fin = fin[2]+'/'+fin[1]+'/'+fin[0]

		ProcessInsertAction = {
								"arg0": {
									"processNbr": { 
											"doubleValue": str(data.file.processId.processNbr.doubleValue) },
											"processType": str(data.file.processId.processType) },
								"arg1": {
									"actionType": str(evento)
									},
								"arg2": {
									"dateValue": ""
									},
								"arg3": {
									"dateValue": ""
									},
								"arg4": {
									"userNbr": {
										"doubleValue": str(userid)
										}
										},
								"arg6": str(nota),
								"arg7": str(f_inicio),
								"arg8": str(f_fin),
								"arg9": "",
								"arg10": "",
								"arg11": "",
								"arg14": {
									"userNbr": {
									"doubleValue": str(userid)
									}
								},
								"arg15": {
									"doubleValue": 0
								}
							}
		return clientMark.service.ProcessInsertAction(**ProcessInsertAction)
	except zeep.exceptions.Fault as e:
		return(str(e))

def Insert_note(exp,pago,userid,nota,evento):   # {"exp":"","pago":"","userid":"","nota":"","evento":"1007"}
	try:
		ultimo = int(len(mark_getlist(exp)))-1
		expediente = mark_getlist(exp)[ultimo]
		data = mark_read(expediente.fileId.fileNbr.doubleValue,expediente.fileId.fileSeq,expediente.fileId.fileSeries.doubleValue,expediente.fileId.fileType)
		ProcessInsertNoteAction = {
					"arg0": {"processNbr": {"doubleValue": str(data.file.processId.processNbr.doubleValue) }, "processType": str(data.file.processId.processType) },
					"arg1": {"actionType": str(evento) },
					"arg2": { "dateValue": str(pago)+"T00:00:00" },
					"arg3": {"userNbr": {"doubleValue": str(userid) }},
					"arg5": str(nota),
					"arg6": "",
					"arg7": "",
					"arg8": "",
					"arg9": "",
					"arg10": "",
					"arg13": {
						"userNbr": {
						"doubleValue": str(userid)
						}
					}
				}
		return clientMark.service.ProcessInsertNoteAction(**ProcessInsertNoteAction)
	except Exception as e:
		print(e)

#Eventos 549, 554, 550, 560, etc.
def Process_Read_EventList(processNbr,processType):
	Event_List = {"arg0": {"processNbr": {"doubleValue":str(processNbr)},"processType": str(processType)}}
	data = clientMark.service.ProcessReadEventList(**Event_List) 
	return data

#Marcas (AG) escrito Oposicion
def Insert_user_doc(
					affectedFileIdList_fileNbr,
					affectedFileIdList_fileSeq,
					affectedFileIdList_fileSeries,
					affectedFileIdList_fileType,
					affectedFileSummaryList_fileId_fileNbr,
					affectedFileSummaryList_fileId_fileSeq,
					affectedFileSummaryList_fileId_fileSeries,
					affectedFileSummaryList_fileId_fileType,
					affectedFileSummaryList_fileSummaryDescription,
					affectedFileSummaryList_fileSummaryOwner,
					applicant_applicantNotes,
					applicant_person_addressStreet,
					applicant_person_email,
					applicant_person_nationalityCountryCode,
					applicant_person_personName,
					applicant_person_residenceCountryCode,
					applicant_person_telephone,
					documentId_docLog,
					documentId_docNbr,
					documentId_docOrigin,
					documentId_docSeries,
					documentId_selected,
					documentSeqId_docSeqNbr,
					documentSeqId_docSeqSeries,
					documentSeqId_docSeqType,
					filingData_captureDate,
					filingData_captureUserId,
					filingData_filingDate,
					filingData_paymentList_receiptAmount,
					filingData_paymentList_receiptDate,
					filingData_paymentList_receiptNbr,
					filingData_paymentList_receiptNotes,
					filingData_paymentList_receiptType,
					filingData_paymentList_receiptTypeName,
					filingData_documentId_docLog,
					filingData_documentId_docNbr,
					filingData_documentId_docOrigin,
					filingData_documentId_docSeries,
					filingData_documentId_selected,
					filingData_userdocTypeList_userdocType,
					ownerList_personName,
					ownerList_addressStreet,
					ownerList_nationalityCountryCode,
					ownerList_residenceCountryCode,
					notes,
					representationData_representativeList_addressStreet,
					representationData_representativeList_agentCode,
					representationData_representativeList_email,
					representationData_representativeList_nationalityCountryCode,
					representationData_representativeList_personName,
					representationData_representativeList_residenceCountryCode,
					representationData_representativeList_telephone,
					representationData_representativeList_zipCode
					):

	opo_data = {
				"arg0": {
					"affectedDocumentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
					},
					"affectedFileIdList": {
					"fileNbr": {
						"doubleValue": affectedFileIdList_fileNbr
					},
					"fileSeq": affectedFileIdList_fileSeq,
					"fileSeries": {
						"doubleValue": affectedFileIdList_fileSeries
					},
					"fileType": affectedFileIdList_fileType
					},
					"affectedFileSummaryList": {
					"disclaimer": "",
					"disclaimerInOtherLang": "",
					"fileId": {
						"fileNbr": {
						"doubleValue": affectedFileSummaryList_fileId_fileNbr
						},
						"fileSeq": affectedFileSummaryList_fileId_fileSeq,
						"fileSeries": {
						"doubleValue": affectedFileSummaryList_fileId_fileSeries
						},
						"fileType": affectedFileSummaryList_fileId_fileType
					},
					"fileIdAsString": "",
					"fileSummaryClasses": "",
					"fileSummaryCountry": "",
					"fileSummaryDescription": affectedFileSummaryList_fileSummaryDescription,
					"fileSummaryDescriptionInOtherLang": "",
					"fileSummaryOwner": affectedFileSummaryList_fileSummaryOwner,
					"fileSummaryOwnerInOtherLang": "",
					"fileSummaryRepresentative": "",
					"fileSummaryRepresentativeInOtherLang": "",
					"fileSummaryResponsibleName": "",
					"fileSummaryStatus": "",
					"filingData": {
						"applicationSubtype": "",
						"applicationType": "",
						"captureDate": "",
						"captureUserId": "",
						"corrFileNbr": "",
						"corrFileSeq": "",
						"corrFileSeries": "",
						"corrFileType": "",
						"externalOfficeCode": "",
						"externalOfficeFilingDate": "",
						"externalSystemId": "",
						"filingDate": "",
						"indIncorrRecpDeleted": "",
						"indManualInterpretationRequired": "false",
						"lawCode": "",
						"novelty1Date": "",
						"novelty2Date": "",
						"receptionDate": "",
						"receptionDocument": {
						"documentEdmsData": {
							"edocDate": "",
							"edocId": "",
							"edocImageCertifDate": "",
							"edocImageCertifUser": "",
							"edocImageLinkingDate": "",
							"edocImageLinkingUser": "",
							"edocNbr": "",
							"edocSeq": "",
							"edocSer": "",
							"edocTyp": "",
							"edocTypeName": "",
							"efolderId": "",
							"efolderNbr": "",
							"efolderSeq": "",
							"efolderSer": "",
							"indInterfaceEdoc": "false",
							"indSpecificEdoc": "false"
						},
						"documentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
							"dataCodeId1": "",
							"dataCodeId2": "",
							"dataCodeId3": "",
							"dataCodeId4": "",
							"dataCodeId5": "",
							"dataCodeName1": "",
							"dataCodeName2": "",
							"dataCodeName3": "",
							"dataCodeName4": "",
							"dataCodeName5": "",
							"dataCodeTyp1": "",
							"dataCodeTyp2": "",
							"dataCodeTyp3": "",
							"dataCodeTyp4": "",
							"dataCodeTyp5": "",
							"dataCodeTypeName1": "",
							"dataCodeTypeName2": "",
							"dataCodeTypeName3": "",
							"dataCodeTypeName4": "",
							"dataCodeTypeName5": "",
							"dataDate1": "",
							"dataDate2": "",
							"dataDate3": "",
							"dataDate4": "",
							"dataDate5": "",
							"dataFlag1": "false",
							"dataFlag2": "false",
							"dataFlag3": "false",
							"dataFlag4": "false",
							"dataFlag5": "false",
							"dataNbr1": "",
							"dataNbr2": "",
							"dataNbr3": "",
							"dataNbr4": "",
							"dataNbr5": "",
							"dataText1": "",
							"dataText2": "",
							"dataText3": "",
							"dataText4": "",
							"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
							"description": "",
							"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							},
							"refNo": ""
						},
						"outputDocumentData": {
							"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							}
						},
						"qtyPages": ""
						},
						"receptionUserId": "",
						"validationDate": "",
						"validationUserId": ""
					},
					"indMark": "false",
					"indPatent": "false",
					"pctApplicationId": "",
					"publicationNbr": "",
					"publicationSer": "",
					"publicationTyp": "",
					"registrationData": {
						"entitlementDate": "",
						"expirationDate": "",
						"indRegistered": "false",
						"registrationDate": "",
						"registrationId": {
						"registrationDup": "",
						"registrationNbr": "",
						"registrationSeries": "",
						"registrationType": ""
						}
					},
					"selected": "",
					"similarityPercent": "",
					"statusId": {
						"processType": "",
						"statusCode": ""
					},
					"workflowWarningText": ""
					},
					"applicant": {
					"applicantNotes": applicant_applicantNotes,
					"person": {
						"addressStreet": applicant_person_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": applicant_person_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": applicant_person_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": applicant_person_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": applicant_person_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": applicant_person_telephone,
						"zipCode": ""
					}
					},
					"auxiliaryRegisterData": {
					"cancellation": "",
					"contractSummary": "",
					"guaranteeData": {
						"payee": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"payer": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					},
					"licenseData": {
						"granteePerson": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"grantorPerson": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"indCompulsoryLicense": "false",
						"indExclusiveLicense": "false"
					},
					"registrationDocumentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					}
					},
					"courtDoc": {
					"courtDocDate": "",
					"courtDocNbr": "",
					"courtDocSeq": "",
					"courtDocSeries": "",
					"courtFile": {
						"court": {
						"courtAddress": "",
						"courtName": ""
						},
						"courtFileName": "",
						"courtFileNbr": "",
						"courtFileSeq": "",
						"courtFileSeries": ""
					},
					"decreeDate": "",
					"decreeNbr": "",
					"decreeSeries": ""
					},
					"documentId": {
					"docLog": documentId_docLog,
					"docNbr": {
						"doubleValue": documentId_docNbr
					},
					"docOrigin": documentId_docOrigin,
					"docSeries": {
						"doubleValue": documentId_docSeries
					},
					"selected": documentId_selected
					},
					"documentSeqId": {
					"docSeqName": "Documentos",
					"docSeqNbr": {
						"doubleValue": documentSeqId_docSeqNbr
					},
					"docSeqSeries": {
						"doubleValue": documentSeqId_docSeqSeries
					},
					"docSeqType": documentSeqId_docSeqType
					},
					"filingData": {
					"applicationSubtype": "",
					"applicationType": "",
					"captureDate": {
						"dateValue": filingData_captureDate
					},
					"captureUserId": {
						"doubleValue": filingData_captureUserId
					},
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": {
						"dateValue": filingData_filingDate
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": "",
					"novelty1Date": "",
					"novelty2Date": "",
					"paymentList": {
						"currencyName": "Guaraníes",
						"currencyType": "GS",
						"receiptAmount": filingData_paymentList_receiptAmount,
						"receiptDate": {
						"dateValue": filingData_paymentList_receiptDate
						},
						"receiptNbr": filingData_paymentList_receiptNbr,
						"receiptNotes": filingData_paymentList_receiptNotes,
						"receiptType": filingData_paymentList_receiptType,
						"receiptTypeName": filingData_paymentList_receiptTypeName
					},
					"receptionDate": "",
					"receptionDocument": {
						"documentEdmsData": {
						"edocDate": "",
						"edocId": "",
						"edocImageCertifDate": "",
						"edocImageCertifUser": "",
						"edocImageLinkingDate": "",
						"edocImageLinkingUser": "",
						"edocNbr": "",
						"edocSeq": "",
						"edocSer": "",
						"edocTyp": "",
						"edocTypeName": "",
						"efolderId": "",
						"efolderNbr": "",
						"efolderSeq": "",
						"efolderSer": "",
						"indInterfaceEdoc": "false",
						"indSpecificEdoc": "false"
						},
						"documentId": {
							"docLog": filingData_documentId_docLog,
							"docNbr": {
								"doubleValue": filingData_documentId_docNbr
							},
							"docOrigin": filingData_documentId_docOrigin,
							"docSeries": {
								"doubleValue": filingData_documentId_docSeries
							},
							"selected": filingData_documentId_selected
						},
						"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
						"dataCodeId1": "",
						"dataCodeId2": "",
						"dataCodeId3": "",
						"dataCodeId4": "",
						"dataCodeId5": "",
						"dataCodeName1": "",
						"dataCodeName2": "",
						"dataCodeName3": "",
						"dataCodeName4": "",
						"dataCodeName5": "",
						"dataCodeTyp1": "",
						"dataCodeTyp2": "",
						"dataCodeTyp3": "",
						"dataCodeTyp4": "",
						"dataCodeTyp5": "",
						"dataCodeTypeName1": "",
						"dataCodeTypeName2": "",
						"dataCodeTypeName3": "",
						"dataCodeTypeName4": "",
						"dataCodeTypeName5": "",
						"dataDate1": "",
						"dataDate2": "",
						"dataDate3": "",
						"dataDate4": "",
						"dataDate5": "",
						"dataFlag1": "false",
						"dataFlag2": "false",
						"dataFlag3": "false",
						"dataFlag4": "false",
						"dataFlag5": "false",
						"dataNbr1": "",
						"dataNbr2": "",
						"dataNbr3": "",
						"dataNbr4": "",
						"dataNbr5": "",
						"dataText1": "",
						"dataText2": "",
						"dataText3": "",
						"dataText4": "",
						"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
						"description": "",
						"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						},
						"refNo": ""
						},
						"outputDocumentData": {
						"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						}
						},
						"qtyPages": ""
					},
					"receptionUserId": "",
					"userdocTypeList": {
						"userdocName": "Presentación de oposición",
						"userdocType": filingData_userdocTypeList_userdocType
					},
					"validationDate": "",
					"validationUserId": ""
					},
					"indNotAllFilesCapturedYet": "false",
					"newOwnershipData": {
					"dummy": "false",
					"ownerList": {
						"indService": "false",
						"orderNbr": "",
						"ownershipNotes": "",
						"person": {
						"addressStreet": ownerList_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": ownerList_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": ownerList_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": ownerList_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					}
					},
					"notes": notes,
					"officeSectionId": {
					"officeDepartmentCode": "",
					"officeDivisionCode": "",
					"officeSectionCode": ""
					},
					"poaData": {
					"documentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"poaDate": "",
					"poaGrantor": {
						"person": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					},
					"poaRegNumber": "",
					"scope": ""
					},
					"representationData": {
						"documentId_PowerOfAttorneyRegister": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"referencedPOAData": {
							"documentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
							},
							"poaDate": "",
							"poaGrantor": {
							"person": {
								"addressStreet": "",
								"addressStreetInOtherLang": "",
								"addressZone": "",
								"agentCode": "",
								"cityCode": "",
								"cityName": "",
								"companyRegisterRegistrationDate": "",
								"companyRegisterRegistrationNbr": "",
								"email": "",
								"indCompany": "false",
								"individualIdNbr": "",
								"individualIdType": "",
								"legalIdNbr": "",
								"legalIdType": "",
								"legalNature": "",
								"legalNatureInOtherLang": "",
								"nationalityCountryCode": "",
								"personGroupCode": "",
								"personGroupName": "",
								"personName": "",
								"personNameInOtherLang": "",
								"residenceCountryCode": "",
								"stateCode": "",
								"stateName": "",
								"telephone": "",
								"zipCode": ""
							}
							},
							"poaRegNumber": "",
							"scope": ""
						},
						"representativeList": {
							"indService": "false",
							"person": {
							"addressStreet": representationData_representativeList_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": {
								"doubleValue": representationData_representativeList_agentCode
							},
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": representationData_representativeList_email,
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": representationData_representativeList_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": representationData_representativeList_personName,
							"personNameInOtherLang": "",
							"residenceCountryCode": representationData_representativeList_residenceCountryCode,
							"stateCode": "",
							"stateName": "",
							"telephone": representationData_representativeList_telephone,
							"zipCode": representationData_representativeList_zipCode
							},
							"representativeType": "AG"
						}
					},
					"respondedOfficedocId": {
					"offidocNbr": "",
					"offidocOrigin": "",
					"offidocSeries": "",
					"selected": ""
					},
					"rowVersion": "",
					"userdocProcessId": {
					"processNbr": "",
					"processType": ""
					}
				}
				}
	return(clientMark.service.UserdocInsert(**opo_data))

def Insert_user_doc_sin_recibo_relacion(applicant_person_applicantNotes,
										applicant_person_addressStreet,
										applicant_person_nationalityCountryCode,
										applicant_person_personName,
										applicant_person_residenceCountryCode,
										documentId_docLog,
										documentId_docNbr,
										documentId_docOrigin,
										documentId_docSeries,
										documentId_selected,
										documentSeqId_docSeqNbr,
										documentSeqId_docSeqSeries,
										documentSeqId_docSeqType,
										filingData_captureDate,
										filingData_captureUserId,
										filingData_filingDate,
										filingData_receptionDocument_documentId_docLog,
										filingData_receptionDocument_documentId_docNbr,
										filingData_receptionDocument_documentId_docOrigin,
										filingData_receptionDocument_documentId_docSeries,
										filingData_receptionDocument_documentId_selected,
										filingData_userdocTypeList_userdocName,
										filingData_userdocTypeList_userdocType,
										ownerList_person_addressStreet,
										ownerList_person_nationalityCountryCode,
										ownerList_person_personName,
										ownerList_person_residenceCountryCode,
										notes,
										representativeList_person_addressStreetAgente,
										representativeList_person_agentCode,
										representativeList_person_email,
										representativeList_person_nationalityCountryCode,
										representativeList_person_AgentepersonName,
										representativeList_person_residenceCountryCode,
										representativeList_person_telephone,
										representativeList_person_zipCode,
										processNbr,
										processType):
	i_u_d_s_r_r_data = {
				"arg0": {
					"affectedDocumentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
					},
					"applicant": {
					"applicantNotes": applicant_person_applicantNotes,
					"person": {
						"addressStreet": applicant_person_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": applicant_person_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": applicant_person_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": applicant_person_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					}
					},
					"auxiliaryRegisterData": {
					"cancellation": "",
					"contractSummary": "",
					"guaranteeData": {
						"payee": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"payer": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					},
					"licenseData": {
						"granteePerson": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"grantorPerson": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"indCompulsoryLicense": "false",
						"indExclusiveLicense": "false"
					},
					"registrationDocumentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
						}
					},
					"courtDoc": {
					"courtDocDate": "",
					"courtDocNbr": "",
					"courtDocSeq": "",
					"courtDocSeries": "",
					"courtFile": {
						"court": {
						"courtAddress": "",
						"courtName": ""
						},
						"courtFileName": "",
						"courtFileNbr": "",
						"courtFileSeq": "",
						"courtFileSeries": ""
					},
					"decreeDate": "",
					"decreeNbr": "",
					"decreeSeries": ""
					},
					"documentId": {
						"docLog": documentId_docLog,
						"docNbr": {
							"doubleValue": documentId_docNbr
						},
						"docOrigin": documentId_docOrigin,
						"docSeries": {
							"doubleValue": documentId_docSeries
						},
						"selected": documentId_selected
					},
					"documentSeqId": {
					"docSeqName": "Documentos",
					"docSeqNbr": {
						"doubleValue": documentSeqId_docSeqNbr
					},
					"docSeqSeries": {
						"doubleValue": documentSeqId_docSeqSeries
					},
					"docSeqType": documentSeqId_docSeqType
					},
					"filingData": {
						"applicationSubtype": "",
						"applicationType": "",
						"captureDate": {
							"dateValue": filingData_captureDate
						},
						"captureUserId": {
							"doubleValue": filingData_captureUserId
						},
						"corrFileNbr": "",
						"corrFileSeq": "",
						"corrFileSeries": "",
						"corrFileType": "",
						"externalOfficeCode": "",
						"externalOfficeFilingDate": "",
						"externalSystemId": "",
						"filingDate": {
							"dateValue": filingData_filingDate
						},
						"indIncorrRecpDeleted": "",
						"indManualInterpretationRequired": "false",
						"lawCode": "",
						"novelty1Date": "",
						"novelty2Date": "",
						"receptionDate": "",
						"receptionDocument": {
							"documentEdmsData": {
							"edocDate": "",
							"edocId": "",
							"edocImageCertifDate": "",
							"edocImageCertifUser": "",
							"edocImageLinkingDate": "",
							"edocImageLinkingUser": "",
							"edocNbr": "",
							"edocSeq": "",
							"edocSer": "",
							"edocTyp": "",
							"edocTypeName": "",
							"efolderId": "",
							"efolderNbr": "",
							"efolderSeq": "",
							"efolderSer": "",
							"indInterfaceEdoc": "false",
							"indSpecificEdoc": "false"
							},
							"documentId": {
							"docLog": filingData_receptionDocument_documentId_docLog,
							"docNbr": {
								"doubleValue": filingData_receptionDocument_documentId_docNbr
							},
							"docOrigin": filingData_receptionDocument_documentId_docOrigin,
							"docSeries": {
								"doubleValue": filingData_receptionDocument_documentId_docSeries
							},
							"selected": filingData_receptionDocument_documentId_selected
							},
							"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
							},
							"externalSystemId": "",
							"extraData": {
							"dataCodeId1": "",
							"dataCodeId2": "",
							"dataCodeId3": "",
							"dataCodeId4": "",
							"dataCodeId5": "",
							"dataCodeName1": "",
							"dataCodeName2": "",
							"dataCodeName3": "",
							"dataCodeName4": "",
							"dataCodeName5": "",
							"dataCodeTyp1": "",
							"dataCodeTyp2": "",
							"dataCodeTyp3": "",
							"dataCodeTyp4": "",
							"dataCodeTyp5": "",
							"dataCodeTypeName1": "",
							"dataCodeTypeName2": "",
							"dataCodeTypeName3": "",
							"dataCodeTypeName4": "",
							"dataCodeTypeName5": "",
							"dataDate1": "",
							"dataDate2": "",
							"dataDate3": "",
							"dataDate4": "",
							"dataDate5": "",
							"dataFlag1": "false",
							"dataFlag2": "false",
							"dataFlag3": "false",
							"dataFlag4": "false",
							"dataFlag5": "false",
							"dataNbr1": "",
							"dataNbr2": "",
							"dataNbr3": "",
							"dataNbr4": "",
							"dataNbr5": "",
							"dataText1": "",
							"dataText2": "",
							"dataText3": "",
							"dataText4": "",
							"dataText5": ""
							},
							"inputDocumentData": "",
							"internalDocumentData": {
							"description": "",
							"offidocId": {
								"offidocNbr": "",
								"offidocOrigin": "",
								"offidocSeries": "",
								"selected": ""
							},
							"refNo": ""
							},
							"outputDocumentData": {
							"officedocId": {
								"offidocNbr": "",
								"offidocOrigin": "",
								"offidocSeries": "",
								"selected": ""
							}
							},
							"qtyPages": ""
						},
						"receptionUserId": "",
						"userdocTypeList": {
							"userdocName": filingData_userdocTypeList_userdocName,
							"userdocType": filingData_userdocTypeList_userdocType
						},
						"validationDate": "",
						"validationUserId": ""
					},
					"indNotAllFilesCapturedYet": "false",
					"newOwnershipData": {
					"dummy": "false",
					"ownerList": {
						"indService": "false",
						"orderNbr": "",
						"ownershipNotes": "",
						"person": {
						"addressStreet": ownerList_person_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": ownerList_person_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": ownerList_person_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": ownerList_person_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					}
					},
					"notes": notes,
					"officeSectionId": {
					"officeDepartmentCode": "",
					"officeDivisionCode": "",
					"officeSectionCode": ""
					},
					"poaData": {
					"documentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"poaDate": "",
					"poaGrantor": {
						"person": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					},
					"poaRegNumber": "",
					"scope": ""
					},
					"representationData": {
					"documentId_PowerOfAttorneyRegister": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"referencedPOAData": {
						"documentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
						},
						"poaDate": "",
						"poaGrantor": {
						"person": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						}
						},
						"poaRegNumber": "",
						"scope": ""
					},
					"representativeList": {
						"indService": "false",
						"person": {
							"addressStreet": representativeList_person_addressStreetAgente,
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": {
								"doubleValue": representativeList_person_agentCode
							},
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": representativeList_person_email,
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": representativeList_person_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": representativeList_person_AgentepersonName,
							"personNameInOtherLang": "",
							"residenceCountryCode": representativeList_person_residenceCountryCode,
							"stateCode": "",
							"stateName": "",
							"telephone": representativeList_person_telephone,
							"zipCode": representativeList_person_zipCode
						},
						"representativeType": "AG"
					}
					},
					"respondedOfficedocId": {
					"offidocNbr": "",
					"offidocOrigin": "",
					"offidocSeries": "",
					"selected": ""
					},
					"rowVersion": "",
					"userdocProcessId": {
					"processNbr": {
						"doubleValue": processNbr
					},
					"processType": processType
					}
				}}
	#print("docNbr => " + str(docNbr))
	return(clientMark.service.UserdocInsert(**i_u_d_s_r_r_data))

def Insert_user_doc_con_recibo_poder(
										applicant_applicantNotes,
										applicant_person_addressStreet,
										applicant_person_agentCode,
										applicant_person_cityCode,
										applicant_person_cityName,
										applicant_person_email,
										applicant_person_nationalityCountryCode,
										applicant_person_personName,
										applicant_person_residenceCountryCode,
										applicant_person_telephone,
										applicant_person_zipCode,
										documentId_docLog,
										documentId_docNbr,
										documentId_docOrigin,
										documentId_docSeries,
										documentId_selected,
										documentSeqId_docSeqNbr,
										documentSeqId_docSeqSeries,
										documentSeqId_docSeqType,
										filingData_captureDate,
										filingData_captureUserId,
										filingData_filingDate,
										filingData_paymentList_currencyName,
										filingData_paymentList_currencyType,
										filingData_paymentList_receiptAmount,
										filingData_paymentList_receiptDate,
										filingData_paymentList_receiptNbr,
										filingData_paymentList_receiptNotes,
										filingData_paymentList_receiptType,
										filingData_paymentList_receiptTypeName,
										filingData_userdocTypeList_userdocName,
										filingData_userdocTypeList_userdocType,
										filingData_receptionDocument_documentId_docLog,
										filingData_receptionDocument_docNbr,
										filingData_receptionDocument_docOrigin,
										filingData_receptionDocument_docSeries,
										receptionDocument_extraData_dataNbr1,
										poaAgpoaData_poaGranteeList_person_agentCode,
										poaData_poaDate,
										ownerList_person_addressStreet,
										ownerList_person_agentCode,
										ownerList_person_nationalityCountryCode,
										ownerList_person_personName,
										ownerList_person_residenceCountryCode,
										ownerList_person_telephone,
										ownerList_person_zipCode,
										poaData_poaGranteeList_person_addressStreet,
										poaData_poaGranteeList_person_addressZone,
										poaData_poaGranteeList_person_cityName,
										poaData_poaGranteeList_person_email,
										poaData_poaGranteeList_person_nationalityCountryCode,
										poaData_poaGranteeList_person_personName,
										poaData_poaGranteeList_person_residenceCountryCode,
										poaData_poaGranteeList_person_telephone,
										poaData_poaGranteeList_person_zipCode,
										poaData_poaGranteeList_representativeType,
										poaData_poaGrantor_person_addressStreet,
										poaData_poaGrantor_person_agentCode,
										poaData_poaGrantor_person_cityName,
										poaData_poaGrantor_person_email,
										poaData_poaGrantor_person_nationalityCountryCode,
										poaData_poaGrantor_person_personName,
										poaData_poaGrantor_person_residenceCountryCode,
										poaData_poaGrantor_person_telephone,
										poaData_poaGrantor_person_zipCode,
										poaData_poaRegNumber,
										poaData_scope,
										representationData_representativeList_person_addressStreet,
										representationData_representativeList_person_addressZone,
										representationData_representativeList_person_agentCode,
										representationData_representativeList_person_cityName,
										representationData_representativeList_person_nationalityCountryCode,
										representationData_representativeList_person_personName,
										representationData_representativeList_person_residenceCountryCode,
										representationData_representativeList_person_telephone,
										representationData_representativeList_person_zipCode,
										representativeList_representativeType,
										notes,
										userdocProcessId_processNbr,
										userdocProcessId_processType):
	iudcrp = {
				"arg0": {
					"affectedDocumentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
					},
					"applicant": {
						"applicantNotes": applicant_applicantNotes,
						"person": {
							"addressStreet": applicant_person_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": applicant_person_agentCode,
							"cityCode": applicant_person_cityCode,
							"cityName": applicant_person_cityName,
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": applicant_person_email,
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": applicant_person_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": applicant_person_personName,
							"personNameInOtherLang": "",
							"residenceCountryCode": applicant_person_residenceCountryCode,
							"stateCode": "",
							"stateName": "",
							"telephone": applicant_person_telephone,
							"zipCode": applicant_person_zipCode
						}
					},
					"auxiliaryRegisterData": {
						"cancellation": "",
						"contractSummary": "",
						"guaranteeData": {
							"payee": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
							},
							"payer": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
							}
						},
						"licenseData": {
							"granteePerson": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
							},
							"grantorPerson": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
							},
							"indCompulsoryLicense": "false",
							"indExclusiveLicense": "false"
						},
						"registrationDocumentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						}
					},
					"courtDoc": {
					"courtDocDate": "",
					"courtDocNbr": "",
					"courtDocSeq": "",
					"courtDocSeries": "",
					"courtFile": {
						"court": {
						"courtAddress": "",
						"courtName": ""
						},
						"courtFileName": "",
						"courtFileNbr": "",
						"courtFileSeq": "",
						"courtFileSeries": ""
					},
					"decreeDate": "",
					"decreeNbr": "",
					"decreeSeries": ""
					},
					"documentId": {
						"docLog": documentId_docLog,
						"docNbr": {
							"doubleValue": documentId_docNbr
						},
						"docOrigin": documentId_docOrigin,
						"docSeries": {
							"doubleValue": documentId_docSeries
						},
						"selected": documentId_selected
					},
					"documentSeqId": {
						"docSeqName": "Documentos",
						"docSeqNbr": {
							"doubleValue": documentSeqId_docSeqNbr
						},
						"docSeqSeries": {
							"doubleValue": documentSeqId_docSeqSeries
						},
						"docSeqType": documentSeqId_docSeqType
					},
					"filingData": {
						"applicationSubtype": "",
						"applicationType": "",
						"captureDate": {
							"dateValue": filingData_captureDate
						},
						"captureUserId": {
							"doubleValue": filingData_captureUserId
						},
						"corrFileNbr": "",
						"corrFileSeq": "",
						"corrFileSeries": "",
						"corrFileType": "",
						"externalOfficeCode": "",
						"externalOfficeFilingDate": "",
						"externalSystemId": "",
						"filingDate": {
							"dateValue": filingData_filingDate
						},
						"indIncorrRecpDeleted": "",
						"indManualInterpretationRequired": "false",
						"lawCode": "",
						"novelty1Date": "",
						"novelty2Date": "",
						"paymentList": {
							"currencyName": filingData_paymentList_currencyName,
							"currencyType": filingData_paymentList_currencyType,
							"receiptAmount": filingData_paymentList_receiptAmount,
							"receiptDate": {
							"dateValue": filingData_paymentList_receiptDate
							},
							"receiptNbr": filingData_paymentList_receiptNbr,
							"receiptNotes": filingData_paymentList_receiptNotes,
							"receiptType": filingData_paymentList_receiptType,
							"receiptTypeName": filingData_paymentList_receiptTypeName
						},
						"receptionDate": "",
						"receptionDocument": {
							"documentEdmsData": {
							"edocDate": "",
							"edocId": "",
							"edocImageCertifDate": "",
							"edocImageCertifUser": "",
							"edocImageLinkingDate": "",
							"edocImageLinkingUser": "",
							"edocNbr": "",
							"edocSeq": "",
							"edocSer": "",
							"edocTyp": "",
							"edocTypeName": "",
							"efolderId": "",
							"efolderNbr": "",
							"efolderSeq": "",
							"efolderSer": "",
							"indInterfaceEdoc": "false",
							"indSpecificEdoc": "false"
							},
							"documentId": {
							"docLog": filingData_receptionDocument_documentId_docLog,
							"docNbr": {
								"doubleValue": filingData_receptionDocument_docNbr
							},
							"docOrigin": filingData_receptionDocument_docOrigin,
							"docSeries": {
								"doubleValue": filingData_receptionDocument_docSeries
							},
							"selected": ""
							},
							"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
							},
							"externalSystemId": "",
							"extraData": {
							"dataCodeId1": "",
							"dataCodeId2": "",
							"dataCodeId3": "",
							"dataCodeId4": "",
							"dataCodeId5": "",
							"dataCodeName1": "",
							"dataCodeName2": "",
							"dataCodeName3": "",
							"dataCodeName4": "",
							"dataCodeName5": "",
							"dataCodeTyp1": "",
							"dataCodeTyp2": "",
							"dataCodeTyp3": "",
							"dataCodeTyp4": "",
							"dataCodeTyp5": "",
							"dataCodeTypeName1": "",
							"dataCodeTypeName2": "",
							"dataCodeTypeName3": "",
							"dataCodeTypeName4": "",
							"dataCodeTypeName5": "",
							"dataDate1": "",
							"dataDate2": "",
							"dataDate3": "",
							"dataDate4": "",
							"dataDate5": "",
							"dataFlag1": "false",
							"dataFlag2": "false",
							"dataFlag3": "false",
							"dataFlag4": "false",
							"dataFlag5": "false",
							"dataNbr1": {
								"doubleValue": receptionDocument_extraData_dataNbr1
							},
							"dataNbr2": "",
							"dataNbr3": "",
							"dataNbr4": "",
							"dataNbr5": "",
							"dataText1": "",
							"dataText2": "",
							"dataText3": "",
							"dataText4": "",
							"dataText5": ""
							},
							"inputDocumentData": "",
							"internalDocumentData": {
							"description": "",
							"offidocId": {
								"offidocNbr": "",
								"offidocOrigin": "",
								"offidocSeries": "",
								"selected": ""
							},
							"refNo": ""
							},
							"outputDocumentData": {
							"officedocId": {
								"offidocNbr": "",
								"offidocOrigin": "",
								"offidocSeries": "",
								"selected": ""
							}
							},
							"qtyPages": ""
						},
						"receptionUserId": "",
						"userdocTypeList": {
							"userdocName": filingData_userdocTypeList_userdocName,
							"userdocType": filingData_userdocTypeList_userdocType
						},
						"validationDate": "",
						"validationUserId": ""
					},
					"indNotAllFilesCapturedYet": "false",
					"newOwnershipData": {
					"dummy": "",
					"ownerList": {
						"indService": "false",
						"orderNbr": "",
						"ownershipNotes": "",
							"person": {
							"addressStreet": ownerList_person_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": ownerList_person_agentCode,
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": ownerList_person_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": ownerList_person_personName,
							"personNameInOtherLang": "",
							"residenceCountryCode": ownerList_person_residenceCountryCode,
							"stateCode": "",
							"stateName": "",
							"telephone": ownerList_person_telephone,
							"zipCode": ownerList_person_zipCode
							}
					}
					},
					"notes": notes,
					"officeSectionId": {
					"officeDepartmentCode": "",
					"officeDivisionCode": "",
					"officeSectionCode": ""
					},
					"poaData": {
						"documentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"poaDate": {
							"dateValue": poaData_poaDate
						},
						"poaGranteeList": {
							"person": {
							"addressStreet": poaData_poaGranteeList_person_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": poaData_poaGranteeList_person_addressZone,
							"agentCode": {
								"doubleValue": poaAgpoaData_poaGranteeList_person_agentCode
							},
							"cityCode": "",
							"cityName": poaData_poaGranteeList_person_cityName,
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": poaData_poaGranteeList_person_email,
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": poaData_poaGranteeList_person_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": poaData_poaGranteeList_person_personName,
							"personNameInOtherLang": "",
							"residenceCountryCode": poaData_poaGranteeList_person_residenceCountryCode,
							"stateCode": "",
							"stateName": "",
							"telephone": poaData_poaGranteeList_person_telephone,
							"zipCode": poaData_poaGranteeList_person_zipCode
							},
							"representativeType": poaData_poaGranteeList_representativeType
						},
						"poaGrantor": {
							"person": {
							"addressStreet": poaData_poaGrantor_person_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": poaData_poaGrantor_person_agentCode,
							"cityCode": "",
							"cityName": poaData_poaGrantor_person_cityName,
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": poaData_poaGrantor_person_email,
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode":poaData_poaGrantor_person_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": poaData_poaGrantor_person_personName,
							"personNameInOtherLang": "",
							"residenceCountryCode": poaData_poaGrantor_person_residenceCountryCode,
							"stateCode": "",
							"stateName": "",
							"telephone": poaData_poaGrantor_person_telephone,
							"zipCode": poaData_poaGrantor_person_zipCode
							}
						},
						"poaRegNumber": {
							"doubleValue": poaData_poaRegNumber
						},
						"scope": poaData_scope
					},
					"representationData": {
						"documentId_PowerOfAttorneyRegister": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"referencedPOAData": {
							"documentId": {
								"docLog": "",
								"docNbr": "",
								"docOrigin": "",
								"docSeries": "",
								"selected": ""
							},
							"poaDate": "",
							"poaGrantor": {
							"person": {
								"addressStreet": "",
								"addressStreetInOtherLang": "",
								"addressZone": "",
								"agentCode": "",
								"cityCode": "",
								"cityName": "",
								"companyRegisterRegistrationDate": "",
								"companyRegisterRegistrationNbr": "",
								"email": "",
								"indCompany": "false",
								"individualIdNbr": "",
								"individualIdType": "",
								"legalIdNbr": "",
								"legalIdType": "",
								"legalNature": "",
								"legalNatureInOtherLang": "",
								"nationalityCountryCode": "",
								"personGroupCode": "",
								"personGroupName": "",
								"personName": "",
								"personNameInOtherLang": "",
								"residenceCountryCode": "",
								"stateCode": "",
								"stateName": "",
								"telephone": "",
								"zipCode": ""
							}
							},
							"poaRegNumber": "",
							"scope": ""
						},
						"representativeList": {
							"indService": "false",
							"person": {
							"addressStreet": representationData_representativeList_person_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": representationData_representativeList_person_addressZone,
							"agentCode": {
								"doubleValue": representationData_representativeList_person_agentCode
							},
							"cityCode": "",
							"cityName": representationData_representativeList_person_cityName,
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "Mirle91_@hotmail.com",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": representationData_representativeList_person_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": representationData_representativeList_person_personName,
							"personNameInOtherLang": "",
							"residenceCountryCode": representationData_representativeList_person_residenceCountryCode,
							"stateCode": "",
							"stateName": "",
							"telephone": representationData_representativeList_person_telephone,
							"zipCode": representationData_representativeList_person_zipCode
							},
							"representativeType": representativeList_representativeType
						}
					},
					"respondedOfficedocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
					},
					"rowVersion": "",
					"userdocProcessId": {
					"processNbr": {
						"doubleValue": userdocProcessId_processNbr
					},
					"processType": userdocProcessId_processType
					}
				}
				}
	return(clientMark.service.UserdocInsert(**iudcrp))

#Insert con recibo sin exp (AG)
def Insert_user_doc_con_recibo_sin_exp(
										applicant_applicantNotes,
										applicant_addressStreet,
										applicant_cityName,
										applicant_email,
										applicant_addressZone,
										applicant_individualIdType,
										applicant_individualIdNbr,
										applicant_nationalityCountryCode,
										applicant_personName,
										applicant_residenceCountryCode,
										applicant_telephone,
										applicant_zipCode,
										docLog,
										docNbr,
										docOrigin,
										docSeries,
										docSeqNbr,
										docSeqSeries,
										captureDate,
										captureUserId,
										docSeqType,
										filingDate,
										paymentList_receiptAmount,
										paymentList_receiptDate,
										paymentList_receiptNbr,
										paymentList_receiptNotes,
										paymentList_receiptType,
										paymentList_receiptTypeName,
										receptionUserId_userdocName,
										receptionUserId_userdocType,
										ownerList_ownershipNotes,
										ownerList_addressStreet,
										ownerList_addressZone,
										ownerList_cityCode,
										ownerList_cityName,
										ownerList_email,
										ownerList_individualIdNbr,
										ownerList_individualIdType,
										ownerList_nationalityCountryCode,
										ownerList_personName,
										ownerList_residenceCountryCode,
										ownerList_telephone,
										ownerList_zipCode,
										notes,
										representativeList_personName,
										representativeList_addressStreet,
										representativeList_agentCode,
										representativeList_email,
										representativeList_nationalityCountryCode,
										representativeList_residenceCountryCode,
										representativeList_telephone,
										representativeList_zipCode,
										representativeList_representativeType
										):
	iudcrse = {
				"arg0": {
					"affectedDocumentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
					},
					"applicant": {
					"applicantNotes": applicant_applicantNotes,
					"person": {
						"addressStreet": applicant_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": applicant_addressZone,
						"agentCode": "",
						"cityCode": "",
						"cityName": applicant_cityName,
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": applicant_email,
						"indCompany": 'false',
						"individualIdNbr": applicant_individualIdNbr,
						"individualIdType": applicant_individualIdType,
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": applicant_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": applicant_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": applicant_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": applicant_telephone,
						"zipCode": applicant_zipCode
					}
					},
					"auxiliaryRegisterData": {
					"cancellation": "",
					"contractSummary": "",
					"guaranteeData": {
						"payee": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": 'false',
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"payer": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": 'false',
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					},
					"licenseData": {
						"granteePerson": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": 'false',
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"grantorPerson": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": 'false',
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"indCompulsoryLicense": 'false',
						"indExclusiveLicense": 'false'
					},
					"registrationDocumentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					}
					},
					"courtDoc": {
					"courtDocDate": "",
					"courtDocNbr": "",
					"courtDocSeq": "",
					"courtDocSeries": "",
					"courtFile": {
						"court": {
						"courtAddress": "",
						"courtName": ""
						},
						"courtFileName": "",
						"courtFileNbr": "",
						"courtFileSeq": "",
						"courtFileSeries": ""
					},
					"decreeDate": "",
					"decreeNbr": "",
					"decreeSeries": ""
					},
					"documentId": {
					"docLog": docLog,
					"docNbr": {
						"doubleValue": docNbr
					},
					"docOrigin": docOrigin,
					"docSeries": {
						"doubleValue": docSeries
					},
					"selected": ""
					},
					"documentSeqId": {
					"docSeqName": "Documentos",
					"docSeqNbr": {
						"doubleValue": docSeqNbr
					},
					"docSeqSeries": {
						"doubleValue": docSeqSeries
					},
					"docSeqType": docSeqType
					},
					"filingData": {
					"applicationSubtype": "",
					"applicationType": "",
					"captureDate": {
						"dateValue": captureDate
					},
					"captureUserId": {
						"doubleValue": captureUserId
					},
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": {
						"dateValue": filingDate
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": 'false',
					"lawCode": "",
					"novelty1Date": "",
					"novelty2Date": "",
					"paymentList": {
						"currencyName": "Guaraníes",
						"currencyType": "GS",
						"receiptAmount": paymentList_receiptAmount,
						"receiptDate": {
						"dateValue": paymentList_receiptDate
						},
						"receiptNbr": paymentList_receiptNbr,
						"receiptNotes": paymentList_receiptNotes,
						"receiptType": paymentList_receiptType,
						"receiptTypeName": paymentList_receiptTypeName
					},
					"receptionDate": "",
					"receptionDocument": {
						"documentEdmsData": {
						"edocDate": "",
						"edocId": "",
						"edocImageCertifDate": "",
						"edocImageCertifUser": "",
						"edocImageLinkingDate": "",
						"edocImageLinkingUser": "",
						"edocNbr": "",
						"edocSeq": "",
						"edocSer": "",
						"edocTyp": "",
						"edocTypeName": "",
						"efolderId": "",
						"efolderNbr": "",
						"efolderSeq": "",
						"efolderSer": "",
						"indInterfaceEdoc": 'false',
						"indSpecificEdoc": 'false'
						},
						"documentId": {
						"docLog": docLog,
						"docNbr": {
							"doubleValue": docNbr
						},
						"docOrigin": docOrigin,
						"docSeries": {
							"doubleValue": docSeries
						},
						"selected": ""
						},
						"documentSeqId": {
						"docSeqName": "",
						"docSeqNbr": "",
						"docSeqSeries": "",
						"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
						"dataCodeId1": "",
						"dataCodeId2": "",
						"dataCodeId3": "",
						"dataCodeId4": "",
						"dataCodeId5": "",
						"dataCodeName1": "",
						"dataCodeName2": "",
						"dataCodeName3": "",
						"dataCodeName4": "",
						"dataCodeName5": "",
						"dataCodeTyp1": "",
						"dataCodeTyp2": "",
						"dataCodeTyp3": "",
						"dataCodeTyp4": "",
						"dataCodeTyp5": "",
						"dataCodeTypeName1": "",
						"dataCodeTypeName2": "",
						"dataCodeTypeName3": "",
						"dataCodeTypeName4": "",
						"dataCodeTypeName5": "",
						"dataDate1": "",
						"dataDate2": "",
						"dataDate3": "",
						"dataDate4": "",
						"dataDate5": "",
						"dataFlag1": 'false',
						"dataFlag2": 'false',
						"dataFlag3": 'false',
						"dataFlag4": 'false',
						"dataFlag5": 'false',
						"dataNbr1": "",
						"dataNbr2": "",
						"dataNbr3": "",
						"dataNbr4": "",
						"dataNbr5": "",
						"dataText1": "",
						"dataText2": "",
						"dataText3": "",
						"dataText4": "",
						"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
						"description": "",
						"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						},
						"refNo": ""
						},
						"outputDocumentData": {
						"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						}
						},
						"qtyPages": ""
					},
					"receptionUserId": "",
					"userdocTypeList": {
						"userdocName": receptionUserId_userdocName,
						"userdocType": receptionUserId_userdocType
					},
					"validationDate": "",
					"validationUserId": ""
					},
					"indNotAllFilesCapturedYet": 'false',
					"newOwnershipData": {
					"dummy": "",
					"ownerList": {
						"indService": 'false',
						"orderNbr": "",
						"ownershipNotes": ownerList_ownershipNotes,
						"person": {
						"addressStreet": ownerList_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": ownerList_addressZone,
						"agentCode": "",
						"cityCode": ownerList_cityCode,
						"cityName": ownerList_cityName,
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": ownerList_email,
						"indCompany": "false",
						"individualIdNbr": ownerList_individualIdNbr,
						"individualIdType": ownerList_individualIdType,
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": ownerList_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": ownerList_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": ownerList_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": ownerList_telephone,
						"zipCode": ownerList_zipCode
						}
					}
					},
					"notes": notes,
					"officeSectionId": {
					"officeDepartmentCode": "",
					"officeDivisionCode": "",
					"officeSectionCode": ""
					},
					"poaData": {
					"documentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"poaDate": "",
					"poaGrantor": {
						"person": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": 'false',
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					},
					"poaRegNumber": "",
					"scope": ""
					},
					"representationData": {
					"documentId_PowerOfAttorneyRegister": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"referencedPOAData": {
						"documentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
						},
						"poaDate": "",
						"poaGrantor": {
						"person": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": 'false',
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						}
						},
						"poaRegNumber": "",
						"scope": ""
					},
					"representativeList": {
						"indService": 'false',
					"person": {
                        "addressStreet": representativeList_addressStreet,
                        "addressStreetInOtherLang": "",
                        "addressZone": "",
                        "agentCode": {
                            "doubleValue": representativeList_agentCode
                        },
                        "cityCode": "",
                        "cityName": "",
                        "companyRegisterRegistrationDate": "",
                        "companyRegisterRegistrationNbr": "",
                        "email": representativeList_email,
                        "indCompany": 'false',
                        "individualIdNbr": "",
                        "individualIdType": "",
                        "legalIdNbr": "",
                        "legalIdType": "",
                        "legalNature": "",
                        "legalNatureInOtherLang": "",
                        "nationalityCountryCode": representativeList_nationalityCountryCode,
                        "personGroupCode": "",
                        "personGroupName": "",
                        "personName": representativeList_personName,
                        "personNameInOtherLang": "",
                        "residenceCountryCode": representativeList_residenceCountryCode,
                        "stateCode": "",
                        "stateName": "",
                        "telephone":  representativeList_telephone,
                        "zipCode":  representativeList_zipCode
                    },
						"representativeType": representativeList_representativeType
					}
					},
					"respondedOfficedocId": {
					"offidocNbr": "",
					"offidocOrigin": "",
					"offidocSeries": "",
					"selected": ""
					},
					"rowVersion": ""
				}
				}
	return(clientMark.service.UserdocInsert(**iudcrse))

#Insert sin recibo con relacion (AG)
def Insert_user_doc_sin_recibo_con_relacion(
											affectedFileIdList_fileNbr,
											affectedFileIdList_fileSeq,
											affectedFileIdList_fileSeries,
											affectedFileIdList_fileType,                                           
											affectedFileSummaryList_fileId_fileNbr,
											affectedFileSummaryList_fileId_fileSeq,
											affectedFileSummaryList_fileId_fileSeries,
											affectedFileSummaryList_fileId_fileType,
											affectedFileSummaryList_fileSummaryDescription,
											affectedFileSummaryList_fileSummaryOwner,
											applicant_applicantNotes,
											applicant_addressStreet,
											applicant_nationalityCountryCode,
											applicant_personName,
											applicant_residenceCountryCode,
											documentId_docLog,
											documentId_docNbr,
											documentId_docOrigin,
											documentId_docSeries,
											documentId_selected,
											documentSeqId_docSeqNbr,
											documentSeqId_docSeqSeries,
											documentSeqId_docSeqType,
											filingData_captureDate,
											filingData_captureUserId,
											filingData_filingDate,
											filingData_documentId_docLog,
											filingData_documentId_docNbr,
											filingData_documentId_docOrigin,
											filingData_documentId_docSeries,
											filingData_userdocTypeList_userdocName,
											filingData_userdocTypeList_userdocType,
											ownerList_person_addressStreet,
											ownerList_person_email,
											ownerList_person_nationalityCountryCode,
											ownerList_person_personName,
											ownerList_person_residenceCountryCode,
											ownerList_person_telephone,
											ownerList_person_zipCode,
											notes,
											representativeList_person_addressStreet,
											representativeList_person_agentCode,
											representativeList_person_email,
											representativeList_person_nationalityCountryCode,
											representativeList_person_personName,
											representativeList_person_residenceCountryCode,
											representativeList_person_telephone,
											representativeList_person_zipCode,
											representativeList_representativeType):
	iudsrcr = {
				"arg0": {
					"affectedDocumentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
					},
					"affectedFileIdList": {
					"fileNbr": {
						"doubleValue": affectedFileIdList_fileNbr
					},
					"fileSeq": affectedFileIdList_fileSeq,
					"fileSeries": {
						"doubleValue": affectedFileIdList_fileSeries
					},
					"fileType": affectedFileIdList_fileType
					},
					"affectedFileSummaryList": {
					"disclaimer": "",
					"disclaimerInOtherLang": "",
					"fileId": {
						"fileNbr": {
						"doubleValue": affectedFileSummaryList_fileId_fileNbr
						},
						"fileSeq": affectedFileSummaryList_fileId_fileSeq,
						"fileSeries": {
						"doubleValue": affectedFileSummaryList_fileId_fileSeries
						},
						"fileType": affectedFileSummaryList_fileId_fileType
					},
					"fileIdAsString": "",
					"fileSummaryClasses": "",
					"fileSummaryCountry": "",
					"fileSummaryDescription": str(affectedFileSummaryList_fileSummaryDescription).replace(chr(13),""),
					"fileSummaryDescriptionInOtherLang": "",
					"fileSummaryOwner": affectedFileSummaryList_fileSummaryOwner,
					"fileSummaryOwnerInOtherLang": "",
					"fileSummaryRepresentative": "",
					"fileSummaryRepresentativeInOtherLang": "",
					"fileSummaryResponsibleName": "",
					"fileSummaryStatus": "",
					"filingData": {
						"applicationSubtype": "",
						"applicationType": "",
						"captureDate": "",
						"captureUserId": "",
						"corrFileNbr": "",
						"corrFileSeq": "",
						"corrFileSeries": "",
						"corrFileType": "",
						"externalOfficeCode": "",
						"externalOfficeFilingDate": "",
						"externalSystemId": "",
						"filingDate": "",
						"indIncorrRecpDeleted": "",
						"indManualInterpretationRequired": "false",
						"lawCode": "",
						"novelty1Date": "",
						"novelty2Date": "",
						"receptionDate": "",
						"receptionDocument": {
						"documentEdmsData": {
							"edocDate": "",
							"edocId": "",
							"edocImageCertifDate": "",
							"edocImageCertifUser": "",
							"edocImageLinkingDate": "",
							"edocImageLinkingUser": "",
							"edocNbr": "",
							"edocSeq": "",
							"edocSer": "",
							"edocTyp": "",
							"edocTypeName": "",
							"efolderId": "",
							"efolderNbr": "",
							"efolderSeq": "",
							"efolderSer": "",
							"indInterfaceEdoc": "false",
							"indSpecificEdoc": "false"
						},
						"documentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
							"dataCodeId1": "",
							"dataCodeId2": "",
							"dataCodeId3": "",
							"dataCodeId4": "",
							"dataCodeId5": "",
							"dataCodeName1": "",
							"dataCodeName2": "",
							"dataCodeName3": "",
							"dataCodeName4": "",
							"dataCodeName5": "",
							"dataCodeTyp1": "",
							"dataCodeTyp2": "",
							"dataCodeTyp3": "",
							"dataCodeTyp4": "",
							"dataCodeTyp5": "",
							"dataCodeTypeName1": "",
							"dataCodeTypeName2": "",
							"dataCodeTypeName3": "",
							"dataCodeTypeName4": "",
							"dataCodeTypeName5": "",
							"dataDate1": "",
							"dataDate2": "",
							"dataDate3": "",
							"dataDate4": "",
							"dataDate5": "",
							"dataFlag1": "false",
							"dataFlag2": "false",
							"dataFlag3": "false",
							"dataFlag4": "false",
							"dataFlag5": "false",
							"dataNbr1": "",
							"dataNbr2": "",
							"dataNbr3": "",
							"dataNbr4": "",
							"dataNbr5": "",
							"dataText1": "",
							"dataText2": "",
							"dataText3": "",
							"dataText4": "",
							"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
							"description": "",
							"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							},
							"refNo": ""
						},
						"outputDocumentData": {
							"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							}
						},
						"qtyPages": ""
						},
						"receptionUserId": "",
						"validationDate": "",
						"validationUserId": ""
					},
					"indMark": "false",
					"indPatent": "false",
					"pctApplicationId": "",
					"publicationNbr": "",
					"publicationSer": "",
					"publicationTyp": "",
					"registrationData": {
						"entitlementDate": "",
						"expirationDate": "",
						"indRegistered": "false",
						"registrationDate": "",
						"registrationId": {
						"registrationDup": "",
						"registrationNbr": "",
						"registrationSeries": "",
						"registrationType": ""
						}
					},
					"selected": "",
					"similarityPercent": "",
					"statusId": {
						"processType": "",
						"statusCode": ""
					},
					"workflowWarningText": ""
					},
					"applicant": {
					"applicantNotes": applicant_applicantNotes,
					"person": {
						"addressStreet": str(applicant_addressStreet).replace(chr(13),""),
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": applicant_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": str(applicant_personName).replace(chr(13),""),
						"personNameInOtherLang": "",
						"residenceCountryCode": applicant_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					}
					},
					"auxiliaryRegisterData": {
					"cancellation": "",
					"contractSummary": "",
					"guaranteeData": {
						"payee": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"payer": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					},
					"licenseData": {
						"granteePerson": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"grantorPerson": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						},
						"indCompulsoryLicense": "false",
						"indExclusiveLicense": "false"
					},
					"registrationDocumentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					}
					},
					"courtDoc": {
					"courtDocDate": "",
					"courtDocNbr": "",
					"courtDocSeq": "",
					"courtDocSeries": "",
					"courtFile": {
						"court": {
						"courtAddress": "",
						"courtName": ""
						},
						"courtFileName": "",
						"courtFileNbr": "",
						"courtFileSeq": "",
						"courtFileSeries": ""
					},
					"decreeDate": "",
					"decreeNbr": "",
					"decreeSeries": ""
					},
					"documentId": {
					"docLog": documentId_docLog,
					"docNbr": {
						"doubleValue": documentId_docNbr
					},
					"docOrigin": documentId_docOrigin,
					"docSeries": {
						"doubleValue": documentId_docSeries
					},
					"selected": documentId_selected
					},
					"documentSeqId": {
					"docSeqName": "Documentos",
					"docSeqNbr": {
						"doubleValue": documentSeqId_docSeqNbr
					},
					"docSeqSeries": {
						"doubleValue": documentSeqId_docSeqSeries
					},
					"docSeqType": documentSeqId_docSeqType
					},
					"filingData": {
					"applicationSubtype": "",
					"applicationType": "",
					"captureDate": {
						"dateValue": filingData_captureDate
					},
					"captureUserId": {
						"doubleValue": filingData_captureUserId
					},
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": {
						"dateValue": filingData_filingDate
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": "",
					"novelty1Date": "",
					"novelty2Date": "",
					"receptionDate": "",
					"receptionDocument": {
						"documentEdmsData": {
						"edocDate": "",
						"edocId": "",
						"edocImageCertifDate": "",
						"edocImageCertifUser": "",
						"edocImageLinkingDate": "",
						"edocImageLinkingUser": "",
						"edocNbr": "",
						"edocSeq": "",
						"edocSer": "",
						"edocTyp": "",
						"edocTypeName": "",
						"efolderId": "",
						"efolderNbr": "",
						"efolderSeq": "",
						"efolderSer": "",
						"indInterfaceEdoc": "false",
						"indSpecificEdoc": "false"
						},
						"documentId": {
						"docLog": filingData_documentId_docLog,
						"docNbr": {
							"doubleValue": filingData_documentId_docNbr
						},
						"docOrigin": filingData_documentId_docOrigin,
						"docSeries": {
							"doubleValue": filingData_documentId_docSeries
						},
						"selected": ""
						},
						"documentSeqId": {
						"docSeqName": "",
						"docSeqNbr": "",
						"docSeqSeries": "",
						"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
						"dataCodeId1": "",
						"dataCodeId2": "",
						"dataCodeId3": "",
						"dataCodeId4": "",
						"dataCodeId5": "",
						"dataCodeName1": "",
						"dataCodeName2": "",
						"dataCodeName3": "",
						"dataCodeName4": "",
						"dataCodeName5": "",
						"dataCodeTyp1": "",
						"dataCodeTyp2": "",
						"dataCodeTyp3": "",
						"dataCodeTyp4": "",
						"dataCodeTyp5": "",
						"dataCodeTypeName1": "",
						"dataCodeTypeName2": "",
						"dataCodeTypeName3": "",
						"dataCodeTypeName4": "",
						"dataCodeTypeName5": "",
						"dataDate1": "",
						"dataDate2": "",
						"dataDate3": "",
						"dataDate4": "",
						"dataDate5": "",
						"dataFlag1": "false",
						"dataFlag2": "false",
						"dataFlag3": "false",
						"dataFlag4": "false",
						"dataFlag5": "false",
						"dataNbr1": "",
						"dataNbr2": "",
						"dataNbr3": "",
						"dataNbr4": "",
						"dataNbr5": "",
						"dataText1": "",
						"dataText2": "",
						"dataText3": "",
						"dataText4": "",
						"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
						"description": "",
						"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						},
						"refNo": ""
						},
						"outputDocumentData": {
						"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						}
						},
						"qtyPages": ""
					},
					"receptionUserId": "",
					"userdocTypeList": {
						"userdocName": filingData_userdocTypeList_userdocName,
						"userdocType": filingData_userdocTypeList_userdocType
					},
					"validationDate": "",
					"validationUserId": ""
					},
					"indNotAllFilesCapturedYet": "false",
					"newOwnershipData": {
					"dummy": "",
					"ownerList": {
						"indService": "false",
						"orderNbr": "",
						"ownershipNotes": "",
						"person": {
						"addressStreet": ownerList_person_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": ownerList_person_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": ownerList_person_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": ownerList_person_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": ownerList_person_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": ownerList_person_telephone,
						"zipCode": ownerList_person_zipCode
						}
					}
					},
					"notes": str(notes).replace(chr(13),""),
					"officeSectionId": {
					"officeDepartmentCode": "",
					"officeDivisionCode": "",
					"officeSectionCode": ""
					},
					"poaData": {
					"documentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"poaDate": "",
					"poaGrantor": {
						"person": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					},
					"poaRegNumber": "",
					"scope": ""
					},
					"representationData": {
					"documentId_PowerOfAttorneyRegister": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"referencedPOAData": {
						"documentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
						},
						"poaDate": "",
						"poaGrantor": {
						"person": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						}
						},
						"poaRegNumber": "",
						"scope": ""
					},
					"representativeList": {
						"indService": "false",
                    "person": {
                        "addressStreet": representativeList_person_addressStreet,
                        "addressStreetInOtherLang": "",
                        "addressZone": "",
                        "agentCode": {
                            "doubleValue": representativeList_person_agentCode
                        },
                        "cityCode": "",
                        "cityName": "",
                        "companyRegisterRegistrationDate": "",
                        "companyRegisterRegistrationNbr": "",
                        "email": representativeList_person_email,
                        "indCompany": "false",
                        "individualIdNbr": "",
                        "individualIdType": "",
                        "legalIdNbr": "",
                        "legalIdType": "",
                        "legalNature": "",
                        "legalNatureInOtherLang": "",
                        "nationalityCountryCode": representativeList_person_nationalityCountryCode,
                        "personGroupCode": "",
                        "personGroupName": "",
                        "personName": representativeList_person_personName,
                        "personNameInOtherLang": "",
                        "residenceCountryCode": representativeList_person_residenceCountryCode,
                        "stateCode": "",
                        "stateName": "",
                        "telephone": representativeList_person_telephone,
                        "zipCode": representativeList_person_zipCode
                        },
						"representativeType": representativeList_representativeType
					}
					},
					"respondedOfficedocId": {
					"offidocNbr": "",
					"offidocOrigin": "",
					"offidocSeries": "",
					"selected": ""
					},
					"rowVersion": "",
					"userdocProcessId": {
					"processNbr": "",
					"processType": ""
					}
				  }
				}
	return(clientMark.service.UserdocInsert(**iudsrcr))

#userDocGetList por escritoNbr
def user_doc_getlist_escrito(docNbrFrom, docNbrTo): # {'docNbrFrom': {'doubleValue':'21108884',},'docNbrTo': {'doubleValue':'21108884'}}
	UserdocGetList = {'arg0': {'criteriaDocumentId': {'docNbrFrom': {'doubleValue':docNbrFrom,},'docNbrTo': {'doubleValue':docNbrTo}},},}
	return clientMark.service.UserdocGetList(**UserdocGetList)

def user_doc_receive(
	arg0,
	arg1,
	arg3,
	arg4_offidocNbr,
	arg4_offidocOrigin,
	arg4_offidocSeries,
	arg4_selected,
	arg5_officeDepartmentCode,
	arg5_officeDivisionCode,
	arg5_officeSectionCode,
	arg6,
	arg7_currencyType,
	arg7_DReceiptAmount,
	arg7_receiptDate,
	arg7_receiptNbr,
	arg7_receiptType,
	arg8,
	arg9,
	arg10_docLog,
	arg10_docNbr,
	arg10_docOrigin,
	arg10_docSeries,
	arg10_selected,
	arg11_docSeqName,
	arg11_docSeqNbr,
	arg11_docSeqSeries,
	arg11_docSeqType,
	arg12_docLog,
	arg12_docNbr,
	arg12_docOrigin,
	arg12_docSeries,
	arg12_selected):
	try:
		daily_log_open(arg6)   
		udr={
				"arg0": arg0,
				"arg1": str(arg1),
				"arg3": arg3,
				"arg4": {
					"offidocNbr": {
					"doubleValue": arg4_offidocNbr
					},
					"offidocOrigin": arg4_offidocOrigin,
					"offidocSeries": {
					"doubleValue": arg4_offidocSeries
					},
					"selected": arg4_selected
				},
				"arg5": {
					"officeDepartmentCode": arg5_officeDepartmentCode,
					"officeDivisionCode": arg5_officeDivisionCode,
					"officeSectionCode": arg5_officeSectionCode
				},
				"arg6": {
					"dateValue": arg6
				},
				"arg7": {
					"currencyType": arg7_currencyType,
					"DReceiptAmount": arg7_DReceiptAmount,
					"receiptDate": {
					"dateValue": arg7_receiptDate
					},
					"receiptNbr": arg7_receiptNbr,
					"receiptType": arg7_receiptType
				},
				"arg8": {
					"doubleValue": arg8
				},
				"arg9": arg9,
				"arg10": {
					"docLog": arg10_docLog,
					"docNbr": {
					"doubleValue": arg10_docNbr
					},
					"docOrigin": arg10_docOrigin,
					"docSeries": {
					"doubleValue": arg10_docSeries
					},
					"selected": arg10_selected
				},
				"arg11": {
					"docSeqName": arg11_docSeqName,
					"docSeqNbr": {
					"doubleValue": arg11_docSeqNbr
					},
					"docSeqSeries": {
					"doubleValue": arg11_docSeqSeries
					},
					"docSeqType": arg11_docSeqType
				},
				"arg12": {
					"docLog": arg12_docLog,
					"docNbr": {
					"doubleValue": arg12_docNbr
					},
					"docOrigin": arg12_docOrigin,
					"docSeries": {
					"doubleValue": arg12_docSeries
					},
					"selected": arg12_selected
				}
				} 
		clientMark.service.UserdocReceive(**udr)
		daily_log_close(arg6)   
		return('true') 
	except zeep.exceptions.Fault as e:
		if(str(e) != 'true'):
			daily_log_close(arg6)
		return(str(e))
		 
"""#User_Doc_UpDate 
def user_doc_update(affectedDocumentId_docLog,
					affectedDocumentId_docNbr,
					affectedDocumentId_docOrigin,
					affectedDocumentId_docSeries,
					applicant_applicantNotes,
					applicant_person_addressStreet,
					applicant_person_agentCode,
					applicant_person_cityCode,
					applicant_person_cityName,
					applicant_person_email,
					applicant_person_nationalityCountryCode,
					applicant_person_personGroupCode,
					applicant_person_personGroupName,
					applicant_person_personName,
					applicant_person_residenceCountryCode,
					applicant_person_stateCode,
					applicant_person_stateName,
					applicant_person_telephone,
					applicant_person_zipCode,
					documentId_docLog,
					documentId_docNbr,
					documentId_docOrigin,
					documentId_docSeries,
					documentSeqId_docSeqNbr,
					documentSeqId_docSeqSeries,
					documentSeqId_docSeqType,
					filingData_captureDate,
					filingData_captureUserId,
					filingData_filingDate,
					filingData_receptionDate,
					filingData_paymentList_currencyName,
					filingData_paymentList_currencyType,
					filingData_paymentList_receiptAmount,
					filingData_paymentList_receiptDate,
					filingData_paymentList_receiptNbr,
					filingData_paymentList_receiptNotes,
					filingData_paymentList_receiptType,
					filingData_paymentList_receiptTypeName,
					filingData_userdocTypeList_userdocName,
					filingData_userdocTypeList_userdocType,
					filingData_documentId_docLog,
					filingData_documentId_receptionDocument_docNbr,
					filingData_documentId_receptionDocument_docOrigin,
					filingData_documentId_receptionDocument_docSeries,
					filingData_documentId_receptionDocument_selected,
					newOwnershipData_ownerList_orderNbr,
					newOwnershipData_ownerList_ownershipNotes,
					newOwnershipData_ownerList_addressStreet,
					newOwnershipData_ownerList_cityName,
					newOwnershipData_ownerList_email,
					newOwnershipData_ownerList_nationalityCountryCode,
					newOwnershipData_ownerList_personName,
					newOwnershipData_ownerList_residenceCountryCode,
					newOwnershipData_ownerList_telephone,
					newOwnershipData_ownerList_zipCode,
					notes,
					representationData_representativeList_person_addressStreet,
					representationData_representativeList_person_addressZone,
					representationData_representativeList_person_agentCode,
					representationData_representativeList_person_cityName,
					representationData_representativeList_person_email,
					representationData_representativeList_person_individualIdNbr,
					representationData_representativeList_person_individualIdType,
					representationData_representativeList_person_legalIdNbr,
					representationData_representativeList_person_legalIdType,
					representationData_representativeList_person_legalNature,
					representationData_representativeList_person_nationalityCountryCode,
					representationData_representativeList_person_personName,
					representationData_representativeList_person_personNameInOtherLang,
					representationData_representativeList_person_residenceCountryCode,
					representationData_representativeList_person_telephone,
					representationData_representativeList_person_zipCode,
					representationData_representativeList_representativeType):
	if filingData_paymentList_receiptNbr != "":	
		data = {
			"arg0": {
				"affectedDocumentId": {
				"docLog": affectedDocumentId_docLog,
				"docNbr": {
					"doubleValue": affectedDocumentId_docNbr
				},
				"docOrigin": affectedDocumentId_docOrigin,
				"docSeries": {
					"doubleValue": affectedDocumentId_docSeries
				},
				"selected": ""
				},
				"applicant": {
				"applicantNotes": applicant_applicantNotes,
				"person": {
					"addressStreet": applicant_person_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": applicant_person_agentCode,
					"cityCode": applicant_person_cityCode,
					"cityName": applicant_person_cityName,
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": applicant_person_email,
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": applicant_person_nationalityCountryCode,
					"personGroupCode": applicant_person_personGroupCode,
					"personGroupName": applicant_person_personGroupName,
					"personName": applicant_person_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": applicant_person_residenceCountryCode,
					"stateCode": applicant_person_stateCode,
					"stateName": applicant_person_stateName,
					"telephone": applicant_person_telephone,
					"zipCode": applicant_person_zipCode
				}
				},
				"documentId": {
				"docLog": documentId_docLog,
				"docNbr": {
					"doubleValue": documentId_docNbr
				},
				"docOrigin": documentId_docOrigin,
				"docSeries": {
					"doubleValue": documentId_docSeries
				}
				},
				"documentSeqId": {
				"docSeqName": "Documentos",
				"docSeqNbr": {
					"doubleValue": documentSeqId_docSeqNbr
				},
				"docSeqSeries": {
					"doubleValue": documentSeqId_docSeqSeries
				},
				"docSeqType": documentSeqId_docSeqType
				},
				"filingData": {
					"applicationSubtype": "",
					"applicationType": "",
					"captureDate": {
						"dateValue": filingData_captureDate
					},
					"captureUserId": {
						"doubleValue": filingData_captureUserId
					},
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": {
						"dateValue": filingData_filingDate
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": "",
					"novelty1Date": "",
					"novelty2Date": "",
					"paymentList": {
						"currencyName": filingData_paymentList_currencyName,
						"currencyType": filingData_paymentList_currencyType,
						"receiptAmount": filingData_paymentList_receiptAmount,
						"receiptDate": {
						"dateValue": filingData_paymentList_receiptDate
						},
						"receiptNbr": filingData_paymentList_receiptNbr,
						"receiptNotes": filingData_paymentList_receiptNotes,
						"receiptType": filingData_paymentList_receiptType,
						"receiptTypeName": filingData_paymentList_receiptTypeName
					},
					"receptionDate": {
						"dateValue": filingData_receptionDate
					},
					"receptionDocument": {
						"documentEdmsData": {
						"edocDate": "",
						"edocId": "",
						"edocImageCertifDate": "",
						"edocImageCertifUser": "",
						"edocImageLinkingDate": "",
						"edocImageLinkingUser": "",
						"edocNbr": "",
						"edocSeq": "",
						"edocSer": "",
						"edocTyp": "",
						"edocTypeName": "",
						"efolderId": "",
						"efolderNbr": "",
						"efolderSeq": "",
						"efolderSer": "",
						"indInterfaceEdoc": "false",
						"indSpecificEdoc": "false"
						},
						"documentId": {
						"docLog": filingData_documentId_docLog,
						"docNbr": {
							"doubleValue": filingData_documentId_receptionDocument_docNbr
						},
						"docOrigin": filingData_documentId_receptionDocument_docOrigin,
						"docSeries": {
							"doubleValue": filingData_documentId_receptionDocument_docSeries
						},
						"selected": filingData_documentId_receptionDocument_selected
						},
						"documentSeqId": {
						"docSeqName": "",
						"docSeqNbr": "",
						"docSeqSeries": "",
						"docSeqType": ""
						},
						"externalSystemId": "",
						"inputDocumentData": "",
						"internalDocumentData": {
						"description": "",
						"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						},
						"refNo": ""
						},
						"outputDocumentData": {
						"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						}
						},
						"qtyPages": ""
					},
					"receptionUserId": "",
					"userdocTypeList": {
						"userdocName": filingData_userdocTypeList_userdocName,
						"userdocType": filingData_userdocTypeList_userdocType
					},
					"validationDate": "",
					"validationUserId": ""
				},
				"newOwnershipData": {
					"ownerList": {
						"orderNbr": {
						"doubleValue": newOwnershipData_ownerList_orderNbr
						},
						"ownershipNotes": newOwnershipData_ownerList_ownershipNotes,
						"person": {
						"addressStreet": newOwnershipData_ownerList_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": newOwnershipData_ownerList_cityName,
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": newOwnershipData_ownerList_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": newOwnershipData_ownerList_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": newOwnershipData_ownerList_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": newOwnershipData_ownerList_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": newOwnershipData_ownerList_telephone,
						"zipCode": newOwnershipData_ownerList_zipCode
						}
					}
				},
				"notes": notes,
				"representationData": {
					"representativeList": {
							"indService": "false",
							"person": {
							"addressStreet": representationData_representativeList_person_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": representationData_representativeList_person_addressZone,
							"agentCode": {
								"doubleValue": representationData_representativeList_person_agentCode
							},
							"cityCode": "",
							"cityName": representationData_representativeList_person_cityName,
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": representationData_representativeList_person_email,
							"indCompany": "true",
							"individualIdNbr": representationData_representativeList_person_individualIdNbr,
							"individualIdType": representationData_representativeList_person_individualIdType,
							"legalIdNbr": representationData_representativeList_person_legalIdNbr,
							"legalIdType": representationData_representativeList_person_legalIdType,
							"legalNature": representationData_representativeList_person_legalNature,
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": representationData_representativeList_person_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": representationData_representativeList_person_personName,
							"personNameInOtherLang": representationData_representativeList_person_personNameInOtherLang,
							"residenceCountryCode": representationData_representativeList_person_residenceCountryCode,
							"stateCode": "",
							"stateName": "",
							"telephone": representationData_representativeList_person_telephone,
							"zipCode": representationData_representativeList_person_zipCode
							},
							"representativeType": representationData_representativeList_representativeType
					}
				}
				}
			}
	else:
		data = {
			"arg0": {
				"affectedDocumentId": {
				"docLog": affectedDocumentId_docLog,
				"docNbr": {
					"doubleValue": affectedDocumentId_docNbr
				},
				"docOrigin": affectedDocumentId_docOrigin,
				"docSeries": {
					"doubleValue": affectedDocumentId_docSeries
				},
				"selected": ""
				},
				"applicant": {
				"applicantNotes": applicant_applicantNotes,
				"person": {
					"addressStreet": applicant_person_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": applicant_person_agentCode,
					"cityCode": applicant_person_cityCode,
					"cityName": applicant_person_cityName,
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": applicant_person_email,
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": applicant_person_nationalityCountryCode,
					"personGroupCode": applicant_person_personGroupCode,
					"personGroupName": applicant_person_personGroupName,
					"personName": applicant_person_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": applicant_person_residenceCountryCode,
					"stateCode": applicant_person_stateCode,
					"stateName": applicant_person_stateName,
					"telephone": applicant_person_telephone,
					"zipCode": applicant_person_zipCode
				}
				},
				"documentId": {
				"docLog": documentId_docLog,
				"docNbr": {
					"doubleValue": documentId_docNbr
				},
				"docOrigin": documentId_docOrigin,
				"docSeries": {
					"doubleValue": documentId_docSeries
				}
				},
				"documentSeqId": {
				"docSeqName": "Documentos",
				"docSeqNbr": {
					"doubleValue": documentSeqId_docSeqNbr
				},
				"docSeqSeries": {
					"doubleValue": documentSeqId_docSeqSeries
				},
				"docSeqType": documentSeqId_docSeqType
				},
				"filingData": {
					"applicationSubtype": "",
					"applicationType": "",
					"captureDate": {
						"dateValue": filingData_captureDate
					},
					"captureUserId": {
						"doubleValue": filingData_captureUserId
					},
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": {
						"dateValue": filingData_filingDate
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": "",
					"novelty1Date": "",
					"novelty2Date": "",
					"receptionDate": {
						"dateValue": filingData_receptionDate
					},
					"receptionDocument": {
						"documentEdmsData": {
						"edocDate": "",
						"edocId": "",
						"edocImageCertifDate": "",
						"edocImageCertifUser": "",
						"edocImageLinkingDate": "",
						"edocImageLinkingUser": "",
						"edocNbr": "",
						"edocSeq": "",
						"edocSer": "",
						"edocTyp": "",
						"edocTypeName": "",
						"efolderId": "",
						"efolderNbr": "",
						"efolderSeq": "",
						"efolderSer": "",
						"indInterfaceEdoc": "false",
						"indSpecificEdoc": "false"
						},
						"documentId": {
						"docLog": filingData_documentId_docLog,
						"docNbr": {
							"doubleValue": filingData_documentId_receptionDocument_docNbr
						},
						"docOrigin": filingData_documentId_receptionDocument_docOrigin,
						"docSeries": {
							"doubleValue": filingData_documentId_receptionDocument_docSeries
						},
						"selected": filingData_documentId_receptionDocument_selected
						},
						"documentSeqId": {
						"docSeqName": "",
						"docSeqNbr": "",
						"docSeqSeries": "",
						"docSeqType": ""
						},
						"externalSystemId": "",
						"inputDocumentData": "",
						"internalDocumentData": {
						"description": "",
						"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						},
						"refNo": ""
						},
						"outputDocumentData": {
						"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						}
						},
						"qtyPages": ""
					},
					"receptionUserId": "",
					"userdocTypeList": {
						"userdocName": filingData_userdocTypeList_userdocName,
						"userdocType": filingData_userdocTypeList_userdocType
					},
					"validationDate": "",
					"validationUserId": ""
				},
				"newOwnershipData": {
					"ownerList": {
						"orderNbr": {
						"doubleValue": newOwnershipData_ownerList_orderNbr
						},
						"ownershipNotes": newOwnershipData_ownerList_ownershipNotes,
						"person": {
						"addressStreet": newOwnershipData_ownerList_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": newOwnershipData_ownerList_cityName,
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": newOwnershipData_ownerList_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": newOwnershipData_ownerList_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": newOwnershipData_ownerList_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": newOwnershipData_ownerList_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": newOwnershipData_ownerList_telephone,
						"zipCode": newOwnershipData_ownerList_zipCode
						}
					}
				},
				"notes": notes,
				"representationData": {
					"representativeList": {
							"indService": "false",
							"person": {
							"addressStreet": representationData_representativeList_person_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": representationData_representativeList_person_addressZone,
							"agentCode": {
								"doubleValue": representationData_representativeList_person_agentCode
							},
							"cityCode": "",
							"cityName": representationData_representativeList_person_cityName,
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": representationData_representativeList_person_email,
							"indCompany": "true",
							"individualIdNbr": representationData_representativeList_person_individualIdNbr,
							"individualIdType": representationData_representativeList_person_individualIdType,
							"legalIdNbr": representationData_representativeList_person_legalIdNbr,
							"legalIdType": representationData_representativeList_person_legalIdType,
							"legalNature": representationData_representativeList_person_legalNature,
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": representationData_representativeList_person_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": representationData_representativeList_person_personName,
							"personNameInOtherLang": representationData_representativeList_person_personNameInOtherLang,
							"residenceCountryCode": representationData_representativeList_person_residenceCountryCode,
							"stateCode": "",
							"stateName": "",
							"telephone": representationData_representativeList_person_telephone,
							"zipCode": representationData_representativeList_person_zipCode
							},
							"representativeType": representationData_representativeList_representativeType
					}
				}
				}
			} 
	return clientMark.service.UserdocUpdate(**data)"""

#User_Doc_UpDate 
def user_doc_update(affectedDocumentId_docLog,
					affectedDocumentId_docNbr,
					affectedDocumentId_docOrigin,
					affectedDocumentId_docSeries,
					applicant_applicantNotes,
					person_addressStreet,
					person_cityName,
					person_email,
					person_nationalityCountryCode,
					person_personName,
					person_residenceCountryCode,
					person_telephone,
					person_zipCode,
					documentId_docLog,
					documentId_docNbr,
					documentId_docOrigin,
					documentId_docSeries,
					documentSeqId_docSeqNbr,
					documentSeqId_docSeqSeries,
					documentSeqId_docSeqType,
					filingData_captureDate,
					filingData_captureUserId,
					filingData_filingDate,
					filingData_receptionDate,
					paymentList_currencyName,
					paymentList_currencyType,
					paymentList_receiptAmount,
					paymentList_receiptDate,
					paymentList_receiptNbr,
					paymentList_receiptNotes,
					paymentList_receiptType,
					paymentList_receiptTypeName,
					receptionDocument_docNbr,
					receptionDocument_docOrigin,
					receptionDocument_docSeries,
					userdocTypeList_userdocName,
					userdocTypeList_userdocType,
					ownerList_orderNbr,
					ownerList_ownershipNotes,
					ownerList_addressStreet,
					ownerList_cityName,
					ownerList_email,
					ownerList_nationalityCountryCode,
					ownerList_personName,
					ownerList_residenceCountryCode,
					ownerList_telephone,
					ownerList_zipCode,
					notes,
					representationData_addressStreet,
					representationData_addressZone,
					representationData_agentCode,
					representationData_cityName,
					representationData_individualIdNbr,
					representationData_individualIdType,
					representationData_legalIdNbr,
					representationData_legalIdType,
					representationData_legalNature,    
					representationData_nationalityCountryCode,
					representationData_personName,
					representationData_personNameInOtherLang,
					representationData_residenceCountryCode,
					representationData_telephone,
					representationData_zipCode,
					representationData_representativeType,
					representationData_email):
	try:				
		if paymentList_receiptNbr != "":
			udud = {
			"arg0": {
				"affectedDocumentId": {
				"docLog": affectedDocumentId_docLog,
				"docNbr": {
					"doubleValue": affectedDocumentId_docNbr
				},
				"docOrigin": affectedDocumentId_docOrigin,
				"docSeries": {
					"doubleValue": affectedDocumentId_docSeries
				},
				"selected": ""
				},
				"applicant": {
				"applicantNotes": applicant_applicantNotes,
				"person": {
					"addressStreet": person_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": person_cityName,
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": person_email,
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": person_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": person_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": person_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": person_telephone,
					"zipCode": person_zipCode
				}
				},
				"documentId": {
				"docLog": documentId_docLog,
				"docNbr": {
					"doubleValue": documentId_docNbr
				},
				"docOrigin": documentId_docOrigin,
				"docSeries": {
					"doubleValue": documentId_docSeries
				}
				},
				"documentSeqId": {
				"docSeqName": "Documentos",
				"docSeqNbr": {
					"doubleValue": documentSeqId_docSeqNbr
				},
				"docSeqSeries": {
					"doubleValue": documentSeqId_docSeqSeries
				},
				"docSeqType": documentSeqId_docSeqType
				},
				"filingData": {
				"applicationSubtype": "",
				"applicationType": "",
				"captureDate": {
					"dateValue": filingData_captureDate
				},
				"captureUserId": {
					"doubleValue": filingData_captureUserId
				},
				"corrFileNbr": "",
				"corrFileSeq": "",
				"corrFileSeries": "",
				"corrFileType": "",
				"externalOfficeCode": "",
				"externalOfficeFilingDate": "",
				"externalSystemId": "",
				"filingDate": {
					"dateValue": filingData_filingDate
				},
				"indIncorrRecpDeleted": "",
				"indManualInterpretationRequired": "false",
				"lawCode": "",
				"novelty1Date": "",
				"novelty2Date": "",
				"paymentList": {
					"currencyName": paymentList_currencyName,
					"currencyType": paymentList_currencyType,
					"receiptAmount": paymentList_receiptAmount,
					"receiptDate": {
					"dateValue": paymentList_receiptDate
					},
					"receiptNbr": paymentList_receiptNbr,
					"receiptNotes": paymentList_receiptNotes,
					"receiptType": paymentList_receiptType,
					"receiptTypeName": paymentList_receiptTypeName
				},
				"receptionDate": {
					"dateValue": filingData_receptionDate
				},
				"receptionDocument": {
					"documentEdmsData": {
					"edocDate": "",
					"edocId": "",
					"edocImageCertifDate": "",
					"edocImageCertifUser": "",
					"edocImageLinkingDate": "",
					"edocImageLinkingUser": "",
					"edocNbr": "",
					"edocSeq": "",
					"edocSer": "",
					"edocTyp": "",
					"edocTypeName": "",
					"efolderId": "",
					"efolderNbr": "",
					"efolderSeq": "",
					"efolderSer": "",
					"indInterfaceEdoc": "false",
					"indSpecificEdoc": "false"
					},
					"documentId": {
					"docLog": "E",
					"docNbr": {
						"doubleValue": receptionDocument_docNbr
					},
					"docOrigin": receptionDocument_docOrigin,
					"docSeries": {
						"doubleValue": receptionDocument_docSeries
					},
					"selected": ""
					},
					"documentSeqId": {
					"docSeqName": "",
					"docSeqNbr": "",
					"docSeqSeries": "",
					"docSeqType": ""
					},
					"externalSystemId": "",
					"inputDocumentData": "",
					"internalDocumentData": {
					"description": "",
					"offidocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
					},
					"refNo": ""
					},
					"outputDocumentData": {
					"officedocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
					}
					},
					"qtyPages": ""
				},
				"receptionUserId": "",
				"userdocTypeList": {
					"userdocName": userdocTypeList_userdocName,
					"userdocType": userdocTypeList_userdocType
				},
				"validationDate": "",
				"validationUserId": ""
				},
				"newOwnershipData": {
				"ownerList": {
					"orderNbr": {
					"doubleValue": ownerList_orderNbr
					},
					"ownershipNotes": ownerList_ownershipNotes,
					"person": {
					"addressStreet": ownerList_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": ownerList_cityName,
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": ownerList_email,
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": ownerList_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": ownerList_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": ownerList_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": ownerList_telephone,
					"zipCode": ownerList_zipCode
					}
				}
				},
				"notes": notes,
				"representationData": {
				"representativeList": {
					"indService": "false",
                    "person": {
					"addressStreet": representationData_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": representationData_addressZone,
					"agentCode": {
						"doubleValue": representationData_agentCode
					},
					"cityCode": "",
					"cityName": representationData_cityName,
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": representationData_email,
					"indCompany": "true",
					"individualIdNbr": representationData_individualIdNbr,
					"individualIdType": representationData_individualIdType,
					"legalIdNbr": representationData_legalIdNbr,
					"legalIdType": representationData_legalIdType,
					"legalNature": representationData_legalNature,
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": representationData_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": representationData_personName,
					"personNameInOtherLang": representationData_personNameInOtherLang,
					"residenceCountryCode": representationData_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": representationData_telephone,
					"zipCode": representationData_zipCode
					},
					"representativeType": representationData_representativeType
				}
				}
			}
			} 
		else:
			udud = {
			"arg0": {
				"affectedDocumentId": {
				"docLog": affectedDocumentId_docLog,
				"docNbr": {
					"doubleValue": affectedDocumentId_docNbr
				},
				"docOrigin": affectedDocumentId_docOrigin,
				"docSeries": {
					"doubleValue": affectedDocumentId_docSeries
				},
				"selected": ""
				},
				"applicant": {
				"applicantNotes": applicant_applicantNotes,
				"person": {
					"addressStreet": person_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": person_cityName,
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": person_email,
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": person_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": person_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": person_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": person_telephone,
					"zipCode": person_zipCode
				}
				},
				"documentId": {
				"docLog": documentId_docLog,
				"docNbr": {
					"doubleValue": documentId_docNbr
				},
				"docOrigin": documentId_docOrigin,
				"docSeries": {
					"doubleValue": documentId_docSeries
				}
				},
				"documentSeqId": {
				"docSeqName": "Documentos",
				"docSeqNbr": {
					"doubleValue": documentSeqId_docSeqNbr
				},
				"docSeqSeries": {
					"doubleValue": documentSeqId_docSeqSeries
				},
				"docSeqType": documentSeqId_docSeqType
				},
				"filingData": {
				"applicationSubtype": "",
				"applicationType": "",
				"captureDate": {
					"dateValue": filingData_captureDate
				},
				"captureUserId": {
					"doubleValue": filingData_captureUserId
				},
				"corrFileNbr": "",
				"corrFileSeq": "",
				"corrFileSeries": "",
				"corrFileType": "",
				"externalOfficeCode": "",
				"externalOfficeFilingDate": "",
				"externalSystemId": "",
				"filingDate": {
					"dateValue": filingData_filingDate
				},
				"indIncorrRecpDeleted": "",
				"indManualInterpretationRequired": "false",
				"lawCode": "",
				"novelty1Date": "",
				"novelty2Date": "",

				"receptionDate": {
					"dateValue": filingData_receptionDate
				},
				"receptionDocument": {
					"documentEdmsData": {
					"edocDate": "",
					"edocId": "",
					"edocImageCertifDate": "",
					"edocImageCertifUser": "",
					"edocImageLinkingDate": "",
					"edocImageLinkingUser": "",
					"edocNbr": "",
					"edocSeq": "",
					"edocSer": "",
					"edocTyp": "",
					"edocTypeName": "",
					"efolderId": "",
					"efolderNbr": "",
					"efolderSeq": "",
					"efolderSer": "",
					"indInterfaceEdoc": "false",
					"indSpecificEdoc": "false"
					},
					"documentId": {
					"docLog": "E",
					"docNbr": {
						"doubleValue": receptionDocument_docNbr
					},
					"docOrigin": receptionDocument_docOrigin,
					"docSeries": {
						"doubleValue": receptionDocument_docSeries
					},
					"selected": ""
					},
					"documentSeqId": {
					"docSeqName": "",
					"docSeqNbr": "",
					"docSeqSeries": "",
					"docSeqType": ""
					},
					"externalSystemId": "",
					"inputDocumentData": "",
					"internalDocumentData": {
					"description": "",
					"offidocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
					},
					"refNo": ""
					},
					"outputDocumentData": {
					"officedocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
					}
					},
					"qtyPages": ""
				},
				"receptionUserId": "",
				"userdocTypeList": {
					"userdocName": userdocTypeList_userdocName,
					"userdocType": userdocTypeList_userdocType
				},
				"validationDate": "",
				"validationUserId": ""
				},
				"newOwnershipData": {
				"ownerList": {
					"orderNbr": {
					"doubleValue": ownerList_orderNbr
					},
					"ownershipNotes": ownerList_ownershipNotes,
					"person": {
					"addressStreet": ownerList_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": ownerList_cityName,
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": ownerList_email,
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": ownerList_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": ownerList_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": ownerList_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": ownerList_telephone,
					"zipCode": ownerList_zipCode
					}
				}
				},
				"notes": notes,
				"representationData": {
				"representativeList": {
					"indService": "false",
                    "person": {
					"addressStreet": representationData_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": representationData_addressZone,
					"agentCode": {
						"doubleValue": representationData_agentCode
					},
					"cityCode": "",
					"cityName": representationData_cityName,
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": representationData_email,
					"indCompany": "true",
					"individualIdNbr": representationData_individualIdNbr,
					"individualIdType": representationData_individualIdType,
					"legalIdNbr": representationData_legalIdNbr,
					"legalIdType": representationData_legalIdType,
					"legalNature": representationData_legalNature,
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": representationData_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": representationData_personName,
					"personNameInOtherLang": representationData_personNameInOtherLang,
					"residenceCountryCode": representationData_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": representationData_telephone,
					"zipCode": representationData_zipCode
					},
					"representativeType": representationData_representativeType
				}
				}
			}
			}
		return clientMark.service.UserdocUpdate(**udud)
	except zeep.exceptions.Fault as e:
		return(str(e))

#User_Doc_UpDate sin recibo
def user_doc_update_sin_recibo(
					affectedDocumentId_docLog,
					affectedDocumentId_docNbr,
					affectedDocumentId_docOrigin,
					affectedDocumentId_docSeries,
					applicant_applicantNotes,
					affectedDocumentId_selected,
					filingData_userdocTypeList_userdocType,
					applicant_person_addressStreet,
					applicant_person_cityName,
					applicant_person_email,
					applicant_person_nationalityCountryCode,
					applicant_person_personName,
					applicant_person_residenceCountryCode,
					applicant_person_telephone,
					applicant_person_zipCode,
					documentId_docLog,
					documentId_docNbr,
					documentId_docOrigin,
					documentId_docSeries,
					documentSeqId_docSeqNbr,
					documentSeqId_docSeqSeries,
					documentSeqId_docSeqType,
					filingData_captureDate,
					filingData_captureUserId,
					filingData_filingDate,
					filingData_receptionDate,
					filingData_receptionDocument_documentId_docLog,
					filingData_receptionDocument_documentId_docNbr,
					filingData_receptionDocument_documentId_docOrigin,
					filingData_receptionDocument_documentId_docSeries,
					filingData_receptionDocument_documentId_selected,
					filingData_userdocTypeList_userdocName,
					newOwnershipData_ownerList_orderNbr,
					newOwnershipData_ownerList_ownershipNotes,
					newOwnershipData_ownerList_addressStreet,
					newOwnershipData_ownerList_cityName,
					newOwnershipData_ownerList_email,
					newOwnershipData_ownerList_nationalityCountryCode,
					newOwnershipData_ownerList_personName,
					newOwnershipData_ownerList_residenceCountryCode,
					newOwnershipData_ownerList_telephone,
					newOwnershipData_ownerList_zipCode,
					notes,
					representationData_representativeList_person_addressStreet,
					representationData_representativeList_person_addressZone,
					representationData_representativeList_person_agentCode,
					representationData_representativeList_person_cityName,
					representationData_representativeList_person_email,
					representationData_representativeList_person_individualIdNbr,
					representationData_representativeList_person_individualIdType,
					representationData_representativeList_person_legalIdNbr,
					representationData_representativeList_person_legalIdType,    
					representationData_representativeList_person_legalNature,
					representationData_representativeList_person_nationalityCountryCode,
					representationData_representativeList_person_personName,
					representationData_representativeList_person_personNameInOtherLang,
					representationData_representativeList_person_residenceCountryCode,
					representationData_representativeList_person_telephone,
					representationData_representativeList_person_zipCode,
					representationData_representativeList_representativeType
					):
	udud = {
			"arg0": {
				"affectedDocumentId": {
				"docLog": affectedDocumentId_docLog,
				"docNbr": {
					"doubleValue": affectedDocumentId_docNbr
				},
				"docOrigin": affectedDocumentId_docOrigin,
				"docSeries": {
					"doubleValue": affectedDocumentId_docSeries
				},
				"selected": affectedDocumentId_selected
				},
				"applicant": {
				"applicantNotes": applicant_applicantNotes,
					"person": {
						"addressStreet": applicant_person_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": applicant_person_cityName,
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": applicant_person_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": applicant_person_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": applicant_person_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": applicant_person_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": applicant_person_telephone,
						"zipCode": applicant_person_zipCode
					}
				},
				"documentId": {
					"docLog": documentId_docLog,
					"docNbr": {
						"doubleValue": documentId_docNbr
					},
					"docOrigin": documentId_docOrigin,
					"docSeries": {
						"doubleValue": documentId_docSeries
					}
				},
				"documentSeqId": {
				"docSeqName": "Documentos",
				"docSeqNbr": {
					"doubleValue": documentSeqId_docSeqNbr
				},
				"docSeqSeries": {
					"doubleValue": documentSeqId_docSeqSeries
				},
				"docSeqType": documentSeqId_docSeqType
				},
				"filingData": {
					"applicationSubtype": "",
					"applicationType": "",
					"captureDate": {
						"dateValue": filingData_captureDate
					},
					"captureUserId": {
						"doubleValue": filingData_captureUserId
					},
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": {
						"dateValue": filingData_filingDate
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": "",
					"novelty1Date": "",
					"novelty2Date": "",
					"receptionDate": {
						"dateValue": filingData_receptionDate
					},
					"receptionDocument": {
						"documentEdmsData": {
						"edocDate": "",
						"edocId": "",
						"edocImageCertifDate": "",
						"edocImageCertifUser": "",
						"edocImageLinkingDate": "",
						"edocImageLinkingUser": "",
						"edocNbr": "",
						"edocSeq": "",
						"edocSer": "",
						"edocTyp": "",
						"edocTypeName": "",
						"efolderId": "",
						"efolderNbr": "",
						"efolderSeq": "",
						"efolderSer": "",
						"indInterfaceEdoc": "false",
						"indSpecificEdoc": "false"
						},
						"documentId": {
							"docLog": filingData_receptionDocument_documentId_docLog,
							"docNbr": {
								"doubleValue": filingData_receptionDocument_documentId_docNbr
							},
							"docOrigin": filingData_receptionDocument_documentId_docOrigin,
							"docSeries": {
								"doubleValue": filingData_receptionDocument_documentId_docSeries
							},
							"selected": filingData_receptionDocument_documentId_selected
						},
						"documentSeqId": {
						"docSeqName": "",
						"docSeqNbr": "",
						"docSeqSeries": "",
						"docSeqType": ""
						},
						"externalSystemId": "",
						"inputDocumentData": "",
						"internalDocumentData": {
						"description": "",
						"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						},
						"refNo": ""
						},
						"outputDocumentData": {
						"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						}
						},
						"qtyPages": ""
					},
					"receptionUserId": "",
					"userdocTypeList": {
						"userdocName": filingData_userdocTypeList_userdocName,
						"userdocType": filingData_userdocTypeList_userdocType
					},
					"validationDate": "",
					"validationUserId": ""
				},
				"newOwnershipData": {
					"ownerList": {
						"orderNbr": {
						"doubleValue": newOwnershipData_ownerList_orderNbr
						},
						"ownershipNotes": newOwnershipData_ownerList_ownershipNotes,
						"person": {
						"addressStreet": newOwnershipData_ownerList_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": newOwnershipData_ownerList_cityName,
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": newOwnershipData_ownerList_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": newOwnershipData_ownerList_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": newOwnershipData_ownerList_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": newOwnershipData_ownerList_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": newOwnershipData_ownerList_telephone,
						"zipCode": newOwnershipData_ownerList_zipCode
						}
					}
				},
				"notes": notes,
				"representationData": {
					"representativeList": {
						"indService": "false",
						"person": {
							"addressStreet": representationData_representativeList_person_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": representationData_representativeList_person_addressZone,
							"agentCode": {
								"doubleValue": representationData_representativeList_person_agentCode
							},
							"cityCode": "",
							"cityName": representationData_representativeList_person_cityName,
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": representationData_representativeList_person_email,
							"indCompany": "true",
							"individualIdNbr": representationData_representativeList_person_individualIdNbr,
							"individualIdType": representationData_representativeList_person_individualIdType,
							"legalIdNbr": representationData_representativeList_person_legalIdNbr,
							"legalIdType": representationData_representativeList_person_legalIdType,
							"legalNature": representationData_representativeList_person_legalNature,
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": representationData_representativeList_person_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": representationData_representativeList_person_personName,
							"personNameInOtherLang": representationData_representativeList_person_personNameInOtherLang,
							"residenceCountryCode": representationData_representativeList_person_residenceCountryCode,
							"stateCode": "",
							"stateName": "",
							"telephone": representationData_representativeList_person_telephone,
							"zipCode": representationData_representativeList_person_zipCode
							},
						"representativeType": representationData_representativeList_representativeType
					}
				}
			}
			} 
	return clientMark.service.UserdocUpdate(**udud)

#Agregar afectado
def user_doc_afectado(
		docLog,
		docNbr,
		docOrigin,
		docSeries,
		fileNbr,
		fileSeq,
		fileSeries,
		fileType):
	try:
		addexpafect = {
						"arg0": {
						"docLog": docLog,
						"docNbr": {
							"doubleValue": docNbr
						},
						"docOrigin": docOrigin,
						"docSeries": {
							"doubleValue": docSeries
						},
						"selected": "true"
						},
						"arg1": {
						"fileNbr": {
							"doubleValue": fileNbr
						},
						"fileSeq": fileSeq,
						"fileSeries": {
							"doubleValue": fileSeries
						},
						"fileType": fileType
						}
					}		
		return clientMark.service.UserdocAddAffectedFile(**addexpafect)
	except zeep.exceptions.Fault as e:
		return(e)

#--------------------------------------------------------------- Patentes ----------------------------------------------------------------------------------------------
#userDoc por expediente
def patent_user_doc_getlist_expediente(docNbrFrom, docNbrTo): # {'docNbrFrom': {'doubleValue':'21108884',},'docNbrTo': {'doubleValue':'21108884'}}
	UserdocGetList = {'arg0': {'criteriaDocumentId': {'docNbrFrom': {'doubleValue':docNbrFrom,},'docNbrTo': {'doubleValue':docNbrTo}},},}
	return clientPatents.service.UserdocGetList(**UserdocGetList)

#GetList por expediente
def patent_getlist(fileNbrFrom, fileNbrTo): # {'doubleValue':'9044393',},'fileNbrTo': {'doubleValue':'9044393'}
	try:    
		patenGetList = {'arg0': {'criteriaFileId': {'fileNbrFrom': {'doubleValue':fileNbrFrom,},'fileNbrTo': {'doubleValue':fileNbrTo}},},}
		return clientPatents.service.PatentGetList(**patenGetList)
	except zeep.exceptions.Fault as e:
		print(e)

#GetList por expediente
def disenio_getlist(fileNbrFrom, fileNbrTo): # {'doubleValue':'9044393',},'fileNbrTo': {'doubleValue':'9044393'}
	patenGetList = {'arg0': {'criteriaFileId': {'fileNbrFrom': {'doubleValue':fileNbrFrom,},'fileNbrTo': {'doubleValue':fileNbrTo}},},}
	return clientDisenio.service.PatentGetList(**patenGetList)

#GetList por fecha
def patent_getlist_fecha(filingDateFrom, filingDateTo):
	GetList = {
					"arg0": {
						"criteriaFilingData": {
						"filingDateFrom": {
							"dateValue": filingDateFrom+"T00:00:00-04:00"
						},
						"filingDateTo": {
							"dateValue": filingDateTo+"T23:59:59-04:00"
						}
						}
					}
					}
	return clientPatents.service.PatentGetList(**GetList)

#UserDocGetList por fecha (Patente)
def patent_user_doc_getlist_fecha(filingDateFrom,filingDateTo):
	pudgf = {
			"arg0": {
				"criteriaUserdocFilingData": {
				"filingDateFrom": {
					"dateValue": filingDateFrom+"T00:00:00-04:00"
				},
				"filingDateTo": {
					"dateValue": filingDateTo+"T23:59:59-04:00"
				}
				}
			}
			}
	return clientPatents.service.UserdocGetList(**pudgf)

#user doc get list diseñio por docNbr
def disenio_user_doc_getlist_docNbr(docNbrFrom, docNbrTo): # {'docNbrFrom': {'doubleValue':'21108884',},'docNbrTo': {'doubleValue':'21108884'}}
	UserdocGetList = { "arg0": { "criteriaDocumentId": { "docNbrFrom": { "doubleValue": docNbrFrom }, "docNbrTo": {"doubleValue": docNbrFrom }}}}
	return clientDisenio.service.UserdocGetList(**UserdocGetList)

def disenio_read(fileNbr,fileSeq,fileSeries,fileType):
	read = {'arg0': {'fileNbr': {'doubleValue': fileNbr,},'fileSeq': fileSeq,'fileSeries': {'doubleValue': fileSeries, },'fileType': fileType, }, 'arg1':'?', 'arg2':'?',	}
	return clientDisenio.service.PatentRead(**read)

#GetList por expediente
def disenio_getlist(fileNbrFrom, fileNbrTo): # {'doubleValue':'9044393',},'fileNbrTo': {'doubleValue':'9044393'}
	patenGetList = {'arg0': {'criteriaFileId': {'fileNbrFrom': {'doubleValue':fileNbrFrom,},'fileNbrTo': {'doubleValue':fileNbrTo}},},}
	return clientDisenio.service.PatentGetList(**patenGetList)

#GetList por fecha
def disenio_getlist_fecha(filingDateFrom, filingDateTo):
	GetList = {
					"arg0": {
						"criteriaFilingData": {
						"filingDateFrom": {
							"dateValue": filingDateFrom+"T00:00:00-04:00"
						},
						"filingDateTo": {
							"dateValue": filingDateTo+"T23:59:59-04:00"
						}
						}
					}
					}
	return clientDisenio.service.PatentGetList(**GetList)

#UserDocGetList por fecha
def disenio_user_doc_getlist_fecha(filingDateFrom,filingDateTo):
	pudgf = {
			"arg0": {
				"criteriaUserdocFilingData": {
				"filingDateFrom": {
					"dateValue": filingDateFrom+"T00:00:00-04:00"
				},
				"filingDateTo": {
					"dateValue": filingDateTo+"T23:59:59-04:00"
				}
				}
			}
			}
	return clientDisenio.service.UserdocGetList(**pudgf)

# creado 23-10-2022 por meet (probando) (AG)
def insert_disenio_registro(
							authorList_addressStreet,
							authorList_nationalityCountryCode,
							authorList_personName,
							authorList_residenceCountryCode,
							authorList_stateCode,
							authorList_stateName,
							authorList_telephone,
							authorList_zipCode,
							file_fileNbr,
							file_fileSeq,
							file_fileSeries,
							file_fileType,
							filingData_applicationSubtype,
							filingData_applicationType,
							filingData_captureDate,
							filingData_captureUserId,
							filingData_filingDate,
							lawCode,
							filingData_novelty1Date,
							filingData_novelty2Date,
							filingData_currencyName,
							filingData_currencyType,
							filingData_receiptAmount,
							filingData_receiptDate,
							filingData_receiptNbr,
							filingData_receiptNotes,
							filingData_receiptType,
							filingData_receiptTypeName,
							filingData_receptionDate,
							documentId_docLog,
							documentId_docNbr,
							documentId_docOrigin,
							documentId_docSeries,
							notes,
							person_addressStreet,
							person_email,
							person_nationalityCountryCode,
							person_personName,
							person_residenceCountryCode,
							person_stateCode,
							person_stateName,
							person_telephone,
							person_zipCode,
							processId_processNbr,
							processId_processType,
							representativeList_addressStreet,
							representativeList_agentCode,
							representativeList_email,
							representativeList_individualIdNbr,
							representativeList_individualIdType,
							representativeList_legalIdNbr,
							representativeList_legalIdType,
							representativeList_nationalityCountryCode,
							representativeList_personName,
							representativeList_residenceCountryCode,
							representativeList_telephone,
							representativeType,
							rowVersion,
							title):
	principal = {"arg0": {
					"authorshipData": {
					"authorList": {
						"authorSeq": "",
						"person": {
						"addressStreet": authorList_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": authorList_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": authorList_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": authorList_residenceCountryCode,
						"stateCode": authorList_stateCode,
						"stateName": authorList_stateName,
						"telephone": authorList_telephone,
						"zipCode": authorList_zipCode
						}
					},
					"indOwnerSameAuthor": "false"
					},
					"file": {
					"fileId": {
						"fileNbr": {
						"doubleValue": file_fileNbr
						},
						"fileSeq": file_fileSeq,
						"fileSeries": {
						"doubleValue": file_fileSeries
						},
						"fileType": file_fileType
					},
					"filingData": {
						"applicationSubtype": filingData_applicationSubtype,
						"applicationType": filingData_applicationType,
						"captureDate": {
						"dateValue": filingData_captureDate
						},
						"captureUserId": {
						"doubleValue": filingData_captureUserId
						},
						"corrFileNbr": "",
						"corrFileSeq": "",
						"corrFileSeries": "",
						"corrFileType": "",
						"externalOfficeCode": "",
						"externalOfficeFilingDate": "",
						"externalSystemId": "",
						"filingDate": {
						"dateValue": filingData_filingDate
						},
						"indIncorrRecpDeleted": "",
						"indManualInterpretationRequired": "false",
						"lawCode": {
						"doubleValue": lawCode
						},
						"novelty1Date": {
						"dateValue": filingData_novelty1Date
						},
						"novelty2Date": {
						"dateValue": filingData_novelty2Date
						},
						"paymentList": {
						"currencyName": filingData_currencyName,
						"currencyType": filingData_currencyType,
						"receiptAmount": filingData_receiptAmount,
						"receiptDate": {
							"dateValue": filingData_receiptDate
						},
						"receiptNbr": filingData_receiptNbr,
						"receiptNotes": filingData_receiptNotes,
						"receiptType": filingData_receiptType,
						"receiptTypeName": filingData_receiptTypeName
						},
						"receptionDate": {
						"dateValue": filingData_receptionDate
						},
						"receptionDocument": {
						"documentEdmsData": {
							"edocDate": "",
							"edocId": "",
							"edocImageCertifDate": "",
							"edocImageCertifUser": "",
							"edocImageLinkingDate": "",
							"edocImageLinkingUser": "",
							"edocNbr": "",
							"edocSeq": "",
							"edocSer": "",
							"edocTyp": "",
							"edocTypeName": "",
							"efolderId": "",
							"efolderNbr": "",
							"efolderSeq": "",
							"efolderSer": "",
							"indInterfaceEdoc": "false",
							"indSpecificEdoc": "false"
						},
						"documentId": {
							"docLog": documentId_docLog,
							"docNbr": {
							"doubleValue": documentId_docNbr
							},
							"docOrigin": documentId_docOrigin,
							"docSeries": {
							"doubleValue": documentId_docSeries
							},
							"selected": ""
						},
						"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
							"dataCodeId1": "",
							"dataCodeId2": "",
							"dataCodeId3": "",
							"dataCodeId4": "",
							"dataCodeId5": "",
							"dataCodeName1": "",
							"dataCodeName2": "",
							"dataCodeName3": "",
							"dataCodeName4": "",
							"dataCodeName5": "",
							"dataCodeTyp1": "",
							"dataCodeTyp2": "",
							"dataCodeTyp3": "",
							"dataCodeTyp4": "",
							"dataCodeTyp5": "",
							"dataCodeTypeName1": "",
							"dataCodeTypeName2": "",
							"dataCodeTypeName3": "",
							"dataCodeTypeName4": "",
							"dataCodeTypeName5": "",
							"dataDate1": "",
							"dataDate2": "",
							"dataDate3": "",
							"dataDate4": "",
							"dataDate5": "",
							"dataFlag1": "false",
							"dataFlag2": "false",
							"dataFlag3": "false",
							"dataFlag4": "false",
							"dataFlag5": "false",
							"dataNbr1": "",
							"dataNbr2": "",
							"dataNbr3": "",
							"dataNbr4": "",
							"dataNbr5": "",
							"dataText1": "",
							"dataText2": "",
							"dataText3": "",
							"dataText4": "",
							"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
							"description": "",
							"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							},
							"refNo": ""
						},
						"outputDocumentData": {
							"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							}
						},
						"qtyPages": ""
						},
						"receptionUserId": "",
						"validationDate": "",
						"validationUserId": ""
					},
					"notes": notes,
					"ownershipData": {
						"dummy": "",
						"ownerList": {
						"indService": "true",
						"orderNbr": "",
						"ownershipNotes": "",
						"person": {
							"addressStreet": person_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": person_email,
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": person_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": person_personName,
							"personNameInOtherLang": "",
							"residenceCountryCode": person_residenceCountryCode,
							"stateCode": person_stateCode,
							"stateName": person_stateName,
							"telephone": person_telephone,
							"zipCode": person_zipCode
						}
						}
					},
					"priorityData": {
						"earliestAcceptedParisPriorityDate": "",
						"exhibitionDate": "",
						"exhibitionNotes": ""
					},
					"processId": {
						"processNbr": {
						"doubleValue": processId_processNbr
						},
						"processType": processId_processType
					},
					"publicationData": {
						"journalCode": "",
						"publicationDate": "",
						"publicationNotes": "",
						"specialPublicationDate": "",
						"specialPublicationRequestDate": ""
					},
					"registrationData": {
						"entitlementDate": "",
						"expirationDate": "",
						"indRegistered": "false",
						"registrationDate": "",
						"registrationId": {
						"registrationDup": "",
						"registrationNbr": "",
						"registrationSeries": "",
						"registrationType": ""
						}
					},
					"representationData": {
						"documentId_PowerOfAttorneyRegister": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
						},
						"referencedPOAData": {
						"documentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"poaDate": "",
						"poaGrantor": {
							"person": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
							}
						},
						"poaRegNumber": "",
						"scope": ""
						},
						"representativeList": {
						"indService": "true",
                        "person": {
                            "addressStreet": representativeList_addressStreet,
                            "addressStreetInOtherLang": "",
                            "addressZone": "",
                            "agentCode": {
                            "doubleValue": representativeList_agentCode
                            },
                            "cityCode": "",
                            "cityName": "",
                            "companyRegisterRegistrationDate": "",
                            "companyRegisterRegistrationNbr": "",
                            "email": representativeList_email,
                            "indCompany": "false",
                            "individualIdNbr": representativeList_individualIdNbr,
                            "individualIdType": representativeList_individualIdType,
                            "legalIdNbr": representativeList_legalIdNbr,
                            "legalIdType": representativeList_legalIdType,
                            "legalNature": "",
                            "legalNatureInOtherLang": "",
                            "nationalityCountryCode": representativeList_nationalityCountryCode,
                            "personGroupCode": "",
                            "personGroupName": "",
                            "personName": representativeList_personName,
                            "personNameInOtherLang": "",
                            "residenceCountryCode": representativeList_residenceCountryCode,
                            "stateCode": "",
                            "stateName": "",
                            "telephone": representativeList_telephone,
                            "zipCode": ""
                        },
						"representativeType": representativeType
						}
					},
					"rowVersion": "",
					"stateValidityData": {
						"dummy": ""
					}
					},
					"indReadDrawingList": "false",
					"indReadWordfileTitle": "false",
					"patentContainsDrawingList": "false",
					"patentContainsWordfileTitle": "true",
					"patentExaminationData": {
					"examResult": "",
					"indExamIndustrial": "false",
					"indExamInventive": "false",
					"indExamNovelty": "false",
					"usedIpcDescription": "",
					"usedKeywordDescription": ""
					},
					"pctApplicationData": {
					"pctApplicationDate": "",
					"pctApplicationId": "",
					"pctPhase": "",
					"pctPublicationCountryCode": "",
					"pctPublicationDate": "",
					"pctPublicationId": "",
					"pctPublicationType": ""
					},
					"regionalApplData": {
					"regionalApplDate": "",
					"regionalApplId": "",
					"regionalPublCountry": "",
					"regionalPublDate": "",
					"regionalPublId": "",
					"regionalPublType": ""
					},
					"rowVersion": {
					"doubleValue": rowVersion
					},
					"technicalData": {
					"englishAbstract": "",
					"englishTitle": "",
					"hasCpc": "false",
					"hasIpc": "false",
					"lastClaimsPageRef": "",
					"lastDescriptionPageRef": "",
					"mainAbstract": "",
					"noveltyDate": "",
					"title": title
					} } }
	try: 
		clientDisenio.service.PatentInsert(**principal)
		return('true')
	except zeep.exceptions.Fault as e:
		return(str(e))

# creado 23-10-2022 por meet (probando) (AG)
def insert_disenio_renovacion(
							authorList_addressStreet,
							authorList_nationalityCountryCode,
							authorList_personName,
							authorList_residenceCountryCode,
							authorList_stateCode,
							authorList_stateName,
							authorList_telephone,
							authorList_zipCode,
							file_fileNbr,
							file_fileSeq,
							file_fileSeries,
							file_fileType,
							filingData_applicationSubtype,
							filingData_applicationType,
							filingData_captureDate,
							filingData_captureUserId,
							filingData_filingDate,
							lawCode,
							filingData_novelty1Date,
							filingData_novelty2Date,
							filingData_currencyName,
							filingData_currencyType,
							filingData_receiptAmount,
							filingData_receiptDate,
							filingData_receiptNbr,
							filingData_receiptNotes,
							filingData_receiptType,
							filingData_receiptTypeName,
							filingData_receptionDate,
							documentId_docLog,
							documentId_docNbr,
							documentId_docOrigin,
							documentId_docSeries,
							notes,
							person_addressStreet,
							person_email,
							person_nationalityCountryCode,
							person_personName,
							person_residenceCountryCode,
							person_stateCode,
							person_stateName,
							person_telephone,
							person_zipCode,
							processId_processNbr,
							processId_processType,
							relationshipList_fileNbr,
							relationshipList_fileSeq,
							relationshipList_fileSeries,
							relationshipList_fileType,
							relationshipList_relationshipRole,
							relationshipList_relationshipType,
							representativeList_addressStreet,
							representativeList_agentCode,
							representativeList_email,
							representativeList_individualIdNbr,
							representativeList_individualIdType,
							representativeList_legalIdNbr,
							representativeList_legalIdType,
							representativeList_nationalityCountryCode,
							representativeList_personName,
							representativeList_residenceCountryCode,
							representativeList_telephone,
							representativeType,
							rowVersion,
							title):
	principal = {"arg0": {
					"authorshipData": {
					"authorList": {
						"authorSeq": "",
						"person": {
						"addressStreet": authorList_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": authorList_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": authorList_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": authorList_residenceCountryCode,
						"stateCode": authorList_stateCode,
						"stateName": authorList_stateName,
						"telephone": authorList_telephone,
						"zipCode": authorList_zipCode
						}
					},
					"indOwnerSameAuthor": "false"
					},
					"file": {
					"fileId": {
						"fileNbr": {
						"doubleValue": file_fileNbr
						},
						"fileSeq": file_fileSeq,
						"fileSeries": {
						"doubleValue": file_fileSeries
						},
						"fileType": file_fileType
					},
					"filingData": {
						"applicationSubtype": filingData_applicationSubtype,
						"applicationType": filingData_applicationType,
						"captureDate": {
						"dateValue": filingData_captureDate
						},
						"captureUserId": {
						"doubleValue": filingData_captureUserId
						},
						"corrFileNbr": "",
						"corrFileSeq": "",
						"corrFileSeries": "",
						"corrFileType": "",
						"externalOfficeCode": "",
						"externalOfficeFilingDate": "",
						"externalSystemId": "",
						"filingDate": {
						"dateValue": filingData_filingDate
						},
						"indIncorrRecpDeleted": "",
						"indManualInterpretationRequired": "false",
						"lawCode": {
						"doubleValue": lawCode
						},
						"novelty1Date": {
						"dateValue": filingData_novelty1Date
						},
						"novelty2Date": {
						"dateValue": filingData_novelty2Date
						},
						"paymentList": {
						"currencyName": filingData_currencyName,
						"currencyType": filingData_currencyType,
						"receiptAmount": filingData_receiptAmount,
						"receiptDate": {
							"dateValue": filingData_receiptDate
						},
						"receiptNbr": filingData_receiptNbr,
						"receiptNotes": filingData_receiptNotes,
						"receiptType": filingData_receiptType,
						"receiptTypeName": filingData_receiptTypeName
						},
						"receptionDate": {
						"dateValue": filingData_receptionDate
						},
						"receptionDocument": {
						"documentEdmsData": {
							"edocDate": "",
							"edocId": "",
							"edocImageCertifDate": "",
							"edocImageCertifUser": "",
							"edocImageLinkingDate": "",
							"edocImageLinkingUser": "",
							"edocNbr": "",
							"edocSeq": "",
							"edocSer": "",
							"edocTyp": "",
							"edocTypeName": "",
							"efolderId": "",
							"efolderNbr": "",
							"efolderSeq": "",
							"efolderSer": "",
							"indInterfaceEdoc": "false",
							"indSpecificEdoc": "false"
						},
						"documentId": {
							"docLog": documentId_docLog,
							"docNbr": {
							"doubleValue": documentId_docNbr
							},
							"docOrigin": documentId_docOrigin,
							"docSeries": {
							"doubleValue": documentId_docSeries
							},
							"selected": ""
						},
						"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
							"dataCodeId1": "",
							"dataCodeId2": "",
							"dataCodeId3": "",
							"dataCodeId4": "",
							"dataCodeId5": "",
							"dataCodeName1": "",
							"dataCodeName2": "",
							"dataCodeName3": "",
							"dataCodeName4": "",
							"dataCodeName5": "",
							"dataCodeTyp1": "",
							"dataCodeTyp2": "",
							"dataCodeTyp3": "",
							"dataCodeTyp4": "",
							"dataCodeTyp5": "",
							"dataCodeTypeName1": "",
							"dataCodeTypeName2": "",
							"dataCodeTypeName3": "",
							"dataCodeTypeName4": "",
							"dataCodeTypeName5": "",
							"dataDate1": "",
							"dataDate2": "",
							"dataDate3": "",
							"dataDate4": "",
							"dataDate5": "",
							"dataFlag1": "false",
							"dataFlag2": "false",
							"dataFlag3": "false",
							"dataFlag4": "false",
							"dataFlag5": "false",
							"dataNbr1": "",
							"dataNbr2": "",
							"dataNbr3": "",
							"dataNbr4": "",
							"dataNbr5": "",
							"dataText1": "",
							"dataText2": "",
							"dataText3": "",
							"dataText4": "",
							"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
							"description": "",
							"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							},
							"refNo": ""
						},
						"outputDocumentData": {
							"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							}
						},
						"qtyPages": ""
						},
						"receptionUserId": "",
						"validationDate": "",
						"validationUserId": ""
					},
					"notes": notes,
					"ownershipData": {
						"dummy": "",
						"ownerList": {
						"indService": "true",
						"orderNbr": "",
						"ownershipNotes": "",
						"person": {
							"addressStreet": person_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": person_email,
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": person_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": person_personName,
							"personNameInOtherLang": "",
							"residenceCountryCode": person_residenceCountryCode,
							"stateCode": person_stateCode,
							"stateName": person_stateName,
							"telephone": person_telephone,
							"zipCode": person_zipCode
						}
						}
					},
					"priorityData": {
						"earliestAcceptedParisPriorityDate": "",
						"exhibitionDate": "",
						"exhibitionNotes": ""
					},
					"processId": {
						"processNbr": {
						"doubleValue": processId_processNbr
						},
						"processType": processId_processType
					},
					"publicationData": {
						"journalCode": "",
						"publicationDate": "",
						"publicationNotes": "",
						"specialPublicationDate": "",
						"specialPublicationRequestDate": ""
					},
					"registrationData": {
						"entitlementDate": "",
						"expirationDate": "",
						"indRegistered": "false",
						"registrationDate": "",
						"registrationId": {
						"registrationDup": "",
						"registrationNbr": "",
						"registrationSeries": "",
						"registrationType": ""
						}
					},
					"relationshipList": {
						"fileId": {
						"fileNbr": {
							"doubleValue": relationshipList_fileNbr #1662008
						},
						"fileSeq": relationshipList_fileSeq, #"PY",
						"fileSeries": {
							"doubleValue": relationshipList_fileSeries #2016
						},
						"fileType": relationshipList_fileType #"P"
						},
						"relationshipRole": relationshipList_relationshipRole, #1,
						"relationshipType": relationshipList_relationshipType #"REN"
					},
					"representationData": {
						"documentId_PowerOfAttorneyRegister": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
						},
						"referencedPOAData": {
						"documentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"poaDate": "",
						"poaGrantor": {
							"person": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
							}
						},
						"poaRegNumber": "",
						"scope": ""
						},
						"representativeList": {
						"indService": "true",
                        "person": {
                            "addressStreet": representativeList_addressStreet,
                            "addressStreetInOtherLang": "",
                            "addressZone": "",
                            "agentCode": {
                            "doubleValue": representativeList_agentCode
                            },
                            "cityCode": "",
                            "cityName": "",
                            "companyRegisterRegistrationDate": "",
                            "companyRegisterRegistrationNbr": "",
                            "email": representativeList_email,
                            "indCompany": "false",
                            "individualIdNbr": representativeList_individualIdNbr,
                            "individualIdType": representativeList_individualIdType,
                            "legalIdNbr": representativeList_legalIdNbr,
                            "legalIdType": representativeList_legalIdType,
                            "legalNature": "",
                            "legalNatureInOtherLang": "",
                            "nationalityCountryCode": representativeList_nationalityCountryCode,
                            "personGroupCode": "",
                            "personGroupName": "",
                            "personName": representativeList_personName,
                            "personNameInOtherLang": "",
                            "residenceCountryCode": representativeList_residenceCountryCode,
                            "stateCode": "",
                            "stateName": "",
                            "telephone": representativeList_telephone,
                            "zipCode": ""
                        },
						"representativeType": representativeType
						}
					},
					"rowVersion": "",
					"stateValidityData": {
						"dummy": ""
					}
					},
					"indReadDrawingList": "false",
					"indReadWordfileTitle": "false",
					"patentContainsDrawingList": "false",
					"patentContainsWordfileTitle": "true",
					"patentExaminationData": {
					"examResult": "",
					"indExamIndustrial": "false",
					"indExamInventive": "false",
					"indExamNovelty": "false",
					"usedIpcDescription": "",
					"usedKeywordDescription": ""
					},
					"pctApplicationData": {
					"pctApplicationDate": "",
					"pctApplicationId": "",
					"pctPhase": "",
					"pctPublicationCountryCode": "",
					"pctPublicationDate": "",
					"pctPublicationId": "",
					"pctPublicationType": ""
					},
					"regionalApplData": {
					"regionalApplDate": "",
					"regionalApplId": "",
					"regionalPublCountry": "",
					"regionalPublDate": "",
					"regionalPublId": "",
					"regionalPublType": ""
					},
					"rowVersion": {
					"doubleValue": rowVersion
					},
					"technicalData": {
					"englishAbstract": "",
					"englishTitle": "",
					"hasCpc": "false",
					"hasIpc": "false",
					"lastClaimsPageRef": "",
					"lastDescriptionPageRef": "",
					"mainAbstract": "",
					"noveltyDate": "",
					"title": title
					} } }
	try: 
		clientDisenio.service.PatentInsert(**principal)
		return('true')
	except zeep.exceptions.Fault as e:
		return(str(e))

# creado 23-10-2022 por meet (probando) (AG_patent)
def Patent_insert_documento_principal(
									file_fileNbr,
									file_fileSeq,
									file_fileSeries,
									file_fileType,
									filingData_applicationSubtype,
									filingData_applicationType,
									filingData_captureDate,
									filingData_captureUserId,
									filingData_filingDate,
									filingData_lawCode,
									filingData_novelty1Date,
									filingData_novelty2Date,
									paymentList_currencyName,
									paymentList_currencyType,
									paymentList_receiptAmount,
									paymentList_receiptDate,
									paymentList_receiptNbr,
									paymentList_receiptNotes,
									paymentList_receiptType,
									paymentList_receiptTypeName,
									filingData_receptionDate,
									notes,
									ownershipData_orderNbr,
									ownershipNotes_addressStreet,
									ownershipData_nationalityCountryCode,
									ownershipData_personName,
									ownershipData_residenceCountryCode,
									ownershipData_email,
									ownershipData_telephone,
									ownershipData_zipCode,
									representativeList_addressStreet,
									representativeList_agentCode,
									representativeList_nationalityCountryCode,
									representativeList_personName,
									representativeList_residenceCountryCode,
									representativeList_representativeType,
									representativeList_email,
									representativeList_telephone,
									representativeList_zipCode,
									rowVersion,
									title):
	try:
		inpare = {
				"arg0": {
					"file": {
					"fileId": {
						"fileNbr": {
						"doubleValue": file_fileNbr
						},
						"fileSeq": file_fileSeq,
						"fileSeries": {
						"doubleValue": file_fileSeries
						},
						"fileType": file_fileType
					},
					"filingData": {
						"applicationSubtype": filingData_applicationSubtype,
						"applicationType": filingData_applicationType,
						"captureDate": {
						"dateValue": filingData_captureDate
						},
						"captureUserId": {
						"doubleValue": filingData_captureUserId
						},
						"corrFileNbr": "",
						"corrFileSeq": "",
						"corrFileSeries": "",
						"corrFileType": "",
						"externalOfficeCode": "",
						"externalOfficeFilingDate": "",
						"externalSystemId": "",
						"filingDate": {
						"dateValue": filingData_filingDate
						},
						"indIncorrRecpDeleted": "",
						"indManualInterpretationRequired": "false",
						"lawCode": {
						"doubleValue": filingData_lawCode
						},
						"novelty1Date": {
						"dateValue": filingData_novelty1Date
						},
						"novelty2Date": {
						"dateValue": filingData_novelty2Date
						},
						"paymentList": {
						"currencyName": paymentList_currencyName,
						"currencyType": paymentList_currencyType,
						"receiptAmount": paymentList_receiptAmount,
						"receiptDate": {
							"dateValue": paymentList_receiptDate
						},
						"receiptNbr": paymentList_receiptNbr,
						"receiptNotes": paymentList_receiptNotes,
						"receiptType": paymentList_receiptType,
						"receiptTypeName": paymentList_receiptTypeName
						},
						"receptionDate": {
						"dateValue": filingData_receptionDate
						},
						"receptionDocument": {
						"documentEdmsData": {
							"edocDate": "",
							"edocId": "",
							"edocImageCertifDate": "",
							"edocImageCertifUser": "",
							"edocImageLinkingDate": "",
							"edocImageLinkingUser": "",
							"edocNbr": "",
							"edocSeq": "",
							"edocSer": "",
							"edocTyp": "",
							"edocTypeName": "",
							"efolderId": "",
							"efolderNbr": "",
							"efolderSeq": "",
							"efolderSer": "",
							"indInterfaceEdoc": "false",
							"indSpecificEdoc": "false"
						},
						"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
							"dataCodeId1": "",
							"dataCodeId2": "",
							"dataCodeId3": "",
							"dataCodeId4": "",
							"dataCodeId5": "",
							"dataCodeName1": "",
							"dataCodeName2": "",
							"dataCodeName3": "",
							"dataCodeName4": "",
							"dataCodeName5": "",
							"dataCodeTyp1": "",
							"dataCodeTyp2": "",
							"dataCodeTyp3": "",
							"dataCodeTyp4": "",
							"dataCodeTyp5": "",
							"dataCodeTypeName1": "",
							"dataCodeTypeName2": "",
							"dataCodeTypeName3": "",
							"dataCodeTypeName4": "",
							"dataCodeTypeName5": "",
							"dataDate1": "",
							"dataDate2": "",
							"dataDate3": "",
							"dataDate4": "",
							"dataDate5": "",
							"dataFlag1": "false",
							"dataFlag2": "false",
							"dataFlag3": "false",
							"dataFlag4": "false",
							"dataFlag5": "false",
							"dataNbr1": "",
							"dataNbr2": "",
							"dataNbr3": "",
							"dataNbr4": "",
							"dataNbr5": "",
							"dataText1": "",
							"dataText2": "",
							"dataText3": "",
							"dataText4": "",
							"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
							"description": "",
							"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							},
							"refNo": ""
						},
						"outputDocumentData": {
							"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							}
						},
						"qtyPages": ""
						},
						"receptionUserId": "",
						"validationDate": "",
						"validationUserId": ""
					},
					"notes": notes,
					"ownershipData": {
						"dummy": "",
						"ownerList": {
						"indService": "true",
						"orderNbr": {
							"doubleValue": ownershipData_orderNbr
						},
						"ownershipNotes": "",
						"person": {
							"addressStreet": ownershipNotes_addressStreet,
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": ownershipData_email,
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": ownershipData_nationalityCountryCode,
							"personGroupCode": "",
							"personGroupName": "",
							"personName": ownershipData_personName,
							"personNameInOtherLang": "",
							"residenceCountryCode": ownershipData_residenceCountryCode,
							"stateCode": "",
							"stateName": "",
							"telephone": ownershipData_telephone,
							"zipCode": ownershipData_zipCode
						}
						}
					},
					"priorityData": "",
					"processId": "",
					"publicationData": {
						"journalCode": "",
						"publicationDate": "",
						"publicationNotes": "",
						"specialPublicationDate": "",
						"specialPublicationRequestDate": ""
					},
					"registrationData": {
						"entitlementDate": "",
						"expirationDate": "",
						"indRegistered": "false",
						"registrationDate": "",
						"registrationId": {
						"registrationDup": "",
						"registrationNbr": "",
						"registrationSeries": "",
						"registrationType": ""
						}
					},
					"representationData": {
						"documentId_PowerOfAttorneyRegister": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
						},
						"referencedPOAData": {
						"documentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"poaDate": "",
						"poaGrantor": {
							"person": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
							}
						},
						"poaRegNumber": "",
						"scope": ""
						},
						"representativeList": {
						"indService": "true",
                        "person": {
                            "addressStreet": representativeList_addressStreet,
                            "addressStreetInOtherLang": "",
                            "addressZone": "",
                            "agentCode": {
                            "doubleValue": representativeList_agentCode
                            },
                            "cityCode": "",
                            "cityName": "",
                            "companyRegisterRegistrationDate": "",
                            "companyRegisterRegistrationNbr": "",
                            "email": representativeList_email,
                            "indCompany": "false",
                            "individualIdNbr": "",
                            "individualIdType": "",
                            "legalIdNbr": "",
                            "legalIdType": "",
                            "legalNature": "",
                            "legalNatureInOtherLang": "",
                            "nationalityCountryCode": representativeList_nationalityCountryCode,
                            "personGroupCode": "",
                            "personGroupName": "",
                            "personName": representativeList_personName,
                            "personNameInOtherLang": "",
                            "residenceCountryCode": representativeList_residenceCountryCode,
                            "stateCode": "",
                            "stateName": "",
                            "telephone": representativeList_telephone,
                            "zipCode": representativeList_zipCode
                        },
						"representativeType": representativeList_representativeType
						}
					},
					"rowVersion": "",
					"stateValidityData": {
						"dummy": ""
					}
					},
					"indReadDrawingList": "false",
					"indReadWordfileTitle": "false",
					"patentContainsDrawingList": "false",
					"patentContainsWordfileTitle": "true",
					"patentExaminationData": {
					"examResult": "",
					"indExamIndustrial": "false",
					"indExamInventive": "false",
					"indExamNovelty": "false",
					"usedIpcDescription": "",
					"usedKeywordDescription": ""
					},
					"pctApplicationData": {
					"pctApplicationDate": "",
					"pctApplicationId": "",
					"pctPhase": "",
					"pctPublicationCountryCode": "",
					"pctPublicationDate": "",
					"pctPublicationId": "",
					"pctPublicationType": ""
					},
					"regionalApplData": {
					"regionalApplDate": "",
					"regionalApplId": "",
					"regionalPublCountry": "",
					"regionalPublDate": "",
					"regionalPublId": "",
					"regionalPublType": ""
					},
					"rowVersion": {
					"doubleValue": rowVersion
					},
					"technicalData": {
					"englishAbstract": "",
					"englishTitle": "",
					"hasCpc": "false",
					"hasIpc": "false",
					"lastClaimsPageRef": "",
					"lastDescriptionPageRef": "",
					"mainAbstract": "",
					"noveltyDate": "",
					"title": title,
					}
				  }
				}
		clientPatents.service.PatentInsert(**inpare)
		return('true')
	except zeep.exceptions.Fault as e:
		return(str(e))

# creado 25-10-2022 por meet (probando) (AG)
def user_doc_insert_patent_sin_pago_relacionado(
												affectedFileIdList_fileNbr,
												affectedFileIdList_fileSeq,
												affectedFileIdList_fileSeries,
												affectedFileIdList_fileType,
												affectedFileSummaryList_fileNbr,
												affectedFileSummaryList_fileSeq,
												affectedFileSummaryList_fileSeries,
												affectedFileSummaryList_fileType,
												fileSummaryDescription,
												fileSummaryOwner,
												applicant_addressStreet,
												applicant_personName,
												applicant_residenceCountryCode,
												applicant_nationalityCountryCode,
												applicant_email,
												applicant_telephone,
												applicant_zipCode,
												documentId_docLog,
												documentId_docNbr,
												documentId_docOrigin,
												documentId_docSeries,
												documentSeqId_docSeqName,
												documentSeqId_docSeqNbr,
												documentSeqId_docSeqSeries,
												documentSeqId_docSeqType,
												filingData_captureDate,
												filingData_captureUserId,
												filingData_filingDate,
												filingData_docLog,
												filingData_docNbr,
												filingData_docOrigin,
												filingData_docSeries,
												userdocTypeList_userdocName,
												userdocTypeList_userdocType,
												ownerList_addressStreet,
												ownerList_nationalityCountryCode,
												ownerList_personName,
												ownerList_residenceCountryCode,
												notes,
												representationData_addressStreet,
												representationData_agentCode,
												representationData_cityName,
												representationData_email,
												representationData_addressZone,
												representationData_nationalityCountryCode,
												representationData_personName,
												representationData_residenceCountryCode,
												representationData_telephone,
												representationData_zipCode,
												representationData_representativeType
):
	try:
		data = {
				"arg0": {
					"affectedFileIdList": {
					"fileNbr": {
						"doubleValue": affectedFileIdList_fileNbr
					},
					"fileSeq": affectedFileIdList_fileSeq,
					"fileSeries": {
						"doubleValue": affectedFileIdList_fileSeries
					},
					"fileType": affectedFileIdList_fileType
					},
					"affectedFileSummaryList": {
					"disclaimer": "",
					"disclaimerInOtherLang": "",
					"fileId": {
						"fileNbr": {
						"doubleValue": affectedFileSummaryList_fileNbr
						},
						"fileSeq": affectedFileSummaryList_fileSeq,
						"fileSeries": {
						"doubleValue": affectedFileSummaryList_fileSeries
						},
						"fileType": affectedFileSummaryList_fileType
					},
					"fileIdAsString": "",
					"fileSummaryClasses": "",
					"fileSummaryCountry": "",
					"fileSummaryDescription": fileSummaryDescription,
					"fileSummaryDescriptionInOtherLang": "",
					"fileSummaryOwner": fileSummaryOwner,
					"fileSummaryOwnerInOtherLang": "",
					"fileSummaryRepresentative": "",
					"fileSummaryRepresentativeInOtherLang": "",
					"fileSummaryResponsibleName": "",
					"fileSummaryStatus": "",
					"filingData": {
						"applicationSubtype": "",
						"applicationType": "",
						"captureDate": "",
						"captureUserId": "",
						"corrFileNbr": "",
						"corrFileSeq": "",
						"corrFileSeries": "",
						"corrFileType": "",
						"externalOfficeCode": "",
						"externalOfficeFilingDate": "",
						"externalSystemId": "",
						"filingDate": "",
						"indIncorrRecpDeleted": "",
						"indManualInterpretationRequired": "false",
						"lawCode": "",
						"novelty1Date": "",
						"novelty2Date": "",
						"receptionDate": "",
						"receptionDocument": {
						"documentEdmsData": {
							"edocDate": "",
							"edocId": "",
							"edocImageCertifDate": "",
							"edocImageCertifUser": "",
							"edocImageLinkingDate": "",
							"edocImageLinkingUser": "",
							"edocNbr": "",
							"edocSeq": "",
							"edocSer": "",
							"edocTyp": "",
							"edocTypeName": "",
							"efolderId": "",
							"efolderNbr": "",
							"efolderSeq": "",
							"efolderSer": "",
							"indInterfaceEdoc": "false",
							"indSpecificEdoc": "false"
						},
						"documentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
							"dataCodeId1": "",
							"dataCodeId2": "",
							"dataCodeId3": "",
							"dataCodeId4": "",
							"dataCodeId5": "",
							"dataCodeName1": "",
							"dataCodeName2": "",
							"dataCodeName3": "",
							"dataCodeName4": "",
							"dataCodeName5": "",
							"dataCodeTyp1": "",
							"dataCodeTyp2": "",
							"dataCodeTyp3": "",
							"dataCodeTyp4": "",
							"dataCodeTyp5": "",
							"dataCodeTypeName1": "",
							"dataCodeTypeName2": "",
							"dataCodeTypeName3": "",
							"dataCodeTypeName4": "",
							"dataCodeTypeName5": "",
							"dataDate1": "",
							"dataDate2": "",
							"dataDate3": "",
							"dataDate4": "",
							"dataDate5": "",
							"dataFlag1": "false",
							"dataFlag2": "false",
							"dataFlag3": "false",
							"dataFlag4": "false",
							"dataFlag5": "false",
							"dataNbr1": "",
							"dataNbr2": "",
							"dataNbr3": "",
							"dataNbr4": "",
							"dataNbr5": "",
							"dataText1": "",
							"dataText2": "",
							"dataText3": "",
							"dataText4": "",
							"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
							"description": "",
							"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							},
							"refNo": ""
						},
						"outputDocumentData": {
							"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
							}
						},
						"qtyPages": ""
						},
						"receptionUserId": "",
						"validationDate": "",
						"validationUserId": ""
					},
					"indMark": "false",
					"indPatent": "false",
					"pctApplicationId": "",
					"publicationNbr": "",
					"publicationSer": "",
					"publicationTyp": "",
					"registrationData": {
						"entitlementDate": "",
						"expirationDate": "",
						"indRegistered": "false",
						"registrationDate": "",
						"registrationId": {
						"registrationDup": "",
						"registrationNbr": "",
						"registrationSeries": "",
						"registrationType": ""
						}
					},
					"selected": "",
					"similarityPercent": "",
					"statusId": {
						"processType": "",
						"statusCode": ""
					},
					"workflowWarningText": ""
					},
					"applicant": {
					"applicantNotes": "",
					"person": {
						"addressStreet": applicant_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": applicant_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": applicant_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": applicant_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": applicant_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": applicant_telephone,
						"zipCode": applicant_zipCode
					}
					},
					"auxiliaryRegisterData": {
					"cancellation": "",
					"contractSummary": ""
					},
					"courtDoc": {
					"courtDocDate": "",
					"courtDocNbr": "",
					"courtDocSeq": "",
					"courtDocSeries": "",
					"courtFile": {
						"court": {
						"courtAddress": "",
						"courtName": ""
						},
						"courtFileName": "",
						"courtFileNbr": "",
						"courtFileSeq": "",
						"courtFileSeries": ""
					},
					"decreeDate": "",
					"decreeNbr": "",
					"decreeSeries": ""
					},
					"documentId": {
					"docLog": documentId_docLog,
					"docNbr": {
						"doubleValue": documentId_docNbr
					},
					"docOrigin": documentId_docOrigin,
					"docSeries": {
						"doubleValue": documentId_docSeries
					},
					"selected": ""
					},
					"documentSeqId": {
					"docSeqName": documentSeqId_docSeqName,
					"docSeqNbr": {
						"doubleValue": documentSeqId_docSeqNbr
					},
					"docSeqSeries": {
						"doubleValue": documentSeqId_docSeqSeries
					},
					"docSeqType": documentSeqId_docSeqType
					},
					"filingData": {
					"applicationSubtype": "",
					"applicationType": "",
					"captureDate": {
						"dateValue": filingData_captureDate
					},
					"captureUserId": {
						"doubleValue": filingData_captureUserId
					},
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": {
						"dateValue": filingData_filingDate
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": "",
					"novelty1Date": "",
					"novelty2Date": "",
					"receptionDate": "",
					"receptionDocument": {
						"documentEdmsData": {
						"edocDate": "",
						"edocId": "",
						"edocImageCertifDate": "",
						"edocImageCertifUser": "",
						"edocImageLinkingDate": "",
						"edocImageLinkingUser": "",
						"edocNbr": "",
						"edocSeq": "",
						"edocSer": "",
						"edocTyp": "",
						"edocTypeName": "",
						"efolderId": "",
						"efolderNbr": "",
						"efolderSeq": "",
						"efolderSer": "",
						"indInterfaceEdoc": "false",
						"indSpecificEdoc": "false"
						},
						"documentId": {
						"docLog": filingData_docLog,
						"docNbr": {
							"doubleValue": filingData_docNbr
						},
						"docOrigin": filingData_docOrigin,
						"docSeries": {
							"doubleValue": filingData_docSeries
						},
						"selected": ""
						},
						"documentSeqId": {
						"docSeqName": "",
						"docSeqNbr": "",
						"docSeqSeries": "",
						"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
						"dataCodeId1": "",
						"dataCodeId2": "",
						"dataCodeId3": "",
						"dataCodeId4": "",
						"dataCodeId5": "",
						"dataCodeName1": "",
						"dataCodeName2": "",
						"dataCodeName3": "",
						"dataCodeName4": "",
						"dataCodeName5": "",
						"dataCodeTyp1": "",
						"dataCodeTyp2": "",
						"dataCodeTyp3": "",
						"dataCodeTyp4": "",
						"dataCodeTyp5": "",
						"dataCodeTypeName1": "",
						"dataCodeTypeName2": "",
						"dataCodeTypeName3": "",
						"dataCodeTypeName4": "",
						"dataCodeTypeName5": "",
						"dataDate1": "",
						"dataDate2": "",
						"dataDate3": "",
						"dataDate4": "",
						"dataDate5": "",
						"dataFlag1": "false",
						"dataFlag2": "false",
						"dataFlag3": "false",
						"dataFlag4": "false",
						"dataFlag5": "false",
						"dataNbr1": "",
						"dataNbr2": "",
						"dataNbr3": "",
						"dataNbr4": "",
						"dataNbr5": "",
						"dataText1": "",
						"dataText2": "",
						"dataText3": "",
						"dataText4": "",
						"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
						"description": "",
						"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						},
						"refNo": ""
						},
						"outputDocumentData": {
						"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						}
						},
						"qtyPages": ""
					},
					"receptionUserId": "",
					"userdocTypeList": {
						"userdocName": userdocTypeList_userdocName,
						"userdocType": userdocTypeList_userdocType
					},
					"validationDate": "",
					"validationUserId": ""
					},
					"indNotAllFilesCapturedYet": "false",
					"newOwnershipData": {
					"dummy": "",
					"ownerList": {
						"indService": "false",
						"orderNbr": "",
						"ownershipNotes": "",
						"person": {
						"addressStreet": ownerList_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": ownerList_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": ownerList_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": ownerList_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					}
					},
					"notes": notes,
					"officeSectionId": {
					"officeDepartmentCode": "",
					"officeDivisionCode": "",
					"officeSectionCode": ""
					},
					"representationData": {
					"representativeList": {
						"indService": "false",
					"person": {
						"addressStreet": representationData_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": representationData_addressZone,
						"agentCode": {
							"doubleValue": representationData_agentCode
						},
						"cityCode": "",
						"cityName": representationData_cityName,
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": representationData_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": representationData_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": representationData_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": representationData_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": representationData_telephone,
						"zipCode": representationData_zipCode
						},
						"representativeType": representationData_representativeType
					}
					},
					"respondedOfficedocId": {
					"offidocNbr": "",
					"offidocOrigin": "",
					"offidocSeries": "",
					"selected": ""
					},
					"rowVersion": "",
					"userdocProcessId": {
					"processNbr": "",
					"processType": ""
					}
				}
				} 
		clientPatents.service.UserdocInsert(**data)
		return('true')
	except zeep.exceptions.Fault as e:
		return(str(e))

# creado 26-10-2022 por meet (probando) (AG)
def user_doc_insert_patent_con_pago_relacionado(
												affectedFileIdList_fileNbr,
												affectedFileIdList_fileSeq,
												affectedFileIdList_fileSeries,
												affectedFileIdList_fileType,
												affectedFileSummaryList_fileNbr,
												affectedFileSummaryList_fileSeq,
												affectedFileSummaryList_fileSeries,
												affectedFileSummaryList_fileType,
												fileSummaryDescription,
												fileSummaryOwner,
												applicant_nationalityCountryCode,
												applicant_personName,
												applicant_residenceCountryCode,
												applicant_addressStreet,
												applicant_email,
												applicant_telephone,
												applicant_zipCode,
												documentId_docLog,
												documentId_docNbr,
												documentId_docOrigin,
												documentId_docSeries,
												documentSeqId_docSeqName,
												documentSeqId_docSeqNbr,
												documentSeqId_docSeqSeries,
												documentSeqId_docSeqType,
												filingData_captureDate,
												filingData_captureUserId,
												filingData_filingDate,
												filingData_novelty1Date,
												filingData_novelty2Date,
												paymentList_currencyName,
												paymentList_currencyType,
												paymentList_receiptAmount,
												paymentList_receiptDate,
												paymentList_receiptNbr,
												paymentList_receiptNotes,
												paymentList_receiptType,
												paymentList_receiptTypeName,
												receptionDate,
												receptionDocument_docLog,
												receptionDocument_docNbr,
												receptionDocument_docOrigin,
												receptionDocument_docSeries,
												userdocTypeList_userdocName,
												userdocTypeList_userdocType,
												ownerList_nationalityCountryCode,
												ownerList_personName,
												ownerList_residenceCountryCode,
												ownerList_addressStreet,
												ownerList_email,
												ownerList_telephone,
												ownerList_zipCode,
												notes,
												representationData_addressStreet,
												representationData_agentCode,
												representationData_email,
												representationData_nationalityCountryCode,
												representationData_personName,
												representationData_residenceCountryCode,
												representationData_telephone,
												representationData_representativeType,
												rowVersion):
	try:    
		data = {
				"arg0": {
					"affectedFileIdList": {
					"fileNbr": {
						"doubleValue": affectedFileIdList_fileNbr
					},
					"fileSeq": affectedFileIdList_fileSeq,
					"fileSeries": {
						"doubleValue": affectedFileIdList_fileSeries
					},
					"fileType": affectedFileIdList_fileType
					},
					"affectedFileSummaryList": {
					"disclaimer": "",
					"disclaimerInOtherLang": "",
					"fileId": {
						"fileNbr": {
						"doubleValue": affectedFileSummaryList_fileNbr
						},
						"fileSeq": affectedFileSummaryList_fileSeq,
						"fileSeries": {
						"doubleValue": affectedFileSummaryList_fileSeries
						},
						"fileType": affectedFileSummaryList_fileType
					},
					"fileIdAsString": "",
					"fileSummaryClasses": "",
					"fileSummaryCountry": "",
					"fileSummaryDescription": fileSummaryDescription,
					"fileSummaryDescriptionInOtherLang": "",
					"fileSummaryOwner": fileSummaryOwner,
					"fileSummaryOwnerInOtherLang": "",
					"fileSummaryRepresentative": "",
					"fileSummaryRepresentativeInOtherLang": "",
					"fileSummaryResponsibleName": "",
					"fileSummaryStatus": "",
					"filingData": {
						"indManualInterpretationRequired": "false"
					},
					"indMark": "false",
					"indPatent": "false",
					"workflowWarningText": ""
					},
					"applicant": {
					"applicantNotes": "",
					"person": {
						"addressStreet": applicant_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": applicant_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": applicant_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": applicant_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": applicant_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": applicant_telephone,
						"zipCode": applicant_zipCode
					}
					},
					"documentId": {
					"docLog": documentId_docLog,
					"docNbr": {
						"doubleValue": documentId_docNbr
					},
					"docOrigin": documentId_docOrigin,
					"docSeries": {
						"doubleValue": documentId_docSeries
					},
					"selected": ""
					},
					"documentSeqId": {
					"docSeqName": documentSeqId_docSeqName,
					"docSeqNbr": {
						"doubleValue": documentSeqId_docSeqNbr
					},
					"docSeqSeries": {
						"doubleValue": documentSeqId_docSeqSeries
					},
					"docSeqType": documentSeqId_docSeqType
					},
					"filingData": {
					"captureDate": {
						"dateValue": filingData_captureDate
					},
					"captureUserId": {
						"doubleValue": filingData_captureUserId
					},
					"filingDate": {
						"dateValue": filingData_filingDate
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": "",
					"novelty1Date": {
						"dateValue": filingData_novelty1Date
					},
					"novelty2Date": {
						"dateValue": filingData_novelty2Date
					},
					"paymentList": {
						"currencyName": paymentList_currencyName,
						"currencyType": paymentList_currencyType,
						"receiptAmount": paymentList_receiptAmount,
						"receiptDate": {
						"dateValue": paymentList_receiptDate
						},
						"receiptNbr": paymentList_receiptNbr,
						"receiptNotes": paymentList_receiptNotes,
						"receiptType": paymentList_receiptType,
						"receiptTypeName": paymentList_receiptTypeName
					},
					"receptionDate": {
						"dateValue": receptionDate
					},
					"receptionDocument": {
						"documentId": {
						"docLog": receptionDocument_docLog,
						"docNbr": {
							"doubleValue": receptionDocument_docNbr
						},
						"docOrigin": receptionDocument_docOrigin,
						"docSeries": {
							"doubleValue": receptionDocument_docSeries
						},
						"selected": ""
						},
						"documentSeqId": {
						"docSeqName": "",
						"docSeqNbr": "",
						"docSeqSeries": "",
						"docSeqType": ""
						},
						"externalSystemId": "",
						"inputDocumentData": ""
					},
					"receptionUserId": "",
					"userdocTypeList": {
						"userdocName": userdocTypeList_userdocName,
						"userdocType": userdocTypeList_userdocType
					},
					"validationDate": "",
					"validationUserId": ""
					},
					"indNotAllFilesCapturedYet": "false",
					"newOwnershipData": {
					"dummy": "",
					"ownerList": {
						"indService": "false",
						"orderNbr": "",
						"ownershipNotes": "",
						"person": {
						"addressStreet": ownerList_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": ownerList_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": ownerList_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": ownerList_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": ownerList_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": ownerList_telephone,
						"zipCode": ownerList_zipCode
						}
					}
					},
					"notes": notes,
					"representationData": {
					"representativeList": {
						"indService": "false",
                        "person": {
                        "addressStreet": representationData_addressStreet,
                        "addressStreetInOtherLang": "",
                        "addressZone": "Tembetary",
                        "agentCode": {
                            "doubleValue": representationData_agentCode
                        },
                        "cityCode": "",
                        "cityName": "Tembetary",
                        "companyRegisterRegistrationDate": "",
                        "companyRegisterRegistrationNbr": "",
                        "email": representationData_email,
                        "indCompany": "false",
                        "individualIdNbr": "",
                        "individualIdType": "",
                        "legalIdNbr": "",
                        "legalIdType": "",
                        "legalNature": "",
                        "legalNatureInOtherLang": "",
                        "nationalityCountryCode": representationData_nationalityCountryCode,
                        "personGroupCode": "",
                        "personGroupName": "",
                        "personName": representationData_personName,
                        "personNameInOtherLang": "",
                        "residenceCountryCode": representationData_residenceCountryCode,
                        "stateCode": "",
                        "stateName": "",
                        "telephone": representationData_telephone,
                        "zipCode": ""
                        },
						"representativeType": representationData_representativeType
					}
					},
					"rowVersion": rowVersion
				}
				}
		clientPatents.service.UserdocInsert(**data)
		return('true')
	except zeep.exceptions.Fault as e:
		return(str(e))

# creado 27-10-2022 por meet (probando) (AG)
def insertUserDocPatent_sin_recibo_sin_relacion(
												applicant_addressStreet,
												applicant_email,
												applicant_nationalityCountryCode,
												applicant_personName,
												applicant_residenceCountryCode,
												applicant_telephone,
												applicant_zipCode,
												documentId_docLog,
												documentId_docNbr,
												documentId_docOrigin,
												documentId_docSeries,
												documentId_selected,
												documentSeqId_docSeqName,
												documentSeqId_docSeqNbr,
												documentSeqId_docSeqSeries,
												documentSeqId_docSeqType,
												filingData_captureDate,
												filingData_captureUserId,
												filingData_filingDate,
												filingData_novelty1Date,
												filingData_novelty2Date,
												filingData_receptionDate,
												receptionDocument_docLog,
												receptionDocument_docNbr,
												receptionDocument_docOrigin,
												receptionDocument_docSeries,
												filingData_receptionUserId,
												userdocTypeList_userdocName,
												userdocTypeList_userdocType,
												ownerList_orderNbr,
												ownerList_addressStreet,
												ownerList_email,
												ownerList_nationalityCountryCode,
												ownerList_personName,
												ownerList_residenceCountryCode,
												ownerList_telephone,
												ownerList_zipCode,
												notes,
												representationData_addressStreet,
												representationData_agentCode,
												representationData_email,
												representationData_nationalityCountryCode,
												representationData_personName,
												representationData_residenceCountryCode,
												representationData_telephone,
												representationData_zipCode,
												representationData_representativeType
):
	try:
		data = {
				"arg0": {
					"applicant": {
					"applicantNotes": "Sprint V 2.0",
					"person": {
						"addressStreet": applicant_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": applicant_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": applicant_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": applicant_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": applicant_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": applicant_telephone,
						"zipCode": applicant_zipCode
					}
					},
					"documentId": {
					"docLog": documentId_docLog,
					"docNbr": {
						"doubleValue": documentId_docNbr
					},
					"docOrigin": documentId_docOrigin,
					"docSeries": {
						"doubleValue": documentId_docSeries
					},
					"selected": documentId_selected
					},
					"documentSeqId": {
					"docSeqName": documentSeqId_docSeqName,
					"docSeqNbr": {
						"doubleValue": documentSeqId_docSeqNbr
					},
					"docSeqSeries": {
						"doubleValue": documentSeqId_docSeqSeries
					},
					"docSeqType": documentSeqId_docSeqType
					},
					"filingData": {
					"captureDate": {
						"dateValue": filingData_captureDate
					},
					"captureUserId": {
						"doubleValue": filingData_captureUserId
					},
					"filingDate": {
						"dateValue": filingData_filingDate
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": "",
					"novelty1Date": {
						"dateValue": filingData_novelty1Date
					},
					"novelty2Date": {
						"dateValue": filingData_novelty2Date
					},
					"receptionDate": {
						"dateValue": filingData_receptionDate
					},
					"receptionDocument": {
						"documentId": {
						"docLog": receptionDocument_docLog,
						"docNbr": {
							"doubleValue": receptionDocument_docNbr
						},
						"docOrigin": receptionDocument_docOrigin,
						"docSeries": {
							"doubleValue": receptionDocument_docSeries
						},
						"selected": ""
						}
					},
					"receptionUserId": filingData_receptionUserId,
					"userdocTypeList": {
						"userdocName": userdocTypeList_userdocName,
						"userdocType": userdocTypeList_userdocType
					},
					"validationDate": "",
					"validationUserId": ""
					},
					"indNotAllFilesCapturedYet": "false",
					"newOwnershipData": {
					"dummy": "",
					"ownerList": {
						"indService": "false",
						"orderNbr": ownerList_orderNbr,
						"ownershipNotes": "",
						"person": {
						"addressStreet": ownerList_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": ownerList_email,
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": ownerList_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": ownerList_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": ownerList_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": ownerList_telephone,
						"zipCode": ownerList_zipCode
						}
					}
					},
					"notes": notes,
					"representationData": {
					"representativeList": {
						"indService": "false",
                     'person': {
                        'addressStreet': str(personAgentePatent(representationData_agentCode)[0].addressStreet).replace("None",""),
                        'addressStreetInOtherLang': str(personAgentePatent(representationData_agentCode)[0].addressStreetInOtherLang).replace("None",""),
                        'addressZone': str(personAgentePatent(representationData_agentCode)[0].addressZone).replace("None",""),
                        'agentCode': {
                        'doubleValue':str(personAgentePatent(representationData_agentCode)[0].agentCode.doubleValue).replace("None","")
                        },
                        'cityCode': str(personAgentePatent(representationData_agentCode)[0].cityCode).replace("None",""),
                        'cityName': str(personAgentePatent(representationData_agentCode)[0].cityName).replace("None",""),
                        'companyRegisterRegistrationDate': str(personAgentePatent(representationData_agentCode)[0].companyRegisterRegistrationDate).replace("None",""),
                        'companyRegisterRegistrationNbr': str(personAgentePatent(representationData_agentCode)[0].companyRegisterRegistrationNbr).replace("None",""),
                        'email': str(personAgentePatent(representationData_agentCode)[0].email).replace("None",""),
                        'indCompany': str(personAgentePatent(str(representationData_agentCode))[0].indCompany),
                        'individualIdNbr': str(personAgentePatent(representationData_agentCode)[0].individualIdNbr).replace("None",""),
                        'individualIdType': str(personAgentePatent(representationData_agentCode)[0].individualIdType).replace("None",""),
                        'legalIdNbr': str(personAgentePatent(representationData_agentCode)[0].legalIdNbr).replace("None",""),
                        'legalIdType': str(personAgentePatent(representationData_agentCode)[0].legalIdType).replace("None",""),
                        'legalNature': str(personAgentePatent(representationData_agentCode)[0].legalNature).replace("None",""),
                        'legalNatureInOtherLang': str(personAgentePatent(representationData_agentCode)[0].legalNatureInOtherLang).replace("None",""),
                        'nationalityCountryCode': str(personAgentePatent(representationData_agentCode)[0].nationalityCountryCode).replace("None",""),
                        'personGroupCode': "",
                        'personGroupName': str(personAgentePatent(representationData_agentCode)[0].personGroupName).replace("None",""),
                        'personName': str(personAgentePatent(representationData_agentCode)[0].personName).replace("None",""),
                        'personNameInOtherLang': str(personAgentePatent(representationData_agentCode)[0].personNameInOtherLang).replace("None",""),
                        'residenceCountryCode': str(personAgentePatent(representationData_agentCode)[0].residenceCountryCode).replace("None",""),
                        'stateCode': str(personAgentePatent(representationData_agentCode)[0].stateCode).replace("None",""),
                        'stateName': str(personAgentePatent(representationData_agentCode)[0].stateName).replace("None",""),
                        'telephone': str(personAgentePatent(representationData_agentCode)[0].telephone).replace("None",""),
                        'zipCode': str(personAgentePatent(representationData_agentCode)[0].zipCode).replace("None","")
                    },
						"representativeType": representationData_representativeType
					}
					}
				}
			} 
		clientPatents.service.UserdocInsert(**data)
		return('true')
	except zeep.exceptions.Fault as e:
		return(str(e))

#FetchAll para gestion de usuario MARCAS
def fetch_all_user_mark(login):
	query = {
				"arg0": "SELECT USER_ID,LOGIN FROM IP_USER IU where LOGIN='"+login+"'",
				"arg1": {
						"sqlColumnList":[
											{"sqlColumnType": "String", "sqlColumnValue":"LOGIN"},
											{"sqlColumnType": "String", "sqlColumnValue":"USER_ID"},
										]
				}
		}  
	return(clientMark.service.SqlFetchAll(**query))

#FetchAll para gestion de usuario PATENTE
def fetch_all_user_patent(login):
	query = {
	"arg0": "SELECT USER_ID,LOGIN FROM IP_USER IU where LOGIN='"+login+"'",
	"arg1": {
			"sqlColumnList":[
							
							{"sqlColumnType": "String", "sqlColumnValue":"LOGIN"},
							{"sqlColumnType": "String", "sqlColumnValue":"USER_ID"},
							]
	}
  }
	
	try: 
		return(clientPatents.service.SqlFetchAll(**query))
	except Exception as e:
		return('undefine')

#FetchAll para gestion de usuario DISEÑO
def fetch_all_user_disenio(login):
	query = {
	"arg0": "SELECT USER_ID,LOGIN FROM IP_USER  where LOGIN='"+login+"'",
	"arg1": {
			"sqlColumnList":[
							
							{"sqlColumnType": "String", "sqlColumnValue":"LOGIN"},
							{"sqlColumnType": "String", "sqlColumnValue":"USER_ID"},
							]
	}
  }
	try: 
		return(clientDisenio.service.SqlFetchAll(**query))
	except Exception as e:
		return('undefine')

# creado 31-10-2022 
def titulares_por_exp(exp):
	titulares = []
	titulares.append(len(Fech_All_Exp_titulares(int(exp))))
	for i in range(0,len(Fech_All_Exp_titulares(int(exp)))):
		try:
			titulares.append(Fech_All_Exp_titulares(int(exp))[i].sqlColumnList[0].sqlColumnValue)
		except Exception as e:
			return(str(titulares))
	return(str(titulares))

#user doc insert patent pay yes, not relation (AG)
def userdocInsert_patente_con_pago_sin_relacion(
												applicant_applicantNotes,
												applicant_addressStreet,
												applicant_email,
												applicant_nationalityCountryCode,
												applicant_personName,
												applicant_residenceCountryCode,
												applicant_telephone,
												applicant_zipCode,
												documentId_docLog,
												documentId_docNbr,
												documentId_docOrigin,
												documentId_docSeries,
												documentId_selected,
												documentSeqId_docSeqName,
												documentSeqId_docSeqNbr,
												documentSeqId_docSeqSeries,
												documentSeqId_docSeqType,
												filingData_captureDate,
												filingData_captureUserId,
												filingData_filingDate,
												filingData_novelty1Date,
												filingData_novelty2Date,
												paymentList_currencyName,
												paymentList_currencyType,
												paymentList_receiptAmount,
												paymentList_receiptDate,
												paymentList_receiptNbr,
												paymentList_receiptNotes,
												paymentList_receiptType,
												paymentList_receiptTypeName,
												receptionDocument_docLog,
												receptionDocument_docNbr,
												receptionDocument_docOrigin,
												receptionDocument_docSeries,
												receptionDocument_selected,
												receptionUserId,
												notes,
												userdocTypeList_userdocName,
												userdocTypeList_userdocType,
												ownerList_addressStreet,
												ownerList_nationalityCountryCode,
												ownerList_personName,
												ownerList_residenceCountryCode,
												ownerList_email,
												ownerList_telephone,
												ownerList_zipCode,
												representativeList_addressStreet,
												representativeList_agentCode,
												representativeList_nationalityCountryCode,
												representativeList_personName,
												representativeList_residenceCountryCode,
												representativeList_email,
												representativeList_telephone,
												representativeList_zipCode,
												representativeList_representativeType):
	try:
		data = {
			"arg0": {
				"applicant": {
				"applicantNotes": applicant_applicantNotes,
				"person": {
					"addressStreet": applicant_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": applicant_email,
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": applicant_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": applicant_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": applicant_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": applicant_telephone,
					"zipCode": applicant_zipCode
				  }
				},

				"documentId": {
				"docLog": documentId_docLog,
				"docNbr": {
					"doubleValue": documentId_docNbr
				},
				"docOrigin": documentId_docOrigin,
				"docSeries": {
					"doubleValue": documentId_docSeries
				},
				"selected": documentId_selected
				},

				"documentSeqId": {
				"docSeqName": documentSeqId_docSeqName,
				"docSeqNbr": {
					"doubleValue": documentSeqId_docSeqNbr
				},
				"docSeqSeries": {
					"doubleValue": documentSeqId_docSeqSeries
				},
				"docSeqType": documentSeqId_docSeqType
				},

				"filingData": {
				"captureDate": {
					"dateValue": filingData_captureDate
				},
				"captureUserId": {
					"doubleValue": filingData_captureUserId
				},
				"filingDate": {
					"dateValue": filingData_filingDate
				},
				"indIncorrRecpDeleted": "",
				"indManualInterpretationRequired": "false",
				"lawCode": "",
				"novelty1Date": {
					"dateValue": filingData_novelty1Date
				},
				"novelty2Date": {
					"dateValue": filingData_novelty2Date
				},
				"paymentList": {
					"currencyName": paymentList_currencyName,
					"currencyType": paymentList_currencyType,
					"receiptAmount": paymentList_receiptAmount,
					"receiptDate": {
					"dateValue": paymentList_receiptDate
					},
					"receiptNbr": paymentList_receiptNbr,
					"receiptNotes": paymentList_receiptNotes,
					"receiptType": paymentList_receiptType,
					"receiptTypeName": paymentList_receiptTypeName
				},
				"receptionDate": "",
				"receptionDocument": {
					"documentId": {
					"docLog": receptionDocument_docLog,
					"docNbr": {
						"doubleValue": receptionDocument_docNbr
					},
					"docOrigin": receptionDocument_docOrigin,
					"docSeries": {
						"doubleValue": receptionDocument_docSeries
					},
					"selected": receptionDocument_selected
					}
				},
				"receptionUserId": receptionUserId,
				"userdocTypeList": {
					"userdocName": userdocTypeList_userdocName,
					"userdocType": userdocTypeList_userdocType
				},
				"validationDate": "",
				"validationUserId": ""
				},
				"indNotAllFilesCapturedYet": "false",
				"newOwnershipData": {
				"dummy": "",
				"ownerList": {
					"indService": "false",
					"orderNbr": "",
					"ownershipNotes": "",
					"person": {
					"addressStreet": ownerList_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": ownerList_email,
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": ownerList_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": ownerList_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": ownerList_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": ownerList_telephone,
					"zipCode": ownerList_zipCode
					}
				}
				},
				"notes": notes,
				"representationData": {
				"representativeList": {
					"indService": "false",
                    "person": {
                    "addressStreet": representativeList_addressStreet,
                    "addressStreetInOtherLang": "",
                    "addressZone": "",
                    "agentCode": {
                        "doubleValue": representativeList_agentCode
                    },
                    "cityCode": "",
                    "cityName": "",
                    "companyRegisterRegistrationDate": "",
                    "companyRegisterRegistrationNbr": "",
                    "email": representativeList_email,
                    "indCompany": "false",
                    "individualIdNbr": "",
                    "individualIdType": "",
                    "legalIdNbr": "",
                    "legalIdType": "",
                    "legalNature": "",
                    "legalNatureInOtherLang": "",
                    "nationalityCountryCode": representativeList_nationalityCountryCode,
                    "personGroupCode": "",
                    "personGroupName": "",
                    "personName": representativeList_personName,
                    "personNameInOtherLang": "",
                    "residenceCountryCode": representativeList_residenceCountryCode,
                    "stateCode": "",
                    "stateName": "",
                    "telephone": representativeList_telephone,
                    "zipCode": representativeList_zipCode
                    },
					"representativeType": representativeList_representativeType
				}
				}
			}
		}
		clientPatents.service.UserdocInsert(**data)
		return('true')
	except zeep.exceptions.Fault as e:
		return(str(e))

#insert user doc desing (AG)
def insert_user_doc_disenio(
							affectedFileIdList_fileNbr,
							affectedFileIdList_fileSeq,
							affectedFileIdList_fileSeries,
							affectedFileIdList_fileType,
							affectedFileSummaryList_fileNbr,
							affectedFileSummaryList_fileSeq,
							affectedFileSummaryList_fileSeries,
							affectedFileSummaryList_fileType,
							affectedFileSummaryList_fileSummaryDescription,
							affectedFileSummaryList_registrationNbr,
							applicant_addressStreet,
							applicant_nationalityCountryCode,
							applicant_personName,
							applicant_residenceCountryCode,
							documentId_docLog,
							documentId_docNbr,
							documentId_docOrigin,
							documentId_docSeries,
							documentId_selected,
							documentSeqId_docSeqName,
							documentSeqId_docSeqNbr,
							documentSeqId_docSeqSeries,
							documentSeqId_docSeqType,
							filingData_captureDate,
							captureUserId,
							filingData_filingDate,
							lawCode,
							receptionDate,
							receptionDocument_docLog,
							receptionDocument_docNbr,
							receptionDocument_docOrigin,
							receptionDocument_docSeries,
							receptionUserId,
							userdocTypeList_userdocName,
							userdocTypeList_userdocType,
							ownerList_ownershipNotes,
							ownerList_addressStreet,
							ownerList_nationalityCountryCode,
							ownerList_personName,
							ownerList_residenceCountryCode,
							notes,
							representativeList_addressStreet,
							representativeList_agentCode,
							representativeList_email,
							representativeList_individualIdNbr,
							representativeList_individualIdType,
							representativeList_legalIdNbr,
							representativeList_legalIdType,
							representativeList_nationalityCountryCode,
							representativeList_personName,
							representativeList_residenceCountryCode,
							representativeList_telephone,
							representativeList_representativeType,
							rowVersion,
							processType):
	i_u_d_d = {
				"arg0": {
					"affectedDocumentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
					},
					"affectedFileIdList": {
					"fileNbr": {
						"doubleValue": affectedFileIdList_fileNbr
					},
					"fileSeq": affectedFileIdList_fileSeq,
					"fileSeries": {
						"doubleValue": affectedFileIdList_fileSeries
					},
					"fileType": affectedFileIdList_fileType
					},
					"affectedFileSummaryList": {
					"disclaimer": "",
					"disclaimerInOtherLang": "",
					"fileId": {
						"fileNbr": {
						"doubleValue": affectedFileSummaryList_fileNbr
						},
						"fileSeq": affectedFileSummaryList_fileSeq,
						"fileSeries": {
						"doubleValue": affectedFileSummaryList_fileSeries
						},
						"fileType": affectedFileSummaryList_fileType
					},
					"fileIdAsString": "",
					"fileSummaryClasses": "",
					"fileSummaryCountry": "",
					"fileSummaryDescription": affectedFileSummaryList_fileSummaryDescription,
					"fileSummaryDescriptionInOtherLang": "",
					"fileSummaryOwner": "Apple Inc.",
					"fileSummaryOwnerInOtherLang": "",
					"fileSummaryRepresentative": "",
					"fileSummaryRepresentativeInOtherLang": "",
					"fileSummaryResponsibleName": "",
					"fileSummaryStatus": "",
					"filingData": {
						"applicationSubtype": "",
						"applicationType": "",
						"captureDate": "",
						"captureUserId": "",
						"corrFileNbr": "",
						"corrFileSeq": "",
						"corrFileSeries": "",
						"corrFileType": "",
						"externalOfficeCode": "",
						"externalOfficeFilingDate": "",
						"externalSystemId": "",
						"filingDate": "",
						"indIncorrRecpDeleted": "",
						"indManualInterpretationRequired": "false",
						"lawCode": "",
						"novelty1Date": "",
						"novelty2Date": "",
						"receptionDate": "",
						"receptionDocument": {
						"documentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
						},
						"externalSystemId": ""
						},
						"receptionUserId": "",
						"validationDate": "",
						"validationUserId": ""
					},
					"indMark": "false",
					"indPatent": "false",
					"pctApplicationId": "",
					"publicationNbr": "",
					"publicationSer": "",
					"publicationTyp": "",
					"registrationData": {
						"entitlementDate": "",
						"expirationDate": "",
						"indRegistered": "false",
						"registrationDate": "",
						"registrationId": {
						"registrationDup": "",
						"registrationNbr": {
							"doubleValue": affectedFileSummaryList_registrationNbr
						},
						"registrationSeries": "",
						"registrationType": ""
						}
					},
					"selected": "",
					"similarityPercent": "",
					"statusId": {
						"processType": "",
						"statusCode": ""
					},
					"workflowWarningText": ""
					},
					"applicant": {
					"applicantNotes": "",
					"person": {
						"addressStreet": applicant_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": applicant_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": applicant_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": applicant_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					}
					},
					"documentId": {
					"docLog": documentId_docLog,
					"docNbr": {
						"doubleValue": documentId_docNbr
					},
					"docOrigin": documentId_docOrigin,
					"docSeries": {
						"doubleValue": documentId_docSeries
					},
					"selected": documentId_selected
					},
					"documentSeqId": {
					"docSeqName": documentSeqId_docSeqName,
					"docSeqNbr": {
						"doubleValue": documentSeqId_docSeqNbr
					},
					"docSeqSeries": {
						"doubleValue": documentSeqId_docSeqSeries
					},
					"docSeqType": documentSeqId_docSeqType
					},
					"filingData": {
					"applicationSubtype": "",
					"applicationType": "",
					"captureDate": {
						"dateValue": filingData_captureDate
					},
					"captureUserId": captureUserId,
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": {
						"dateValue": filingData_filingDate
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": lawCode,
					"novelty1Date": "",
					"novelty2Date": "",
					"receptionDate": {
						"dateValue": receptionDate
					},
					"receptionDocument": {
						"documentId": {
						"docLog": receptionDocument_docLog,
						"docNbr": {
							"doubleValue": receptionDocument_docNbr
						},
						"docOrigin": receptionDocument_docOrigin,
						"docSeries": {
							"doubleValue": receptionDocument_docSeries
						},
						"selected": ""
						},
						"documentSeqId": {
						"docSeqName": "",
						"docSeqNbr": {
							"doubleValue": ""
						},
						"docSeqSeries": {
							"doubleValue": ""
						},
						"docSeqType": ""
						},
						"externalSystemId": "",
						"inputDocumentData": ""
					},
					"receptionUserId": receptionUserId,
					"userdocTypeList": {
						"userdocName": userdocTypeList_userdocName,
						"userdocType": userdocTypeList_userdocType
					},
					"validationDate": "",
					"validationUserId": ""
					},
					"indNotAllFilesCapturedYet": "false",
					"newOwnershipData": {
					"dummy": "",
					"ownerList": {
						"indService": "false",
						"orderNbr": "",
						"ownershipNotes": ownerList_ownershipNotes,
						"person": {
						"addressStreet": ownerList_addressStreet,
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": ownerList_nationalityCountryCode,
						"personGroupCode": "",
						"personGroupName": "",
						"personName": ownerList_personName,
						"personNameInOtherLang": "",
						"residenceCountryCode": ownerList_residenceCountryCode,
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
						}
					}
					},
					"notes": notes,
					"officeSectionId": {
					"officeDepartmentCode": "",
					"officeDivisionCode": "",
					"officeSectionCode": ""
					},
					"representationData": {
					"representativeList": {
						"indService": "false",
                        "person": {
                        "addressStreet": representativeList_addressStreet,
                        "addressStreetInOtherLang": "",
                        "addressZone": "",
                        "agentCode": {
                            "doubleValue": representativeList_agentCode
                        },
                        "cityCode": "",
                        "cityName": "",
                        "companyRegisterRegistrationDate": "",
                        "companyRegisterRegistrationNbr": "",
                        "email": representativeList_email,
                        "indCompany": "false",
                        "individualIdNbr": representativeList_individualIdNbr,
                        "individualIdType": representativeList_individualIdType,
                        "legalIdNbr": representativeList_legalIdNbr,
                        "legalIdType": representativeList_legalIdType,
                        "legalNature": "",
                        "legalNatureInOtherLang": "",
                        "nationalityCountryCode": representativeList_nationalityCountryCode,
                        "personGroupCode": "",
                        "personGroupName": "",
                        "personName": representativeList_personName,
                        "personNameInOtherLang": "",
                        "residenceCountryCode": representativeList_residenceCountryCode,
                        "stateCode": "",
                        "stateName": "",
                        "telephone": representativeList_telephone,
                        "zipCode": ""
                        },
						"representativeType": representativeList_representativeType
					}
					},
					"rowVersion": rowVersion,
					"userdocProcessId": {
					"processNbr": "",
					"processType": processType
					}
				}
				}
	try: 
		clientDisenio.service.UserdocInsert(**i_u_d_d)
		return('true')
	except zeep.exceptions.Fault as e:
		return(str(e))

#Existe o no imagen
def val_img(exp):
	try:
		mark_getlist(exp)
		if(len(str(mark_read(str(int(mark_getlist(exp)[0].fileId.fileNbr.doubleValue)), str(mark_getlist(exp)[0].fileId.fileSeq) , str(int(mark_getlist(exp)[0].fileId.fileSeries.doubleValue)) , str(mark_getlist(exp)[0].fileId.fileType)).signData.logo)) < 200 ):
			return('sin imagen')
		else:
			return('con imagen')
	except Exception as e:
		pass 

# insert user doc desing with pay and relation (AG)
def UserDoc_Insert_Con_Recibo_con_relacion_disenio(
											affectedFileIdList_fileNbr,
											affectedFileIdList_fileSeq,
											affectedFileIdList_fileSeries,
											affectedFileIdList_fileType,
											affectedFileSummaryList_fileNbr,
											affectedFileSummaryList_fileSeq,
											affectedFileSummaryList_fileSeries,
											affectedFileSummaryList_fileType,
											affectedFileSummaryList_fileSummaryDescription,
											applicant_addressStreet,
											applicant_nationalityCountryCode,
											applicant_personName,
											applicant_residenceCountryCode,
											documentId_docLog,
											documentId_docNbr,
											documentId_docOrigin,
											documentId_docSeries,
											documentSeqId_docSeqNbr,
											documentSeqId_docSeqSeries,
											documentSeqId_docSeqType,
											filingData_captureDate,
											filingData_captureUserId,
											filingData_filingDate,
											filingData_currencyName,
											filingData_currencyType,
											filingData_receiptAmount,
											filingData_receiptDate,
											filingData_receiptNbr,
											filingData_receiptNotes,
											filingData_receiptType,
											filingData_receiptTypeName,
											filingData_docLog,
											filingData_docNbr,
											filingData_docOrigin,
											filingData_docSeries,
											filingData_userdocName,
											filingData_userdocType,
											newOwnershipData_addressStreet,
											newOwnershipData_nationalityCountryCode,
											newOwnershipData_personName,
											newOwnershipData_residenceCountryCode,
											notes,
											representativeList_addressStreet,
											representativeList_agentCode,
											representativeList_email,
											representativeList_individualIdNbr,
											representativeList_individualIdType,
											representativeList_legalIdNbr,
											representativeList_legalIdType,
											representativeList_nationalityCountryCode,
											representativeList_personName,
											representativeList_residenceCountryCode,
											representativeList_telephone,
											representativeList_representativeType):
	try:
		data= {
			"arg0": {
				"affectedDocumentId": {
				"docLog": "",
				"docNbr": "",
				"docOrigin": "",
				"docSeries": "",
				"selected": ""
				},
				"affectedFileIdList": {
				"fileNbr": {
					"doubleValue": affectedFileIdList_fileNbr
				},
				"fileSeq": affectedFileIdList_fileSeq,
				"fileSeries": {
					"doubleValue": affectedFileIdList_fileSeries
				},
				"fileType": affectedFileIdList_fileType
				},
				"affectedFileSummaryList": {
				"disclaimer": "",
				"disclaimerInOtherLang": "",
				"fileId": {
					"fileNbr": {
					"doubleValue": affectedFileSummaryList_fileNbr
					},
					"fileSeq": affectedFileSummaryList_fileSeq,
					"fileSeries": {
					"doubleValue": affectedFileSummaryList_fileSeries
					},
					"fileType": affectedFileSummaryList_fileType
				},
				"fileIdAsString": "",
				"fileSummaryClasses": "",
				"fileSummaryCountry": "",
				"fileSummaryDescription": affectedFileSummaryList_fileSummaryDescription,
				"fileSummaryDescriptionInOtherLang": "",
				"fileSummaryOwner": "Crocs Inc",
				"fileSummaryOwnerInOtherLang": "",
				"fileSummaryRepresentative": "",
				"fileSummaryRepresentativeInOtherLang": "",
				"fileSummaryResponsibleName": "",
				"fileSummaryStatus": "",
				"filingData": {
					"applicationSubtype": "",
					"applicationType": "",
					"captureDate": "",
					"captureUserId": "",
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": "",
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": 'false',
					"lawCode": "",
					"novelty1Date": "",
					"novelty2Date": "",
					"receptionDate": "",
					"receptionDocument": {
					"documentEdmsData": {
						"edocDate": "",
						"edocId": "",
						"edocImageCertifDate": "",
						"edocImageCertifUser": "",
						"edocImageLinkingDate": "",
						"edocImageLinkingUser": "",
						"edocNbr": "",
						"edocSeq": "",
						"edocSer": "",
						"edocTyp": "",
						"edocTypeName": "",
						"efolderId": "",
						"efolderNbr": "",
						"efolderSeq": "",
						"efolderSer": "",
						"indInterfaceEdoc": 'false',
						"indSpecificEdoc": 'false'
					},
					"documentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"documentSeqId": {
						"docSeqName": "",
						"docSeqNbr": "",
						"docSeqSeries": "",
						"docSeqType": ""
					},
					"externalSystemId": "",
					"extraData": {
						"dataCodeId1": "",
						"dataCodeId2": "",
						"dataCodeId3": "",
						"dataCodeId4": "",
						"dataCodeId5": "",
						"dataCodeName1": "",
						"dataCodeName2": "",
						"dataCodeName3": "",
						"dataCodeName4": "",
						"dataCodeName5": "",
						"dataCodeTyp1": "",
						"dataCodeTyp2": "",
						"dataCodeTyp3": "",
						"dataCodeTyp4": "",
						"dataCodeTyp5": "",
						"dataCodeTypeName1": "",
						"dataCodeTypeName2": "",
						"dataCodeTypeName3": "",
						"dataCodeTypeName4": "",
						"dataCodeTypeName5": "",
						"dataDate1": "",
						"dataDate2": "",
						"dataDate3": "",
						"dataDate4": "",
						"dataDate5": "",
						"dataFlag1": 'false',
						"dataFlag2": 'false',
						"dataFlag3": 'false',
						"dataFlag4": 'false',
						"dataFlag5": 'false',
						"dataNbr1": "",
						"dataNbr2": "",
						"dataNbr3": "",
						"dataNbr4": "",
						"dataNbr5": "",
						"dataText1": "",
						"dataText2": "",
						"dataText3": "",
						"dataText4": "",
						"dataText5": ""
					},
					"inputDocumentData": "",
					"internalDocumentData": {
						"description": "",
						"offidocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
						},
						"refNo": ""
					},
					"outputDocumentData": {
						"officedocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
						}
					},
					"qtyPages": ""
					},
					"receptionUserId": "",
					"validationDate": "",
					"validationUserId": ""
				},
				"indMark": 'false',
				"indPatent": 'false',
				"pctApplicationId": "",
				"publicationNbr": "",
				"publicationSer": "",
				"publicationTyp": "",
				"registrationData": {
					"entitlementDate": "",
					"expirationDate": "",
					"indRegistered": 'false',
					"registrationDate": "",
					"registrationId": {
					"registrationDup": "",
					"registrationNbr": "",
					"registrationSeries": "",
					"registrationType": ""
					}
				},
				"selected": "",
				"similarityPercent": "",
				"statusId": {
					"processType": "",
					"statusCode": ""
				},
				"workflowWarningText": ""
				},
				"applicant": {
				"applicantNotes": "",
				"person": {
					"addressStreet": applicant_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": 'false',
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": applicant_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": applicant_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": applicant_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
				}
				},
				"auxiliaryRegisterData": {
				"cancellation": "",
				"contractSummary": "",
				"guaranteeData": {
					"payee": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": 'false',
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
					},
					"payer": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": 'false',
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
					}
				},
				"licenseData": {
					"granteePerson": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": 'false',
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
					},
					"grantorPerson": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": 'false',
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
					},
					"indCompulsoryLicense": 'false',
					"indExclusiveLicense": 'false'
				},
				"registrationDocumentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
				}
				},
				"courtDoc": {
				"courtDocDate": "",
				"courtDocNbr": "",
				"courtDocSeq": "",
				"courtDocSeries": "",
				"courtFile": {
					"court": {
					"courtAddress": "",
					"courtName": ""
					},
					"courtFileName": "",
					"courtFileNbr": "",
					"courtFileSeq": "",
					"courtFileSeries": ""
				},
				"decreeDate": "",
				"decreeNbr": "",
				"decreeSeries": ""
				},
				"documentId": {
				"docLog": documentId_docLog,
				"docNbr": {
					"doubleValue": documentId_docNbr
				},
				"docOrigin": documentId_docOrigin,
				"docSeries": {
					"doubleValue": documentId_docSeries
				},
				"selected": ""
				},
				"documentSeqId": {
				"docSeqName": "Documentos DINAPI",
				"docSeqNbr": {
					"doubleValue": documentSeqId_docSeqNbr
				},
				"docSeqSeries": {
					"doubleValue": documentSeqId_docSeqSeries
				},
				"docSeqType": documentSeqId_docSeqType
				},
				"filingData": {
				"applicationSubtype": "",
				"applicationType": "",
				"captureDate": {
					"dateValue": filingData_captureDate
				},
				"captureUserId": {
					"doubleValue": filingData_captureUserId
				},
				"corrFileNbr": "",
				"corrFileSeq": "",
				"corrFileSeries": "",
				"corrFileType": "",
				"externalOfficeCode": "",
				"externalOfficeFilingDate": "",
				"externalSystemId": "",
				"filingDate": {
					"dateValue": filingData_filingDate
				},
				"indIncorrRecpDeleted": "",
				"indManualInterpretationRequired": 'false',
				"lawCode": "",
				"novelty1Date": "",
				"novelty2Date": "",
				"paymentList": {
					"currencyName": filingData_currencyName,
					"currencyType": filingData_currencyType,
					"receiptAmount": filingData_receiptAmount,
					"receiptDate": {
					"dateValue": filingData_receiptDate
					},
					"receiptNbr": filingData_receiptNbr,
					"receiptNotes": filingData_receiptNotes,
					"receiptType": filingData_receiptType,
					"receiptTypeName": filingData_receiptTypeName
				},
				"receptionDate": "",
				"receptionDocument": {
					"documentEdmsData": {
					"edocDate": "",
					"edocId": "",
					"edocImageCertifDate": "",
					"edocImageCertifUser": "",
					"edocImageLinkingDate": "",
					"edocImageLinkingUser": "",
					"edocNbr": "",
					"edocSeq": "",
					"edocSer": "",
					"edocTyp": "",
					"edocTypeName": "",
					"efolderId": "",
					"efolderNbr": "",
					"efolderSeq": "",
					"efolderSer": "",
					"indInterfaceEdoc": 'false',
					"indSpecificEdoc": 'false'
					},
					"documentId": {
					"docLog": filingData_docLog,
					"docNbr": {
						"doubleValue": filingData_docNbr
					},
					"docOrigin": filingData_docOrigin,
					"docSeries": {
						"doubleValue": filingData_docSeries
					},
					"selected": ""
					},
					"documentSeqId": {
					"docSeqName": "",
					"docSeqNbr": "",
					"docSeqSeries": "",
					"docSeqType": ""
					},
					"externalSystemId": "",
					"extraData": {
					"dataCodeId1": "",
					"dataCodeId2": "",
					"dataCodeId3": "",
					"dataCodeId4": "",
					"dataCodeId5": "",
					"dataCodeName1": "",
					"dataCodeName2": "",
					"dataCodeName3": "",
					"dataCodeName4": "",
					"dataCodeName5": "",
					"dataCodeTyp1": "",
					"dataCodeTyp2": "",
					"dataCodeTyp3": "",
					"dataCodeTyp4": "",
					"dataCodeTyp5": "",
					"dataCodeTypeName1": "",
					"dataCodeTypeName2": "",
					"dataCodeTypeName3": "",
					"dataCodeTypeName4": "",
					"dataCodeTypeName5": "",
					"dataDate1": "",
					"dataDate2": "",
					"dataDate3": "",
					"dataDate4": "",
					"dataDate5": "",
					"dataFlag1": 'false',
					"dataFlag2": 'false',
					"dataFlag3": 'false',
					"dataFlag4": 'false',
					"dataFlag5": 'false',
					"dataNbr1": "",
					"dataNbr2": "",
					"dataNbr3": "",
					"dataNbr4": "",
					"dataNbr5": "",
					"dataText1": "",
					"dataText2": "",
					"dataText3": "",
					"dataText4": "",
					"dataText5": ""
					},
					"inputDocumentData": "",
					"internalDocumentData": {
					"description": "",
					"offidocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
					},
					"refNo": ""
					},
					"outputDocumentData": {
					"officedocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
					}
					},
					"qtyPages": ""
				},
				"receptionUserId": "",
				"userdocTypeList": {
					"userdocName": filingData_userdocName,
					"userdocType": filingData_userdocType
				},
				"validationDate": "",
				"validationUserId": ""
				},
				"indNotAllFilesCapturedYet": 'false',
				"newOwnershipData": {
				"dummy": "",
				"ownerList": {
					"indService": 'false',
					"orderNbr": "",
					"ownershipNotes": "",
					"person": {
					"addressStreet": newOwnershipData_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": 'false',
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": newOwnershipData_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": newOwnershipData_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": newOwnershipData_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
					}
				}
				},
				"notes": notes,
				"officeSectionId": {
				"officeDepartmentCode": "",
				"officeDivisionCode": "",
				"officeSectionCode": ""
				},
				"poaData": {
				"documentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
				},
				"poaDate": "",
				"poaGrantor": {
					"person": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": 'false',
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
					}
				},
				"poaRegNumber": "",
				"scope": ""
				},
				"representationData": {
				"documentId_PowerOfAttorneyRegister": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
				},
				"referencedPOAData": {
					"documentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
					},
					"poaDate": "",
					"poaGrantor": {
					"person": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": 'false',
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					}
					},
					"poaRegNumber": "",
					"scope": ""
				},
				"representativeList": {
					"indService": 'false',
                    "person": {
                    "addressStreet": representativeList_addressStreet,
                    "addressStreetInOtherLang": "",
                    "addressZone": "",
                    "agentCode": {
                        "doubleValue": representativeList_agentCode
                    },
                    "cityCode": "",
                    "cityName": "",
                    "companyRegisterRegistrationDate": "",
                    "companyRegisterRegistrationNbr": "",
                    "email": representativeList_email,
                    "indCompany": 'false',
                    "individualIdNbr": representativeList_individualIdNbr,
                    "individualIdType": representativeList_individualIdType,
                    "legalIdNbr": representativeList_legalIdNbr,
                    "legalIdType": representativeList_legalIdType,
                    "legalNature": "",
                    "legalNatureInOtherLang": "",
                    "nationalityCountryCode": representativeList_nationalityCountryCode,
                    "personGroupCode": "",
                    "personGroupName": "",
                    "personName": representativeList_personName,
                    "personNameInOtherLang": "",
                    "residenceCountryCode": representativeList_residenceCountryCode,
                    "stateCode": "",
                    "stateName": "",
                    "telephone": representativeList_telephone,
                    "zipCode": ""
                    },
					"representativeType": representativeList_representativeType
				}
				},
				"respondedOfficedocId": {
				"offidocNbr": "",
				"offidocOrigin": "",
				"offidocSeries": "",
				"selected": ""
				},
				"rowVersion": "",
				"userdocProcessId": {
				"processNbr": "",
				"processType": ""
				}
			}
			} 
		return(str(clientDisenio.service.UserdocInsert(**data)))
	except zeep.exceptions.Fault as e:
		return(str(e))

# insert user doc desing not payment, not relation (AG)
def UserDoc_Insert_sin_Recibo_sin_relacion_disenio(
													applicant_applicantNotes,
													applicant_addressStreet,
													applicant_email,
													applicant_nationalityCountryCode,
													applicant_personName,
													applicant_residenceCountryCode,
													applicant_telephone,
													applicant_zipCode,
													documentId_docLog,
													documentId_docNbr,
													documentId_docOrigin,
													documentId_docSeries,
													documentSeqId_docSeqNbr,
													documentSeqId_docSeqSeries,
													documentSeqId_docSeqType,
													filingData_captureDate,
													filingData_captureUserId,
													filingData_filingDate,
													filingData_docLog,
													filingData_docNbr,
													filingData_docOrigin,
													filingData_docSeries,
													filingData_userdocName,
													filingData_userdocType,
													newOwnershipData_ownershipNotes,
													newOwnershipData_addressStreet,
													newOwnershipData_email,
													newOwnershipData_nationalityCountryCode,
													newOwnershipData_personName,
													newOwnershipData_residenceCountryCode,
													newOwnershipData_telephone,
													newOwnershipData_zipCode,
													notes,
													representativeList_addressStreet,
													representativeList_agentCode,
													representativeList_email,
													representativeList_individualIdNbr,
													representativeList_individualIdType,
													representativeList_legalIdNbr,
													representativeList_legalIdType,
													representativeList_nationalityCountryCode,
													representativeList_personName,
													representativeList_residenceCountryCode,
													representativeList_telephone,
													representativeList_representativeType):
	try:    
		data = {
			"arg0": {
				"affectedDocumentId": {
				"docLog": "",
				"docNbr": "",
				"docOrigin": "",
				"docSeries": "",
				"selected": ""
				},
				"applicant": {
				"applicantNotes": applicant_applicantNotes,
				"person": {
					"addressStreet": applicant_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": applicant_email,
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": applicant_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": applicant_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": applicant_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": applicant_telephone,
					"zipCode": applicant_zipCode
				}
				},
				"auxiliaryRegisterData": {
				"cancellation": "",
				"contractSummary": "",
				"guaranteeData": {
					"payee": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
					},
					"payer": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
					}
				},
				"licenseData": {
					"granteePerson": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
					},
					"grantorPerson": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
					},
					"indCompulsoryLicense": "false",
					"indExclusiveLicense": "false"
				},
				"registrationDocumentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
				}
				},
				"courtDoc": {
				"courtDocDate": "",
				"courtDocNbr": "",
				"courtDocSeq": "",
				"courtDocSeries": "",
				"courtFile": {
					"court": {
					"courtAddress": "",
					"courtName": ""
					},
					"courtFileName": "",
					"courtFileNbr": "",
					"courtFileSeq": "",
					"courtFileSeries": ""
				},
				"decreeDate": "",
				"decreeNbr": "",
				"decreeSeries": ""
				},
				"documentId": {
				"docLog": documentId_docLog,
				"docNbr": {
					"doubleValue": documentId_docNbr
				},
				"docOrigin": documentId_docOrigin,
				"docSeries": {
					"doubleValue": documentId_docSeries
				},
				"selected": ""
				},
				"documentSeqId": {
				"docSeqName": "Documentos DINAPI",
				"docSeqNbr": {
					"doubleValue": documentSeqId_docSeqNbr
				},
				"docSeqSeries": {
					"doubleValue": documentSeqId_docSeqSeries
				},
				"docSeqType": documentSeqId_docSeqType
				},
				"filingData": {
				"applicationSubtype": "",
				"applicationType": "",
				"captureDate": {
					"dateValue": filingData_captureDate
				},
				"captureUserId": {
					"doubleValue": filingData_captureUserId
				},
				"corrFileNbr": "",
				"corrFileSeq": "",
				"corrFileSeries": "",
				"corrFileType": "",
				"externalOfficeCode": "",
				"externalOfficeFilingDate": "",
				"externalSystemId": "",
				"filingDate": {
					"dateValue": filingData_filingDate
				},
				"indIncorrRecpDeleted": "",
				"indManualInterpretationRequired": "false",
				"lawCode": "",
				"novelty1Date": "",
				"novelty2Date": "",
				"receptionDate": "",
				"receptionDocument": {
					"documentEdmsData": {
					"edocDate": "",
					"edocId": "",
					"edocImageCertifDate": "",
					"edocImageCertifUser": "",
					"edocImageLinkingDate": "",
					"edocImageLinkingUser": "",
					"edocNbr": "",
					"edocSeq": "",
					"edocSer": "",
					"edocTyp": "",
					"edocTypeName": "",
					"efolderId": "",
					"efolderNbr": "",
					"efolderSeq": "",
					"efolderSer": "",
					"indInterfaceEdoc": "false",
					"indSpecificEdoc": "false"
					},
					"documentId": {
					"docLog": filingData_docLog,
					"docNbr": {
						"doubleValue": filingData_docNbr
					},
					"docOrigin": filingData_docOrigin,
					"docSeries": {
						"doubleValue": filingData_docSeries
					},
					"selected": ""
					},
					"documentSeqId": {
					"docSeqName": "",
					"docSeqNbr": "",
					"docSeqSeries": "",
					"docSeqType": ""
					},
					"externalSystemId": "",
					"extraData": {
					"dataCodeId1": "",
					"dataCodeId2": "",
					"dataCodeId3": "",
					"dataCodeId4": "",
					"dataCodeId5": "",
					"dataCodeName1": "",
					"dataCodeName2": "",
					"dataCodeName3": "",
					"dataCodeName4": "",
					"dataCodeName5": "",
					"dataCodeTyp1": "",
					"dataCodeTyp2": "",
					"dataCodeTyp3": "",
					"dataCodeTyp4": "",
					"dataCodeTyp5": "",
					"dataCodeTypeName1": "",
					"dataCodeTypeName2": "",
					"dataCodeTypeName3": "",
					"dataCodeTypeName4": "",
					"dataCodeTypeName5": "",
					"dataDate1": "",
					"dataDate2": "",
					"dataDate3": "",
					"dataDate4": "",
					"dataDate5": "",
					"dataFlag1": "false",
					"dataFlag2": "false",
					"dataFlag3": "false",
					"dataFlag4": "false",
					"dataFlag5": "false",
					"dataNbr1": "",
					"dataNbr2": "",
					"dataNbr3": "",
					"dataNbr4": "",
					"dataNbr5": "",
					"dataText1": "",
					"dataText2": "",
					"dataText3": "",
					"dataText4": "",
					"dataText5": ""
					},
					"inputDocumentData": "",
					"internalDocumentData": {
					"description": "",
					"offidocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
					},
					"refNo": ""
					},
					"outputDocumentData": {
					"officedocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
					}
					},
					"qtyPages": ""
				},
				"receptionUserId": "",
				"userdocTypeList": {
					"userdocName": filingData_userdocName,
					"userdocType": filingData_userdocType
				},
				"validationDate": "",
				"validationUserId": ""
				},
				"indNotAllFilesCapturedYet": "false",
				"newOwnershipData": {
				"dummy": "",
				"ownerList": {
					"indService": "false",
					"orderNbr": "",
					"ownershipNotes": newOwnershipData_ownershipNotes,
					"person": {
					"addressStreet": newOwnershipData_addressStreet,
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": newOwnershipData_email,
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": newOwnershipData_nationalityCountryCode,
					"personGroupCode": "",
					"personGroupName": "",
					"personName": newOwnershipData_personName,
					"personNameInOtherLang": "",
					"residenceCountryCode": newOwnershipData_residenceCountryCode,
					"stateCode": "",
					"stateName": "",
					"telephone": newOwnershipData_telephone,
					"zipCode": newOwnershipData_zipCode
					}
				}
				},
				"notes": notes,
				"officeSectionId": {
				"officeDepartmentCode": "",
				"officeDivisionCode": "",
				"officeSectionCode": ""
				},
				"poaData": {
				"documentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
				},
				"poaDate": "",
				"poaGrantor": {
					"person": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
					}
				},
				"poaRegNumber": "",
				"scope": ""
				},
				"representationData": {
				"documentId_PowerOfAttorneyRegister": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
				},
				"referencedPOAData": {
					"documentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
					},
					"poaDate": "",
					"poaGrantor": {
					"person": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					}
					},
					"poaRegNumber": "",
					"scope": ""
				},
				"representativeList": {
					"indService": "false",
                     'person': {
                        'addressStreet': str(personAgenteDisenio(representativeList_agentCode)[0].addressStreet).replace("None",""),
                        'addressStreetInOtherLang': str(personAgenteDisenio(representativeList_agentCode)[0].addressStreetInOtherLang).replace("None",""),
                        'addressZone': str(personAgenteDisenio(representativeList_agentCode)[0].addressZone).replace("None",""),
                        'agentCode': {
                        'doubleValue':str(personAgenteDisenio(representativeList_agentCode)[0].agentCode.doubleValue).replace("None","")
                        },
                        'cityCode': str(personAgenteDisenio(representativeList_agentCode)[0].cityCode).replace("None",""),
                        'cityName': str(personAgenteDisenio(representativeList_agentCode)[0].cityName).replace("None",""),
                        'companyRegisterRegistrationDate': str(personAgenteDisenio(representativeList_agentCode)[0].companyRegisterRegistrationDate).replace("None",""),
                        'companyRegisterRegistrationNbr': str(personAgenteDisenio(representativeList_agentCode)[0].companyRegisterRegistrationNbr).replace("None",""),
                        'email': str(personAgenteDisenio(representativeList_agentCode)[0].email).replace("None",""),
                        'indCompany': str(personAgenteDisenio(str(representativeList_agentCode))[0].indCompany).replace("True","true").replace("False","false"),
                        'individualIdNbr': str(personAgenteDisenio(representativeList_agentCode)[0].individualIdNbr).replace("None",""),
                        'individualIdType': str(personAgenteDisenio(representativeList_agentCode)[0].individualIdType).replace("None",""),
                        'legalIdNbr': str(personAgenteDisenio(representativeList_agentCode)[0].legalIdNbr).replace("None",""),
                        'legalIdType': str(personAgenteDisenio(representativeList_agentCode)[0].legalIdType).replace("None",""),
                        'legalNature': str(personAgenteDisenio(representativeList_agentCode)[0].legalNature).replace("None",""),
                        'legalNatureInOtherLang': str(personAgenteDisenio(representativeList_agentCode)[0].legalNatureInOtherLang).replace("None",""),
                        'nationalityCountryCode': str(personAgenteDisenio(representativeList_agentCode)[0].nationalityCountryCode).replace("None",""),
                        'personGroupCode': "",
                        'personGroupName': str(personAgenteDisenio(representativeList_agentCode)[0].personGroupName).replace("None",""),
                        'personName': str(personAgenteDisenio(representativeList_agentCode)[0].personName).replace("None",""),
                        'personNameInOtherLang': str(personAgenteDisenio(representativeList_agentCode)[0].personNameInOtherLang).replace("None",""),
                        'residenceCountryCode': str(personAgenteDisenio(representativeList_agentCode)[0].residenceCountryCode).replace("None",""),
                        'stateCode': str(personAgenteDisenio(representativeList_agentCode)[0].stateCode).replace("None",""),
                        'stateName': str(personAgenteDisenio(representativeList_agentCode)[0].stateName).replace("None",""),
                        'telephone': str(personAgenteDisenio(representativeList_agentCode)[0].telephone).replace("None",""),
                        'zipCode': str(personAgenteDisenio(representativeList_agentCode)[0].zipCode).replace("None","")
                    },
					"representativeType": representativeList_representativeType
				}
				},
				"respondedOfficedocId": {
				"offidocNbr": "",
				"offidocOrigin": "",
				"offidocSeries": "",
				"selected": ""
				},
				"rowVersion": "",
				"userdocProcessId": {
				"processNbr": "",
				"processType": ""
				}
			}
			}
		return(str(clientDisenio.service.UserdocInsert(**data)))
	except zeep.exceptions.Fault as e:
		return(str(e))

################# Consultar marca por expediente usando FileRead y ProcessRead ##################################
def File_Get_List(exp):
	FileGet= {"arg0": {"criteriaFileId": {"fileNbrFrom": {"doubleValue": exp},"fileNbrTo": {"doubleValue": exp}}}}
	return clientMark.service.FileGetList(**FileGet)

def File_Read(fileNbr, fileSeq, fileSeries, fileType):
	FileRead = {"arg0": {"fileNbr": {"doubleValue": fileNbr},"fileSeq": fileSeq,"fileSeries": {"doubleValue": fileSeries},"fileType": fileType}}
	return clientMark.service.FileRead(**FileRead)

def Process_Read(processNbr, processType):
	Process_Read = {"arg0": {"processNbr": {"doubleValue": processNbr }, "processType": processType },"arg1": "","arg2": ""}
	return clientMark.service.ProcessRead(**Process_Read)

def consultar_expediente_ipas(exp):
	try:
		res = []
		#Datos requeridos para (FileRead)
		file_Nbr = str(int(File_Get_List(exp)[0].fileId.fileNbr.doubleValue))
		file_Seq = str(File_Get_List(exp)[0].fileId.fileSeq)
		file_Series = str(int(File_Get_List(exp)[0].fileId.fileSeries.doubleValue))
		file_Type = str(File_Get_List(exp)[0].fileId.fileType)

		#Datos del expediente requerido
		#print(File_Read(file_Nbr,file_Seq,file_Series,file_Type))
		res.append(File_Read(file_Nbr,file_Seq,file_Series,file_Type))

		#Datos requeridos para (ProcessRead)
		process_Nbr = str(int(File_Read(file_Nbr,file_Seq,file_Series,file_Type).processId.processNbr.doubleValue))
		process_Type = str(File_Read(file_Nbr,file_Seq,file_Series,file_Type).processId.processType)

		#Informacion de proceso del expediente requerido
		#print(Process_Read(process_Nbr,process_Type))
		res.append(Process_Read(process_Nbr,process_Type))

		return(str(process_Nbr))

	except zeep.exceptions.Fault as e:
		return(str(e))

def check_serv_marcas():
	try:
		mark_service = conn_serv.ipas_sprint 
		wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
		clientMark = Client(wsdl)
		return('Ok')
	except Exception as e:
		return('error')
def check_serv_patente():
	try:
		Patents_service = conn_serv.ipas_produccion_patent
		wsdlPatente = Patents_service + "/IpasServices/IpasServices?wsdl"
		clientPatents = Client(wsdlPatente)
		return('Ok')
	except Exception as e:
		return('error')
def check_serv_disenio():
	try:
		disenio_service = conn_serv.ipas_produccion_disenio
		wsdlDisenio = disenio_service + "/IpasServices/IpasServices?wsdl"
		clientDisenio = Client(wsdlDisenio)
		return('Ok')
	except Exception as e:
		return('error')

def daily_log_open(fecha):
	try:
		mDailyLog = {
				"arg0": {
					"affectedFilesReadyDate": "",
					"certificationReadyDate": "",
					"dailyLogId": {
					"dailyLogDate": {
						"dateValue": str(fecha)+"T00:00:00-04:00"
					},
					"docLog": "E",
					"docOrigin": str(connex.MEA_SFE_FORMULARIOS_ID_Origin)
					},
					"digitalizationReadyDate": "",
					"fileCaptureReadyDate": "",
					"firstDocNbr": "",
					"indClosed": "false",
					"indOpen": "true",
					"lastDocNbr": "",
					"logoCaptureReadyDate": "",
					"searchCodesReadyDate": "",
					"userdocCaptureReadyDate": ""
				}
				}
		return(str(clientMark.service.DailyLogUpdate(**mDailyLog)))
	except zeep.exceptions.Fault as e:
		return(str(e))

def daily_log_close(fecha):
	try:
		mDailyLog = {
				"arg0": {
					"affectedFilesReadyDate": "",
					"certificationReadyDate": "",
					"dailyLogId": {
					"dailyLogDate": {
						"dateValue": str(fecha)+"T00:00:00-04:00"
					},
					"docLog": "E",
					"docOrigin": str(connex.MEA_SFE_FORMULARIOS_ID_Origin)
					},
					"digitalizationReadyDate": "",
					"fileCaptureReadyDate": "",
					"firstDocNbr": "",
					"indClosed": "false",
					"indOpen": "false",
					"lastDocNbr": "",
					"logoCaptureReadyDate": "",
					"searchCodesReadyDate": "",
					"userdocCaptureReadyDate": ""
				}
				}
		return(str(clientMark.service.DailyLogUpdate(**mDailyLog)))
	except zeep.exceptions.Fault as e:
		return(str(e))

def get_agente(arg):
	code = {
		   "arg0": {
			 "agentCode": {
			   "doubleValue": arg
			 }
		   }
		 }
	
	return clientMark.service.AgentRead(**code)

#print(consultar_expediente_ipas('2264188'))
################# Consultar marca por expediente usando FileRead y ProcessRead ##################################

#print(fetch_all_user_patent('CABENITEZ'))

#print(fetch_all_user_disenio('CABENITEZ'))

########################################### Detalle de expediente pedido SFE ####################################

#print(mark_getlist('915149'))
#print(mark_read('915149','PY','2009','M'))
#print(Process_Read_EventList('312021','1'))

#print(Process_Read_Action('9','312021','1').actionType.actionName)
#print(Process_Read_Action('9','312021','1').actionType.actionTypeId.actionType)

#
#                    #Detalles
#for i in range(0,len(Process_Get_Possible_Option_List('706'))):
#    if Process_Get_Possible_Option_List('706')[int(i)].name == 'Providencia Abandono':
#        print(Process_Get_Possible_Option_List('706')[int(i)].optionNbr)
#        print(Process_Get_Possible_Option_List('706')[int(i)].name)
#        print(Process_Get_Possible_Option_List('706')[int(i)].longName)

#################################################################################################################

#movimiento segun processNbr 
def event_list(exp):
	list_data = []
	try:
		file_data = mark_read(
			str(int(mark_getlist(str(exp))[0].fileId.fileNbr.doubleValue)),
			str(mark_getlist(str(exp))[0].fileId.fileSeq),
			str(int(mark_getlist(str(exp))[0].fileId.fileSeries.doubleValue)),
			str(mark_getlist(str(exp))[0].fileId.fileType))
		for i in range(1,len(Process_Read_EventList(str(file_data.file.processId.processNbr.doubleValue),str(file_data.file.processId.processType)))):
			#print(Process_Read_Action(str(i),str(file_data.file.processId.processNbr.doubleValue),str(file_data.file.processId.processType)))
			list_data.append({
			"event": Process_Read_Action(str(i),str(file_data.file.processId.processNbr.doubleValue),str(file_data.file.processId.processType)).actionType.actionName , 
			"code": Process_Read_Action(str(i),str(file_data.file.processId.processNbr.doubleValue),str(file_data.file.processId.processType)).actionType.actionTypeId.actionType,
			"listCode":Process_Read_Action(str(i),str(file_data.file.processId.processNbr.doubleValue),str(file_data.file.processId.processType)).actionType.listCode
			})
		return jsonify(list_data)    
	except Exception as e:
		print(e) 

#Pasar el expediente y el codigo que contiene el detalla (la implementacion puede ser diferente este es un script de prueba)
def detalle_exp(code,optionNbr):
	for i in range(0,len(Process_Get_Possible_Option_List(code))):
		if Process_Get_Possible_Option_List(code)[int(i)].optionNbr == optionNbr:
			return(
				jsonify({
					"optionNbr":Process_Get_Possible_Option_List(code)[int(i)].optionNbr,
					"name":Process_Get_Possible_Option_List(code)[int(i)].name,
					"longName":Process_Get_Possible_Option_List(code)[int(i)].longName,
					"listCode":Process_Get_Possible_Option_List(code)[int(i)].listCode
				}))

#print(detalle_exp('601','2'))

#--------------------------------------------------------------- posgreSql -------------------------------------------------------------------------------------------
def consulta_fop(exp):
	lista = []
	try:
		conn = psycopg2.connect(
			host='192.168.50.231',
			user='user-developer',
			password='user-developer--201901',
			database='centura'
		)
		cursor = conn.cursor()
		cursor.execute("select * from public.form_orden_publicacion where num_acta = '"+exp+"'  ORDER BY id DESC LIMIT 1")
		row=cursor.fetchall()
		for i in row:        
			lista.append({
					'num_acta': i[0],        
					'tip_movimiento': i[1], 
					'tip_signo': i[2],      
					'fec_movimiento':i[3],  
					'tip_solicitud': i[4],  
					'cod_usuario': i[5],   
					'estado': i[6],        
					'tipo': i[7],          
					'num_agente': i[8],     
					'des_movimiento': i[9], 
					'nom_denominacion': i[10],
					'nom_agente': i[11],     
					'fecha_pago': i[12],   
					'id': i[13],             
					'fecha_inicio': i[14],   
					'fecha_fin': i[15],      
					'pdf': i[16],             
					'fecha_reg': i[17],       
					'proceso_id': i[18]
					})
		#print(lista)            
		return(lista)
	except Exception as e:
		print('Error de conexion')
	finally:
		conn.close()
		print('conexion cerrada')
#--------------------------------------------------------------- mongoDB ---------------------------------------------------------------------------------------------




										   # Zona de pruebas #  `\_(-_-)_/´   
##################################################################################################################################
#Compilar ficheros
#python3 -mpy_compile nombre_fichero.py



#{'docLog':'E','docNbr':{'doubleValue':'2104647'},'docOrigin':'2','docSeries':{'doubleValue':'2021'}
'''
print(len(user_doc_read('E','2104647','2','2021')))
for i in range(0,len(user_doc_read('E','2104647','2','2021'))):
	print(user_doc_read('E','2104647','2','2021'))'''


#event redpi insert
'''
exp_ipas = [22100937,2273856]
for i in range(len(exp_ipas)):	
	Insert_Action_soporte(exp_ipas[i],'2023-01-02','282','Publicado en RedPI','573')
'''




#print(patent_getlist('2270226','2270226'))

#print(disenio_getlist('2123461','2123461'))

#print(insert_disenio_registro())

#print(user_doc_getList_escrito('2126686'))

#print(personTitular("unilever"))

#print(personAgente('6199'))

#print(user_doc_getlist_fecha('2021-04-06','2021-04-07'))

#print(fetch_all_user('admin'))

#Ultima prueba de insert en IPAS 194 
#Insert_Action('2271507','2022-11-26','298','probando Insert PARA EL EVENTO 573','1007')

#Insert_Action('2297506','2022-11-28','47','Publicacion REDPI','573')

#Consulta titulares por fetch_all

'''
# TITULARES POR EXPEDIENTES
titulares = []
for i in range(0,len(Fech_All_Exp_titulares(1932419))):
	try:
		titulares.append(Fech_All_Exp_titulares(1932419)[i].sqlColumnList[0].sqlColumnValue)
		#print(Fech_All_Exp_titulares(1932419)[i].sqlColumnList[1].sqlColumnValue)
		#print(Fech_All_Exp_titulares(1932419)[i].sqlColumnList[3].sqlColumnValue)
	except Exception as e:
	   pass
print(titulares)
'''

#print(titulares_por_exp(2039290))

# Consulta de titulares por metodo
'''for i in range(0,5):
	try:
		print(mark_read('2237224', 'PY', '2022', 'M').file.ownershipData.ownerList[i].person.addressStreet)
		print(mark_read('2237224', 'PY', '2022', 'M').file.ownershipData.ownerList[i].person.personName)
	except Exception as e:
	   pass
'''

									#Pruebas con apostrofe
#//////////////////////////////////////////////////////////////////////////////////////////////////////
#L'OREAL '8801488', 'PY', '1988', 'M'
#Scooter's '2259176','PY','2022','M'
#print(str(mark_read('8801488', 'PY', '1988', 'M').signData.markName).replace("'","\'"))

#'8801488', 'PY', '1988', 'M'
#'2259176','PY','2022','M'
#try:	
#	data = str(mark_read('8801488','PY','1988','M').signData.markName)
#except Exception as e:
#	data = str(mark_read('8801488','PY','1988','M')).replace("'","\'").replace("´","\'")
#print(str(data))
#//////////////////////////////////////////////////////////////////////////////////////////////////////



#validar imagen
'''
if(len(str(mark_read('2236460', 'PY', '2022', 'M').signData.logo)) < 200 and signo_format(mark_read('2177877', 'PY', '2021', 'M').signData.signType) != 'Denominativa'):
	print('No hay imagen')
else:
	print('Si hay imagen')
'''


#print(fetch_all_list_proc_nbr('1366596'))

#print(office_doc_read())
#print(fetch_all_officdoc()[0].sqlColumnList[0].sqlColumnValue)

#print(base64.b64encode(fetch_all_officdoc()[0].sqlColumnList[0].sqlColumnValue.encode()))

#print(fetch_all_officdoc()[0].sqlColumnList[0].sqlColumnValue)

#                   Marcas
#print(user_doc_getlist_fecha('2021-04-15','2021-04-15'))
#print(user_doc_read('E','2104647','2','2021'))


#                   Control de expedientes proceados tabla
#print(user_doc_getlist_fecha('2021-01-14','2021-01-14'))
#print(patent_user_doc_getlist_fecha('2021-04-15','2021-04-15'))
#print(disenio_user_doc_getlist_fecha('2021-04-15','2021-04-15'))


#print(len(Fech_All_Exp('21104495')[1].sqlColumnList))
#position = int(len(Fech_All_Exp('21104495')[1].sqlColumnList))-1
#print(Fech_All_Exp('21104495')[1].sqlColumnList[position].sqlColumnValue)

#print(user_doc_getlist('2022-01-14','2022-01-14'))

#print(fetch_all('2021-01-14', ''))

#print(io.BytesIO(base64.b64decode(office_doc_read().contentData)))


#print(base64.b64encode(office_doc_read().contentData).decode("UTF-8"))
#print(str(office_doc_read().contentData).replace("x", "").split("\\"))
#print(str(office_doc_read().contentData).replace("x", "").replace("\\",""))


#try:
#    with open('file_binary', 'wb') as outfile:
#        outfile.write(str(office_doc_read().contentData).replace("x", "").replace("\\",""))
#        outfile.close()
#        #print("Filename Saved as: " + base64.a85decode(office_doc_read().contentData).decode('ascii')) 
#except:
#   pass


#print(base64.b64decode(office_doc_read().contentData))


#print(Consulta_expediente_orden_fecha('2020-01-14'))
"""
for i in range(1,18):
	try:
		if(Process_Read_Action(i,'1641242','2').actionType.actionTypeId.actionType == '550' or Process_Read_Action(i,'1641242','2').actionType.actionTypeId.actionType == '549'):
			print(Process_Read_Action(i,'1641242','2').actionType.actionTypeId.actionType)
			break
	except Exception as e:
			print('No existe el movimiento')
			break

for i in range(1,18):
	try:
		if(Process_Read_Action(i,'1653222','1').actionType.actionTypeId.actionType == '549'):
			print(Process_Read_Action(i,'1653222','1').actionType.actionTypeId.actionType)
			break
	except Exception as e:
			print('No existe el movimiento')
			break"""

#Generar_orden('2002251','')

#item = Consulta_expediente_orden('2002251','AMEDINA')

#print(int(item['clase']))
#try:
#    for i in Process_Read_EventList('561780','2'):
#        print(i)
#
#except Exception as e:
#    pass    


#consulta por fecha 
#for i in mark_getlistFecha('2021-01-14T08:00:00','2021-01-14T13:59:00'):
	#print(i)


'''for i in Process_Read_EventList('1486465','1'):
	if(i.eventActionTypeCode == '550' or i.eventActionTypeCode == '549' or i.eventActionTypeCode == '560'):
		print(i.eventActionTypeCode)'''

#print(Process_Read_EventList('1486465','1'))       

#Generar_orden('2220843','LCARDOZO')

#print(process_read('1486465','1').processOriginData.topFileSummary.filingData.applicationType)

#print(process_read('1486465','1'))

# UserdocInsert(arg0: ns0:cUserdoc)

#consulta_prueba()

#print(mark_getlist("2177877")[0].fileId.fileNbr.doubleValue)

#print(val_img('2249386'))

#mark_insert_reg()

#Insert_Action('21104495','','147','insert nuevo FOP Python','554')

#Insert_note('21104495','2022-06-22','147','insert Nota nuevo FOP Python','1007')

##################################################################################################################################

#Para inspeccionar rápidamente un archivo WSDL
  #python -m zeep http://192.168.50.16:8060/IpasServices/IpasServices?wsdl

