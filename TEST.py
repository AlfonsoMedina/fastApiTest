
import base64
import binascii
import os
from threading import Thread #----------------------
import psycopg2
from zeep import Client
import zeep
from auto_process import captura_pendientes
from tools.base64Decode import decode_img, delete_img
from models.InsertUserDocModel import userDocModel
from dinapi.sfe import email_receiver, exist_main_mark, exist_notifi, main_State, pendientes_sfe_not_pag, registro_sfe, renovacion_sfe, respuesta_sfe_campo,  titulare_reg
from email_pdf_AG import registro_pdf_con_acuse, renovacion_pdf_con_acuse
from getFileDoc import compilePDF, getFile, getFile_reg_and_ren
from tools.send_mail import enviar_back_notFile
from sfe_no_presencial_reg_local import registro_pdf_sfe_local
from sfe_no_presencial_ren_local import renovacion_pdf_sfe_local
from tools.filing_date import capture_day
import tools.connect as connex
from wipo.function_for_reception_in import user_doc_getList_escrito, user_doc_read_min
from wipo.ipas import Process_Read_Action, Process_Read_EventList, daily_log_close, daily_log_open, fetch_all_user_mark, getPoder, mark_getlist, mark_getlistReg, mark_read, process_read
import tools.connect as conn_serv
from PyPDF2 import PdfFileMerger,PdfMerger



try:
	mark_service = conn_serv.MEA_IPAS_DESTINO
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')

# Ultimo dia
def getDia_proceso():
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.LAST_DAY_PROCESS)
		row=cursor.fetchall()
		for i in row:
			return(str(i[0]))	
	except Exception as e:
		print(e)
	finally:
		conn.close()

#Ultimo numero
def getLast_number():
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.LAST_NUMBER)
		row=cursor.fetchall()
		for i in row:
			return(str(i[0]))	
	except Exception as e:
		print(e)
	finally:
		conn.close()

#Cerrar dia
def closed_process_day(fecha):
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.CLOSE_PROCESS_DATE.format(fecha))
		conn.commit()
		conn.close()
		return(True)
	except Exception as e:
		return(e)

#Abrir dia
def open_process_day(fecha):
	try:
		num = int(getLast_number())
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.OPEN_PROCESS_DATE.format(fecha,num,num))
		conn.commit()
		conn.close()
		return(True)
	except Exception as e:
		return(e)

def newDayProcess():
	last_date = getDia_proceso() 					# Ultima fecha de proceso 
	today = capture_day()							# fecha de hoy
	if closed_process_day(last_date) == True:		# Cierra ultima fecha 
		if open_process_day(today) == True:			# Abre fecha nueva
			return(True)			

#print(fetch_all_user_mark('AMEDINA')[0]['sqlColumnList'][0]['sqlColumnValue'])

#print(newDayProcess())

#print(ProcessGroupGetList('298'))

#print(USER_GROUP('CP'))

"""
	data = email_receiver('GEN')

	print(data[0][0])
	print(data[0][1])
	print(data[0][2])
"""

#print(renovacion_sfe('1795'))

#renovacion_pdf_sfe_local('1795')

#print(titulare_reg('1586',10))

#registro_pdf_sfe_local('1586')

#renovacion_pdf_sfe_local('1941')

#registro_pdf_con_acuse('1586')

#print(user_doc_getList_escrito('2348615'))

#print(mark_getlist('2348612.0')[0])

#print(main_State('2348612.0'))

"""def getFile_reg_and_ren(doc_id,fileNbr):

	os.mkdir('temp_pdf/'+fileNbr)
	try:
		remote_url = respuesta_sfe_campo(doc_id)['observacion_documentos']['archivo']['url']
		local_file = 'temp_pdf/'+fileNbr+'/'+fileNbr+'-1.pdf' 
		request.urlretrieve(remote_url, local_file)
	except Exception as e:
		pass
	try:	
		remote_url = respuesta_sfe_campo(doc_id)['datosrepresentacion_decjurada']['archivo']['url']
		local_file = 'temp_pdf/'+fileNbr+'/'+fileNbr+'-2.pdf' 
		request.urlretrieve(remote_url, local_file)
	except Exception as e:
		pass
	try:		
		remote_url = respuesta_sfe_campo(doc_id)['datosrepresentacion_copcedula']['archivo']['url']
		local_file = 'temp_pdf/'+fileNbr+'/'+fileNbr+'-3.pdf' 
		request.urlretrieve(remote_url, local_file)
	except Exception as e:
		pass
	try:		
		remote_url = respuesta_sfe_campo(doc_id)['datosrepresentacion_docpatrocionio']['archivo']['url']
		local_file = 'temp_pdf/'+fileNbr+'/'+fileNbr+'-4.pdf' 
		request.urlretrieve(remote_url, local_file)
	except Exception as e:
		pass	"""

#compilePDF('2348619')

#print(getFile_reg_and_ren('1439','2348619'))

#print(email_receiver('GEN'))

#rule_notification('dpj1','2348614')

#exist_notifi('AMA')

#print(compilePDF())

#registro_pdf_sfe_local('1439')

#print(respuesta_sfe_campo('1985'))
#print()
#print(respuesta_sfe_campo('1982')['datostitular_agregar'])
#print()
#print(respuesta_sfe_campo('1985')['datospersonales_tipo'])
#print()
#print(fetch_all_user_mark('MEA')[0]['sqlColumnList'][0]['sqlColumnValue'])

#print(exist_main_mark('PDM'))

#print(main_State('2348737'))

def rule_notification(sig,exp):
	if exist_main_mark(sig) == 'S' and main_State(exp) != False:
		try:	
			status_exp = main_State(exp)
			rule = email_receiver(str(status_exp))
			print(str(rule[0][0]), str(rule[0][2]), f"{str(rule[0][1])} {exp} status {str(status_exp)}")
			enviar_back_notFile(str(rule[0][0]), str(rule[0][2]), f"{str(rule[0][1])} {exp} status {str(status_exp)}")
		except Exception as e:
			status_exp = main_State(exp)
			rule = email_receiver('GEN')
			print(str(rule[0][0]), str(rule[0][2]), f"{str(rule[0][1])} {exp} status {str(status_exp)}")
			enviar_back_notFile(str(rule[0][0]), str(rule[0][2]), f"{str(rule[0][1])} {exp} status {str(status_exp)}")			
	else:
		if exist_notifi(sig) != 'null':
			rule = email_receiver(str(sig))
			try:
				print(str(rule[0][0]), str(rule[0][2]), f"{str(rule[0][1])} {exp}")	
				enviar_back_notFile(str(rule[0][0]), str(rule[0][2]), f"{str(rule[0][1])} {exp}")
			except Exception as e:
				pass

		elif exist_notifi(sig) == 'null':
			rule = email_receiver('GEN')
			try:
				print(str(rule[0][0]), str(rule[0][2]), f"{str(rule[0][1])} {exp} de tipo {sig}")
				enviar_back_notFile(str(rule[0][0]), str(rule[0][2]), f"{str(rule[0][1])} {exp} de tipo {sig}")
			except Exception as e:
				pass
		

#print(registro_sfe('26336'))

#print(user_doc_read_min('E','2355704','3','2023'))

#print(pendientes_sfe_not_pag('2023-07-13'))

#rule_notification('CP','2348740')

#rule_notification('PDM','2348741')

#print(email_receiver('GEN'))

#ETIQUETA PARA CANTIDAD DE TITULARES ['datostitular_agregar']

#print(respuesta_sfe_campo('2002'))



#print(fetch_all_user_mark('MEA')[0]['sqlColumnList'][0]['sqlColumnValue'])

def test(a=17,b=32):
	return(a,b)



#print(getPoder('76583'))

#print(test())

#print(Process_Read_EventList('2002432','1'))

#print(process_read('2005484', '1'))

#print(Process_Read_Action('','2002432','1'))

#print(registro_sfe('1982'))


#print(registro_sfe('2019'))


def b64_to_img_pdf(base,exp):
	try:
		image = base64.b64decode(base, validate=True)
		file_to_save = exp+'.png'
		with open(file_to_save, "wb") as f:
			f.write(image)
	except binascii.Error as e:
		print(e)

#logo = "AA=="
#b64_to_img(logo,'2355761')
#renovacion_pdf_con_acuse('26832')

#registro_pdf_con_acuse('26836')



#get_List = mark_getlist('2356458')				
#get_data_mark = mark_read(get_List[0].fileId.fileNbr.doubleValue,get_List[0].fileId.fileSeq,get_List[0].fileId.fileSeries.doubleValue,get_List[0].fileId.fileType)

#print(b64_to_img_pdf(base64.b64encode(get_data_mark['signData']['logo']['logoData']),'2356458'))

#decode_img(get_data_mark['signData']['logo']['logoData'])

#print(get_data_mark['file']['filingData']['captureDate']['dateValue'])



#renovacion_pdf_con_acuse('26919')

#renovacion_pdf_con_acuse('26891')


#registro_pdf_sfe_local('26938')

captura_pendientes()



"""
def file_Receive():
	try:
		data = {
				"arg0": "3",
				"arg1": "REG",
				"arg2": "MP",
				"arg3": {
					"fileId": {
					"fileNbr": {
						"doubleValue": ""
					},
					"fileSeq": "",
					"fileSeries": {
						"doubleValue": ""
					},
					"fileType": ""
					},
					"relationshipRole": "",
					"relationshipType": ""
				},
				"arg4": {
					"dateValue": "2023-06-30 13:10:00"
				},
				"arg5": {
					"currencyType": "GS",
					"DReceiptAmount": "100000",
					"receiptDate": {
					"dateValue": "2023-06-30"
					},
					"receiptNbr": "000222",
					"receiptType": "1"
				},
				"arg6": {
					"fileNbr": {
					"doubleValue": "2348748"
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
					"doubleValue": "2348748"
					},
					"docOrigin": "3",
					"docSeries": {
					"doubleValue": "2023"
					},
					"selected": ""
				},
				"arg8": "2023-06-30 13:08:00"
				}
		return clientMark.service.FileReceive(**data)
	except zeep.exceptions.Fault as e:
		return(e)


print(daily_log_open('2023-06-30'))
print(file_Receive())
print(daily_log_close('2023-06-30'))"""