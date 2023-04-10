import time
import psycopg2
from tools.connect import  PENDING, host_SFE_conn,user_SFE_conn,password_SFE_conn, database_SFE_conn ,MEA_SFE_FORMULARIOS_ID_estado,MEA_SFE_FORMULARIOS_ID_tipo
from urllib import request	
	
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
					local_file = fileNbr+'.pdf' 
					request.urlretrieve(remote_url, local_file)
	except Exception as e:
		conn.close()
	finally:
		conn.close()

