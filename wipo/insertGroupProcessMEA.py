import time
from zeep import Client
from tools.data_format import fecha_barra
import tools.connect as conn_serv
import zeep

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
			processGroupName:str = ''
			data = ProcessGroupGetList(userNbr)[i]
			processGroupName = str(groupName in data.processGroupName) # existe el nombre de grupo
			if str(processGroupName) == 'None':
				resp = False
			if str(processGroupName) == 'True':
				if str(data.processType) == str(typ):
					resp = True
			else:
				resp = False
		return(resp)
	except Exception as e:
		return(False)

def Insert_Group_Process_reg_ren(fileNbr,user,typ):
	try:
		expediente = mark_getlist(fileNbr)
		fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" )) 
		userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
		data = mark_read(
			expediente[0]['fileId']['fileNbr']['doubleValue'], 
			expediente[0]['fileId']['fileSeq'], 
			expediente[0]['fileId']['fileSeries']['doubleValue'], 
			expediente[0]['fileId']['fileType'])
		group_count = last_group(userId) # cantidad de grupos que tiene el usuario
		if valid_group(userId,group_typ(str(typ)),typ) == False: # no existe el grupo
			print((group_count + 1),userId,fecha,'descripcion','1',typ)
			ProcessGroupInsert((group_count + 1),userId,fecha,'descripcion','1',typ)
			time.sleep(1) 
			ProcessGroupAddProcess((group_count + 1),userId,data['file']['processId']['processNbr']['doubleValue'],data['file']['processId']['processType'])
			res = 'true'
		else: # existe el grupo
			ProcessGroupAddProcess(group_today(userId,group_typ(str(typ)),typ),userId,data['file']['processId']['processNbr']['doubleValue'],data['file']['processId']['processType'])
			res = 'true'
		return(res)
	except Exception as e:
		return('false')

def group_typ(num):
	list = {'1':' [Expediente]','10':' [Escrito+expediente]','11':' [Escrito]'}
	group_name = str(fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" ))+list[str(num)])
	return(group_name)

def group_today(userNbr,groupName,typ):
	try:
		for i in range(len(ProcessGroupGetList(userNbr))):
			processGroupName:str = ''
			data = ProcessGroupGetList(userNbr)[i]
			#print(data)
			processGroupName = str(groupName in data.processGroupName) # existe el nombre de grupo
			if str(processGroupName) == 'None':
				resp = False
			if str(processGroupName) == 'True':
				if str(data.processType) == str(typ):
					resp = data.processGroupId.processGroupCode
			else:
				resp = False
		return(resp)
	except Exception as e:
		return(False)

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