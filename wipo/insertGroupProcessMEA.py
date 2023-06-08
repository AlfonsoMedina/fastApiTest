import time
from zeep import Client
from tools.data_format import fecha_barra
import tools.connect as conn_serv
import zeep
from wipo.function_for_reception_in import user_doc_getList_escrito, user_doc_read

from wipo.ipas import fetch_all_user_mark, mark_getlist, mark_read


try:
	mark_service = conn_serv.MEA_IPAS_DESTINO
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')

def ProcessGroupAddProcess(processGroupCode,userNbr,processNbr,processType):
	try:
		data = {
				"arg0": {
					"processGroupCode": processGroupCode,
					"userId": {
					"userNbr": {
						"doubleValue": userNbr
					}
					}
				},
				"arg1": {
					"processNbr": {
					"doubleValue": processNbr
					},
					"processType": processType
				}
				}
		return clientMark.service.ProcessGroupAddProcess(**data)        
	except zeep.exceptions.Fault as e:
		return(str(e))

def ProcessGroupInsert(processGroupCode,userNbr,processGroupName,description,relatedToWorkcode,processType):
	try:
		data = {
				"arg0": {
						"processGroupId": {
						"processGroupCode": processGroupCode,
						"userId": {
							"userNbr": {
							"doubleValue": userNbr
							}
						}
						},
						"processGroupName": processGroupName,
						"processSummaryList": {
						"description": description,
						"relatedToWorkcode": {
							"doubleValue": relatedToWorkcode
						},
						"workflowWarningText": ""
						},
						"processType": processType
					}
				}
		return clientMark.service.ProcessGroupInsert(**data)
	except zeep.exceptions.Fault as e:
		return([])

def ProcessGroupRead(processGroupCode,userNbr):
	try:
		data = {
				"arg0": {
					"processGroupCode": processGroupCode,
					"userId": {
						"userNbr": {
							"doubleValue": userNbr
						}
					}
				},
				"arg1": "",
				"arg2": {
					"doubleValue": ""
				}
			}
		exist = clientMark.service.ProcessGroupRead(**data).processGroupId.processGroupCode
		
		if exist != 'El grupo de tramites ya existe':
			return(True)
		else:
			return(False)
	
	except zeep.exceptions.Fault as e:
		if e == 'El grupo de tramites ya existe':
			return(False)
		else:
			return(False)

def ProcessGroupGetList(userNbr):
	try:
		data = {
					"arg0": {
						"userNbr": {
						"doubleValue":userNbr
						}
					}
				}
		return(clientMark.service.ProcessGroupGetList(**data))
	except zeep.exceptions.Fault as e:
		return(e)

def valid_group(userNbr,groupName,typ):
	try:
		for i in range(len(ProcessGroupGetList(userNbr))):
			processGroupname:bool = False
			data = ProcessGroupGetList(userNbr)[i]
			processGroupname = groupName in data.processGroupName # existe el nombre de grupo
			if str(processGroupname) == 'None':
				resp = False
			if str(processGroupname) == 'True':
				if str(data.processType) == str(typ):
					resp = True
			else:
				resp = False
		return(resp)
	except Exception as e:
		return(False)

def insertar_o_crear_grupo_expediente(user,exp):
	expediente = mark_getlist(exp)
	fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" )) 
	userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
	data = mark_read(
		expediente[0]['fileId']['fileNbr']['doubleValue'], 
		expediente[0]['fileId']['fileSeq'], 
		expediente[0]['fileId']['fileSeries']['doubleValue'], 
		expediente[0]['fileId']['fileType'])
	#####################################################################################################
	group_name = f'{fecha} [Expediente]'
	if group_today(userId, group_name) != False:

		ProcessGroupAddProcess(
			str(group_today(userId, group_name)[1]), 
			userId, 
			data['file']['processId']['processNbr']['doubleValue'],
			data['file']['processId']['processType']
			)
	else:
		pass
	#####################################################################################################
	if group_today(userId, group_name) == False:
		ProcessGroupInsert(
							last_group(userId)+1,
							userId,
							fecha,
							'Creado por M.E.A.',
							'1',
							'1')

		ProcessGroupAddProcess(
							str(group_today(userId, group_name)[1]), 
							userId, 
							data['file']['processId']['processNbr']['doubleValue'],
							data['file']['processId']['processType']
							)
	
	else:
		pass

def insertar_o_crear_grupo_escrito(user,esc):
	data_doc = user_doc_getList_escrito(esc)
	fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" )) 
	userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
	process = user_doc_read(data_doc['documentId']['docLog'],data_doc['documentId']['docNbr']['doubleValue'],data_doc['documentId']['docOrigin'],data_doc['documentId']['docSeries']['doubleValue'])
	print(process['userdocProcessId']['processNbr']+" "+process['userdocProcessId']['processType'])
	#####################################################################################################
	group_name = f'{fecha} [Escrito]'
	if group_today(userId, group_name) != False:

		ProcessGroupAddProcess(
								str(group_today(userId, group_name)[1]), 
								userId, 
								process['userdocProcessId']['processNbr'],
								process['userdocProcessId']['processType']
								)
	else:
		pass
	#####################################################################################################
	if group_today(userId, group_name) == False:
		ProcessGroupInsert(
							last_group(userId)+1,
							userId,
							fecha,
							'Creado por M.E.A.',
							'1',
							'11')

		ProcessGroupAddProcess(
								str(group_today(userId, group_name)[1]), 
								userId, 
								process['userdocProcessId']['processNbr'],
								process['userdocProcessId']['processType']
								)
	
	else:
		pass

def insertar_o_crear_grupo_escritoMasExpediente(user,esc):

	data_doc = user_doc_getList_escrito(esc)
	fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" )) 
	userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
	process = user_doc_read(data_doc['documentId']['docLog'],data_doc['documentId']['docNbr']['doubleValue'],data_doc['documentId']['docOrigin'],data_doc['documentId']['docSeries']['doubleValue'])
	print(process['userdocProcessId']['processNbr']+" "+process['userdocProcessId']['processType'])

	#####################################################################################################
	group_name = f'{fecha} [Escrito+expediente]'
	if group_today(userId, group_name) != False:

		ProcessGroupAddProcess(
								str(group_today(userId, group_name)[1]), 
								userId, 
								process['userdocProcessId']['processNbr'],
								process['userdocProcessId']['processType']
								)
	else:
		pass
	#####################################################################################################
	if group_today(userId, group_name) == False:
		ProcessGroupInsert(
							last_group(userId)+1,
							userId,
							fecha,
							'Creado por M.E.A.',
							'1',
							'10')

		ProcessGroupAddProcess(
								str(group_today(userId, group_name)[1]), 
								userId, 
								process['userdocProcessId']['processNbr'],
								process['userdocProcessId']['processType']
								)
	
	else:
		pass

def group_typ(num):
	list = {'1':'[Expediente]','10':'[Escrito+expediente]','11':'[Escrito]'}
	group_name = str(fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00"))+" "+list[str(num)])
	return(group_name)

def group_today(userNbr,groupName):	
	data = ProcessGroupGetList(userNbr)
	list_data = []
	respuesta = False
	for i in range(1,len(data)):
		if str(groupName) == str(data[i].processGroupName):
			list_data.append(data[i].processGroupName)
			list_data.append(data[i].processGroupId.processGroupCode)
		respuesta = list_data

		if str(groupName) != str(data[i].processGroupName):
			respuesta = False
	return(respuesta)

def last_group(userNbr):
	list = []
	list_int = []
	data = ProcessGroupGetList(userNbr)
	for i in range(0,len(data)):
		list.append(data[i].processGroupId.processGroupCode)
	for i in list:
		list_int.append(int(i))
	list_int.sort()
	ultimo = int(len(list_int))-1
	#print(list_int)
	return(list_int[ultimo])