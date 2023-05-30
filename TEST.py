
import time
import zeep
from zeep import Client
from tools.data_format import fecha_barra
import tools.connect as conn_serv
from wipo.insertGroupProcessMEA import ProcessGroupAddProcess, ProcessGroupGetList, ProcessGroupInsert
from wipo.ipas import daily_log_close, daily_log_open, fetch_all_user_mark, mark_getlist, mark_read
import tools.filing_date as captureDate

try:
	mark_service = conn_serv.MEA_IPAS_DESTINO
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')

# el numero de grupo de la fecha y usuario
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

#EXISTE O NO EL GRUPO USUARIO DE LA FECHA
#print(group_today('297', '30/05/2023', '1'))

def group_typ(num):
	list = {'1':' [Expediente]','10':' [Escrito+expediente]','11':' [Escrito]'}
	group_name = str(fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" ))+list[str(num)])
	return(group_name)

#print(group_typ('10'))

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
			print((group_count + 1),userId,group_typ(str(typ)),'descripcion','1',typ)
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


def fileResave(ORIGIN):
	try:
		daily_log_open("2023-05-30")
		data = {
				"arg0": ORIGIN,
				"arg1": "REG",
				"arg2": "MS",

				"arg4": {
					"dateValue": "2023-05-30"
				},
				"arg5": {
					"currencyType": "",
					"DReceiptAmount": "",
					"receiptDate": {
					"dateValue": ""
					},
					"receiptNbr": "",
					"receiptType": ""
				},
				"arg6": {
					"fileNbr": {
					"doubleValue": "23006290"
					},
					"fileSeq": "PY",
					"fileSeries": {
					"doubleValue": "2023"
					},
					"fileType": "M"
				},
				"arg7": {
					"docLog": "E",
					"docNbr": {
					"doubleValue": "23006290"
					},
					"docOrigin": ORIGIN,
					"docSeries": {
					"doubleValue": "2023"
					},
					"selected": ""
				},
				"arg8": "PRUEBA M.E.A."
				}	
		clientMark.service.FileReceive(**data)
		print(daily_log_close("2023-05-30"))
		return(True)
	except zeep.exceptions.Fault as e:
		daily_log_close("2023-05-30")
		return(e)			


print(Insert_Group_Process_reg_ren('23006295','CABENITEZ','1'))


#print(valid_group('298',group_typ('1'),'1'))

#print(fileResave('3'))

#print(last_group('297'))

#print(Insert_Group_Process('1','2177877','AMEDINA','1'))