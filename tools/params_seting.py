from ast import Try
from base64 import encode
import base64
import psycopg2


####################################################################################################################################

#Conexion con la tabla parametros
def get_parametros():
	params = []
	try:
		conn = psycopg2.connect(
			host = "192.168.50.216",
			user = "user_app_recepcion",
			password="user_app_recepcion-202201!",
			database="db_sfe_presencial"
		)
		cursor = conn.cursor()
		cursor.execute("select * from parametros")
		row=cursor.fetchall()
		for i in row:
			params.append({'id':i[0],
							'origen':i[1],
							'descripcion':i[2],
							'valor1':i[3],
							'valor2':i[4],
							'valor3':i[5],
							'valor4':i[6],
							'valor5':i[7],
							'estado':i[8],
							'sistema_id':i[9]})
		return(params)          
	except Exception as e:
		print(e)
	finally:
		conn.close()

def get_parametros_mea():
	params = []
	try:
		conn = psycopg2.connect(
			host = "192.168.50.216",
			user = "user_app_recepcion",
			password="user_app_recepcion-202201!",
			database="db_sfe_presencial"
		)
		cursor = conn.cursor()
		cursor.execute("select * from parametros")
		row=cursor.fetchall()
		for i in row:
			if i[1] == 'MEA':
				params.append({'id':i[0],
							'origen':i[1],
							'descripcion':i[2],
							'valor1':i[3],
							'valor2':i[4],
							'valor3':i[5],
							'valor4':i[6],
							'valor5':i[7],
							'estado':i[8],
							'sistema_id':i[9]})
		return(params)          
	except Exception as e:
		print(e)
	finally:
		conn.close()

def get_parametro(id):
	params = []
	try:
		conn = psycopg2.connect(
			host = "192.168.50.216",
			user = "user_app_recepcion",
			password="user_app_recepcion-202201!",
			database="db_sfe_presencial"
		)
		cursor = conn.cursor()
		cursor.execute("select * from parametros where id = "+id)
		row=cursor.fetchall()
		for i in row:
			params.append({'id':i[0],
							'origen':i[1],
							'descripcion':i[2],
							'valor1':i[3],
							'valor2':i[4],
							'valor3':i[5],
							'valor4':i[6],
							'valor5':i[7],
							'estado':i[8],
							'sistema_id':i[9]})
		return(params)          
	except Exception as e:
		print(e)
	finally:
		conn.close()

def upDate_parametro(param_id:int,origen:str,descripcion:str,valor1:str,valor2:str,valor3:str,valor4:str,valor5:str,estado:int,sistema_id:int):
	try:
		conn = psycopg2.connect(
					host = "192.168.50.216",
					user = "user_app_recepcion",
					password="user_app_recepcion-202201!",
					database="db_sfe_presencial"
				)
		cursor = conn.cursor()
		cursor.execute("UPDATE public.parametros SET origen='"+origen+"',descripcion='"+descripcion+"',valor1='"+valor1+"',valor2='"+valor2+"',valor3='"+valor3+"',valor4='"+valor4+"',valor5='"+valor5+"',estado=0,sistema_id=0 WHERE id="+str(param_id))
		cursor.rowcount
		conn.commit()
		conn.close()
		return(get_parametro(str(param_id)))
	except Exception as e:
		return(False)

