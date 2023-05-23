import time
import psycopg2
import os, shutil
from tools.filing_date import capture_year
from tools.connect import  PENDING, MEA_ADJUNTOS_DESTINO_location, host_SFE_conn,user_SFE_conn,password_SFE_conn, database_SFE_conn ,MEA_SFE_FORMULARIOS_ID_estado,MEA_SFE_FORMULARIOS_ID_tipo
from urllib import request	
from PyPDF2 import PdfMerger, PdfReader # pip install PyPDF2 - pip install PyPDF


def getFile(doc_id,fileNbr):	
	try:
		conn = psycopg2.connect(host = host_SFE_conn,user= user_SFE_conn,password = password_SFE_conn,database = database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute(PENDING.format(doc_id))
		row=cursor.fetchall()
		for i in row:
			for x in range(0,len(i[6])):
				if i[6][x]['campo'] == 'observacion_documentos':
					remote_url = i[6][x]['valor']['archivo']['url']
					local_file = str(MEA_ADJUNTOS_DESTINO_location)+'PY-E-'+capture_year()+'-'+fileNbr+'.pdf' 
					request.urlretrieve(remote_url, local_file)
	except Exception as e:
		conn.close()
	finally:
		conn.close()

def getFile_reg_and_ren(doc_id,fileNbr):
	os.mkdir('temp_pdf/'+fileNbr)	
	try:
		conn = psycopg2.connect(host = host_SFE_conn,user= user_SFE_conn,password = password_SFE_conn,database = database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute(PENDING.format(doc_id))
		row=cursor.fetchall()
		for i in row:
			for x in range(0,len(i[6])):
	
				if i[6][x]['campo'] == 'observacion_documentos':
					remote_url = i[6][x]['valor']['archivo']['url']
					local_file = 'temp_pdf/'+fileNbr+'/'+fileNbr+'-1.pdf' 
					request.urlretrieve(remote_url, local_file)

				if i[6][x]['campo'] == 'datosrepresentacion_decjurada':
					remote_url = i[6][x]['valor']['archivo']['url']
					local_file = 'temp_pdf/'+fileNbr+'/'+fileNbr+'-2.pdf' 
					request.urlretrieve(remote_url, local_file)					

				if i[6][x]['campo'] == 'datosrepresentacion_copcedula':
					remote_url = i[6][x]['valor']['archivo']['url']
					local_file = 'temp_pdf/'+fileNbr+'/'+fileNbr+'-3.pdf' 
					request.urlretrieve(remote_url, local_file)	

				if i[6][x]['campo'] == 'datosrepresentacion_docpatrocionio':
					remote_url = i[6][x]['valor']['archivo']['url']
					local_file = 'temp_pdf/'+fileNbr+'/'+fileNbr+'-4.pdf' 
					request.urlretrieve(remote_url, local_file)

	except Exception as e:
		conn.close()
	finally:
		conn.close()
	
	compilePDF(fileNbr)

def compilePDF(exp):
	listaPdfs = os.listdir('temp_pdf/'+exp)
	merger = PdfMerger()
	for file in listaPdfs:
		merger.append(PdfReader('temp_pdf/'+exp+'/'+file))
	merger.write(str(MEA_ADJUNTOS_DESTINO_location)+exp+'.pdf')
	try:
		shutil.rmtree('temp_pdf/'+exp)
	except OSError:
		os.remove('temp_pdf/'+exp)

	
