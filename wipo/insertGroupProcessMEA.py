from zeep import Client
import tools.connect as conn_serv
import zeep


try:
	mark_service = conn_serv.MEA_IPAS_DESTINO
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')

def ProcessGroupAddProcess(processGroupCode,userNbr,processNbr,processType):
	try:
		data = {
				"arg0": {
					"processGroupCode": processGroupCode,
					"userId": {
					"userNbr": {
						"doubleValue": userNbr
					}
					}
				},
				"arg1": {
					"processNbr": {
					"doubleValue": processNbr
					},
					"processType": processType
				}
				}
		return clientMark.service.ProcessGroupAddProcess(**data)        
	except zeep.exceptions.Fault as e:
		return(str(e))