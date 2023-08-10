import time

import psycopg2
from wipo.ipas import Insert_Action_soporte
from redpi.Clasificados import edicion_cont, insertar_edicion_finde, previa_edicion,insertar_edicion
from datetime import date, datetime, timedelta
from tools.connect import db_host, db_user, db_password, db_database, host_SFE_conn, user_SFE_conn, password_SFE_conn, database_SFE_conn,host_centura, user_centura, password_centura, database_centura
from tools.send_mail import redpi_mail

#print(str(date.today()))

insertOk = 0
list_for_mail = ''
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
			if(H == '00:10:01'):
			##############################################################################################################                
				check_date()
			##############################################################################################################

			if(H == '06:05:01'):
			##############################################################################################################
				list_for_mail = report_package_this_today()                
				redpi_mail('jun.taniwaki@dinapi.gov.py', 'REDPI', F'Publicacion REDPI e IPAS de la fecha {dia} - {list_for_mail} ')
			##############################################################################################################			
			
			time.sleep(0.5)	
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
	'''
	##############################################################################################################
	if(M == '30:01' and insertOk == 0):
	##############################################################################################################                
		re_insert_redpi('1977-09-01')
	##############################################################################################################
	if(M == '40:01' and insertOk == 0):
	##############################################################################################################                
		re_insert_redpi('1977-09-01')
	##############################################################################################################
	if(M == '50:01' and insertOk == 0):
	##############################################################################################################                
		re_insert_redpi('1977-09-01')
	##############################################################################################################
	if(M == '59:01' and insertOk == 0):
	##############################################################################################################                
		re_insert_redpi('1977-09-01')'''
	
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
				print(Insert_Action_soporte(exp_ipas[x],str(date.today()),'4','Publicacion REDPI','573'))

		connH.close()
		insertOk = 1
	except Exception as e:
		pass

def report_package_this_today():
	try:
		connH = psycopg2.connect(host=db_host,user=db_user,password=db_password,database=db_database)
		cursor = connH.cursor()
		cursor.execute("select  id,nexpedientes  from publicaciones_publicaciones pp order by id desc limit 1")    
		row=cursor.fetchall()
		for i in row:
			return(str(i[1]))
		connH.close()
	except Exception as e:
		pass

timer(3)



	





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