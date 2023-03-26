"""
Administrador de recepcion MEA
"""
import string
import time
from time import sleep
from dinapi.sfe import cambio_estado, count_pendiente, format_userdoc, pendiente_sfe, pendientes_sfe
import tools.connect as connex
from wipo.function_for_reception_in import insert_user_doc_escritos


"""
def timer(step):
	print('M.E.A Online............')
	i = 0
	while i < step:
		for i in range(step):
			check_date()
			#print('.')
			if(i == 10):
				i=0
		sleep(int(connex.MEA_TIEMPO_ACTUALIZACION))		

def check_date(): # Captura lista pendiente
	today = time.strftime("%Y-%m-%d")
	for i in pendientes_sfe(today,0):
		try:
			if i['estado'] == 7:
				list_id.append(str(i['Id'])+"-"+str(i['tip_doc']))
		except Exception as e:
			pass
	if list_id != []:
		for n in list_id:
			params = str(n).split('-')
			insert_list(params[0],params[1])


"""

list_id = []
def listar():
	print('crear lista')
	check_date() # Captura lista pendiente
	time.sleep(int(connex.MEA_TIEMPO_ACTUALIZACION))
	insertar()

def insertar():
	time.sleep(int(connex.MEA_TIEMPO_ACTUALIZACION)/2)
	print('ordenar lista')
	time.sleep(1)
	list_id.sort()
	#print(list_id)
	if list_id != []:
		for i in list_id:
			params = str(i).split('-')
			print('insertar docs '+str(params[0]))
			insert_list(str(params[0]),str(params[1]))
		time.sleep(2)
	listar()

def check_date(): # Captura lista pendiente
	today = time.strftime("%Y-%m-%d")
	for i in pendientes_sfe(today,0):
		try:
			if i['estado'] == 7:
				list_id.append(str(i['Id'])+"-"+str(i['tip_doc']))
		except Exception as e:
			pass

def insert_list(arg0:string,arg1:string): # Insercion segun tipo de formulario
	if arg1 == "68":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)

		cambio_estado(arg0)

	if arg1 == "70":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)

		cambio_estado(arg0)

	if arg1 == "69":
		print(arg0 + " Procesado...") 
		list_id.remove(arg0+"-"+arg1)

		cambio_estado(arg0)

	if arg1 == "36":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)

		cambio_estado(arg0)

	if arg1 == "39":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

	if arg1 == "42":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

	if arg1 == "95":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

	if arg1 == "3":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

	if arg1 == "4":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

	if arg1 == "27":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)
		cambio_estado(arg0)

#listar()



