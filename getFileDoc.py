import time
import psycopg2
import os, shutil
from dinapi.sfe import respuesta_sfe_campo
from tools.filing_date import capture_year
from tools.connect import  MEA_ADJUNTOS_DESTINO_REG_REN, PENDING, MEA_ADJUNTOS_DESTINO_location, host_SFE_conn,user_SFE_conn,password_SFE_conn, database_SFE_conn ,MEA_SFE_FORMULARIOS_ID_estado,MEA_SFE_FORMULARIOS_ID_tipo
from urllib import request	
from PyPDF2 import PdfMerger, PdfReader
import tools.filing_date as captureDate

from wipo.function_for_reception_in import user_doc_getList_escrito # pip install PyPDF2 - pip install PyPDF

def getFile(doc_id,fileNbr):
	#data_doc = user_doc_getList_escrito(fileNbr)
	#print(data_doc)
	remote_url = respuesta_sfe_campo(doc_id)['observacion_documentos']['archivo']['url'] #descripcion_documentos2
	local_file = str(MEA_ADJUNTOS_DESTINO_location)+str('3')+'-'+str('PY')+'-'+str(capture_year())+'-'+str(fileNbr)+'.pdf' 
	#local_file = f"temp_pdf/ {str('3')}-{str('E')}-{str('2023')}-{str(fileNbr)}.pdf" 					
	request.urlretrieve(remote_url, local_file)

def getFile_reg_and_ren(doc_id,fileNbr):
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
		pass

def compilePDF(exp):
	listaPdfs = os.listdir('temp_pdf/'+exp)
	merger = PdfMerger()
	try:
		merger.append(PdfReader(f'temp_pdf/{exp}/{exp}-0.pdf'))
	except Exception as e:
		pass	
	try:
		merger.append(PdfReader(f'temp_pdf/{exp}/{exp}-1.pdf'))
	except Exception as e:
		pass	
	try:
		merger.append(PdfReader(f'temp_pdf/{exp}/{exp}-2.pdf'))
	except Exception as e:
		pass	
	try:
		merger.append(PdfReader(f'temp_pdf/{exp}/{exp}-3.pdf'))
	except Exception as e:
		pass	
	try:
		merger.append(PdfReader(f'temp_pdf/{exp}/{exp}-4.pdf'))
	except Exception as e:
		pass	
	#for file in listaPdfs:
		#merger.append(PdfReader('temp_pdf/'+exp+'/'+file))
	merger.write(str(MEA_ADJUNTOS_DESTINO_REG_REN)+'PY-M-'+captureDate.capture_year()+'-'+exp+'.pdf')
	#merger.write('temp_pdf/'+'PY-M-'+captureDate.capture_year()+'-'+exp+'.pdf')
	try:
		shutil.rmtree('temp_pdf/'+exp)
	except OSError:
		os.remove('temp_pdf/'+exp)
