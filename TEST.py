
import time
import zeep
from zeep import Client
from tools.data_format import fecha_barra
import tools.connect as conn_serv
from wipo.insertGroupProcessMEA import ProcessGroupAddProcess, ProcessGroupGetList, ProcessGroupInsert, valid_group
from wipo.ipas import fetch_all_user_mark, mark_getlist, mark_read
import tools.filing_date as captureDate

try:
	mark_service = conn_serv.MEA_IPAS_DESTINO
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')


def Insert_Group_Process(grupo,fileNbr,user,typ):
	try:
		fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" ))
		expediente = mark_getlist(fileNbr)
		userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
		data = mark_read(
			expediente[0]['fileId']['fileNbr']['doubleValue'], 
			expediente[0]['fileId']['fileSeq'], 
			expediente[0]['fileId']['fileSeries']['doubleValue'], 
			expediente[0]['fileId']['fileType'])
		group_count = len(ProcessGroupGetList(userId)) # cantidad de grupos que tiene el usuario
		if valid_group(userId,fecha,typ) == False: # no existe el grupo
			print((group_count + 1),userId,fecha,'','1',typ)
			ProcessGroupInsert((group_count + 1),userId,fecha,'','1',typ)
			time.sleep(1) 
			ProcessGroupAddProcess((group_count + 1),userId,data['file']['processId']['processNbr']['doubleValue'],data['file']['processId']['processType'])
			res = 'true'
		else: # existe el grupo
			ProcessGroupAddProcess(grupo,userId,data['file']['processId']['processNbr']['doubleValue'],data['file']['processId']['processType'])
			res = 'true'
		return(res)
	except Exception as e:
		return('false')


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
	for i in range(0,len(ProcessGroupGetList(userNbr))):
		list.append(ProcessGroupGetList(userNbr)[i].processGroupId.processGroupCode)
	for i in list:
		list_int.append(int(i))
	list_int.sort()
	ultimo = int(len(list_int))-1
	return(list_int[ultimo])


print(last_group('156'))

#print(Insert_Group_Process('1','2177877','AMEDINA','1'))