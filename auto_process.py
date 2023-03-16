import time
from time import sleep
from dinapi.sfe import pendientes_sfe


list_id = []
def timer(step):
	print('MEA On')
	i = 0
	while i < step:
		for i in range(step):
			check_date()
			sleep(30)
			if(i == 10):
				i=0



def check_date():
	for i in pendientes_sfe('2023-03-14'):
		try:
			list_id.append(i['Id'])
		except Exception as e:
			pass
	if list_id != []:
		for n in list_id:	
			insert_list(n)


def insert_list(arg):
	#evaluar tipo de documento para insertar
	print('insertar lista =>' + str(arg))



















timer(60) # Inicio


	

