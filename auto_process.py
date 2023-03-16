"""
Administrador de recepcion MEA
"""
import string
import time
from time import sleep
from dinapi.sfe import pendientes_sfe
import tools.connect as connex

list_id = []
def timer(step):
	print('M.E.A On')
	i = 0
	while i < step:
		for i in range(step):
			check_date()
			sleep(int(connex.MEA_TIEMPO_ACTUALIZACION))
			if(i == 10):
				i=0

def check_date(): # Captura lista pendiente
	today = time.strftime("%Y-%m-%d")
	for i in pendientes_sfe(today):
		try:
			if i['estado'] == 7:
				list_id.append(str(i['Id'])+"-"+str(i['formulario_id']))
		except Exception as e:
			pass
	#print(list_id)	
	if list_id != []:
		for n in list_id:
			params = str(n).split('-')
			insert_list(params[0],params[1])

def insert_list(arg0:string,arg1:string): # Insercion segun tipo de formulario
	if arg1 == "68":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)

	if arg1 == "70":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)

	if arg1 == "69":
		print(arg0 + " Procesado...") 
		list_id.remove(arg0+"-"+arg1)

	if arg1 == "36":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)

	if arg1 == "39":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)

	if arg1 == "42":
		print(arg0 + " Procesado...")
		list_id.remove(arg0+"-"+arg1)

























timer(60) 


	

