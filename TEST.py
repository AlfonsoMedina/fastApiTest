from turtle import back
import psycopg2
from dinapi.sfe import renovacion_sfe, titulare_reg
from email_pdf_AG import registro_pdf_con_acuse
from sfe_no_presencial_reg_local import registro_pdf_sfe_local
from sfe_no_presencial_ren_local import renovacion_pdf_sfe_local
from tools.filing_date import capture_day
import tools.connect as connex




# Ultimo dia
def getDia_proceso():
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.LAST_DAY_PROCESS)
		row=cursor.fetchall()
		for i in row:
			return(str(i[0]))	
	except Exception as e:
		print(e)
	finally:
		conn.close()

#Ultimo numero
def getLast_number():
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.LAST_NUMBER)
		row=cursor.fetchall()
		for i in row:
			return(str(i[0]))	
	except Exception as e:
		print(e)
	finally:
		conn.close()

#Cerrar dia
def closed_process_day(fecha):
	try:
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.CLOSE_PROCESS_DATE.format(fecha))
		conn.commit()
		conn.close()
		return(True)
	except Exception as e:
		return(e)

#Abrir dia
def open_process_day(fecha):
	try:
		num = int(getLast_number())
		conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
		cursor = conn.cursor()
		cursor.execute(connex.OPEN_PROCESS_DATE.format(fecha,num,num))
		conn.commit()
		conn.close()
		return(True)
	except Exception as e:
		return(e)

def newDayProcess():
	last_date = getDia_proceso() 					# Ultima fecha de proceso 
	today = capture_day()							# fecha de hoy
	if closed_process_day(last_date) == True:		# Cierra ultima fecha 
		if open_process_day(today) == True:			# Abre fecha nueva
			return(True)			


#print(fetch_all_user_mark('AMEDINA')[0]['sqlColumnList'][0]['sqlColumnValue'])

#print(newDayProcess())

#print(ProcessGroupGetList('298'))

#print(USER_GROUP('CP'))





#print(renovacion_sfe('1795'))



#renovacion_pdf_sfe_local('1795')

#print(titulare_reg('1586'))

#registro_pdf_sfe_local('1586')

#renovacion_pdf_sfe_local('1941')

#registro_pdf_con_acuse('1586')