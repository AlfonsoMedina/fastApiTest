import time
from auto_process import insert_list
from dinapi.sfe import pendientes_sfe_not_pag
from tools.filing_date import capture_full






# se ejecuta cada minuto
def refresh():
	try:	
		print('_____________________________________________________')
		time.sleep(60) # 1 Minuto
		control_process()
		refresh()
	except Exception as e:
		pass


def control_process():
	print(f'current time {capture_full()}')
	captura_pendientes()

	
def captura_pendientes():
	list_id = []
	today = time.strftime("%Y-%m-%d")
	for i in pendientes_sfe_not_pag(today):
		try:
			sigla_doc = str(i['tool_tip']).split("-")
			list_id.append(str(i['Id'])+"/"+str(sigla_doc[0]))
		except Exception as e:
			pass
	print(list_id)
	if list_id != []:
		for i in list_id:
			params = str(i).split('/')
			print('doc pendiente '+str(params[0]))
			#insert_list(str(params[0]),str(params[1]))
			time.sleep(1)	





































refresh()