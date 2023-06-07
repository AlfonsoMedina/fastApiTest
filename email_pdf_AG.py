from dataclasses import replace
import json
import os
from time import sleep
from fpdf import FPDF, HTMLMixin  #pip install fpdf2
from os import getcwd
import barcode
from barcode.writer import ImageWriter
import psycopg2
from dinapi.sfe import pendiente_sfe, qr_code
import tools.filing_date as captureDate
from wipo.ipas import *
from tools.base64Decode import decode_pdf
from tools.data_format import fecha_barra, hora, signo_format
import tools.connect as connex

global_data = {}
def envio_agente_recibido(arg0,arg1):
	try:
		qr_code('https://sfe-beta.dinapi.gov.py/dashboard/expedientes/tramites/'+str(arg0))
		"""
		data = pendiente_sfe(arg0)


		try:
			for i in range(0,len(data[0]['respuestas'])):
				if data[0]['respuestas'][i]['campo'] == 'expedienteoescrito_pais':
					global_data = str(data[0]['respuestas'][i]['valor'])
		except Exception as e:
			global_data = ""

		
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
				print(backhour)
				return(str(fecha_formatE+" "+str(backhour)))
		def convert_fecha_hora(data):
			date_fullE = str(data).split(" ")
			fecha_fullE = date_fullE[0].split("-")
			fecha_formatE = fecha_fullE[2]+"/"+fecha_fullE[1]+"/"+fecha_fullE[0]
			hora_puntoE = date_fullE[1].split(".")
			hora_guionE = hora_puntoE[0].split("-")
			return(str(fecha_formatE+" "+str(hora_guionE[0])))
		"""

		def traer_datos_pdf():

			#codebarheard(str(global_data['expediente']))
			#codebarfoot(str(global_data['codigo_barr']))

			pdf = FPDF()
			pdf.add_page()
			pdf.set_font("helvetica", "B", 12)



			"""
			pdf.image('static/IMG.PNG',x=76,y=4,w=50,h=18)
			
			pdf.cell(0, 20, "________________________________________________________________________________________________________", align='c',ln=1)
			
			pdf.cell(0, 0, "------", align='c',ln=1)


			pdf.set_font('helvetica', 'I', 8)
			pdf.text(x=18, y=38, txt='Dirección General de Propiedad Industrial')
			pdf.text(x=18, y=43, txt='Dirección de Asuntos Marcarios Litigiosos')
			pdf.text(x=18, y=48, txt='Secretaría General - Mesa de Entradas')
			pdf.image("static/sfe_no_pres_head.png",x=145,y=(pdf.get_y() + 4),w=30,h=15)

			pdf.set_font("helvetica", "B", 9)

			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
			pdf.cell(w=0, h=4, txt='', border=0,ln=1 )


			pdf.cell(w=40, h=8, txt='Fecha de Envío', border=1 , align='c' )
			
			pdf.cell(w=150, h=8, txt="", border=1, align='l' )
		

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=40, h=8, txt='Expediente Nro.', border=1, align='c')
			
			pdf.cell(w=50, h=8, txt="", border=1, align='l' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=50, h=8, txt='Fecha y Hora de Recepción', border=1, align='c' )
			
			pdf.cell(w=50, h=8, txt="", border=1, align='l' )


			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 12)
			pdf.cell(w=190, h=8, txt='DATOS DE LA SOLICITUD A LA QUE SE OPONE', border=1, align='c' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )


			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=30, h=8, txt='Solicitud Nro.:', border=1, align='c')
			
			pdf.cell(w=32, h=8, txt="", border=1, align='l' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=32, h=8, txt='Fecha', border=1, align='c' )
			
			pdf.cell(w=32, h=8, txt="", border=1, align='l' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=32, h=8, txt='Clase', border=1, align='c' )
			
			pdf.cell(w=32, h=8, txt="", border=1, align='l' )

			
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=40, h=8, txt='Denominación', border=1 , align='c' )
			
			pdf.cell(w=150, h=8, txt="", border=1, align='l' )


			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 12)
			pdf.cell(w=190, h=8, txt='DATOS DE LA MARCA POR LA CUAL SE OPONE', border=1, align='c' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )


			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=30, h=8, txt='Solicitud Nro.:', border=1, align='c')
			
			pdf.cell(w=32, h=8, txt="", border=1, align='l' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=32, h=8, txt='Fecha', border=1, align='c' )
			
			pdf.cell(w=32, h=8, txt="", border=1, align='l' )
			pdf.set_font("helvetica", "B", 9)	
			pdf.cell(w=32, h=8, txt='Clase', border=1, align='c' )
			
			pdf.cell(w=32, h=8, txt="------", border=1, align='l' )

			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=40, h=8, txt='Registro Nro:', border=1 , align='c' )
			
			pdf.cell(w=150, h=8, txt="", border=1, align='l' )


			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "B", 9)
			pdf.cell(w=40, h=8, txt='Denominación', border=1 , align='c' )
			
			pdf.cell(w=150, h=8, txt="", border=1, align='l' )
			
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			"""

			hora_envio = hora(str(form_id(arg0)[1])).split(".")
			hora_recep = hora(str(form_id(arg0)[2])).split(".")

			pdf.image('static/IMG.PNG',x=12,y=22,w=49,h=15)

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=76, y=20, txt='Formulario')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=20, txt=str(form_descrip(str(form_id(arg0)[0]))))			

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=74, y=25, txt='Fecha envio')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=25, txt=fecha_barra(str(form_id(arg0)[1]))+" "+hora_envio[0])			

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=66, y=30, txt='Fecha Recepcion')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=30, txt=fecha_barra(str(form_id(arg0)[2]))+" "+ hora_recep[0])			

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=75, y=35, txt='Expediente')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=35, txt= str(captureDate.capture_year())+'-'+str(arg1))

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=85, y=40, txt='Tipo')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=40, txt=str(sigla_id(str(form_id(arg0)[3]))))

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=80, y=48, txt='Titulo de presentación:')			

			pdf.multi_cell(w=190, h=40, txt='', border="LRT" , align='c' )
			
			pdf.cell(w=0, h=0, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "", 8)
			pdf.multi_cell(w=190, h=8, txt="                                                                                         "+str(description(arg0)), border="LRB", align='L' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			pdf.image('pdf/output.png',x=170,y=20,w=18,h=18)			

			
			pdf.output('pdf/notificacion-DINAPI.pdf')

		traer_datos_pdf()

		#print(global_data)
		return(True)
	except Exception as e:
		print(e)

def envio_agente_recibido_reg(arg0,arg1):
	try:
		qr_code('https://sfe-beta.dinapi.gov.py/dashboard/expedientes/tramites/'+str(arg0))

		def traer_datos_pdf():

			#codebarheard(str(global_data['expediente']))
			#codebarfoot(str(global_data['codigo_barr']))

			pdf = FPDF()
			pdf.add_page()
			pdf.set_font("helvetica", "B", 12)


			hora_envio = hora(str(form_id(arg0)[1])).split(".")
			hora_recep = hora(str(form_id(arg0)[2])).split(".")

			pdf.image('static/IMG.PNG',x=12,y=22,w=49,h=15)

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=76, y=20, txt='Formulario')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=20, txt=str(form_descrip(str(form_id(arg0)[0]))))			

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=74, y=25, txt='Fecha envio')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=25, txt=fecha_barra(str(form_id(arg0)[1]))+" "+hora_envio[0])			

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=66, y=30, txt='Fecha Recepcion')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=30, txt=fecha_barra(str(form_id(arg0)[2]))+" "+ hora_recep[0])			

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=75, y=35, txt='Expediente')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=35, txt= str(captureDate.capture_year())+'-'+str(arg1))

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=85, y=40, txt='Tipo')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=40, txt="REG - Registro de marca")

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=80, y=48, txt='Titulo de presentación:')			

			pdf.multi_cell(w=190, h=40, txt='', border="LRT" , align='c' )
			
			pdf.cell(w=0, h=0, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "", 8)
			pdf.multi_cell(w=190, h=8, txt="                                                                                     Solicitud de registro de marca", border="LRB", align='L' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			pdf.image('pdf/output.png',x=170,y=20,w=18,h=18)			

			
			pdf.output('pdf/notificacion-DINAPI.pdf')

		traer_datos_pdf()

		#print(global_data)
		return(True)
	except Exception as e:
		print(e)

def envio_agente_recibido_ren(arg0,arg1):
	try:
		qr_code('https://sfe-beta.dinapi.gov.py/dashboard/expedientes/tramites/'+str(arg0))

		def traer_datos_pdf():

			#codebarheard(str(global_data['expediente']))
			#codebarfoot(str(global_data['codigo_barr']))

			pdf = FPDF()
			pdf.add_page()
			pdf.set_font("helvetica", "B", 12)


			hora_envio = hora(str(form_id(arg0)[1])).split(".")
			hora_recep = hora(str(form_id(arg0)[2])).split(".")

			pdf.image('static/IMG.PNG',x=12,y=22,w=49,h=15)

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=76, y=20, txt='Formulario')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=20, txt=str(form_descrip(str(form_id(arg0)[0]))))			

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=74, y=25, txt='Fecha envio')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=25, txt=fecha_barra(str(form_id(arg0)[1]))+" "+hora_envio[0])			

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=66, y=30, txt='Fecha Recepcion')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=30, txt=fecha_barra(str(form_id(arg0)[2]))+" "+ hora_recep[0])			

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=75, y=35, txt='Expediente')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=35, txt= str(captureDate.capture_year())+'-'+str(arg1))

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=85, y=40, txt='Tipo')
			pdf.set_font("helvetica", "", 8)
			pdf.text(x=100, y=40, txt="REN - Renovación de marca")

			pdf.set_font("helvetica", "B", 9)
			pdf.text(x=80, y=48, txt='Titulo de presentación:')			

			pdf.multi_cell(w=190, h=40, txt='', border="LRT" , align='c' )
			
			pdf.cell(w=0, h=0, txt='', border=0,ln=1 )
			pdf.set_font("helvetica", "", 8)
			pdf.multi_cell(w=190, h=8, txt="                                                                                     Solicitud de renovación de marca", border="LRB", align='L' )
			pdf.cell(w=0, h=12, txt='', border=0,ln=1 )

			pdf.image('pdf/output.png',x=170,y=20,w=18,h=18)			

			
			pdf.output('pdf/notificacion-DINAPI.pdf')

		traer_datos_pdf()

		#print(global_data)
		return(True)
	except Exception as e:
		print(e)

def form_descrip(arg):
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select nombre  from formularios where id = {}""".format(str(arg)))
		row=cursor.fetchall()
		for i in row:
			return(i[0])	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def form_id(arg):
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select formulario_id, enviado_at, recepcionado_at, tipo_documento_id from tramites where id = {}""".format(str(arg)))
		row=cursor.fetchall()
		for i in row:
			return(i)	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def sigla_id(arg):
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select nombre from tipos_documento where id = {}""".format(str(arg)))
		row=cursor.fetchall()
		for i in row:
			return(i[0])	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def description(arg):
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select respuestas from tramites where id = {}""".format(str(arg)))
		row=cursor.fetchall()
		for i in row:
			for item in range(0,len(i[0])):
				if i[0][item]['campo'] == 'observacion_descobservacion':
					return(i[0][item]['valor'])	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def agent_email(arg):
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select usuario_id from tramites where id = {}""".format(str(arg)))
		row=cursor.fetchall()
		for i in row:
			return(agent_id(i[0]))	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def agent_id(arg):
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select email from usuarios where id = {}""".format(str(arg)))
		row=cursor.fetchall()
		for i in row:
			return(i[0])	
	except Exception as e:
		print(e)
	finally:
		conn.close()

