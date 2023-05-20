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
								where t.id  = {};""".format(int(arg)))
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
				"""____________________________________________________F 39___________________________________________________________"""
				try:
					if(i['descripcion'] == "Descripción" and i['campo'] == "tp2descripcion_descripcion"):
						print(i['valor'])
				except Exception as e:
					print('No definido')
				try:	
					if(i['descripcion'] == "Descripción de la Observación" and i['campo'] == "observacion_descobservacion"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Agregar Documentos" and i['campo'] == "observacion_documentos"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "País " and i['campo'] == "datospersonales_pais"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Correo Electrónico" and i['campo'] == "datospersonales_correoelectronico"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Teléfono" and i['campo'] == "datospersonales_telefono"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Número" and i['campo'] == "datospersonales_numero"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Referencia" and i['campo'] == "datospersonales_referencia"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Código Postal" and i['campo'] == "datospersonales_codigopostal"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Datos de Contacto" and i['campo'] == "datospersonales_datoscontacto"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Tipo" and i['campo'] == "datospersonales_tipo"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Sexo" and i['campo'] == "datospersonales_sexo"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "RUC" and i['campo'] == "datospersonales_ruc"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "N° de Documento" and i['campo'] == "datospersonales_nrodocumento"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Ciudad" and i['campo'] == "datospersonales_ciudad"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Nombres y Apellidos" and i['campo'] == "datospersonales_nombreapellido"):
						print(i['valor'])
				except Exception as e:
					print('No definido')
				try:	
					if(i['descripcion'] == "Razón Social" and i['campo'] == "datospersonales_razonsocial"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Dirección" and i['campo'] == "datospersonales_calle"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "En Fecha" and i['campo'] == "expedientebmarcas_fechab"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Denominación" and i['campo'] == "expedientebmarcas_denominacionb"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:
					if(i['descripcion'] == "-" and i['campo'] == "expedientebmarcas_tipomarcab"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Nombres y Apellidos / Razón Social" and i['campo'] == "expedientebmarcas_nombrerazonb"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Clase" and i['campo'] == "expedientebmarcas_claseb"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Productos o Servicios que distingue" and i['campo'] == "expedientebmarcas_proserdistingueb"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Marca relacionada" and i['campo'] == "expedientebmarcas_marcarelacionadab"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Buscar Registro N°" and i['campo'] == "expedientebmarcas_buscarregistrob"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Clasificación" and i['campo'] == "expedientebmarcas_clasificacionbp"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Clasificación" and i['campo'] == "expedientebmarcas_clasificacionb"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				
				'''
				try:	
					if(i['descripcion'] == "Tipo de marca" and i['campo'] == "expedientebmarcas_tipobdenominativa"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Tipo de marca" and i['campo'] == "expedientebmarcas_tipobfigurativa"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Tipo de marca" and i['campo'] == "expedientebmarcas_tipobmixta"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					 
				try:	
					if(i['descripcion'] == "Tipo de marca" and i['campo'] == "expedientebmarcas_tipobtridimensional"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Tipo de marca" and i['campo'] == "expedientebmarcas_tipobsonora"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Tipo de marca" and i['campo'] == "expedientebmarcas_tipobolfativa"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				'''
				
				print(tipo_marca)

				try:	
					if(i['descripcion'] == "Buscar Solicitud N°" and i['campo'] == "expedientebmarcas_buscarsolicitudb"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Registro N°" and i['campo'] == "expedientebmarcas_registrob"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					
				try:	
					if(i['descripcion'] == "Solicitud N°" and i['campo'] == "expedientebmarcas_solicitudb"):
						print(i['valor'])
				except Exception as e:
					print('No definido')					

			print('---------------------------')		
	except Exception as e:
		print(e)
	finally:
		conn.close()
	return(global_data)

print(new_document("24224"))