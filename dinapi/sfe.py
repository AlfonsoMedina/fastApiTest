import base64
from math import ceil
import string
import time
import psycopg2
from tools.data_format import fecha_barra,hora
from tools.send_mail import enviar_back_notFile
import tools.filing_date as captureDate
import tools.connect as connex
from wipo.insertGroupProcessMEA import ProcessGroupAddProcess
from wipo.ipas import Process_Read, fetch_all_user_mark,  mark_getlist, mark_read, personAgente
from urllib import request
import qrcode


create_userdoc = {}
default_val = lambda arg: arg if arg == "null" else "" 
list_titulare = []


def respuesta_sfe_campo(arg):
	try:
		list_campos = []
		list_valores = {}
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
			from tramites where expediente_electronico = true and id = {}
		""".format(arg))
		row=cursor.fetchall()
		list_valores['id'] = row[0][0]
		list_valores['fecha'] = row[0][1]
		list_valores['formulario_id'] = row[0][2]
		list_valores['estado'] = row[0][3]
		list_valores['created_at'] = str(row[0][4])
		list_valores['updated_at'] = str(row[0][5])
		list_valores['costo'] = str(row[0][7])
		list_valores['usuario_id'] = str(row[0][8])
		list_valores['codigo'] = str(row[0][10])
		list_valores['firmado_at'] = str(row[0][11])
		list_valores['pagado_at'] = str(row[0][12])
		list_valores['enviado_at'] = str(row[0][15])
		list_valores['expediente_afectado'] = str(row[0][19])
		list_valores['tipo_documento_id'] = str(row[0][25])
		for i in range(0,len(row[0][6])):
			list_campos.append(row[0][6][i]['campo'])
		
		#print(" ")
		#print('[[[[[[[Lista de campos]]]]]]]]]')
		#print(list_campos)

		#print(" ")
		#print('(((((((((]Lista de valores[)))))))))')

		for item in range(0,len(list_campos)):
			for x in list_campos:
				if row[0][6][item]['campo'] == x:
					try:
						list_valores[x] = row[0][6][item]['valor']
					except Exception as e:
						list_valores[x] = 'sin valor'

	except Exception as e:
		print(e)
	finally:
		conn.close()
	return(list_valores)

def registro_sfe(arg):
	global_data = {}
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute(connex.TRAMITE_REG.format(int(arg)))
		row=cursor.fetchall()
		global_data['fecha_envio'] = str(row[0][17])
		global_data['expediente'] = str(row[0][15])
		global_data['fecha_solicitud'] = str(row[0][18])
		global_data['codigo_barr'] = str(row[0][12])
		global_data['usuario'] = str(row[0][19])
		global_data['code_agente'] = str(row[0][26])
		global_data['agente'] = str(row[0][25])
		global_data['email_agente'] = str(row[0][27])
		global_data['ag_tel'] = str(row[0][28])
		global_data['direccion_agente'] = str(row[0][29])
		global_data['nombre_formulario'] = str(row[0][3])
		global_data['pais_agente'] = "PY"
		for i in row[0][8]:
			if(i['descripcion'] == "Clase" and i['campo'] == 'marca_clase'):
				clase_tipo = i['valor']
				if(int(clase_tipo.replace(".0","")) <= 34):
					#print('PRODUCTO')
					global_data['clasificacion']= 'PRODUCTO'
				if(int(clase_tipo.replace(".0","")) >= 35):
					#print('SERVICIOS')
					global_data['clasificacion']= 'SERVICIOS'
			try:
				if(i['campo'] == "marca_distintivo"):
					global_data['distintivo'] = i['valor']['archivo']['url']
			except Exception as e:
				global_data['distintivo'] = "No definido"					
			try:
				if(i['descripcion'] == "N° de Documento" and i['campo'] == "datospersonales_nrodocumento"):
					global_data['documento'] = i['valor']
			except Exception as e:
				global_data['documento'] = "No definido"
			try:
				if(i['descripcion'] == "RUC" and i['campo'] == 'datospersonales_ruc'):
					#print(i['valor'])				
					global_data['RUC']=i['valor']
			except Exception as e:
				global_data['RUC'] = "No definido"	
			try:
				if(i['descripcion'] == "Productos o Servicios que distingue"):
					global_data['distingue'] = i['valor']
			except Exception as e:
				global_data['distingue'] = "No definido"										
			try:
				if(i['descripcion'] == "Reivindicaciones"):
					global_data['reivindicaciones'] = i['valor']
			except Exception as e:
				global_data['reivindicaciones'] = "No definido"	
			try:
				if(i['campo'] == "marca_tipomarca"):
					global_data["tipo_on"] = i['valor']
			except Exception as e:
				global_data['tipo_on'] = "No definido"	
			try:
				if(i['descripcion'] == "Denominación"):
					global_data['denominacion_on'] = i['valor']
			except Exception as e:
				global_data['denominacion_on'] = "No definido"
			try:
				if(i['descripcion'] == "Especificar"):
					global_data['especificar'] = i['valor']
			except Exception as e:
				global_data['especificar'] = "No definido"


			try:
				if(i['campo'] == 'datospersonales_nombreapellido'): 
					global_data['nombre_soli'] = i['valor']
			except Exception as e:
				global_data['nombre_soli'] = "No definido"

			try:
				if(i['campo'] == 'datospersonales_razonsocial'):
					global_data['razon_social']=i['valor']
			except Exception as e:
				global_data['razon_social'] = "No definido"	


			try:
				if(i['campo'] == 'datospersonales_calle'):
					global_data['direccion']=i['valor']
			except Exception as e:
				global_data['direccion'] = "No definido"
			try:
				if(i['campo'] == 'datospersonales_direccion'):
					global_data['direccion_dir']=i['valor']
			except Exception as e:
				global_data['direccion_dir'] = "No definido"
		
			try:
				if(i['descripcion'] == "Ciudad" and i['campo'] == 'datospersonales_ciudad'):
					global_data['ciudad']=i['valor']
			except Exception as e:
				global_data['ciudad'] = "No definido"					
			try:
				if(i['descripcion'] == "País " and i['campo'] == 'datospersonales_pais'):
					global_data['pais']=i['valor']
			except Exception as e:
				global_data['pais'] = "No definido"					
			try:
				if(i['descripcion'] == "Código Postal"):
					global_data['codigo_postal']=i['valor']
			except Exception as e:
				global_data['codigo_postal'] = "No definido"					
			try:
				if(i['descripcion'] == "Teléfono" and i['campo'] == 'datospersonales_telefono'):
					global_data['telefono']=i['valor']
			except Exception as e:
				global_data['telefono'] = "No definido"					
			try:
				if(i['descripcion'] == "Correo Electrónico" and i['campo'] == 'datospersonales_correoelectronico'):
					global_data['email']=i['valor']
			except Exception as e:
				global_data['email'] = "No definido"					
			try:
				if(i['descripcion'] == "Distrito"):
					global_data['distrito']=i['valor']
			except Exception as e:
				global_data['distrito'] = "No definido"
			try:
				if(i['descripcion'] == "Clase"):
					global_data['clase_on']=i['valor']
			except Exception as e:
				global_data['clase_on'] = "No definido"
			try:
				if(i['descripcion'] == "Documento" and i['campo'] == 'prioridad_docuprioridad'):
					global_data['documento_pri']=i['valor']
			except Exception as e:
				global_data['documento_pri'] = "No definido"
			try:
				if(i['descripcion'] == "N° de Solicitud" and i['campo'] == 'prioridad_nodesolicitud'):
					global_data['solicitud_pri']=i['valor']
			except Exception as e:
				global_data['solicitud_pri'] = "No definido"
			try:
				if(i['descripcion'] == "Fecha de Prioridad" and i['campo'] == 'prioridad_fechaprioridad'):
					global_data['fecha_pri']=i['valor']
			except Exception as e:
				global_data['fecha_pri'] = "No definido"
			try:
				if(i['descripcion'] == "País/Oficina" and i['campo'] == 'prioridad_paisoficina'):
					global_data['pais_pri']=i['valor']
			except Exception as e:
				global_data['pais_pri'] = "No definido"
			try:
				if(i['descripcion'] == "Especificar" and i['campo'] == 'marca_especificar'):
					global_data['espe']=i['valor']
			except Exception as e:
				global_data['espe'] = "No definido"
		
		#print(global_data)
		return(global_data)
	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def titulare_reg(arg):
	list_titulare = []

	for i in range(2,10):
		list_titulare.append(catch_owner(arg,i))

	if list_titulare[0]['person']['personName'] == '':	
		list_titulare.pop(0)
	if list_titulare[1]['person']['personName'] == '':	
		list_titulare.pop(1)
	if list_titulare[1]['person']['personName'] == '':	
		list_titulare.pop(1)
	if list_titulare[1]['person']['personName'] == '':	
		list_titulare.pop(1)
	if list_titulare[1]['person']['personName'] == '':	
		list_titulare.pop(1)
	if list_titulare[1]['person']['personName'] == '':	
		list_titulare.pop(1)
	if list_titulare[1]['person']['personName'] == '':	
		list_titulare.pop(1)
	if list_titulare[1]['person']['personName'] == '':	
		list_titulare.pop(1)
						
	return(list_titulare)

def catch_owner(arg,number):
	personas = {}
	global_data_titu = {}
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select t.id,t.fecha,t.formulario_id,f.nombre as nombre_formulario ,t.estado as estado_id,case when t.estado =7 then 'Enviado' when t.estado =8 then 'Recepcionado' end estado_desc,
						to_char(t.created_at,'yyyy-mm-dd hh24:mi:ss')created_at,to_char(t.updated_at,'yyyy-mm-dd hh24:mi:ss')updated_at,t.respuestas,t.costo,t.usuario_id, t.deleted_at,
						t.codigo,t.firmado_at,to_char(t.pagado_at,'yyyy-mm-dd hh24:mi:ss') as pagado_at,t.expediente_id,t.pdf_url,to_char(t.enviado_at,'yyyy-mm-dd hh24:mi:ss') as enviado_at,
						to_char(t.recepcionado_at,'yyyy-mm-dd hh24:mi:ss') as recepcionado_at,t.nom_funcionario,t.pdf,t.expediente_afectado,t.notificacion_id,t.expedientes_autor,t.autorizado_por_id,u.nombre as nombre_agente,pa.numero_agente,
						u.email as email_agente,pa.celular as telefonoAgente,pa.domicilio_agpi,t.nom_funcionario as funcionario_autorizado 
						from tramites t join formularios f on t.formulario_id  = f.id  
						join usuarios u on u.id = t.usuario_id  
						join perfiles_agentes pa on pa.usuario_id = u.id         
						where t.id = {};""".format(int(arg)))
		row=cursor.fetchall()
		for i in row[0][8]:
			if(i['campo'] == f"titular{number}_calle{number}"):
				global_data_titu['addressStreet'] = i['valor']
			if(i['campo'] == f"titular{number}_pais{number}"):
				global_data_titu['nationalityCountryCode'] = i['valor']
			if(i['campo'] == f"titular{number}_nombreapellido{number}"):
				global_data_titu['personName'] = i['valor']
			if(i['campo'] == f"titular{number}_pais{number}"):
				global_data_titu['residenceCountryCode'] = i['valor']
			if(i['campo'] == f"titular{number}_departamento{number}"):
				global_data_titu['addressZone'] = i['valor']
#			if(i['campo'] == f"titular{number}_actividad{number}"):
#				global_data_titu['actividad'] = i['valor']
#			if(i['campo'] == f"titular{number}_razonsocial{number}"):
#				global_data_titu['razonsocial'] = i['valor']
			if(i['campo'] == f"titular{number}_ciudad{number}"):
				global_data_titu['cityName'] = i['valor']
			if(i['campo'] == f"titular{number}_nrodocumento{number}"):
				global_data_titu['legalIdNbr'] = i['valor']                                    
			if(i['campo'] == f"titular{number}_ruc{number}"):
				global_data_titu['individualIdNbr'] = i['valor']
			if(i['campo'] == f"titular{number}_tipo{number}"):
				if i['valor'] == 'Persona Fisica':
					global_data_titu['individualIdType'] = 'RUC'
				else:
					global_data_titu['legalIdType'] = 'CI'
#			if(i['campo'] == f"titular{number}_sexo{number}"):
#				global_data_titu['sexo'] = i['valor']
			if(i['campo'] == f"titular{number}_correoelectronico{number}"):
				global_data_titu['email'] = i['valor']
			if(i['campo'] == f"titular{number}_codigopostal{number}"):
				global_data_titu['zipCode'] = i['valor']
			if(i['campo'] == f"titular{number}_telefono{number}"):
				global_data_titu['telephone'] = i['valor']
			

			personas['indService'] = "true"
			personas['orderNbr'] = ""
			personas['ownershipNotes'] = ""
			personas["person"] = global_data_titu

		return(personas)
	except Exception as e:
		print(e)
	finally:
		conn.close()	

def renovacion_sfe(arg):
	global_data = {}
	try:
		conn = psycopg2.connect(
					host = '192.168.50.219',
					user= 'user-developer',
					password = 'user-developer--201901',
					database = 'db_sfe_production'
				)
		cursor = conn.cursor()
		cursor.execute("""select t.id,t.fecha,t.formulario_id,f.nombre as nombre_formulario ,t.estado as estado_id,case when t.estado =7 then 'Enviado' when t.estado =8 then 'Recepcionado' end estado_desc,
								to_char(t.created_at,'yyyy-mm-dd hh24:mi:ss')created_at,to_char(t.updated_at,'yyyy-mm-dd hh24:mi:ss')updated_at,t.respuestas,t.costo,t.usuario_id, t.deleted_at,
								t.codigo,t.firmado_at,to_char(t.pagado_at,'yyyy-mm-dd hh24:mi:ss') as pagado_at,t.expediente_id,t.pdf_url,to_char(t.enviado_at,'yyyy-mm-dd hh24:mi:ss') as enviado_at,
								to_char(t.recepcionado_at,'yyyy-mm-dd hh24:mi:ss') as recepcionado_at,t.nom_funcionario,t.pdf,t.expediente_afectado,t.notificacion_id,t.expedientes_autor,t.autorizado_por_id,u.nombre as nombre_agente,pa.numero_agente,
								u.email as email_agente,pa.celular as telefonoAgente,pa.domicilio_agpi,t.nom_funcionario as funcionario_autorizado 
								from tramites t join formularios f on t.formulario_id  = f.id  
								join usuarios u on u.id = t.usuario_id  
								join perfiles_agentes pa on pa.usuario_id = u.id         
								where t.id = {};""".format(int(arg)))
		row=cursor.fetchall()
		print(row[0])
		global_data['fecha_envio'] = str(row[0][17])
		global_data['expediente'] = str(row[0][15])
		global_data['fecha_solicitud'] = str(row[0][18])
		global_data['codigo_barr'] = str(row[0][12])
		global_data['usuario'] = str(row[0][19])
		global_data['code_agente'] = str(row[0][26])
		global_data['nombre_agente'] = str(row[0][25])
		global_data['dir_agente'] = str(row[0][29])
		global_data['TEL_agente'] = str(row[0][28])
		global_data['email_agente'] = str(row[0][27])
		global_data['nombre_formulario'] = str(row[0][3])
		
		for i in row[0][8]:

			if(i['campo'] == 'marcarenov_clase'):
				clase_tipo = i['valor']
				if(int(clase_tipo.replace(".0","")) <= 34):
					global_data['clasificacion']= 'PRODUCTO'
				if(int(clase_tipo.replace(".0","")) >= 35):
					global_data['clasificacion']= 'SERVICIO'			


			try:					
				if(i['campo'] == "marcarenov_distintivo"):
					global_data['distintivo'] = i['valor']['archivo']['url']
			except Exception as e:
					global_data['distintivo'] = "No definido"	

			try:					
				if(i['campo'] == "actualizacion_refdistitivo"):
					global_data['distintivoAct'] = i['valor']['archivo']['url']
			except Exception as e:
					global_data['distintivoAct'] = "No definido"					
			
			try:	
				if(i['campo'] == "actualizacion_refdistitivo"):
					global_data['distintivo2'] = i['valor']['archivo']['url']
			except Exception as e:
				global_data['distintivo2'] = "No definido"							
			
			
			try:	
				if(i['descripcion'] == "N° de Documento"):
					global_data['documento'] = i['valor']
			except Exception as e:
				global_data['documento'] = "No definido"							
			
			try:	
				if(i['descripcion'] == "RUC"):				
					global_data['RUC']=i['valor']
			except Exception as e:
				global_data['RUC'] = "No definido"							
			
			try:	
				if(i['descripcion'] == "Productos o Servicios que distingue"):
					global_data['distingue'] = i['valor']
			except Exception as e:
				global_data['distingue'] = "No definido"							
			try:								
				if(i['descripcion'] == "Reivindicaciones"):
					global_data['reivindicaciones'] = i['valor']
			except Exception as e:
				global_data['reivindicaciones'] = "No definido"							
			try:	
				if(i['campo'] == 'marcarenov_tipomarca'):
					global_data["tipo_guion"] = i['valor']
			except Exception as e:
				global_data['tipo_guion'] = "No definido"
			try:	
				if(i['descripcion'] == "Denominación"):
					global_data['denominacion_on'] = i['valor']
			except Exception as e:
				global_data['denominacion_on'] = "No definido"							
			try:	
				if(i['descripcion'] == "Especificar"):
					global_data['especificar'] = i['valor']
			except Exception as e:
				global_data['especificar'] = "No definido"

			try:	
				if(i['campo'] == 'datospersonalesrenov_nombrerazon'): 
					global_data['nombre_soli'] = i['valor']
			except Exception as e:
				global_data['nombre_soli'] = "No definido"							
			try:						
				if(i['campo'] == 'marcarenov_denominacion'):
					global_data['razon_social']=i['valor']
			except Exception as e:
				global_data['razon_social'] = "No definido"

			try:	
				if(i['descripcion'] == "Dirección"):
					global_data['direccion']=i['valor']
			except Exception as e:
				global_data['direccion'] = "No definido"							
			try:	
				if(i['descripcion'] == "Ciudad"):
					global_data['ciudad']=i['valor']
			except Exception as e:
				global_data['ciudad'] = "No definido"							
			try:	
				if(i['descripcion'] == "País "):
					global_data['pais']=i['valor']
			except Exception as e:
				global_data['pais'] = "No definido"							
			try:						
				if(i['descripcion'] == "Código Postal"):
					global_data['codigo_postal']=i['valor']
			except Exception as e:
				global_data['codigo_postal'] = "No definido"							
			try:	
				if(i['descripcion'] == "Teléfono"):
					global_data['telefono']=i['valor']
			except Exception as e:
				global_data['telefono'] = "No definido"							
			try:	
				if(i['descripcion'] == "Correo Electrónico"):
					global_data['email']=i['valor']
			except Exception as e:
				global_data['email'] = "No definido"							
			try:
				if(i['descripcion'] == "Distrito"):
					global_data['distrito']=i['valor']
			except Exception as e:
				global_data['distrito'] = "No definido"						
			try:	
				if(i['descripcion'] == "N° de Documento / RUC" and i['campo'] == 'actualizacion_nodocumentoruc'):
					global_data['act_numero']=i['valor']
			except Exception as e:
				global_data['act_numero'] = "No definido"

			try:	
				if(i['campo'] == 'actualizacion_pais'):
					global_data['act_pais']=i['valor']
			except Exception as e:
				global_data['act_pais'] = "No definido"
						
			try:	
				if(i['descripcion'] == "Ciudad" and i['campo'] == 'actualizacion_ciudad'):
					global_data['act_ciudad']=i['valor']
			except Exception as e:
				global_data['act_ciudad'] = "No definido"
			try:	
				if(i['descripcion'] == "Código Postal" and i['campo'] == 'actualizacion_codigopostal'):
					global_data['act_post']=i['valor']
			except Exception as e:
				global_data['act_post'] = "No definido"
			try:	
				if(i['descripcion'] == "Teléfono" and i['campo'] == 'actualizacion_telefono'):
					global_data['act_tel']=i['valor']
			except Exception as e:
				global_data['act_tel'] = "No definido"
			try:	
				if(i['descripcion'] == "Correo Electrónico" and i['campo'] == 'actualizacion_correoelectronico'):
					global_data['act_email']=i['valor']
			except Exception as e:
				global_data['act_email'] = "No definido"
			try:	
				if(i['descripcion'] == "Clase" and i['campo'] == 'marcarenov_clase'):
					global_data['clase_on']=i['valor']
			except Exception as e:
				global_data['clase_on'] = "No definido"
			try:	
				if(i['campo'] == 'marcarenov_registrono'): 
					global_data['registro_nbr']=i['valor']
			except Exception as e:
				global_data['registro_nbr'] = "No definido"
			try:	
				if(i['descripcion'] == "País " and i['campo'] == 'datospersonalesrenov_pais'):
					global_data['solic_pais']=i['valor']
			except Exception as e:
				global_data['solic_pais'] = "No definido"
	
			try:	
				if(i['campo'] == 'datospersonalesrenov_calle'):
					global_data['solic_dir'] = str(i['valor']).replace(" – "," | ")
			except Exception as e:
				global_data['solic_dir'] = "No definido"

			try:
				if(i['campo'] == 'actualizacion_calle'):
					global_data['solic_dir2'] = str(i['valor']).replace(" – "," | ")
			except Exception as e:
				global_data['solic_dir2'] = "No definido"

			try:	
				if(i['descripcion'] == "Teléfono" and i['campo'] == 'datospersonalesrenov_telefono'):
					global_data['solic_tel']=i['valor']
			except Exception as e:
				global_data['solic_tel'] = "No definido"
			try:	
				if(i['descripcion'] == "Correo Electrónico" and i['campo'] == 'datospersonalesrenov_correoelectronico'):
					global_data['solic_email']=i['valor']
			except Exception as e:
				global_data['solic_email'] = "No definido"
			try:	
				if(i['descripcion'] == "Número" and i['campo'] == 'actualizacion_numero'):
					global_data['actc_num']=i['valor']
			except Exception as e:
				global_data['actc_num'] = "No definido"

		return(global_data)
	except Exception as e:
		print(e)
	finally:
		conn.close()

def oposicion_sfe(arg):
			global_data = {}
			try:
				conn = psycopg2.connect(
					host = 'pgsql-sprint.dinapi.gov.py',
					user= 'user-sprint',
					password = 'user-sprint--201901',
					database = 'db_sfe_production'
				)
				cursor = conn.cursor()
				cursor.execute("""select t.id,t.fecha,t.formulario_id,f.nombre as nombre_formulario ,t.estado as estado_id,case when t.estado =7 then 'Enviado' when t.estado =8 then 'Recepcionado' end estado_desc,
								to_char(t.created_at,'yyyy-mm-dd hh24:mi:ss')created_at,to_char(t.updated_at,'yyyy-mm-dd hh24:mi:ss')updated_at,t.respuestas,t.costo,t.usuario_id, t.deleted_at,
								t.codigo,t.firmado_at,to_char(t.pagado_at,'yyyy-mm-dd hh24:mi:ss') as pagado_at,t.expediente_id,t.pdf_url,to_char(t.enviado_at,'yyyy-mm-dd hh24:mi:ss') as enviado_at,
								to_char(t.recepcionado_at,'yyyy-mm-dd hh24:mi:ss') as recepcionado_at,t.nom_funcionario,t.pdf,t.expediente_afectado,t.notificacion_id,t.expedientes_autor,t.autorizado_por_id,u.nombre as nombre_agente,pa.numero_agente,
								u.email as email_agente,pa.celular as telefonoAgente,pa.domicilio_agpi,t.nom_funcionario as funcionario_autorizado 
								from tramites t join formularios f on t.formulario_id  = f.id  
								join usuarios u on u.id = t.usuario_id  
								join perfiles_agentes pa on pa.usuario_id = u.id         
								where t.id = {};""".format(int(arg)))
				row=cursor.fetchall()
				global_data['fecha_envio'] = str(row[0][17])
				global_data['expediente'] = str(row[0][15])
				global_data['fecha_solicitud'] = str(row[0][18])
				global_data['codigo_barr'] = str(row[0][12])
				global_data['usuario'] = str(row[0][19])
				global_data['code_agente'] = str(row[0][26])
				global_data['nombre_agente'] = str(row[0][25])
				global_data['email_agente'] = str(row[0][27])
				global_data['tel_agente'] = str(row[0][28])
				global_data['direc_agente'] = str(row[0][29])
				global_data['nombre_formulario'] = str(row[0][3])
				for i in row[0][8]:
					try:
						if(i['descripcion'] == "Buscar Solicitud N°" and i['campo'] == 'expedienteamarcas_buscarsolicitud'):
							global_data['solicitud'] = i['valor']
					except Exception as e:
						global_data['solicitud'] = "No definido"

					try:
						if(i['descripcion'] == "En Fecha" and i['campo'] == 'expedienteamarcas_fecha'):				
							global_data['fecha']=i['valor']
					except Exception as e:
						global_data['fecha'] = "No definido"

					try:
						if(i['descripcion'] == "Nombres y Apellidos / Razón Social" and i['campo'] == 'datospersonalesv2_nombresrazon'):				
							global_data['ras_social']=i['valor']
					except Exception as e:
						global_data['ras_social'] = "No definido"

					try:
						if(i['descripcion'] == "Clase" and i['campo'] == 'expedienteamarcas_clase'):
							global_data['clase'] = i['valor']
					except Exception as e:
						global_data['clase'] = "No definido"

					try:
						if(i['descripcion'] == "Denominación" and i['campo'] == 'expedientebmarcas_denominacionb'):
							global_data['denominacionB'] = i['valor']
					except Exception as e:
						global_data['denominacionB'] = "No definido"
						
					try:
						if(i['descripcion'] == "Clase" and i['campo'] == 'expedientebmarcas_claseb'):
							global_data['claseB'] = i['valor']
					except Exception as e:
						global_data['claseB'] = "No definido"

					try: # Marca extranjera
						if(i['descripcion'] == "Clase" and i['campo'] == 'datosopone1_claseint'):
							global_data['clase_b'] = i['valor']
					except Exception as e:
						global_data['clase_b'] ="No definido"

					try: # Marca extranjera
						if(i['descripcion'] == "Denominación" and i['campo'] == 'datosopone1_denominacionint'):
							global_data['denominacion_b'] = i['valor']
					except Exception as e:
						global_data['denominacion_b'] ="No definido"

					try:				
						if(i['descripcion'] == "Denominación" and i['campo'] == 'expedienteamarcas_denominacion'):
							global_data['denominacion'] = i['valor']
					except Exception as e:
						global_data['denominacion'] = "No definido"					
					
					try:
						if(i['descripcion'] == "Solicitud N°" and i['campo'] == 'expedientebmarcas_solicitudb'):
							global_data["solicitud2"] = i['valor']
					except Exception as e:
						global_data["solicitud2"] =	"No definido"				
					
					try:
						if(i['descripcion'] == "En Fecha" and i['campo'] == 'expedientebmarcas_fechab'):
							global_data["fecha2"] = i['valor']						
					except Exception as e:
						global_data["fecha2"] = "No definido"					
					
					try:
						if(i['descripcion'] == "Buscar Registro N°" and i['campo'] == 'expedientebmarcas_buscarregistrob'):
							global_data['registro'] = i['valor']
					except Exception as e:
						global_data['registro'] = "No definido"					
					
					try:						
						if(i['descripcion'] == "Nombres y Apellidos / Razón Social" and i['campo'] == 'expedientebmarcas_nombrerazonb'):
							global_data['razon_socialB']=i['valor']
					except Exception as e:
						global_data['razon_socialB']="No definido"					
					
					try:
						if(i['descripcion'] == "País " and i['campo'] ==  'datospersonalesv2_pais'):
							global_data['pais']=i['valor']
					except Exception as e:
						global_data['pais']="No definido"					
					
					try:
						if(i['descripcion'] == "Ciudad" and i['campo'] ==  'datospersonalesv2_ciudad'):
							global_data['ciudad']=i['valor']
					except Exception as e:
						global_data['ciudad']="No definido"					
					
					try:
						if(i['descripcion'] == "Código Postal" and i['campo'] == 'datospersonalesv2_codigopostal'):
							global_data['code_post']=i['valor']
					except Exception as e:
						global_data['code_post']="No definido"					
					
					try:						
						if(i['descripcion'] == "Dirección" and i['campo'] == 'datospersonalesv2_direccion'):
							global_data['direccion']=i['valor']
					except Exception as e:
						global_data['direccion']="No definido"					
					
					try:
						if(i['descripcion'] == "Teléfono" and i['campo'] == 'datospersonalesv2_telefono'):
							global_data['telefono']=i['valor']
					except Exception as e:
						global_data['telefono']="No definido"					
					
					try:
						if(i['descripcion'] == "Correo Electrónico" and i['campo'] == 'datospersonalesv2_correoelectronico'):
							global_data['email']=i['valor']
					except Exception as e:
						global_data['email']="No definido"					
					
					try:
						if(i['descripcion'] == "Número de Poder" and i['campo'] == 'datosrepresentacion2_podernro'):
							global_data['poder']=i['valor']
					except Exception as e:
						global_data['poder']="No definido"					
					
					try:
						if(i['descripcion'] == "Descripción de la Observación" and i['campo'] == 'observacion_descobservacion'):
							global_data['observaciones']=i['valor']
					except Exception as e:
						global_data['observaciones']="No definido"

				return(global_data)
			except Exception as e:
				print(e)
			finally:
				conn.close()

def pendientes_sfe(fecha:string,ver,pag):
	try:
		lista = []
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""
select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,
codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,
to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,
notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id, enviado_at as bruto from tramites where estado in ({}) and formulario_id in ({}) 
and enviado_at >= '{} 00:59:59' and expediente_electronico = true and enviado_at <= '{} 23:59:59' order by enviado_at asc LIMIT {} offset {}
		""".format(connex.MEA_SFE_FORMULARIOS_ID_estado,connex.MEA_SFE_FORMULARIOS_ID_tipo,fecha,fecha,ver,pag))
		row=cursor.fetchall()
		for i in row:
			lista.append({
						'Id':i[0],
						'fecha':i[1],
						'tip_doc':i[2],             
						'formulario_id':tipo_form(i[2]),     
						'estado': i[3],            
						'created_at':i[4],        
						'updated_at':i[5],        
						'respuestas':i[6],        
						'costo':i[7],             
						'usuario_id':i[8],        
						'deleted_at':i[9],        
						'codigo':i[10],            
						'firmado_at':i[11],        
						'pagado_at':str(pago_id(i[0])),         
						'expediente_id':i[13],     
						'pdf_url':i[14],           
						'enviado_at':str(i[15])[0:10]+" "+str(captureDate.time_difference(str(i[26]),3))[10:19],        
						'recepcionado_at':i[16],   
						'nom_funcionario':i[17],   
						'pdf':str(i[18]),               
						'expediente_afectad':i[19],
						'notificacion_id':i[20],   
						'expedientes_autor':i[21], 
						'autorizado_por_id':i[22], 
						'locked_at':i[23],         
						'locked_by_id':i[24],      
						'tipo_documento_id':status_typ(str(i[25]))[2],
						'tool_tip':status_typ(str(i[25]))[1],
						'row':str(captureDate.time_difference(str(i[26]),3))
						})
			
		return(lista)	
	except Exception as e:
		pass
	finally:
		conn.close()	

def pendientes_sfe_not_pag(fecha:string):
	try:
		lista = []
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""
select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,
codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,
to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,
notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id, enviado_at as bruto from tramites where estado in ({}) and formulario_id in ({}) 
and enviado_at >= '{} 00:59:59' and expediente_electronico = true and enviado_at <= '{} 23:59:59' order by enviado_at asc 
		""".format(connex.MEA_SFE_FORMULARIOS_ID_estado,connex.MEA_SFE_FORMULARIOS_ID_tipo,fecha,fecha))
		row=cursor.fetchall()
		for i in row:
			lista.append({
						'Id':i[0],
						'fecha':i[1],
						'tip_doc':i[2],             
						'formulario_id':tipo_form(i[2]),     
						'estado': i[3],            
						'created_at':i[4],        
						'updated_at':i[5],        
						'respuestas':i[6],        
						'costo':i[7],             
						'usuario_id':i[8],        
						'deleted_at':i[9],        
						'codigo':i[10],            
						'firmado_at':i[11],        
						'pagado_at':str(pago_id(i[0])),         
						'expediente_id':i[13],     
						'pdf_url':i[14],           
						'enviado_at':str(i[15])[0:10]+" "+str(captureDate.time_difference(str(i[26]),3))[10:19],        
						'recepcionado_at':i[16],   
						'nom_funcionario':i[17],   
						'pdf':str(i[18]),               
						'expediente_afectad':i[19],
						'notificacion_id':i[20],   
						'expedientes_autor':i[21], 
						'autorizado_por_id':i[22], 
						'locked_at':i[23],         
						'locked_by_id':i[24],      
						'tipo_documento_id':status_typ(str(i[25]))[2],
						'tool_tip':status_typ(str(i[25]))[1],
						'row':str(captureDate.time_difference(str(i[26]),3))
						})
			
		return(lista)	
	except Exception as e:
		conn.close()
	finally:
		conn.close()

def pendientes_sfe_soporte(fecha:string):
	try:
		lista = []
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""
select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,
codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,
to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,
notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id from tramites where estado in ({}) and formulario_id in ({}) 
and enviado_at >= '{} 00:59:59' and expediente_electronico = true and enviado_at <= '{} 23:59:59'; 
		""".format('99',connex.MEA_SFE_FORMULARIOS_ID_tipo,fecha,fecha))
		row=cursor.fetchall()
		for i in row:
			lista.append({
						'Id':i[0],
						'fecha':i[1],
						'tip_doc':i[2],             
						'formulario_id':tipo_form(i[2]),     
						'estado': i[3],            
						'created_at':i[4],        
						'updated_at':i[5],        
						'respuestas':i[6],        
						'costo':i[7],             
						'usuario_id':i[8],        
						'deleted_at':i[9],        
						'codigo':i[10],            
						'firmado_at':i[11],        
						'pagado_at':str(pago_id(i[0])),         
						'expediente_id':i[13],     
						'pdf_url':i[14],           
						'enviado_at':i[15],        
						'recepcionado_at':i[16],   
						'nom_funcionario':i[17],   
						'pdf':str(i[18]),               
						'expediente_afectad':i[19],
						'notificacion_id':i[20],   
						'expedientes_autor':i[21], 
						'autorizado_por_id':i[22], 
						'locked_at':i[23],         
						'locked_by_id':i[24],      
						'tipo_documento_id':status_typ(str(i[25]))[2],
						'tool_tip':status_typ(str(i[25]))[1]
						})
		return(lista)	
	except Exception as e:
		pass
	finally:
		conn.close()

def pendiente_sfe(arg):
	try:
		lista = []
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
			from tramites where expediente_electronico = true and id = {}
		""".format(arg))
		row=cursor.fetchall()
		for i in row:
			sigla = str(status_typ(str(i[25]))[1]).split("-")
			t_id = str(reglas_me_ttasa(status_typ(str(i[25]))[2])[0])
			if t_id == '0':
				id_tasa = ''
				desc_tasa = ''
			else:
				id_tasa = str(reglas_me_ttasa(status_typ(str(i[25]))[2])[0])
				desc_tasa = str(tasa_id(str(reglas_me_ttasa(status_typ(str(i[25]))[2])[0]))[1])					
			lista.append({
						'Id':i[0],
						'fecha':i[1],
						'tip_doc':i[2],             
						'formulario_id':tipo_form(i[2]),     
						'estado': i[3],            
						'created_at':i[4],        
						'updated_at':i[5],        
						'respuestas':i[6],        
						'costo':i[7],             
						'usuario_id':i[8],        
						'deleted_at':i[9],        
						'codigo':i[10],            
						'firmado_at':i[11],        
						'pagado_at':str(pago_id(i[0])),         
						'expediente_id':str(i[13]),     
						'pdf_url':i[14],           
						'enviado_at':i[15],        
						'recepcionado_at':i[16],   
						'nom_funcionario':i[17],   
						'pdf':str(i[18]),               
						'expediente_afectad':str(i[19]),
						'notificacion_id':i[20],   
						'expedientes_autor':i[21], 
						'autorizado_por_id':i[22], 
						'locked_at':i[23],         
						'locked_by_id':i[24],      
						'tipo_documento_id':status_typ(str(i[25]))[2],
						'tool_tip':status_typ(str(i[25]))[1],
						'tasa_id':id_tasa,
						'tasa_desc':desc_tasa,
						'sigl':sigla[0]
						})
		return(lista)	
	except Exception as e:
		pass
	finally:
		conn.close()

def tipo_form(form):
	try:
		lista = []
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select nombre,id  from formularios where id = {}""".format(form))
		row=cursor.fetchall()
		for i in row:
			return(i[0])	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def status_typ(tipo):
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select id,nombre,siglas  from tipos_documento where id = {} """.format(tipo))
		row=cursor.fetchall()
		for i in row:
			return(i)	
	except Exception as e:
		return(12, '', '[SIN DATO]')
	finally:
		conn.close()

def pago_id(pago):
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select authorization_number from bancard_transactions where status = 1 and  payable_id = {} """.format(str(pago)))
		row=cursor.fetchall()
		for i in row:
			return(i[0])	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def code_ag(arg): 
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select numero_agente from perfiles_agentes where usuario_id = {}  """.format(arg))
		row=cursor.fetchall()
		for i in row:
			return(i[0])	
	except Exception as e:
		return(e)
	finally:
		conn.close()

def estado(arg):
	if arg == 7:
		return('Enviado')
	if arg == 8:
		return('Recibido')

def cambio_estado(Id,exp):
	try:
		connA = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursorA = connA.cursor()
		cursorA.execute("""select * from tramites where id = {}""".format(Id))
		row=cursorA.fetchall()
		for i in row:
			conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
			cursor = conn.cursor()
			cursor.execute("""UPDATE public.tramites set estado = 8, expediente_id = {},recepcionado_at = '{}' WHERE id={};""".format( exp , captureDate.capture_full_upd(), Id))
			cursor.rowcount
			conn.commit()
			conn.close()
	except Exception as e:
		print(e)
	finally:
		connA.close()	

def cambio_estado_soporte(Id):
	try:
		connA = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursorA = connA.cursor()
		cursorA.execute("""select * from tramites where id = {}""".format(Id))
		row=cursorA.fetchall()
		for i in row:
			conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
			cursor = conn.cursor()
			cursor.execute("""UPDATE public.tramites set estado = 99 WHERE id={};""".format(Id))
			cursor.rowcount
			conn.commit()
			conn.close()
	except Exception as e:
		print(e)
	finally:
		connA.close()

def count_pendiente(fecha:string):
	try:
		lista = []
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select count(*) from tramites where estado in ({}) and formulario_id in ({}) and enviado_at >= '{} 00:59:59' 
		and expediente_electronico = true and enviado_at <= '{} 23:59:59'""".format(connex.MEA_SFE_FORMULARIOS_ID_estado,connex.MEA_SFE_FORMULARIOS_ID_tipo,fecha,fecha))
		row=cursor.fetchall()
		for i in row:
			reg=i[0]
			pag=reg/10
			cant = []
			for i in range(ceil(pag)):
				cant.append(i)
		return({"registros":reg,"paginas":cant})	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def tip_doc():
	try:
		tipo_form = []
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select siglas  from tipos_documento  where formulario_id  in  ({})""".format(connex.MEA_SFE_FORMULARIOS_ID_tipo))
		row=cursor.fetchall()
		for i in row:
			tipo_form.append(i)
		return(tipo_form)	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def reglas_me():
	try:
		reglas = []
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select tipo_doc,ma,pa,di,ig,rq_cb,rq_pago,ttasa,exp_ri,esc_ri,rq_sol,rq_ag,estado from reglas_me where estado = 'Activo' and tipo_escrito in ({})""".format(str(tip_doc()).replace("[","").replace("]","").replace("(","").replace(",)","")))
		row=cursor.fetchall()
		for i in row:
			reglas.append(i)
		return(reglas)	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def reglas_me_ttasa(sig):
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select ttasa from reglas_me where tipo_escrito = '{}'""".format(sig)) #select ttasa from reglas_me where tipo_doc like '{} %'
		row=cursor.fetchall()
		for i in row:
			return(i)	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def format_userdoc(doc_Id):
	ruc_Typ:str = ''
	ci_Typ:str = ''	
	ruc_Nbr:str = ''
	ci_Nbr:str = ''
	fileSeq:str =''
	fileTyp:str = '' 
	data = pendiente_sfe(doc_Id)
	try:
		ag_data = personAgente(code_ag(data[0]['usuario_id']))[0]
	except Exception as e:
		print("No existe el Agente")

	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_tipo':	
				if str(data[0]['respuestas'][i]['valor']) == 'Persona Jurídica':
					ruc_Typ = 'RUC'
				else:
					ci_Typ = 'CED'	 
	except Exception as e:
		pass

	try:
		if ruc_Typ == 'RUC': 
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_documento':	
					ruc_Nbr = str(data[0]['respuestas'][i]['valor'])
		if ci_Typ == 'CED': 
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'datospersonales_documento':	
					ci_Nbr = str(data[0]['respuestas'][i]['valor'])							
	except Exception as e:
		pass
	
	if str(data[0]['expediente_afectad']) != "None":
		fileSeq = "PY"
		fileTyp = "M"
	else:
		fileSeq = ""
		fileTyp = ""		


	create_userdoc['affectedFileIdList_fileNbr'] = str(data[0]['expediente_afectad']).replace("None","")
	create_userdoc['affectedFileIdList_fileSeq'] = fileSeq
	try:#
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'expedienteoescrito_fecha':	
				create_userdoc['affectedFileIdList_fileSeries'] = str(data[0]['respuestas'][i]['valor'][0:4])
		#create_userdoc['affectedFileIdList_fileSeries']=str(int(mark_getlist(data[0]['expediente_afectad'])[0]['fileId']['fileSeries']['doubleValue']))
	except Exception as e:
		create_userdoc['affectedFileIdList_fileSeries']=""
	
	create_userdoc['affectedFileIdList_fileType'] = fileTyp


	create_userdoc['affectedFileSummaryList_disclaimer'] = ""
	create_userdoc['affectedFileSummaryList_disclaimerInOtherLang'] = ""
	create_userdoc['affectedFileSummaryList_fileNbr'] = ""
	create_userdoc['affectedFileSummaryList_fileSeq'] = ""
	create_userdoc['affectedFileSummaryList_fileSeries'] = ""
	create_userdoc['affectedFileSummaryList_fileType'] = ""
	create_userdoc['affectedFileSummaryList_fileIdAsString'] = ""
	create_userdoc['affectedFileSummaryList_fileSummaryClasses'] = ""
	create_userdoc['affectedFileSummaryList_fileSummaryCountry'] = ""
	create_userdoc['affectedFileSummaryList_fileSummaryDescription'] = ""
	create_userdoc['affectedFileSummaryList_fileSummaryDescriptionInOtherLang'] = ""
	create_userdoc['affectedFileSummaryList_fileSummaryOwner'] = ""
	create_userdoc['affectedFileSummaryList_fileSummaryOwnerInOtherLang'] = ""
	create_userdoc['affectedFileSummaryList_fileSummaryRepresentative'] = ""
	create_userdoc['affectedFileSummaryList_fileSummaryRepresentativeInOtherLang'] = ""
	create_userdoc['affectedFileSummaryList_fileSummaryResponsibleName'] = ""
	create_userdoc['affectedFileSummaryList_fileSummaryStatus'] = ""


	create_userdoc['applicant_applicantNotes'] = "Aplicante SPRINT M.E.A."

	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_direccion':	
				create_userdoc['applicant_person_addressStreet'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['applicant_person_addressStreet'] = ""

	create_userdoc['applicant_person_addressStreetInOtherLang'] = ""
	create_userdoc['applicant_person_addressZone'] = ""
	create_userdoc['applicant_person_agentCode'] = ""

	create_userdoc['applicant_person_cityCode'] = ""

	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_ciudad':			
				create_userdoc['applicant_person_cityName'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['applicant_person_cityName'] =""

	create_userdoc['applicant_person_companyRegisterRegistrationDate'] = ""
	create_userdoc['applicant_person_companyRegisterRegistrationNbr'] = ""
	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_correoelectronico':			
				create_userdoc['applicant_person_email'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['applicant_person_email'] = ""

	create_userdoc['applicant_person_individualIdNbr'] = ci_Nbr
	
	create_userdoc['applicant_person_individualIdType'] = ci_Typ
	
	create_userdoc['applicant_person_legalIdNbr'] = ruc_Nbr

	create_userdoc['applicant_person_legalIdType'] = ruc_Typ		
	
	create_userdoc['applicant_person_legalNature'] = ""
	create_userdoc['applicant_person_legalNatureInOtherLang'] = ""
	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_pais':
				create_userdoc['applicant_person_nationalityCountryCode'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['applicant_person_nationalityCountryCode'] = ""
	create_userdoc['applicant_person_personGroupCode'] = ""
	create_userdoc['applicant_person_personGroupName'] = ""
	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_nombresrazon':
				create_userdoc['applicant_person_personName'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['applicant_person_personName'] = ""
	create_userdoc['applicant_person_personNameInOtherLang'] = ""
	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_pais':
				create_userdoc['applicant_person_residenceCountryCode'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['applicant_person_residenceCountryCode'] = "" 
	create_userdoc['applicant_person_stateCode'] = ""
	create_userdoc['applicant_person_stateName'] = ""
	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_telefono':
				create_userdoc['applicant_person_telephone'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['applicant_person_telephone'] = ""
	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_codigopostal':
				create_userdoc['applicant_person_zipCode'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['applicant_person_zipCode'] = ""
	
	
	
	try:
		create_userdoc['documentId_docLog'] = "E"
	except Exception as e:
		create_userdoc['documentId_docLog'] = ""
	try:
		create_userdoc['documentId_docNbr'] = str(process_day_Nbr())
	except Exception as e:
		create_userdoc['documentId_docNbr'] = ""	
	try:
		create_userdoc['documentId_docOrigin'] = str(connex.MEA_SFE_FORMULARIOS_ID_Origin)
	except Exception as e:
		create_userdoc['documentId_docOrigin'] = ""	
	try:
		create_userdoc['documentId_docSeries'] = captureDate.capture_year()
	except Exception as e:
		create_userdoc['documentId_docSeries'] = ""	
	try:
		create_userdoc['documentId_selected'] = ""
	except Exception as e:
		create_userdoc['documentId_selected'] = ""	
	try:	
		create_userdoc['documentSeqId_docSeqName'] = "Documentos"
	except Exception as e:
		create_userdoc['documentSeqId_docSeqName'] = ""	
	try:	
		create_userdoc['documentSeqId_docSeqNbr'] = str(process_day_Nbr())
	except Exception as e:
		create_userdoc['documentSeqId_docSeqNbr'] = ""	
	try:	
		create_userdoc['documentSeqId_docSeqSeries'] = captureDate.capture_year()
	except Exception as e:
		create_userdoc['documentSeqId_docSeqSeries'] = ""	
	try:
		create_userdoc['documentSeqId_docSeqType'] = "PY"
	except Exception as e:
		create_userdoc['documentSeqId_docSeqType'] = ""	
	
	

	create_userdoc['filingData_applicationSubtype'] = ""
	create_userdoc['filingData_applicationType'] = ""
	create_userdoc['filingData_captureDate'] = captureDate.capture_full()
	create_userdoc['filingData_captureUserId'] = "4"
	create_userdoc['filingData_filingDate'] = captureDate.capture_full()
	create_userdoc['filingData_lawCode'] = ""
	create_userdoc['filingData_novelty1Date'] = ""
	create_userdoc['filingData_novelty2Date'] = ""


	create_userdoc['filingData_paymentList_currencyName'] = "Guaraníes"
	create_userdoc['filingData_paymentList_currencyType'] = "GS"
	try:
		create_userdoc['filingData_paymentList_receiptAmount'] = str(pago_data(doc_Id)[1])
	except Exception as e:
		create_userdoc['filingData_paymentList_receiptAmount'] = ""
	try:	
		create_userdoc['filingData_paymentList_receiptDate'] = str(pago_data(doc_Id)[2])[0:10]
	except Exception as e:
		create_userdoc['filingData_paymentList_receiptDate'] = ""		
	try:
		create_userdoc['filingData_paymentList_receiptNbr'] = str(pago_data(doc_Id)[0])
	except Exception as e:
		create_userdoc['filingData_paymentList_receiptNbr'] = ""		

	create_userdoc['filingData_paymentList_receiptNotes'] = " Caja MEA"
	create_userdoc['filingData_paymentList_receiptType'] = str(data[0]['tasa_id'])
	create_userdoc['filingData_paymentList_receiptTypeName'] = str(data[0]['tasa_desc'])


	create_userdoc['filingData_receptionDate'] = captureDate.capture_full()
	create_userdoc['filingData_documentId_receptionDocument_docLog'] = "E"
	create_userdoc['filingData_documentId_receptionDocument_docNbr'] = str(process_day_Nbr())
	create_userdoc['filingData_documentId_receptionDocument_docOrigin'] = str(connex.MEA_SFE_FORMULARIOS_ID_Origin)
	create_userdoc['filingData_documentId_receptionDocument_docSeries'] = captureDate.capture_year()
	create_userdoc['filingData_documentId_receptionDocument_selected'] = ""
	create_userdoc['filingData_userdocTypeList_userdocName'] = str(data[0]['tool_tip'])
	create_userdoc['filingData_userdocTypeList_userdocType'] = str(data[0]['tipo_documento_id'])
	
	

	create_userdoc['newOwnershipData_ownerList_orderNbr'] = ""
	create_userdoc['newOwnershipData_ownerList_ownershipNotes'] = ""
	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_direccion':	
				create_userdoc['newOwnershipData_ownerList_person_addressStreet'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['newOwnershipData_ownerList_person_addressStreet'] = ""
	create_userdoc['newOwnershipData_ownerList_person_addressStreetInOtherLang'] = ""
	create_userdoc['newOwnershipData_ownerList_person_addressZone'] = ""
	create_userdoc['newOwnershipData_ownerList_person_agentCode'] = ""
	create_userdoc['newOwnershipData_ownerList_person_cityCode'] = ""


	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_ciudad':			
				create_userdoc['newOwnershipData_ownerList_person_cityName'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['newOwnershipData_ownerList_person_cityName'] =""

	create_userdoc['newOwnershipData_ownerList_person_companyRegisterRegistrationDate'] = ""
	create_userdoc['newOwnershipData_ownerList_person_companyRegisterRegistrationNbr'] = ""
	create_userdoc['newOwnershipData_ownerList_person_email'] = ""
	create_userdoc['newOwnershipData_ownerList_person_individualIdNbr'] = ci_Nbr
	create_userdoc['newOwnershipData_ownerList_person_individualIdType'] = ci_Typ
	create_userdoc['newOwnershipData_ownerList_person_legalIdNbr'] = ruc_Nbr
	create_userdoc['newOwnershipData_ownerList_person_legalIdType'] = ruc_Typ
	create_userdoc['newOwnershipData_ownerList_person_legalNature'] = ""
	create_userdoc['newOwnershipData_ownerList_person_legalNatureInOtherLang'] = ""
	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_pais':
				create_userdoc['newOwnershipData_ownerList_person_nationalityCountryCode'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['newOwnershipData_ownerList_person_nationalityCountryCode'] = "" 
	create_userdoc['newOwnershipData_ownerList_person_personGroupCode'] = ""
	create_userdoc['newOwnershipData_ownerList_person_personGroupName'] = ""
	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_nombresrazon':
				create_userdoc['newOwnershipData_ownerList_person_personName'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['newOwnershipData_ownerList_person_personName'] = ""

	create_userdoc['newOwnershipData_ownerList_person_personNameInOtherLang'] = ""
	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_pais':
				create_userdoc['newOwnershipData_ownerList_person_residenceCountryCode'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['newOwnershipData_ownerList_person_residenceCountryCode'] = ""
	create_userdoc['newOwnershipData_ownerList_person_stateCode'] = ""
	create_userdoc['newOwnershipData_ownerList_person_stateName'] = ""
	try:
		for i in range(0,len(data[0]['respuestas'])):
			if data[0]['respuestas'][i]['campo'] == 'datospersonales_telefono':
				create_userdoc['newOwnershipData_ownerList_person_telephone'] = str(data[0]['respuestas'][i]['valor'])
	except Exception as e:
		create_userdoc['newOwnershipData_ownerList_person_telephone'] = ""	
	create_userdoc['newOwnershipData_ownerList_person_zipCode'] = ""



	create_userdoc['notes'] = ""


	create_userdoc['poaData_poaGranteeList_person_addressStreet'] = ""
	create_userdoc['poaData_poaGranteeList_person_addressStreetInOtherLang'] = ""
	create_userdoc['poaData_poaGranteeList_person_addressZone'] = ""
	create_userdoc['poaData_poaGranteeList_person_agentCode'] = ""
	create_userdoc['poaData_poaGranteeList_person_cityCode'] = ""
	create_userdoc['poaData_poaGranteeList_person_cityName'] = ""
	create_userdoc['poaData_poaGranteeList_person_companyRegisterRegistrationDate'] = ""
	create_userdoc['poaData_poaGranteeList_person_companyRegisterRegistrationNbr'] = ""
	create_userdoc['poaData_poaGranteeList_person_email'] = ""
	create_userdoc['poaData_poaGranteeList_person_individualIdNbr'] = ""
	create_userdoc['poaData_poaGranteeList_person_individualIdType'] = ""
	create_userdoc['poaData_poaGranteeList_person_legalIdNbr'] = ""
	create_userdoc['poaData_poaGranteeList_person_legalIdType'] = ""
	create_userdoc['poaData_poaGranteeList_person_legalNature'] = ""
	create_userdoc['poaData_poaGranteeList_person_legalNatureInOtherLang'] = ""
	create_userdoc['poaData_poaGranteeList_person_nationalityCountryCode'] = ""
	create_userdoc['poaData_poaGranteeList_person_personGroupCode'] = ""
	create_userdoc['poaData_poaGranteeList_person_personGroupName'] = ""
	create_userdoc['poaData_poaGranteeList_person_personName'] = ""
	create_userdoc['poaData_poaGranteeList_person_personNameInOtherLang'] = ""
	create_userdoc['poaData_poaGranteeList_person_residenceCountryCode'] = ""
	create_userdoc['poaData_poaGranteeList_person_stateCode'] = ""
	create_userdoc['poaData_poaGranteeList_person_stateName'] = ""
	create_userdoc['poaData_poaGranteeList_person_telephone'] = ""
	create_userdoc['poaData_poaGranteeList_person_zipCode'] = ""
	create_userdoc['poaData_poaGrantor_person_addressStreet'] = ""
	create_userdoc['poaData_poaGrantor_person_addressStreetInOtherLang'] = ""
	create_userdoc['poaData_poaGrantor_person_addressZone'] = ""
	create_userdoc['poaData_poaGrantor_person_agentCode'] = ""
	create_userdoc['poaData_poaGrantor_person_cityCode'] = ""
	create_userdoc['poaData_poaGrantor_person_cityName'] = ""
	create_userdoc['poaData_poaGrantor_person_companyRegisterRegistrationDate'] = ""
	create_userdoc['poaData_poaGrantor_person_companyRegisterRegistrationNbr'] = ""
	create_userdoc['poaData_poaGrantor_person_email'] = ""
	create_userdoc['poaData_poaGrantor_person_individualIdNbr'] = ""
	create_userdoc['poaData_poaGrantor_person_individualIdType'] = ""
	create_userdoc['poaData_poaGrantor_person_legalIdNbr'] = ""
	create_userdoc['poaData_poaGrantor_person_legalIdType'] = ""
	create_userdoc['poaData_poaGrantor_person_legalNature'] = ""
	create_userdoc['poaData_poaGrantor_person_legalNatureInOtherLang'] = ""
	create_userdoc['poaData_poaGrantor_person_nationalityCountryCode'] = ""
	create_userdoc['poaData_poaGrantor_person_personGroupCode'] = ""
	create_userdoc['poaData_poaGrantor_person_personGroupName'] = ""
	create_userdoc['poaData_poaGrantor_person_personName'] = ""
	create_userdoc['poaData_poaGrantor_person_personNameInOtherLang'] = ""
	create_userdoc['poaData_poaGrantor_person_residenceCountryCode'] = ""
	create_userdoc['poaData_poaGrantor_person_stateCode'] = ""
	create_userdoc['poaData_poaGrantor_person_stateName'] = ""
	create_userdoc['poaData_poaGrantor_person_telephone'] = ""
	create_userdoc['poaData_poaGrantor_person_zipCode'] = ""
	create_userdoc['poaData_poaRegNumber'] = ""
	create_userdoc['poaData_scope'] = ""
	
	

	try:
		create_userdoc['representationData_representativeList_person_addressStreet'] = ag_data['addressStreet']
	except Exception as e:
		create_userdoc['representationData_representativeList_person_addressStreet'] = ""
	try:	
		create_userdoc['representationData_representativeList_person_addressStreetInOtherLang'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_addressStreetInOtherLang'] = ""	
	try:
		create_userdoc['representationData_representativeList_person_addressZone'] = default_val(ag_data['addressZone'])
	except Exception as e:
		create_userdoc['representationData_representativeList_person_addressZone'] = ""	
	try:
		create_userdoc['representationData_representativeList_person_agentCode'] = str(int(ag_data['agentCode']['doubleValue']))
	except Exception as e:
		create_userdoc['representationData_representativeList_person_agentCode'] = ""	
	try:
		create_userdoc['representationData_representativeList_person_cityCode'] =  default_val(ag_data['cityCode'])
	except Exception as e:
		create_userdoc['representationData_representativeList_person_cityCode'] = ""	
	try:	
		create_userdoc['representationData_representativeList_person_cityName'] = default_val(ag_data['cityName'])
	except Exception as e:
		create_userdoc['representationData_representativeList_person_cityName'] = ""	
	try:	
		create_userdoc['representationData_representativeList_person_companyRegisterRegistrationDate'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_companyRegisterRegistrationDate'] = ""	
	try:	
		create_userdoc['representationData_representativeList_person_companyRegisterRegistrationNbr'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_companyRegisterRegistrationNbr'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_email'] = ag_data['email']
	except Exception as e:
		create_userdoc['representationData_representativeList_person_email'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_individualIdNbr'] = ""	
	except Exception as e:
		create_userdoc['representationData_representativeList_person_individualIdNbr'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_individualIdType'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_individualIdType'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_legalIdNbr'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_legalIdNbr'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_legalIdType'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_legalIdType'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_legalNature'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_legalNature'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_legalNatureInOtherLang'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_legalNatureInOtherLang'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_nationalityCountryCode'] = ag_data['nationalityCountryCode']
	except Exception as e:
		create_userdoc['representationData_representativeList_person_nationalityCountryCode'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_personGroupCode'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_personGroupCode'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_personGroupName'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_personGroupName'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_personName'] = ag_data['personName']
	except Exception as e:
		create_userdoc['representationData_representativeList_person_personName'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_personNameInOtherLang'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_personNameInOtherLang'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_residenceCountryCode'] = ag_data['residenceCountryCode']
	except Exception as e:
		create_userdoc['representationData_representativeList_person_residenceCountryCode'] = ""
	try:		
		create_userdoc['representationData_representativeList_person_stateCode'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_stateCode'] = ""
	try:		
		create_userdoc['representationData_representativeList_person_stateName'] = ""
	except Exception as e:
		create_userdoc['representationData_representativeList_person_stateName'] = ""
	try:		
		create_userdoc['representationData_representativeList_person_telephone'] = ag_data['telephone']
	except Exception as e:
		create_userdoc['representationData_representativeList_person_telephone'] = ""		
	try:		
		create_userdoc['representationData_representativeList_person_zipCode'] = ag_data['zipCode']
	except Exception as e:
		create_userdoc['representationData_representativeList_person_zipCode'] = ""	
	try:
		create_userdoc['representationData_representativeList_representativeType'] = ag_data['representativeType']
	except Exception as e:
		create_userdoc['representationData_representativeList_representativeType'] = "AG"
	

	return(create_userdoc)
 
def process_day_commit_Nbr():
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select num_acta_ultima from dia_proceso where fec_proceso = '{}' and ind_atencion_comp = 'N' order by num_acta_ultima desc""".format(str(captureDate.capture_day())))
		row=cursor.fetchall()
		for i in row:
			conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
			cursor = conn.cursor()
			cursor.execute("""UPDATE public.dia_proceso SET  num_acta_ultima={}, fec_recepcion_comp=null WHERE fec_proceso='{}';""".format((int(i[0])+1),str(captureDate.capture_day())))
			cursor.rowcount
			conn.commit()
			#conn.close()
			return(i[0])				
	except Exception as e:
		print(e)
	finally:
		conn.close()

def process_day_Nbr():
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select num_acta_ultima from dia_proceso where fec_proceso = '{}' and ind_atencion_comp = 'N' and ind_recepcion_comp = 'N' order by num_acta_ultima desc""".format(str(captureDate.capture_day())))
		row=cursor.fetchall()
		for i in row:
			return(i[0])				
	except Exception as e:
		print(e)
	finally:
		conn.close()			

def COMMIT_NBR():
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select num_acta_ultima from dia_proceso where fec_proceso = '{}' and ind_atencion_comp = 'N' order by num_acta_ultima desc""".format(str(captureDate.capture_day())))
		row=cursor.fetchall()
		for i in row:
			conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
			cursor = conn.cursor()
			cursor.execute("""UPDATE public.dia_proceso SET  num_acta_ultima={}, fec_recepcion_comp=null WHERE fec_proceso='{}';""".format((int(i[0])+1),str(captureDate.capture_day())))
			cursor.rowcount
			conn.commit()
			#conn.close()
			return(int(i[0])+1)				
	except Exception as e:
		print(e)
	finally:
		conn.close()	

def pago_data(pago):
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select authorization_number,amount,created_at from bancard_transactions where status = 1 and  payable_id = {} """.format(str(pago)))
		row=cursor.fetchall()
		for i in row:
			return(i)	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def paymentYeasOrNot(typ):
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select  rq_pago from reglas_me where tipo_escrito = '{}'""".format(typ))#select  rq_pago from reglas_me where tipo_doc like '{}%'
		row=cursor.fetchall()
		for i in row:
			return(i)	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def exp_relation(typ):
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select exp_ri from reglas_me where tipo_escrito = '{}'""".format(typ))
		row=cursor.fetchall()
		for i in row:
			return(i)	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def esc_relation(typ):
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select esc_ri from reglas_me where tipo_escrito = '{}'""".format(typ))
		row=cursor.fetchall()
		for i in row:
			return(i)	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def tasa_id(arg):
	try:
		conn = psycopg2.connect(host = connex.hostCJ,user= connex.userCJ,password = connex.passwordCJ,database = connex.databaseCJ)
		cursor = conn.cursor()
		cursor.execute("""select id, descripcion  from tasas  where id  = {}""".format(arg))
		row=cursor.fetchall()
		for i in row:
			return i
		return(tipo_form)	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def tasa_SIGLA(arg):
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select ttasa from reglas_me where tipo_escrito = '{}'""".format(arg))
		row=cursor.fetchall()
		for i in row:
			return(i)	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def data_validator(msg,status,t_id):
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""INSERT INTO public.log_error( fecha_evento, evento, descripcion_evento, sistema_origen,break,id_tramite)
						  VALUES( '{}', 'E99', '{}', 'M.E.A.','{}',{});""".format(captureDate.capture_full(), msg, status,t_id))
		cursor.rowcount
		conn.commit()
		conn.close()
	except Exception as e:
		print(e)
	finally:
		conn.close()

def qr_code(text): # convierte el texto en codigo QR y crea fichero .png
	img = qrcode.make(text)
	f = open("pdf/output.png", "wb")
	img.save(f)
	f.close()

	with open("pdf/output.png", "rb") as image2string: 
		converted_string = base64.b64encode(image2string.read()) 
	return(str(converted_string).replace("b'",'').replace("'","")) 

def sendToUser(arg):
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select email_user from reglas_notificacion where status_cod = '{}'""".format(arg))
		row=cursor.fetchall()
		for i in row:
			return(i)	
	except Exception as e:
		print(e)
	finally:
		conn.close()	

def stop_request():
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select count(break)  from log_error where  break = 'true'""")
		row=cursor.fetchall()
		for i in row:
			return(i[0])	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def main_State(exp):
	data_exp = mark_getlist(exp)[0]
	data_exp_process = mark_read(data_exp.fileId.fileNbr.doubleValue, data_exp.fileId.fileSeq, data_exp.fileId.fileSeries.doubleValue, data_exp.fileId.fileType)
	status_exp = Process_Read(data_exp_process.file.processId.processNbr.doubleValue, data_exp_process.file.processId.processType)
	return(status_exp.status.statusId.statusCode)

def email_receiver(sig):
	data_user = {}
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select email_user,notas,status_name from reglas_notificacion where status_cod = '{}'""".format(str(sig)))
		row=cursor.fetchall()
		return(row)	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def exist_notifi(sig):
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select email_user,notas from reglas_notificacion where status_cod = '{}'""".format(str(sig)))
		row=cursor.fetchall()
		if row == []:
			return('null')
		else:
			return(row)	
	except Exception as e:
		print(e)
	finally:
		conn.close()
	
def exist_main_mark(sig):	
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select exp_ri from reglas_me where tipo_escrito = '{}'""".format(sig)) #select ttasa from reglas_me where tipo_doc like '{} %'
		row=cursor.fetchall()
		for i in row:
			return(i[0])	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def rule_notification(sig,exp):
	print(sig)
	if exist_main_mark(sig) == 'S':
		status_exp = main_State(exp)
		#print(status_exp)
		rule = email_receiver(str(status_exp))
		#print(rule)
		try:	
			enviar_back_notFile(str(rule[0][0]), str(rule[0][2]), f"{str(rule[0][1])} -  {exp} status {str(status_exp)}")
		except Exception as e:
			pass			
	else:
		if exist_notifi(sig) != 'null':
			rule = email_receiver(str(sig))
			try:	
				enviar_back_notFile(str(rule[0][0]), str(rule[0][2]), f"{str(rule[0][1])} -  {exp}")
			except Exception as e:
				pass		
			try:	
				enviar_back_notFile(str(rule[1][0]), str(rule[0][2]), f"{str(rule[0][1])} -  {exp}")
			except Exception as e:
				pass
		else:
			rule = email_receiver('GEN')
			try:	
				enviar_back_notFile(str(rule[0][0]), str(rule[0][2]), f"{str(rule[0][1])} -  {exp}")
			except Exception as e:
				pass		
			try:	
				enviar_back_notFile(str(rule[1][0]), str(rule[0][2]), f"{str(rule[0][1])} -  {exp}")
			except Exception as e:
				pass				

def log_info():
	pack_data = []
	conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
	cursor = conn.cursor()
	cursor.execute("""SELECT * FROM public.log_error where evento = 'E99'""")
	row=cursor.fetchall()
	for it in range(len(row)):
		compl = log_info_id_tramites(row[it][6])
		pack_data.append({
							'err_id':row[it][0],
							'fecha':fecha_barra(str(row[it][1]))+" "+hora(str(row[it][1])),
							'err_code':row[it][2],
							'descrip':row[it][3],
							'origin':row[it][4],
							'run':row[it][5],
							'tramite':row[it][6],
							'typ':compl[0],
							'enviado_at':fecha_barra(captureDate.time_difference(str(compl[1]),3))+" "+hora(captureDate.time_difference(str(compl[1]),3)),
							'form_typ':compl[2]
						})
	conn.close()

	return(pack_data)
 
def log_info_id_tramites(arg):
	try:
		list_info = []
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select formulario_id,enviado_at,estado from tramites t where id = {}""".format(int(arg)))
		row=cursor.fetchall()
		return(row[0])
	except Exception as e:
		print(e)
	finally:
		conn.close()

def log_info_serch(fecha,estado):
	pack_data = []
	conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
	cursor = conn.cursor()
	cursor.execute(f"""SELECT * FROM public.log_error where  evento = '{estado}' and  fecha_evento >= '{fecha} 00:59' and fecha_evento <= '{fecha} 21:59'""")
	row=cursor.fetchall()
	print(len(row))
	for it in range(len(row)):
		compl = log_info_id_tramites(row[it][6])
		pack_data.append({
							'err_id':row[it][0],
							'fecha':fecha_barra(str(row[it][1]))+" "+hora(str(row[it][1])),
							'err_code':row[it][2],
							'descrip':row[it][3],
							'origin':row[it][4],
							'run':row[it][5],
							'tramite':row[it][6],
							'typ':compl[0],
							'enviado_at':fecha_barra(captureDate.time_difference(str(compl[1]),3))+" "+hora(captureDate.time_difference(str(compl[1]),3)),
							'form_typ':compl[2]
						})
	conn.close()
	return(pack_data)

def log_info_delete(t_id):
	log_data = {}
	conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
	cursor = conn.cursor()
	cursor.execute("""UPDATE public.log_error SET evento='E00' , break='false' WHERE id_tramite= {};""".format(t_id))
	conn.commit()
	conn.close()	
	return(log_data)		

def getSigla_tipoDoc(arg):
	try:
		return(pendiente_sfe(arg)[0]['tipo_documento_id'])
	except Exception as e:
		return("")

def what_it_this(arg):
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select formulario_id from tramites t where id = {}""".format(int(arg)))
		row=cursor.fetchall()
		return(row[0][0])
	except Exception as e:
		print(e)
	finally:
		conn.close()

def Insert_Group_Process(grupo,fileNbr,user): 
	expediente = mark_getlist(fileNbr)
	userId = fetch_all_user_mark(user)[0].sqlColumnList[0].sqlColumnValue
	data = mark_read(
		expediente[0]['fileId']['fileNbr']['doubleValue'], 
		expediente[0]['fileId']['fileSeq'], 
		expediente[0]['fileId']['fileSeries']['doubleValue'], 
		expediente[0]['fileId']['fileType'])
	return(ProcessGroupAddProcess(
		grupo,
		userId,
		data['file']['processId']['processNbr']['doubleValue'],
		data['file']['processId']['processType']))

def USER_GROUP(sig):
	data_user = {}
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute("""select usuario FROM public.reglas_notificacion WHERE status_cod='{}'""".format(str(sig)))
		row=cursor.fetchall()
		return(row[0][0])	
	except Exception as e:
		print(e)
	finally:
		conn.close()

'''
EXISTE O NO EL GRUPO 
valid_group(userNbr,groupName,typ)

EXISTE 
ProcessGroupAddProcess

NO EXISTE
ProcessGroupInsert
ProcessGroupAddProcess


'''







"""def afected_relation_auth(arg):"""

'''

SELECT * FROM public.log_error where evento = 'E99'

print(personAgente(code_ag('43'))[0].agentCode.doubleValue) #Consulta agente

select * from tramites where formulario_id IN (39, 40, 66, 67,69,70,3,4,27,95) and estado  in (7)
'''