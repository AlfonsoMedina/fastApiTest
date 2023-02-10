from ast import Return
from base64 import encode
import base64
from zeep import Client
import zeep
from io import open
import base64Decode
from subprocess import  Popen

file_temp=''
out_folder = 'PUB_FILE'

#Complemento LibreOffice en linux
#LIBRE_OFFICE = r"/usr//lib64//libreoffice//program//soffice"

#Complemento LibreOffice en Windows
LIBRE_OFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

def convert_to_pdf(input_docx, out_folder):
    p = Popen([LIBRE_OFFICE, '--headless', '--convert-to', 'pdf', '--outdir',
               out_folder, input_docx])
    print([LIBRE_OFFICE, '--convert-to', 'pdf', input_docx])
    p.communicate()


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
try:
	mark_service = 'http://192.168.50.200:8050'
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')
'''
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
	print('Error de coneccion  IPAS Diseño!!')'''

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


'''def fetch_all_offic_doc_PROC_NBR_ORD_PUBL(PROC_NBR):
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

def fetch_all_offic_doc_PROC_NBR_INFO_EXA(PROC_NBR):
	try:
		query = {
				  "arg0": "SELECT top 1 CONTENT_DATA FROM MARCAS_PY.ADMIN.IP_OFFIDOC WHERE OFFIDOC_TYP = 'INFO_EXA' and PROC_NBR = "+PROC_NBR,
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

def fetch_all_offic_doc_PROC_NBR_RENOVACI(PROC_NBR):
	try:
		query = {
				  "arg0": "SELECT top 1 CONTENT_DATA FROM MARCAS_PY.ADMIN.IP_OFFIDOC WHERE OFFIDOC_TYP = 'RENOVACI' and PROC_NBR = "+PROC_NBR,
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


decoded = base64.b64decode(base64Decode.decode_pdf(fetch_all_offic_doc_PROC_NBR_ORD_PUBL('1846886')))

#print(decoded)
            
with open('PUB_FILE/prueba uploader.doc','wb') as f:
	f.write(decoded)


decoded_INFO_EXA = base64.b64decode(base64Decode.decode_pdf(fetch_all_offic_doc_PROC_NBR_INFO_EXA('1363867')))

            
with open('PUB_FILE/prueba_INFO_EXA.doc','wb') as f:
	f.write(decoded_INFO_EXA)



decoded_RENOVACI = base64.b64decode(base64Decode.decode_pdf(fetch_all_offic_doc_PROC_NBR_RENOVACI('1366313')))

            
with open('PUB_FILE/prueba_RENOVACI.doc','wb') as f:
	f.write(decoded_RENOVACI)


file_temp= 'PUB_FILE/prueba_RENOVACI.doc'

convert_to_pdf(file_temp, out_folder)'''


def get_offi_doc_file(PROC_TYP,PROC_NBR,ACTION_NBR):
	try:
		query = {
				  "arg0": "SELECT  CONTENT_DATA FROM MARCAS_PY.ADMIN.IP_OFFIDOC WHERE ACTION_NBR = "+ACTION_NBR+" AND PROC_TYP = "+PROC_TYP+" AND PROC_NBR = "+PROC_NBR,
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

def file_create_pdf(PROC_TYP,PROC_NBR,ACTION_NBR):
	offiDoc = base64.b64decode(base64Decode.decode_pdf(get_offi_doc_file(PROC_TYP,PROC_NBR,ACTION_NBR)))           
	with open('PUB_FILE/offiDoc.doc','wb') as f:
		f.write(offiDoc)
	file_temp= 'PUB_FILE/offiDoc.doc'
	convert_to_pdf(file_temp, out_folder)

#file_create_pdf('2','1367136','7')




#descarga el archivo segunsu extencion
with open('PUB_FILE/prueba uploader.pdf','wb') as f:
	f.write("")#cadena de bytes