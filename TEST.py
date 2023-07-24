from dataclasses import replace
import json
import psycopg2
import tools.connect as connex



















































































































def respuesta_sfe_campo(arg):
	data = ''
	try:
		list_campos = []
		list_valores = {}
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
			from tramites where formulario_id in (29,4,3,27) and id = {}
		""".format(arg))
		row=cursor.fetchall()
		#print(row[0][6])
		for i in row[0][6]:
			try:
				list_campos.append({"campo": i['campo'],"valor": i['valor'],"isValid": "true","condicion": "","requerido": "false","componente": "textview","validacion": "","descripcion": i['descripcion']})			
			except Exception as e:
				list_campos.append({"campo": "","valor": "","isValid": "true","condicion": "","requerido": "false","componente": "textview","validacion": "","descripcion": ""})

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


listId = [27042,27040,27035,27034,27033,27032,27031,27030,27029,27028,27027,27026,27025,27024,27023,27022,27015,27014,27013,27012,27009,27007,27005,27004,27003,27002,27001,26998,26997,26996,26995,26990,26987,26986,26985,26983,26981,26980,26977,26975,26965,26964,26963,26962,26951,26949,26946,26945,26944,26943,26941,26939,26938,26937,26933,26932,26930,26922,26921,26919,26916,26915,26913,26911,26910,26909,26908,26907,26902,26901,26900,26899,26898,26897,26896,26895,26894,26893,26892,26891,26890,26889,26887,26886,26885,26884,26883,26882,26881,26880,26879,26878,26877,26876,26875,26874,26873,26872,26868,26867,26864,26863,26862,26861,26860,26857,26855,26854,26853,26852,26851,26850,26848,26847,26846,26845,26842,26841,26840,26839,26838,26837,26836,26835,26834,26833,26832,26831,26830,26829,26827,26826,26795,26794,26793,26788,26786,26785,26765,26760,25838,22340,22339]

for i in listId:
	respuesta_sfe_campo(i)