from dataclasses import replace
from dbm import dumb
import json
import os
from time import sleep
from fpdf import FPDF, HTMLMixin  #pip install fpdf2
from os import getcwd
import barcode
from barcode.writer import ImageWriter
import psycopg2
import tools.connect as connex


global_data = {}


def new_document(arg):
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
								where t.estado  = {};""".format(int(arg)))
		row=cursor.fetchall()
		for item in range(0,len(row)):
			for i in row[item][8]:								
				tipo_marca:str = ""
				desc_marca:str = ""
				try:
					if(i['descripcion'] == "-" and i['campo'] == 'marcaredpi_tipomarcaredpi'):
						if i['valor'] == 'N':
							tipo_marca = 'DENOMINATIVA'
						if i['valor'] == 'L':
							tipo_marca = 'FIGURATIVA'
						if i['valor'] == 'B':
							tipo_marca = 'MIXTA'
						if i['valor'] == 'T':
							tipo_marca = 'TRIDIMENSIONAL'
						if i['valor'] == 'S':
							tipo_marca = 'SONORA'
					print(tipo_marca)																												
				except Exception as e:
					tipo_marca = 'No definido'

				try:
					if(i['descripcion'] == "Clase" and i['campo'] == 'marcaredpi_claseredpi'):
						if i['valor'] <= 34:
							desc_marca = "PRODUCTOS"
						if i['valor'] >= 35:
							desc_marca = "SERVICIOS"
					print(desc_marca)							
				except Exception as e:
					desc_marca = 'No definido'





				try:
					if(i['descripcion'] == "Buscar Solicitud N°" and i['campo'] == 'marcaredpi_expediente' ):
						print(i['valor'])
				except Exception as e:
					print('No definido')		

				try:
					if(i['descripcion'] == "Solicitud N°" and i['campo'] == 'marcaredpi_expedienteredpi'):
						print(i['valor'])
				except Exception as e:
					print('No definido')
				
				try:
					if(i['descripcion'] == "Tipo de solicitud" and i['campo'] == 'marcaredpi_tiposolicitudrepi'):
						print(i['valor'])
				except Exception as e:
					print('No definido')

				try:
					if(i['descripcion'] == "Tipo de movimiento" and i['campo'] == 'marcaredpi_tipomovimientoredpi'):
						print(i['valor'])
				except Exception as e:
					print('No definido')
				
				try:
					if(i['descripcion'] == "Denominación" and i['campo'] == 'marcaredpi_denominacionredpi'):
						print(i['valor'])
				except Exception as e:
					print('No definido')

				try:
					if(i['descripcion'] == "Productos o Servicios que distingue" and i['campo'] == 'marcaredpi_proserdistingueredpi'):
						print(i['valor'])
				except Exception as e:
					print('No definido')

				try:
					if(i['descripcion'] == "Nombres y Apellidos / Razón Social" and i['campo'] == 'marcaredpi_nombrerazonredpi'):
						print(i['valor'])
				except Exception as e:
					print('No definido')

				try:
					if(i['descripcion'] == "Validación" and i['campo'] == 'marcaredpi_mensajesi'):
						print(i['valor'])
				except Exception as e:
					print('No definido')

				try:
					if(i['descripcion'] == "NO PUEDE FIRMAR. Verifique si recibió el archivo PDF de la orden de publicación en su Buzón" and i['campo'] == 'marcaredpi_mensajeno'):
						print(i['valor'])
				except Exception as e:
					print('No definido')

				try:
					if(i['descripcion'] == "Buscar Solicitud N°" and i['campo'] == 'expedienteamarcas_buscarsolicitud'):
						print(i['valor'])
				except Exception as e:
					print('No definido')













			print('---------------------------')		
	except Exception as e:
		print(e)
	finally:
		conn.close()
	return(global_data)

#print(new_document("7"))

def registro_sfe(arg):
	try:
		conn = psycopg2.connect(
			host = connex.host_SFE_conn,
			user= connex.user_SFE_conn,
			password = connex.password_SFE_conn,
			database = connex.database_SFE_conn
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
				if(i['descripcion'] == "Tipo de Marca" and i['campo'] == 'marca_tipomarca'):
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
				if(i['descripcion'] == "Nombres y Apellidos" and i['campo'] == 'datospersonales_nombreapellido'):
					global_data['nombre_soli'] = i['valor']
			except Exception as e:
				global_data['nombre_soli'] = "No definido"											
			try:
				if(i['descripcion'] == "Razón Social" and i['campo'] == 'datospersonales_razonsocial'):
					global_data['razon_social']=i['valor']
			except Exception as e:
				global_data['razon_social'] = "No definido"					
			try:
				if(i['descripcion'] == "Dirección" and i['campo'] == 'datospersonales_calle'):
					global_data['direccion']=i['valor']
			except Exception as e:
				global_data['direccion'] = "No definido"					
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

		return(global_data)
	except Exception as e:
		print(e)
	finally:
		conn.close()
#print(registro_sfe("22106763"))


def renovacion_sfe(arg):
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
		global_data['dir_agente'] = str(row[0][29])
		global_data['TEL_agente'] = str(row[0][28])
		global_data['email_agente'] = str(row[0][27])
		global_data['nombre_formulario'] = str(row[0][3])
		for i in row[0][8]:

			if(i['descripcion'] == "Clase" and i['campo'] == 'marcarenov_clase'):
				clase_tipo = i['valor']
				if(int(clase_tipo.replace(".0","")) <= 34):
					global_data['clasificacion']= 'PRODUCTO'
				if(int(clase_tipo.replace(".0","")) >= 35):
					global_data['clasificacion']= 'SERVICIOS'						
					try:					
						if(i['campo'] == "marca_distintivo"):
							global_data['distintivo'] = i['valor']['archivo']['url']
					except Exception as e:
						global_data['distintivo'] = ""							
					try:	
						if(i['campo'] == "actualizacion_refdistitivo"):
							global_data['distintivo2'] = i['valor']['archivo']['url']
					except Exception as e:
						global_data['distintivo2'] = ""							
					try:	
						if(i['descripcion'] == "N° de Documento"):
							global_data['documento'] = i['valor']
					except Exception as e:
						global_data['documento'] = ""							
					try:	
						if(i['descripcion'] == "RUC"):				
							global_data['RUC']=i['valor']
					except Exception as e:
						global_data['RUC'] = ""							
					try:	
						if(i['descripcion'] == "Productos o Servicios que distingue"):
							global_data['distingue'] = i['valor']
					except Exception as e:
						global_data['distingue'] = ""							
					try:								
						if(i['descripcion'] == "Reivindicaciones"):
							global_data['reivindicaciones'] = i['valor']
					except Exception as e:
						global_data['reivindicaciones'] = ""							
					try:	
						if(i['descripcion'] == "-" and i['campo'] == 'marcarenov_tipomarca'):
							global_data["tipo_guion"] = i['valor']
					except Exception as e:
						global_data['tipo_guion'] = ""
					try:	
						if(i['descripcion'] == "Denominación"):
							global_data['denominacion_on'] = i['valor']
					except Exception as e:
						global_data['denominacion_on'] = ""							
					try:	
						if(i['descripcion'] == "Especificar"):
							global_data['especificar'] = i['valor']
					except Exception as e:
						global_data['especificar'] = ""							
					try:	
						if(i['descripcion'] == "Nombres y Apellidos / Razón Social" and i['campo'] == 'datospersonalesrenov_nombrerazon'):
							global_data['nombre_soli'] = i['valor']
					except Exception as e:
						global_data['nombre_soli'] = ""							
					try:						
						if(i['descripcion'] == "Razón Social" and i['campo'] == 'datospersonales_razonsocial'):
							global_data['razon_social']=i['valor']
					except Exception as e:
						global_data['razon_social'] = ""							
					try:	
						if(i['descripcion'] == "Dirección"):
							global_data['direccion']=i['valor']
					except Exception as e:
						global_data['direccion'] = ""							
					try:	
						if(i['descripcion'] == "Ciudad"):
							global_data['ciudad']=i['valor']
					except Exception as e:
						global_data['ciudad'] = ""							
					try:	
						if(i['descripcion'] == "País "):
							global_data['pais']=i['valor']
					except Exception as e:
						global_data['pais'] = ""							
					try:						
						if(i['descripcion'] == "Código Postal"):
							global_data['codigo_postal']=i['valor']
					except Exception as e:
						global_data['codigo_postal'] = ""							
					try:	
						if(i['descripcion'] == "Teléfono"):
							global_data['telefono']=i['valor']
					except Exception as e:
						global_data['telefono'] = ""							
					try:	
						if(i['descripcion'] == "Correo Electrónico"):
							global_data['email']=i['valor']
					except Exception as e:
						global_data['email'] = ""							
					try:
						if(i['descripcion'] == "Distrito"):
							global_data['distrito']=i['valor']
					except Exception as e:
						global_data['distrito'] = ""						
					try:	
						if(i['descripcion'] == "N° de Documento / RUC" and i['campo'] == 'actualizacion_nodocumentoruc'):
							global_data['act_numero']=i['valor']
					except Exception as e:
						global_data['act_numero'] = ""
					try:	
						if(i['descripcion'] == "País " and i['campo'] == 'actualizacion_pais'):
							global_data['act_pais']=i['valor']
					except Exception as e:
						global_data['act_pais'] = ""
					try:	
						if(i['descripcion'] == "Ciudad" and i['campo'] == 'actualizacion_ciudad'):
							global_data['act_ciudad']=i['valor']
					except Exception as e:
						global_data['act_ciudad'] = ""
					try:	
						if(i['descripcion'] == "Código Postal" and i['campo'] == 'actualizacion_codigopostal'):
							global_data['act_post']=i['valor']
					except Exception as e:
						global_data['act_post'] = ""
					try:	
						if(i['descripcion'] == "Teléfono" and i['campo'] == 'actualizacion_telefono'):
							global_data['act_tel']=i['valor']
					except Exception as e:
						global_data['act_tel'] = ""
					try:	
						if(i['descripcion'] == "Correo Electrónico" and i['campo'] == 'actualizacion_correoelectronico'):
							global_data['act_email']=i['valor']
					except Exception as e:
						global_data['act_email'] = ""
					try:	
						if(i['descripcion'] == "Clase" and i['campo'] == 'marcarenov_clase'):
							global_data['clase_on']=i['valor']
					except Exception as e:
						global_data['clase_on'] = ""
					try:	
						if(i['descripcion'] == "Buscar Registro N°" and i['campo'] == 'marcarenov_registrono'):
							global_data['registro_nbr']=i['valor']
					except Exception as e:
						global_data['registro_nbr'] = ""
					try:	
						if(i['descripcion'] == "País " and i['campo'] == 'datospersonalesrenov_pais'):
							global_data['solic_pais']=i['valor']
					except Exception as e:
						global_data['solic_pais'] = ""
					try:	
						if(i['descripcion'] == "Dirección" and i['campo'] == 'datospersonalesrenov_calle'):
							global_data['solic_dir'] = str(i['valor']).replace(" – "," | ")
					except Exception as e:
						global_data['solic_dir'] = ""
					try:	
						if(i['descripcion'] == "Teléfono" and i['campo'] == 'datospersonalesrenov_telefono'):
							global_data['solic_tel']=i['valor']
					except Exception as e:
						global_data['solic_tel'] = ""
					try:	
						if(i['descripcion'] == "Correo Electrónico" and i['campo'] == 'datospersonalesrenov_correoelectronico'):
							global_data['solic_email']=i['valor']
					except Exception as e:
						global_data['solic_email'] = ""
					try:	
						if(i['descripcion'] == "Número" and i['campo'] == 'actualizacion_numero'):
							global_data['actc_num']=i['valor']
					except Exception as e:
						global_data['actc_num'] = ""
		return(global_data)
	except Exception as e:
		print(e)
	finally:
		conn.close()
#print(renovacion_sfe('22106266'))


def oposicion_sfe(arg):
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
						global_data['solicitud'] = ""

					try:
						if(i['descripcion'] == "En Fecha" and i['campo'] == 'expedienteamarcas_fecha'):				
							global_data['fecha']=i['valor']
					except Exception as e:
						global_data['fecha'] = ""

					try:
						if(i['descripcion'] == "Nombres y Apellidos / Razón Social" and i['campo'] == 'datospersonalesv2_nombresrazon'):				
							global_data['ras_social']=i['valor']
					except Exception as e:
						global_data['ras_social'] = ""

					try:
						if(i['descripcion'] == "Clase" and i['campo'] == 'expedienteamarcas_clase'):
							global_data['clase'] = i['valor']
					except Exception as e:
						global_data['clase'] = ""

					try:
						if(i['descripcion'] == "Denominación" and i['campo'] == 'expedientebmarcas_denominacionb'):
							global_data['denominacionB'] = i['valor']
					except Exception as e:
						global_data['denominacionB'] = ""
						
					try:
						if(i['descripcion'] == "Clase" and i['campo'] == 'expedientebmarcas_claseb'):
							global_data['claseB'] = i['valor']
					except Exception as e:
						global_data['claseB'] = ""

					try: # Marca extranjera
						if(i['descripcion'] == "Clase" and i['campo'] == 'datosopone1_claseint'):
							global_data['clase_b'] = i['valor']
					except Exception as e:
						global_data['clase_b'] =""

					try: # Marca extranjera
						if(i['descripcion'] == "Denominación" and i['campo'] == 'datosopone1_denominacionint'):
							global_data['denominacion_b'] = i['valor']
					except Exception as e:
						global_data['denominacion_b'] =""

					try:				
						if(i['descripcion'] == "Denominación" and i['campo'] == 'expedienteamarcas_denominacion'):
							global_data['denominacion'] = i['valor']
					except Exception as e:
						global_data['denominacion'] = ""					
					
					try:
						if(i['descripcion'] == "Solicitud N°" and i['campo'] == 'expedientebmarcas_solicitudb'):
							global_data["solicitud2"] = i['valor']
					except Exception as e:
						global_data["solicitud2"] =	""				
					
					try:
						if(i['descripcion'] == "En Fecha" and i['campo'] == 'expedientebmarcas_fechab'):
							global_data["fecha2"] = i['valor']						
					except Exception as e:
						global_data["fecha2"] = ""					
					
					try:
						if(i['descripcion'] == "Buscar Registro N°" and i['campo'] == 'expedientebmarcas_buscarregistrob'):
							global_data['registro'] = i['valor']
					except Exception as e:
						global_data['registro'] = ""					
					
					try:						
						if(i['descripcion'] == "Nombres y Apellidos / Razón Social" and i['campo'] == 'expedientebmarcas_nombrerazonb'):
							global_data['razon_socialB']=i['valor']
					except Exception as e:
						global_data['razon_socialB']=""					
					
					try:
						if(i['descripcion'] == "País " and i['campo'] ==  'datospersonalesv2_pais'):
							global_data['pais']=i['valor']
					except Exception as e:
						global_data['pais']=""					
					
					try:
						if(i['descripcion'] == "Ciudad" and i['campo'] ==  'datospersonalesv2_ciudad'):
							global_data['ciudad']=i['valor']
					except Exception as e:
						global_data['ciudad']=""					
					
					try:
						if(i['descripcion'] == "Código Postal" and i['campo'] == 'datospersonalesv2_codigopostal'):
							global_data['code_post']=i['valor']
					except Exception as e:
						global_data['code_post']=""					
					
					try:						
						if(i['descripcion'] == "Dirección" and i['campo'] == 'datospersonalesv2_direccion'):
							global_data['direccion']=i['valor']
					except Exception as e:
						global_data['direccion']=""					
					
					try:
						if(i['descripcion'] == "Teléfono" and i['campo'] == 'datospersonalesv2_telefono'):
							global_data['telefono']=i['valor']
					except Exception as e:
						global_data['telefono']=""					
					
					try:
						if(i['descripcion'] == "Correo Electrónico" and i['campo'] == 'datospersonalesv2_correoelectronico'):
							global_data['email']=i['valor']
					except Exception as e:
						global_data['email']=""					
					
					try:
						if(i['descripcion'] == "Número de Poder" and i['campo'] == 'datosrepresentacion2_podernro'):
							global_data['poder']=i['valor']
					except Exception as e:
						global_data['poder']=""					
					
					try:
						if(i['descripcion'] == "Descripción de la Observación" and i['campo'] == 'observacion_descobservacion'):
							global_data['observaciones']=i['valor']
					except Exception as e:
						global_data['observaciones']=""

				return(global_data)
			except Exception as e:
				print(e)
			finally:
				conn.close()
#print(oposicion_sfe('2310140'))