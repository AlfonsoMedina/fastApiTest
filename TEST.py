
import psycopg2
import tools.connect as connex



def log_info_id_tramites(arg):
	try:
		list_info = []
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute("""select formulario_id,enviado_at,estado from tramites t where id = {}""".format(int(arg)))
		row=cursor.fetchall()
		return(row[0])
	except Exception as e:
		print(e)
	finally:
		conn.close()


print(log_info_id_tramites('1546')[1])