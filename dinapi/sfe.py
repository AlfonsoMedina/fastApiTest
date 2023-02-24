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
								where t.estado  = {};""".format(int(arg)))
		row=cursor.fetchall()
		for item in range(0,len(row)):
			#print(row[item][8])
			for i in row[item][8]:
				try:
					if(i['descripcion'] == "Buscar Solicitud N°" and i['campo'] == 'marcaredpi_expediente' ):
						print(i['valor'])
				except Exception as e:
					pass

				try:
					if(i['descripcion'] == "Solicitud N°" and i['campo'] == 'marcaredpi_expedienteredpi'):
						print(i['valor'])
				except Exception as e:
					pass
				try:
					if(i['descripcion'] == "Tipo de solicitud" and i['campo'] == 'marcaredpi_tiposolicitudrepi'):
						print(i['valor'])
				except Exception as e:
					pass

				try:
					if(i['descripcion'] == "Tipo de movimiento" and i['campo'] == 'marcaredpi_tipomovimientoredpi'):
						print(i['valor'])
				except Exception as e:
					pass
				try:
					if(i['descripcion'] == "Clase" and i['campo'] == 'marcaredpi_claseredpi'):
						print(i['valor'])
				except Exception as e:
					pass
				try:
					if(i['descripcion'] == "Denominación" and i['campo'] == 'marcaredpi_denominacionredpi'):
						print(i['valor'])
				except Exception as e:
					pass

				try:
					if(i['descripcion'] == "Productos o Servicios que distingue" and i['campo'] == 'marcaredpi_proserdistingueredpi'):
						print(i['valor'])
				except Exception as e:
					pass

				try:
					if(i['descripcion'] == "Nombres y Apellidos / Razón Social" and i['campo'] == 'marcaredpi_nombrerazonredpi'):
						print(i['valor'])
				except Exception as e:
					pass

				try:
					if(i['descripcion'] == "Validación" and i['campo'] == 'marcaredpi_mensajesi'):
						print(i['valor'])
				except Exception as e:
					pass

				try:
					if(i['descripcion'] == "NO PUEDE FIRMAR. Verifique si recibió el archivo PDF de la orden de publicación en su Buzón" and i['campo'] == 'marcaredpi_mensajeno'):
						print(i['valor'])
				except Exception as e:
					pass

				try:
					if(i['descripcion'] == "-" and i['campo'] == 'marcaredpi_tipomarcaredpi'):
						print(i['valor'])
				except Exception as e:
					pass

				try:
					if(i['descripcion'] == "Tipo de movimiento" and i['campo'] == 'marcaredpi_tipomovimientoredpi'):
						print(i['valor'])
				except Exception as e:
					pass

				try:
					if(i['valor'] == "PRODUCTOS" and i['campo'] == 'marcaredpi_clasificacionredpip'):
						print(i['condicion'])
				except Exception as e:
					pass

				try:
					if(i['valor'] == "SERVICIOS" and i['campo'] == 'marcaredpi_clasificacionredpis'):
						print(i['condicion'])
				except Exception as e:
					pass

				try:
					if(i['descripcion'] == "Tipo de marca" and i['campo'] == 'marcaredpi_tiporedpidenominativa'):
						print(i['valor'])
				except Exception as e:
					pass				
			print('---------------------------')		
	except Exception as e:
		print(e)
	finally:
		conn.close()
	return(global_data)
			
		
		

print(new_document("7"))