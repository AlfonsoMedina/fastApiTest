from dataclasses import replace
import json
import os
from telnetlib import PRAGMA_HEARTBEAT
from time import sleep
from fpdf import FPDF, HTMLMixin  #pip install fpdf2
from os import getcwd
import barcode
from barcode.writer import ImageWriter
import psycopg2
from wipo.ipas import *
from tools.base64Decode import decode_pdf
from tools.data_format import signo_format


def renovacion_pdf_sfe_local(arg):
	try:
		global_data = {}
		clase_tipo = 0
		try:
			get_list = mark_getlist(arg)
			data = mark_read(str(int(get_list[0].fileId.fileNbr.doubleValue)),str(get_list[0].fileId.fileSeq),str(get_list[0].fileId.fileSeries.doubleValue),str(get_list[0].fileId.fileType))
		except Exception as e:
			data = ''


		def recorrer_sfe(arg):
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
						if(i['campo'] == 'actualizacion_nodocumentoruc' or i['campo'] == 'actualizacion_noodocumentoruc'):
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
						if(i['campo'] == 'marcarenov_registrono'):
							global_data['registro_nbr']=i['valor']
					except Exception as e:
						global_data['registro_nbr'] = ""


					try:	
						if(i['descripcion'] == "País " and i['campo'] == 'datospersonalesrenov_pais'):
							global_data['solic_pais']=i['valor']
					except Exception as e:
						global_data['solic_pais'] = ""


					try:	
						if(i['campo'] == 'datospersonalesrenov_calle'):
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


					#try:	
					#	if(i['campo'] == 'actualizacion_numero'):
					#		global_data['actc_num']=i['valor']
					#except Exception as e:
					global_data['actc_num'] = ""






			except Exception as e:
				print(e)
			finally:
				conn.close()

		recorrer_sfe(arg)

		def codebarheard(arg):
			#Define content of the barcode as a string
			number = arg
			#Get the required barcode format
			barcode_format = barcode.get_barcode_class('code128')
			#Generate barcode and render as image
			my_barcode = barcode_format(number, writer=ImageWriter())
			#Save barcode as PNG
			my_barcode.save("static/sfe_no_pres_head")

		def codebarfoot(arg):
			#Define content of the barcode as a string
			number = arg
			#Get the required barcode format
			barcode_format = barcode.get_barcode_class('code128')
			#Generate barcode and render as image
			my_barcode = barcode_format(number, writer=ImageWriter())
			#Save barcode as PNG
			my_barcode.save("static/sfe_no_pres_foot")
		def convert_fecha_hora_sfe(data):
				date_fullE = str(data).split(" ")
				fecha_fullE = date_fullE[0].split("-")
				fecha_formatE = fecha_fullE[2]+"/"+fecha_fullE[1]+"/"+fecha_fullE[0]
				hora_puntoE = date_fullE[1].split(".")
				hora_guionE = hora_puntoE[0].split("-")
				a=hora_guionE[0].split(":")
				backhour = str(int(a[0])-3)+":"+a[1]+":"+a[2]
				#print(backhour)
				return(str(fecha_formatE+" "+str(backhour)))
		def convert_fecha_hora(data):
			date_fullE = str(data).split(" ")
			fecha_fullE = date_fullE[0].split("-")
			fecha_formatE = fecha_fullE[2]+"/"+fecha_fullE[1]+"/"+fecha_fullE[0]
			hora_puntoE = date_fullE[1].split(".")
			hora_guionE = hora_puntoE[0].split("-")
			return(str(fecha_formatE+" "+str(hora_guionE[0])))

		def traer_datos_pdf(arg):

			codebarheard("*"+str(global_data['expediente'])+"*")
			codebarfoot("*"+str(global_data['codigo_barr'])+"*")

			pdf = FPDF()
			pdf.add_page()
			pdf.set_font("helvetica", "B", 12)
			pdf.image('static/IMG.PNG',x=76,y=4,w=70,h=25)
			pdf.cell(0, 40, "________________________________________________________________________________________________________", align='c',ln=1)
			
			pdf.cell(0, -20, str(global_data['nombre_formulario']), align='c',ln=1)

			pdf.set_font('helvetica', 'I', 8)
			pdf.text(x=18, y=50, txt='Dirección General de Propiedad Industrial')
			pdf.text(x=18, y=54, txt='Dirección de Marcas')
			pdf.text(x=18, y=60, txt='Secretaría General - Mesa de Entradas')
			pdf.image("static/sfe_no_pres_head.png",x=145,y=(pdf.get_y() + 18),w=30,h=15)

			pdf.set_font("helvetica", "B", 9)

			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )			

			pdf.cell(w=35, h=8, txt='Fecha de Envío', border=1 , align='c' )
			
			try:
				pdf.cell(w=155, h=8, txt=convert_fecha_hora_sfe(str(global_data['fecha_envio'])), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=155, h=8, txt="", border=1, align='c' )	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Expediente Nro.', border=1, align='c')
			
			try:
				pdf.cell(w=50, h=8, txt=str(str(global_data['expediente'])), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=55, h=8, txt='Fecha y Hora de Solicitud', border=1, align='c' )
			
			try:
				pdf.cell(w=50, h=8, txt=convert_fecha_hora(str(global_data['fecha_solicitud'])), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 12)
			pdf.cell(w=190, h=8, txt='DATOS DE LA MARCA', border=1, align='c' )

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Registro Nro.', border=1, align='c')
			
			pdf.cell(w=35, h=8, txt=str(global_data['registro_nbr']), border=1, align='l')


			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Tipo de Marca', border=1, align='c')
			
			pdf.cell(w=35, h=8, txt=signo_format(str(global_data['tipo_guion'])), border=1, align='l')
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Denominación ', border=1 , align='c' )
			
			pdf.multi_cell(w=155, h=8, txt=str(global_data['denominacion_on']), border=1, align='l' )
			pdf.cell(w=0, h=8, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Clasificación', border=1, align='c')
			
			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['clasificacion']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=55, h=8, txt='Clase Niza', border=1, align='c' )
			

			try:
				pdf.cell(w=50, h=8, txt=str(global_data['clase_on']).replace('.0',""), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			pdf.set_font("helvetica", "B", 9) 
			pdf.cell(w=60, h=8, txt='Productos o Servicios que distingue:', border=1 , align='c' )
			

			try:
				pdf.multi_cell(w=130, h=4, txt=str(global_data['distingue']), border=1, align='L',ln=1)
			except Exception as e:
				pdf.multi_cell(w=130, h=4, txt="", border=1, align='L',ln=1) 
			
			########################################################################################################################################


			pdf.cell(w=0, h=5, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=70, h=28, txt='Referencia de Distintivo:', border=1 , align='c' )

			pdf.multi_cell(w=120, h=28, txt="", border=1, align='L',ln=1) 
			try:
				pdf.image(str(global_data['distintivo2']),x=123,y=(pdf.get_y()-27),w=25,h=25)
			except Exception as e:
				pdf.image("static/sfe_default.PNG",x=123,y=(pdf.get_y()-27),w=25,h=25)

			"""			
			pdf.cell(w=0, h=5, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=60, h=8, txt='Referencia de Distintivo:', border=1 , align='c' )
			
			pdf.multi_cell(w=130, h=4, txt="El archivo correspondiente al distintivo se ha recibido correctamente y se encuentra alojado en nuestros servidores. Lo puede verificar en el buzón de trámites.", border=1, align='L',ln=1) 
			"""
			########################################################################################################################################

			pdf.cell(w=0, h=5, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Reivindicaciones', border=1, align='c')
			
			pdf.cell(w=35, h=8, txt="", border=1, align='c')
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Especificar', border=1 , align='c' )
			pdf.cell(w=155, h=8, txt='', border=1, align='c' )	

			pdf.image("static/sfe_no_pres_foot.png",x=85,y=(pdf.get_y() + 15),w=35,h=15)




			pdf.add_page()

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			pdf.image("static/sfe_no_pres_head.png",x=145,y=(pdf.get_y()-18),w=30,h=15)

			pdf.set_font("helvetica", "B", 12)
			pdf.cell(w=190, h=8, txt='DATOS DEL SOLICITANTE', border=1, align='c' )



			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=55, h=8, txt='Nombre y Apellido, Rason Social', border=1, align='c')
			
			pdf.cell(w=135, h=8, txt=str(global_data['nombre_soli']), border=1, align='l')


			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=40, h=8, txt='Calle', border=1, align='c')
			
			pdf.multi_cell(w=150, h=8, txt = str(global_data['solic_dir']), border=1, align='l')
			

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=40, h=8, txt='Ciudad', border=1, align='c')
			
			pdf.cell(w=50, h=8, txt=str(global_data['ciudad']), border=1, align='l')

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=40, h=8, txt='País', border=1, align='c')
			
			pdf.cell(w=50, h=8, txt=str(global_data['solic_pais']), border=1, align='l')

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Codigo Postal', border=1, align='c')
			
			pdf.cell(w=50, h=8, txt=str(global_data['codigo_postal']), border=1, align='l')

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=40, h=8, txt='Teléfono', border=1, align='c')
			
			pdf.cell(w=50, h=8, txt=str(global_data['telefono']), border=1, align='l')

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Correo Electronico', border=1, align='c')
			
			pdf.cell(w=50, h=8, txt=str(global_data['solic_email']), border=1, align='l')

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			pdf.set_font("helvetica", "B", 12)
			pdf.cell(w=190, h=8, txt='DATOS DEL AGENTE DE PROPIEDAD INTELECTUAL', border=1, align='c' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )


			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Matricula', border=1, align='c')
			
			try:
				pdf.cell(w=35, h=8, txt=str(global_data['code_agente']), border=1, align='l')
			except Exception as e:
				pdf.cell(w=35, h=8, txt="", border=1, align='c')

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Nombre y Apellido', border=1 , align='c' )
			
			pdf.cell(w=155, h=8, txt=str(global_data['nombre_agente']), border=1, align='l' )

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Calle', border=1, align='c')
			
			pdf.cell(w=155, h=8, txt=str(global_data['dir_agente']), border=1, align='l')


			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)

			pdf.cell(w=35, h=8, txt='País', border=1, align='c')
			
			pdf.cell(w=55, h=8, txt="PY", border=1, align='l')

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Departamento', border=1, align='c')
			
			pdf.cell(w=50, h=8, txt="", border=1, align='c')

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Distrito', border=1, align='c')
			
			pdf.cell(w=55, h=8, txt="", border=1, align='c')

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Barrio', border=1, align='c')
			
			pdf.cell(w=50, h=8, txt="", border=1, align='c')

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Teléfono', border=1, align='c')
			
			pdf.cell(w=55, h=8, txt=str(global_data['TEL_agente']), border=1, align='l')

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Correo Electronico', border=1, align='c')
			
			pdf.cell(w=50, h=8, txt=str(global_data['email_agente']), border=1, align='l')

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			pdf.cell(w=190, h=8, txt='DATOS DE ACTUALIZACION', border=1, align='c' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )


			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Numero Documento', border=1, align='c')
			pdf.cell(w=55, h=8, txt=str(global_data['act_numero'])+str(global_data['actc_num']), border=1, align='l')
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Correo Electronico', border=1, align='c')
			pdf.cell(w=50, h=8, txt=str(global_data['act_email']), border=1, align='c')
			pdf.set_font("helvetica", "B", 12)

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Ciudad', border=1, align='c')
			pdf.cell(w=55, h=8, txt=str(global_data['act_ciudad']), border=1, align='l')
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Codigo Postal', border=1, align='c')
			pdf.cell(w=50, h=8, txt=str(global_data['act_post']), border=1, align='c')
			pdf.set_font("helvetica", "B", 12)

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Pais', border=1, align='c')
			pdf.cell(w=55, h=8, txt=str(global_data['act_pais']), border=1, align='l')
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Teléfono', border=1, align='c')
			pdf.cell(w=50, h=8, txt=str(global_data['act_tel']), border=1, align='c')
			pdf.set_font("helvetica", "B", 12)

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )


			pdf.set_font("helvetica", "B", 12)
			pdf.cell(w=190, h=8, txt='Funcionario Autorizado', border=1, align='c' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Nombre y Apellido', border=1 , align='c' )
			
			pdf.cell(w=155, h=8, txt=str(global_data['usuario']), border=1, align='l' )

			pdf.image("static/sfe_no_pres_foot.png",x=85,y=(pdf.get_y() + 15),w=35,h=15)
			
			
			pdf.output(getcwd()+f"/temp_pdf/{str(global_data['expediente'])}/{str(global_data['expediente'])}-0.pdf") #"/pdf/SFE_REGISTRO_"+str(arg)+"_local.pdf"

		traer_datos_pdf(str(global_data['expediente']))

		#print(global_data)

	except Exception as e:
		print(e)
			

#renovacion_pdf_sfe_local("22106266")