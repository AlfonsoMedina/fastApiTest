
import psycopg2
import tools.connect as connex



def log_info_serch(fecha,estado):
	log_data = {}
	conn = psycopg2.connect(host = connex.hostME,user= connex.userME,password = connex.passwordME,database = connex.databaseME)
	cursor = conn.cursor()
	cursor.execute(f"""SELECT * FROM public.log_error where  evento = '{estado}' and  fecha_evento >= '{fecha} 00:59' and fecha_evento <= '{fecha} 21:59'""")
	row=cursor.fetchall()
	log_data = row
	conn.close()	
	return(log_data)


#print(log_info_serch('2023-05-24','E00'))