import json
from time import sleep
from unicodedata import numeric
from fpdf import FPDF, HTMLMixin  #pip install fpdf2
from os import getcwd
import barcode
from barcode.writer import ImageWriter
import psycopg2
from dinapi.sfe import titulare_reg
from wipo.ipas import mark_getlist, mark_read
from tools.data_format import signo_format
import tools.connect as connex

def registro_pdf_sfe_local(arg):
	try:
		multitu = []	
		global_data = {}
		clase_tipo = 0
		def recorrer_sfe(arg):
			try:
				conn = psycopg2.connect(host = connex.MEA_DB_ORIGEN_host,user = connex.MEA_DB_ORIGEN_user,password = connex.MEA_DB_ORIGEN_password,database = connex.MEA_DB_ORIGEN_database)
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
						global_data['distintivo'] = ""


					try:
						if(i['campo'] == "marca_deslogotipo"):
							global_data['deslogotipo'] = i['valor']['valor']['archivo']['url']
					except Exception as e:
						global_data['deslogotipo'] = ""



					try:
						if(i['campo'] == "marca_deslogotipofg"):
							global_data['deslogotipofg'] = i['valor']['archivo']['url']
					except Exception as e:
						global_data['deslogotipofg'] = ""


					try:
						if(i['campo'] == "marca_distintivofg"):
							global_data['distintivofg'] = i['valor']['archivo']['url']
					except Exception as e:
						global_data['distintivofg'] = ""
					


					try:
						if(i['descripcion'] == "N° de Documento" and i['campo'] == "datospersonales_nrodocumento"):
							global_data['documento'] = i['valor']
					except Exception as e:
						global_data['documento'] = ""

					try:
						if(i['campo'] == 'datospersonales_ruc'):				
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
						if(i['campo'] == 'marca_tipomarca'):
							global_data["tipo_on"] = i['valor']
					except Exception as e:
						global_data['tipo_on'] = ""	

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
						if(i['descripcion'] == "Nombres y Apellidos" and i['campo'] == 'datospersonales_nombreapellido'):
							global_data['nombre_soli'] = i['valor']
					except Exception as e:
						global_data['nombre_soli'] = ""
											
					try:
						if(i['campo'] == 'datospersonales_razonsocial'):
							global_data['razon_social']=i['valor']
					except Exception as e:
						global_data['razon_social'] = ""					
					try:
						if(i['campo'] == 'datospersonales_calle'):
							global_data['direccion']=i['valor']
					except Exception as e:
						global_data['direccion'] = ""					
					try:
						if(i['descripcion'] == "Ciudad" and i['campo'] == 'datospersonales_ciudad'):
							global_data['ciudad']=i['valor']
					except Exception as e:
						global_data['ciudad'] = ""					
					try:
						if(i['descripcion'] == "País " and i['campo'] == 'datospersonales_pais'):
							global_data['pais']=i['valor']
					except Exception as e:
						global_data['pais'] = ""					
					try:
						if(i['campo'] == "datospersonales_codigopostal"):
							global_data['codigo_postal']=i['valor']
					except Exception as e:
						global_data['codigo_postal'] = ""					
					try:
						if(i['descripcion'] == "Teléfono" and i['campo'] == 'datospersonales_telefono'):
							global_data['telefono']=i['valor']
					except Exception as e:
						global_data['telefono'] = ""					
					try:
						if(i['descripcion'] == "Correo Electrónico" and i['campo'] == 'datospersonales_correoelectronico'):
							global_data['email']=i['valor']
					except Exception as e:
						global_data['email'] = ""					
					try:
						if(i['descripcion'] == "Distrito"):
							global_data['distrito']=i['valor']
					except Exception as e:
						global_data['distrito'] = ""


					try:
						if(i['descripcion'] == "Clase"):
							global_data['clase_on']=i['valor']
					except Exception as e:
						global_data['clase_on'] = ""

					try:
						if(i['descripcion'] == "Documento" and i['campo'] == 'prioridad_docuprioridad'):
							global_data['documento_pri']=i['valor']
					except Exception as e:
						global_data['documento_pri'] = ""

					try:
						if(i['descripcion'] == "N° de Solicitud" and i['campo'] == 'prioridad_nodesolicitud'):
							global_data['solicitud_pri']=i['valor']
					except Exception as e:
						global_data['solicitud_pri'] = ""

					try:
						if(i['descripcion'] == "Fecha de Prioridad" and i['campo'] == 'prioridad_fechaprioridad'):
							global_data['fecha_pri']=i['valor']
					except Exception as e:
						global_data['fecha_pri'] = ""

					try:
						if(i['descripcion'] == "País/Oficina" and i['campo'] == 'prioridad_paisoficina'):
							global_data['pais_pri']=i['valor']
					except Exception as e:
						global_data['pais_pri'] = ""

					try:
						if(i['descripcion'] == "Especificar" and i['campo'] == 'marca_especificar'):
							global_data['espe']=i['valor']
					except Exception as e:
						global_data['espe'] = ""

					try:	
						if(i['campo'] == 'datostitular_agregar'):
							global_data["titu_cant"] = i['valor']
					except Exception as e:
						global_data['titu_cant'] = ""

				#print(global_data)


			except Exception as e:
				print(e)
			finally:
				conn.close()

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
				#if (str(a[0]) <= '01'):
					#fail_hour_sfe = (int(a[0]) + 3)
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
		recorrer_sfe(arg)
		
		try:
			multitu = titulare_reg(arg,global_data["titu_cant"])
			if multitu != []:
				if multitu[0]['person']['personName'] == '':
					multitu = []
		except Exception as e:
			multitu = []	

		sleep(1)

		#print(global_data)
		
		def traer_datos_pdf(arg):
			codebarheard("*"+str(global_data['expediente'])+"*")
			codebarfoot("*"+str(global_data['codigo_barr'])+"*")
			pdf = FPDF()
			pdf.add_page()
			pdf.set_font("helvetica", "B", 12)
			pdf.image('static/IMG.PNG',x=76,y=5,w=63,h=17)
			pdf.cell(0, 40, "________________________________________________________________________________________________________", align='c',ln=1)
			pdf.cell(0, -20, str(global_data['nombre_formulario']), align='c',ln=1)
			pdf.set_font('helvetica', 'I', 8)
			pdf.text(x=18, y=54, txt='Dirección General de Propiedad Industrial')
			pdf.text(x=18, y=59, txt='Dirección de Marcas')
			pdf.text(x=18, y=64, txt='Secretaría General - Mesa de Entradas')
			pdf.image("static/sfe_no_pres_head.png",x=145,y=(pdf.get_y() + 20),w=30,h=15)
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
				pdf.cell(w=50, h=8, txt=str(global_data['expediente']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='l' )
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
			pdf.cell(w=35, h=8, txt='Tipo de Marca', border=1, align='c')
			
			try:
				pdf.cell(w=35, h=8, txt=signo_format(str(global_data['tipo_on'])), border=1, align='l')
			except Exception as e:
				pdf.cell(w=35, h=8, txt=str(global_data['tipo_on']), border=1, align='l')	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Denominación ', border=1 , align='c' )
			
			pdf.multi_cell(w=155, h=8, txt=str(global_data['denominacion_on']), border=1, align='l' )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Clasificación', border=1, align='l')
			

			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['clasificacion']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=55, h=8, txt='Clase Niza', border=1, align='c' )
			

			try:
				pdf.cell(w=50, h=8, txt=str(global_data['clase_on']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9) 
			pdf.cell(w=60, h=8, txt='Productos o Servicios que distingue:', border=1 , align='c' )
			
			try:
				pdf.multi_cell(w=130, h=4, txt=str(global_data['distingue']), border=1, align='L',ln=1)
			except Exception as e:
				pdf.multi_cell(w=130, h=4, txt="", border=1, align='L',ln=1)

			######################################################################################################################

			pdf.cell(w=0, h=5, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=70, h=28, txt='Referencia de Distintivo:', border=1 , align='c' )

			pdf.multi_cell(w=120, h=28, txt="", border=1, align='L',ln=1) 
			

			try:
				pdf.image(str(global_data['distintivo'] + global_data['deslogotipofg']),x=123,y=(pdf.get_y()-27),w=25,h=25)
			except Exception as e:
				pdf.image("static/sfe_default.PNG",x=123,y=(pdf.get_y()-27),w=25,h=25)

			alt_fil:int = (round(len(global_data['deslogotipofg']+global_data['deslogotipo'])/98))
			val_num:int = 0
			val_lab:int = 0
			if alt_fil == 0:
				val_num = 8
				val_lab = 4
			else:
				val_lab = alt_fil
				val_num = alt_fil

			pdf.cell(w=70, h=6, txt='Descripción de Distintivo:', border=1 , align='c' )

			pdf.set_font("helvetica", "B", 7)

			try:
				pdf.multi_cell(w=120, h=4, txt=str(global_data['deslogotipo']) + str(global_data['deslogotipofg']), border=1, align='L',ln=1)
			except Exception as e:
				pdf.multi_cell(w=130, h=6, txt="", border=1, align='L',ln=1)

			"""			
			pdf.cell(w=0, h=5, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=60, h=8, txt='Referencia de Distintivo:', border=1 , align='l' )

			pdf.multi_cell(w=130, h=4, txt="El archivo correspondiente al distintivo se ha recibido correctamente y se encuentra alojado en nuestros servidores. Lo puede verificar en el buzón de trámites.", border=1, align='L',ln=1) 
			"""
			######################################################################################################################

			pdf.cell(w=0, h=5, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=70, h=6, txt='Reivindicaciones', border=1, align='l')
			
			pdf.cell(w=120, h=6, txt=global_data['reivindicaciones'], border=1, align='l')
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=30, h=8, txt='Especificar', border=1 , align='c' )
			
			pdf.set_font("helvetica", "", 7)
			pdf.multi_cell(w=160, h=8, txt=global_data['espe'], border=1, align='l' )	
			pdf.image("static/sfe_no_pres_foot.png",x=85,y=(pdf.get_y() + 15),w=35,h=15)
			
			
			
			#############################################################################################################################



			pdf.add_page()
			pdf.set_font("helvetica", "B", 12)
			pdf.image("static/sfe_no_pres_head.png",x=145,y=(pdf.get_y() + 4),w=30,h=15)
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=190, h=8, txt='DATOS DEL SOLICITANTE', border=1, align='c' )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.cell(w=50, h=8, txt='N° de Documento / RUC', border=1, align='c')
			
			try:
				pdf.cell(w=50, h=8, txt=str(global_data['documento']+global_data['RUC']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt=str(global_data['RUC']), border=1, align='l' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 8)
			pdf.cell(w=50, h=8, txt='Nombres y Apellidos Razón Social', border=1 , align='l' )
			
			pdf.cell(w=140, h=8, txt=str(str(global_data['nombre_soli'])+str(global_data['razon_social'])), border=1, align='l' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Calle', border=1 , align='c' )
			
			try:	
				pdf.multi_cell(w=140, h=8, txt=str(global_data['direccion']), border=1, align='l',ln=1) 	
			except Exception as e:
				pdf.multi_cell(w=140, h=8, txt="", border=1, align='l',ln=1) 

			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Ciudad', border=1 , align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['ciudad']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Pais', border=1 , align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['pais']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=55, h=8, txt='Codigo Postal', border=1, align='c' )

			try:
				pdf.cell(w=50, h=8, txt=str(global_data['codigo_postal']), border=1, align='c' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Telefono', border=1 , align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['telefono']), border=1, align='l' )
			except Exception as e:
				pass
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=40, h=8, txt='Correo Electronico ', border=1, align='c' )
			
			try:
				pdf.cell(w=65, h=8, txt=str(global_data['email']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=65, h=8, txt="", border=1, align='c' )		
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )



			################################################################################################################################################
															##Titulares adicionales##
			try:												
				contador:int = 1
				numTitle:str = ""
				for i in multitu:
					contador = contador + 1
					numTitle = contador
					pdf.set_font("helvetica", "B", 12)
					pdf.cell(w=190, h=8, txt=f'DATOS DEL SOLICITANTE {str(numTitle)}', border=1, align='c' )
					pdf.set_font("helvetica", "B", 9)
					pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

					pdf.cell(w=50, h=8, txt='N° de Documento / RUC', border=1, align='c')
					
					try:
						pdf.cell(w=50, h=8, txt=str(i['person']['legalIdNbr']) + str(i['person']['individualIdNbr']), border=1, align='l' )
					except Exception as e:
						pdf.cell(w=50, h=8, txt="", border=1, align='l' )

					pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
					pdf.set_font("helvetica", "B", 8)
					pdf.cell(w=50, h=8, txt='Nombres y Apellidos Razón Social', border=1 , align='l' )
					
					pdf.cell(w=140, h=8, txt=str(i['person']['personName']), border=1, align='l' )
					pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
					pdf.set_font("helvetica", "B", 9)
					pdf.cell(w=50, h=8, txt='Calle', border=1 , align='c' )
					
					try:	
						pdf.multi_cell(w=140, h=8, txt=str(i['person']['addressStreet']), border=1, align='l',ln=1) 	
					except Exception as e:
						pdf.multi_cell(w=140, h=8, txt="", border=1, align='l',ln=1)

					pdf.cell(w=0, h=4, txt='', border=0,ln=1 )

					pdf.set_font("helvetica", "B", 9)
					pdf.cell(w=35, h=8, txt='Ciudad', border=1 , align='c' )
					
					try:	
						pdf.cell(w=50, h=8, txt=str(i['person']['cityName']), border=1, align='l' )
					except Exception as e:
						pdf.cell(w=50, h=8, txt="", border=1, align='c' )	
					pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
					pdf.set_font("helvetica", "B", 9)
					pdf.cell(w=35, h=8, txt='Pais', border=1 , align='c' )
					
					try:	
						pdf.cell(w=50, h=8, txt=str(i['person']['nationalityCountryCode']), border=1, align='l' )
					except Exception as e:
						pdf.cell(w=50, h=8, txt="", border=1, align='c' )
					pdf.set_font("helvetica", "B", 9)	
					pdf.cell(w=55, h=8, txt='Codigo Postal', border=1, align='c' )
					
					try:	
						pdf.cell(w=50, h=8, txt=str(i['person']['zipCode']), border=1, align='c' )
					except Exception as e:
						pdf.cell(w=50, h=8, txt="", border=1, align='c' )	
					pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
					pdf.set_font("helvetica", "B", 9)
					pdf.cell(w=35, h=8, txt='Telefono', border=1 , align='c' )
					
					try:	
						pdf.cell(w=50, h=8, txt=str(i['person']['telephone']), border=1, align='l' )
					except Exception as e:
						pass
					pdf.set_font("helvetica", "B", 9)	
					pdf.cell(w=40, h=8, txt='Correo Electronico ', border=1, align='c' )
					
					try:
						pdf.cell(w=65, h=8, txt=str(i['person']['email']), border=1, align='l' )
					except Exception as e:
						pdf.cell(w=65, h=8, txt="", border=1, align='c' )		
					pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			except Exception as e:
				pass
			################################################################################################################################################




			pdf.set_font("helvetica", "B", 12)
			pdf.cell(w=190, h=8, txt='DATOS DE PRIORIDAD', border=1, align='c' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			############

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Documento', border=1 , align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['documento_pri']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=55, h=8, txt='Nro de Solicitud', border=1, align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['solicitud_pri']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			#############

			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Fecha de Prioridad', border=1 , align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt=convert_fecha_hora(str(global_data['fecha_pri']).replace("T"," ").replace("Z","")), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=55, h=8, txt='Pais/Oficina', border=1, align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['pais_pri']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			#############			


			pdf.set_font("helvetica", "B", 12)
			pdf.cell(w=190, h=8, txt='DATOS DEL AGENTE DE PROPIEDAD INTELECTUAL', border=1, align='c' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )




			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Matricula', border=1 , align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['code_agente']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Nombres y Apellidos', border=1 , align='c' )
			
			try:	
				pdf.cell(w=140, h=8, txt=str(global_data['agente']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=140, h=8, txt="", border=1, align='c' )	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			"""
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=50, h=8, txt='Calle', border=1 , align='c' )
			
			
			try:	
				pdf.cell(w=140, h=8, txt=str(global_data['direccion_agente']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=140, h=8, txt="", border=1, align='c' )	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='País', border=1 , align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['pais_agente']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=55, h=8, txt='Departamento', border=1, align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Distrito', border=1 , align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=55, h=8, txt='Barrio', border=1, align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['barrio_agente']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )	
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=35, h=8, txt='Teléfono', border=1 , align='c' )
			
			try:	
				pdf.cell(w=50, h=8, txt=str(global_data['ag_tel']), border=1, align='l' )
			except Exception as e:
				pdf.cell(w=50, h=8, txt="", border=1, align='c' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=40, h=8, txt='Correo electrónico', border=1, align='c' )
			
			try:	
				pdf.cell(w=65, h=8, txt=str(global_data['email_agente']), border=1, align='l' )			
			except Exception as e:
				pdf.cell(w=65, h=8, txt="", border=1, align='c' )
						
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 12)
			pdf.cell(w=190, h=8, txt='Funcionario Autorizado', border=1, align='c' )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.cell(w=50, h=8, txt='Nombre y Apellido', border=1 , align='c' )
			pdf.set_font("helvetica", "B", 7)
			try:	
				pdf.cell(w=140, h=8, txt=str(global_data['usuario']), border=1, align='l' )	
			except Exception as e:
				pdf.cell(w=140, h=8, txt="", border=1, align='c' )
			"""	

			pdf.image("static/sfe_no_pres_foot.png",x=85,y=(pdf.get_y() + 15),w=35,h=15)


			#pdf.output(getcwd()+f"/temp_pdf/{str(global_data['expediente'])}/{str(global_data['expediente'])}-0.pdf") 
			pdf.output(getcwd()+"/pdf/SFE_REGISTRO_"+str(arg)+"_local.pdf")

		traer_datos_pdf(arg)
	except Exception as e:
		print(e)
	

registro_pdf_sfe_local('27493')



