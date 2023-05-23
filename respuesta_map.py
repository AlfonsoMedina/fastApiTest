from dinapi.sfe import registro_sfe as data

import psycopg2

import tools.connect as connex




################################# start reg ##################################

def nom_titu(arg):
	global_data = []
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute(connex.TRAMITE_REG.format(int(arg)))
		row=cursor.fetchall()
		for i in row[0][8]:

			try:
				if(i['campo'] == 'datospersonales_nombreapellido'): 
					global_data.append(i['valor']) 
				else:
					pass
				
				if(i['campo'] == 'datospersonales_razonsocial'): 
					global_data.append(i['valor'])
				else:
					pass

				if(i['campo'] == 'datospersonalesrenov_nombrerazon'): 
					global_data.append(i['valor'])
				else:
					pass					 
			except Exception as e:
				pass
			
			
			for i in global_data:
				if i == '':
					global_data.remove('')

		return(global_data)
	
	except Exception as e:
		print(e)
	finally:
		conn.close()

def dir_titu(arg):
	global_data = []
	try:
		conn = psycopg2.connect(host = connex.host_SFE_conn,user= connex.user_SFE_conn,password = connex.password_SFE_conn,database = connex.database_SFE_conn)
		cursor = conn.cursor()
		cursor.execute(connex.TRAMITE_REG.format(int(arg)))
		row=cursor.fetchall()
		for i in row[0][8]:

			try:
				if(i['campo'] == 'datospersonales_calle'): 
					global_data.append(i['valor']) 
				else:
					pass
				
				if(i['campo'] == 'datospersonales_direccion'): 
					global_data.append(i['valor'])
				else:
					pass

				if(i['campo'] == 'datospersonalesrenov_calle'):
					global_data.append(i['valor'])
				else:
					pass

				if(i['campo'] == 'actualizacion_calle'): 
					global_data.append(i['valor'])
				else:
					pass									 
			except Exception as e:
				pass
			
			
			for i in global_data:
				if i == '':
					global_data.remove('')

		return(global_data)
	
	except Exception as e:
		print(e)
	finally:
		conn.close()

#print(dir_titu('1584')[0])


################################# End reg ##################################