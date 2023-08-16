import time
import psycopg2
from zeep import Client
import tools.filing_date as captureDate
from tools.data_format import fecha_barra
import tools.connect as conn_serv
import zeep
import tools.connect as connex
from wipo.function_for_reception_in import user_doc_getList_escrito, user_doc_read
from wipo.ipas import Process_Read, fetch_all_user_mark, mark_getlist, mark_read


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

#print(ProcessGroupGetList('147')) #buscar grupo de tramite por usuario

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

# insertar en grupo expediente registro y renovacion por nombre de usuario (AMEDINA)
def insertar_grupo_expediente(user,exp):
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
	return(ProcessGroupAddProcess(
		str(group_today(userId, group_name)[1]),
		str(userId),str(data['file']['processId']['processNbr']['doubleValue']),
		str(data['file']['processId']['processType'])))

def insertar_grupo_escrito(user,esc):
	data_doc = user_doc_getList_escrito(esc)
	fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" )) 
	userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
	process = user_doc_read(data_doc['documentId']['docLog'],data_doc['documentId']['docNbr']['doubleValue'],data_doc['documentId']['docOrigin'],data_doc['documentId']['docSeries']['doubleValue'])
	print(process['userdocProcessId']['processNbr']+" "+process['userdocProcessId']['processType'])
	#####################################################################################################
	group_name = f'{fecha} [Escrito]'
	group = group_today(userId, group_name)
	return(ProcessGroupAddProcess(str(group[1]),str(userId),str(process['userdocProcessId']['processNbr']),str(process['userdocProcessId']['processType'])))

#ESCRITO RELACINADO CON EXPEDIENTE
def insertar_escritoMasExpediente(user,esc,sigla):
	fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" )) 
	userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
	data_process = Process_Get_List(esc,esc,captureDate.capture_year(),sigla)[0]
	#####################################################################################################
	group_name = f'{fecha} [Escrito+expediente]'
	return(ProcessGroupAddProcess(str(group_today(userId, group_name)[1]),str(userId),str(data_process.processId.processNbr.doubleValue),str(data_process.processId.processType)))
	#####################################################################################################

def main_State(exp):
	data_exp = mark_getlist(exp)[0]
	data_exp_process = mark_read(data_exp.fileId.fileNbr.doubleValue, data_exp.fileId.fileSeq, data_exp.fileId.fileSeries.doubleValue, data_exp.fileId.fileType)
	status_exp = Process_Read(data_exp_process.file.processId.processNbr.doubleValue, data_exp_process.file.processId.processType)
	return(status_exp.status.statusId.statusCode)


#print(main_State('2359548'))


def group_typ(num):
	list = {'1':'[Expediente]','10':'[Escrito+expediente]','11':'[Escrito]'}
	group_name = str(fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00"))+" "+list[str(num)])
	return(group_name)

def group_today(userNbr,groupName):	
	data = ProcessGroupGetList(userNbr)
	list_data = []
	if data == []:
		return(False)
	else:
		for i in range(0,len(data)):
			if str(groupName) == str(data[i].processGroupName):
				list_data.append(data[i].processGroupName)
				list_data.append(data[i].processGroupId.processGroupCode)		
		if list_data == []:
			return(False)
		else:
			return(list_data)

def last_group(userNbr):
	try:
		list = []
		list_int = []
		data = ProcessGroupGetList(userNbr)
		for i in range(0,len(data)):
			list.append(data[i].processGroupId.processGroupCode)
		for i in list:
			list_int.append(int(i))
		list_int.sort()
		ultimo = int(len(list_int))-1
		return(list_int[ultimo])
	except Exception as e:
		return(0)

def Process_Get_List(userdocSeqNbrFrom,userdocSeqNbrTo,userdocSeqSeries,userdocType):
	data_exp = {
				"arg0": {
					"criteriaProcessByUserdoc": {
					"userdocSeqNbrFrom": {
						"doubleValue": userdocSeqNbrFrom
					},
					"userdocSeqNbrTo": {
						"doubleValue": userdocSeqNbrTo
					},
					"userdocSeqSeries": {
						"doubleValue": userdocSeqSeries
					},
					"userdocSeqType": "PY",
					"userdocType": userdocType
					}
				},
				"arg1": {
					"doubleValue": ""
				}
				}
	data = clientMark.service.ProcessGetList(**data_exp)
	return(data)

#print(Process_Get_List('2364500','2364500','2023','ED'))	

def SIGLA_DE_ESTADO(sig,exp):
	#print(sig)
	if exist_main_mark(sig) == 'S':
		try:
			status_exp = main_State(exp)
		except Exception as e:
			return('GEN')
		#print(status_exp)
		rule = email_receiver(str(status_exp))
		return(status_exp)	
	else:
		pass

def sigla_estado_exp(sig,fileNbr):
	#print(sig)
	if exist_main_mark(sig) == 'S':
		try:
			status_exp = main_State(fileNbr)
		except Exception as e:
			return('GEN')
		#print(status_exp)
		rule = email_receiver(str(status_exp))
		return(status_exp)	
	else:
		pass

def email_receiver(sig):
	data_user = {}
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.email_user_notas_status_name.format(str(sig)))
		row=cursor.fetchall()
		return(row)	
	except Exception as e:
		print(e)
	finally:
		conn.close()		

def USER_GROUP(sig):
	data_user = {}
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.usuario_reglas_notificacion.format(str(sig)))
		row=cursor.fetchall()
		return(row[0][0])	
	except Exception as e:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.usuario_reglas_notificacion.format('GEN'))
		row=cursor.fetchall()
		return(row[0][0])
	finally:
		conn.close()

def exist_main_mark(sig):	
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.exp_ri_reglas_me.format(sig)) #select ttasa from reglas_me where tipo_doc like '{} %'
		row=cursor.fetchall()
		for i in row:
			return(i[0])	
	except Exception as e:
		print(e)
	finally:
		conn.close()

# requeridos sigla y fileNbr, affectNbr en caso de escrito que aecta expediente 
def group_addressing(sig,affectNbr,fileNbr):
	relation_typ = exist_main_mark(sig)	#devuelve si la regla es relacionada a esc o exp 
	if relation_typ == 'S':
		try:
			# ultimo estado correspondiente al expediente
			state = sigla_estado_exp(sig,affectNbr) 
			# usuario segun estado del expediente - si no existe (GEN)	
			user = USER_GROUP(state) 			

			# Crea grupo o inserta file en grupo existente segun el estado del expediente afectado 
			return(insertar_escritoMasExpediente(user,fileNbr,sig))

		except Exception as e:
			print('sigla o expediente no validos')
	elif relation_typ == 'N':
		return(insertar_grupo_escrito(USER_GROUP(sig),str(fileNbr)))
	else:
		print('sin Relacion')

# Solo CREAR GRUPO por nombre usuario (AMEDINA)
def crear_grupo(user):
	try:
		fecha = fecha_barra(str(time.strftime("%Y-%m-%d")+" 00:00:00" ))
		userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
		#####################################################################################################
		group_exp = f'{fecha} [Expediente]'
		group_esc = f'{fecha} [Escrito]'
		group_esc_exp = f'{fecha} [Escrito+expediente]'

		exists_group_exp = group_today(userId, group_exp)

		exists_group_esc = group_today(userId, group_esc)

		exists_group_esc_exp = group_today(userId, group_esc_exp)

		#####################################################################################################

		if exists_group_exp == False:
			ProcessGroupInsert(last_group(userId)+1,userId,fecha,'Creado por M.E.A.','1','1')
		else:
			pass
			
		if exists_group_esc == False:
			ProcessGroupInsert(last_group(userId)+1,userId,fecha,'Creado por M.E.A.','1','10')
		else:
			pass

		if exists_group_esc_exp == False:
			ProcessGroupInsert(last_group(userId)+1,userId,fecha,'Creado por M.E.A.','1','11')
		else:
			pass
		return(True)	
	except Exception as e:
		return(e)

def crear_grupo_fecha(user,yourDate):
	try:
		fecha = fecha_barra(f'{yourDate} 00:00:00')
		userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
		#####################################################################################################
		group_exp = f'{fecha} [Expediente]'
		group_esc = f'{fecha} [Escrito]'
		group_esc_exp = f'{fecha} [Escrito+expediente]'

		exists_group_exp = group_today(userId, group_exp)

		exists_group_esc = group_today(userId, group_esc)

		exists_group_esc_exp = group_today(userId, group_esc_exp)

		#####################################################################################################

		if exists_group_exp == False:
			ProcessGroupInsert(last_group(userId)+1,userId,fecha,'Creado por M.E.A.','1','1')
		else:
			pass
			
		if exists_group_esc == False:
			ProcessGroupInsert(last_group(userId)+1,userId,fecha,'Creado por M.E.A.','1','10')
		else:
			pass

		if exists_group_esc_exp == False:
			ProcessGroupInsert(last_group(userId)+1,userId,fecha,'Creado por M.E.A.','1','11')
		else:
			pass
		return(True)	
	except Exception as e:
		return(e)

# insertar en grupo expediente registro y renovacion por nombre de usuario (AMEDINA)
def insertar_grupo_expediente(user,exp):
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
	return(ProcessGroupAddProcess(str(group_today(userId, group_name)[1]),str(userId),str(data['file']['processId']['processNbr']['doubleValue']),str(data['file']['processId']['processType'])))

