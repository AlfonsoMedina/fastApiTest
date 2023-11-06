from zeep import Client, AsyncClient
import zeep
from io import open
import tools.connect as conn_serv
from tools.service_system import config_parametro
import tools.connect as connex




try:
	mark_service = conn_serv.MEA_IPAS_DESTINO
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')

try:
	Patents_service = conn_serv.ipas_produccion_patent
	wsdlPatente = Patents_service + "/IpasServices/IpasServices?wsdl"
	clientPatents = Client(wsdlPatente)
except Exception as e:
	print('Error de coneccion  IPAS Patentes!!')

try:
	disenio_service = conn_serv.ipas_produccion_disenio 
	wsdlDisenio = disenio_service + "/IpasServices/IpasServices?wsdl"
	clientDisenio = Client(wsdlDisenio)
except Exception as e:
	print('Error de coneccion  IPAS Diseño!!')



def get_agente(arg):
    code = {
           "arg0": {
             "agentCode": {
               "doubleValue": arg
             }
           }
         }
    
    return clientMark.service.AgentRead(**code)



print(get_agente('400'))