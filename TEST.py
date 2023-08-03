from email_pdf_AG import envio_agente_recibido
from getFileDoc import compilePDF_DOCS, getFile
from tools.filing_date import capture_day, capture_full, capture_full_upd
from dataclasses import replace
import json
import time
import psycopg2
from dinapi.sfe import respuesta_sfe_campo
import tools.connect as connex


#respuesta_sfe_campo('27228')

#getFile('27328','2360799')

#compilePDF_DOCS('2359729')




































































def campo_scan(arg):
	try:
		list_campos = []
		list_valores = {}
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
			from tramites where formulario_id in (27,28,29,4,70,95,3,100,101,102) and id = {}
		""".format(arg))
		row=cursor.fetchall()
		#print(row[0][6])
		for i in row[0][6]:
			try:
				if i['campo'] != 'descripcion_documentos2':
					list_campos.append({"campo": i['campo'],"valor": i['valor'],"isValId": "true","condicion": "","requerido": "false","componente": "textview","validacion": "","descripcion": i['descripcion']})			
			except Exception as e:
				list_campos.append({"campo": "","valor": "","isValId": "true","condicion": "","requerido": "false","componente": "textview","validacion": "","descripcion": ""})

		connUP = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = connUP.cursor()
		cursor.execute("""UPDATE public.tramites SET  respuestas='{}' WHERE id={};""".format( json.dumps(list_campos), arg))
		cursor.rowcount
		connUP.commit()
		connUP.close()		
	except Exception as e:
		print(e)
	finally:
		conn.close()

	#print(json.dumps(list_campos))
	
	return('true')

def create_list(arg):
	listId = []
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""SELECT id FROM public.tramites WHERE created_at >= '{} 00:59' and formulario_id in (27,28,29,95,4,70,3,100,101,102) and created_at <= '{} 22:59'""".format(arg,arg))
		row=cursor.fetchall()
		for i in row:
			campo_scan(i[0])
			listId.append(i[0])
		return listId
	except Exception as e:
		print(e)
	finally:
		conn.close()	 

#print(create_list('2023-07-25'))

def timer(step):
	print('')
	i = 0
	while i < step:
	##############################################################################################################                
		try:
			print(create_list(capture_day()))
		except Exception as e:
			pass
	##############################################################################################################
		time.sleep(3)

timer(59)



