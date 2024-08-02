import time
import requests
import psycopg2
from wipo.ipas import Insert_Action_soporte
from redpi.Clasificados import edicion_cont, insertar_edicion_finde, previa_edicion,insertar_edicion, processToDate
from datetime import date, datetime, timedelta
from tools.connect import db_host, db_user, db_password, db_database, host_SFE_conn, user_SFE_conn, password_SFE_conn, database_SFE_conn,host_centura, user_centura, password_centura, database_centura
from tools.send_mail import redpi_mail

import aiohttp
import asyncio


#print(str(date.today()))

insertOk = 0
list_for_mail = {}
def timer(step):
	dia = str(time.strftime("%Y-%m-%d"))
	print('Proceso de publicacion automatica............... Proxima publicacion 00:11AM Horas')
	print('Envio de correo...............  06:10AM Horas')
	H = str(time.strftime("%H:%M:%S"))
	i = 0
	while i < step:
		check_new_package(step)
		for i in range(step):
			H = str(time.strftime("%H:%M:%S"))
			if(H == '00:11:01'):
			##############################################################################################################                
				check_date()
			##############################################################################################################
			if(H == '06:05:01'):
			##############################################################################################################
				list_for_mail = report_package_this_today()               
				redpi_mail('gustavo.britez@dinapi.gov.py', 'REDPI', f'Publicacion REDPI e IPAS de la fecha { list_for_mail["fecha"] } - { list_for_mail["exp"] } ')
				asyncio.run(main()) # crear grupos
			##############################################################################################################
			time.sleep(0.5)
			##############################################################################################################			
			if(H == '18:05:01'):
			##############################################################################################################
				publication_check()
			##############################################################################################################				
			if(i == 10):
				i=0

def check_new_package(step):
	M = str(time.strftime("%M:%S"))
	if(M == '05:01' and insertOk == 0):
	##############################################################################################################                
		re_insert_redpi('1977-09-01')
	##############################################################################################################
	if(M == '20:01' and insertOk == 0):
	##############################################################################################################                
		re_insert_redpi('1977-09-01')
	
def check_date():
	try:
		msg = ''
		dia = str(time.strftime("%Y-%m-%d"))
		db_id = bool
		conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
		cursor = conn.cursor()
		cursor.execute("SELECT id, fecha_publicacion,tipo_publicacion FROM public.publicaciones_publicaciones where fecha_publicacion = '1977-09-01'")
		row=cursor.fetchall()
		for i in row:
			if str(i[1]) == '1977-09-01':
				db_id = True
			else:
				db_id = False

		time.sleep(1) # Pausa
		
		if db_id == True:
			print('publicado por el usuario')

			iniciar_publicacion()

			time.sleep(2)

			re_insert_redpi('1977-09-01')

			msg = 'publicado por el usuario: '+ str(dia)
		else:
		#########################################################################################################################
									#zona de ejecucion
			try:
				# 1) definir la edicion (consultar edicion para incrementar)
				num_edicion = int(edicion_cont())+1

				time.sleep(2) # Pausa

				# 3) Publicar  (ver formato de la fecha)
				insertar_edicion(dia,str(num_edicion))

				time.sleep(2)

				iniciar_publicacion()

			except Exception as e:
				pass
			# print(num_edicion)
			print('publicado por el sistema')
			print('Publicacion de ' + dia + ' edicion N° ' + str(num_edicion) )	
		######################################################################################################            
					   
		return(msg)
	except Exception as e:
		print(e)
	finally:
		conn.close()

def iniciar_publicacion():
	try:       
		connX = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
		cursor = connX.cursor()
		cursor.execute("SELECT id, fecha_publicacion,tipo_publicacion FROM public.publicaciones_publicaciones where fecha_publicacion = '1977-09-01'")    
		row=cursor.fetchall()
		for i in row:
			#print(i[1]) # captura la fecha pendiente
			#print(date.today()) # capturo la fecha de publicacion
			try:   
				conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
				cursor = conn.cursor()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           #Nombre
				url = "UPDATE public.publicaciones_publicaciones SET fecha_publicacion='"+str(date.today())+"', tipo_publicacion='CLASIFICADOS' WHERE id="+str(i[0])   
				cursor.execute(url)
				cursor.rowcount
				conn.commit()
				conn.close()
			except Exception as e:
				print(e)
		connX.close()
	except Exception as e:
		print(e)

def re_insert_redpi(fecha):
	list_for_mail = ''
	try:
		connH = psycopg2.connect(host=db_host,user=db_user,password=db_password,database=db_database)
		cursor = connH.cursor()
		cursor.execute("SELECT fecha_publicacion,nexpedientes FROM public.publicaciones_publicaciones where fecha_publicacion = '"+str(fecha)+"'")    
		row=cursor.fetchall()
		for i in row:
			#print(str(i[0]))
			list_for_mail = str(i[0])
			exp_ipas = str(i[1]).replace("[","").replace("]","").split(',')
			print(exp_ipas)
			for x in range(len(exp_ipas)):
				print(Insert_Action_soporte(exp_ipas[x],str(date.today()),'47','Publicacion REDPI','573'))
		connH.close()
		insertOk = 1
	except Exception as e:
		pass

def report_package_this_today():
	try:
		connH = psycopg2.connect(host=db_host,user=db_user,password=db_password,database=db_database)
		cursor = connH.cursor()
		cursor.execute("select  id, fecha_publicacion, nexpedientes from publicaciones_publicaciones pp order by id desc limit 1")    
		row=cursor.fetchall()
		for i in row:
			return({"id":str(i[0]),"fecha":str(i[1]),"exp":str(i[2])})
		connH.close()
	except Exception as e:
		pass

async def fetch_data(url):
	async with aiohttp.ClientSession() as apiRest:
		async with apiRest.get(url) as response:
			return await response.text()

async def main():
	try:
		url = "http://192.168.50.228:8077/sis/create_all_group"
		response_data = await fetch_data(url)
		print(response_data)
	except Exception as e:
		print('Create groups successfuly')

def publication_check():
	try:
		msg = ''
		db_id = bool
		conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
		cursor = conn.cursor()
		cursor.execute("SELECT id, fecha_publicacion,tipo_publicacion FROM public.publicaciones_publicaciones where fecha_publicacion = '1977-09-01'")
		row=cursor.fetchall()
		for i in row:
			if str(i[1]) == '1977-09-01':
				db_id = True
			else:
				db_id = False
		time.sleep(1)
		if db_id == True:
			print('Procesado por el usuario, esperando para crear edicion')
		else:
		######################################################################################################
			fin_de_semana = datetime.now()
			dia_semana = fin_de_semana.weekday()
			if dia_semana == 5:
				return "No se procesa los sábado"
			elif dia_semana == 6:
				return "No se procesa los domingo"
			else:
				fecha_actual = datetime.now()
				fecha_formateada = fecha_actual.strftime('%Y-%m-%d')
				processToDate(fecha_formateada,'4') # '2023-07-17','4'
				print(f'Procesado por el sistema, la fecha {fecha_formateada} el dia {dia_semana} # TEST')
		######################################################################################################            			   
		return(msg)
	except Exception as e:
		print(e)
	finally:
		conn.close()


timer(3)

#asyncio.run(main())

#iniciar_publicacion()

'''
##############################################################################################################
Hora por 24H
	time.strftime("%H:%M:%S") #Formato de 24 horas

Hora por 12H
	time.strftime("%I:%M:%S") #Formato de 12 horas

Fecha formato: dd/mm/yyyy
	print (time.strftime("%d/%m/%y"))
	
Las siguientes directivas se pueden utilizar en el formato de cadena:

%a - Nombre del día de la semana
%A - Nombre del día completo
%b - Nombre abreviado del mes
%B - Nombre completo del mes
%c - Fecha y hora actual
%d - Día del mes
%H - Hora (formato 24 horas)
%I - Hora (formato 12 horas)
%j - Día del año
%m - Mes en número
%M- Minutos
%p - Equivalente de AM o PM
%S - Segundos
%U - Semana del año (domingo como primer día de la semana)
%w - Día de la semana
%W - Semana del año (lunes como primer día de la semana)
%x - Fecha actual
%X - Hora actual
%y - Número de año (14)
%Y - Numero de año entero (2014)
%Z - Zona horaria

'''