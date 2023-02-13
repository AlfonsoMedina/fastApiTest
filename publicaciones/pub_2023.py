from ast import Return
from base64 import encode
from datetime import date, timedelta
from dis import code_info
from time import sleep
from click import File
from zeep import Client
from io import BytesIO, FileIO
from io import open
import tools.connect as conn_serv


try:
	mark_service = conn_serv.ipas_sprint
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')

def orden_emitida(fecha,user_id):
	emitidas = {
				"arg0": {
					"criteriaProcessByAction": {
					"actionDateFrom": {
						"dateValue": str(fecha)
					},
					"actionDateTo": {
						"dateValue": str(fecha)
					},
					"captureUserId": {
						"userNbr": {
						"doubleValue": str(user_id)
						}
					}
					}
				},
				"arg1": {
					"doubleValue": ""
				}
			}
	data = clientMark.service.ProcessGetList(**emitidas)
	return(data)

def orden_emitida_exp(fileNbr,fileSeq,fileSeries,fileType):
	data_exp = {
			"arg0": {
				"criteriaProcessByOfficedoc": {
				"topFileId": {
					"fileNbr": {
					"doubleValue": fileNbr
					},
					"fileSeq": fileSeq,
					"fileSeries": {
					"doubleValue": fileSeries
					},
					"fileType": fileType
				}
				}
			},
			"arg1": {
				"doubleValue": ""
			}
		}
	data = clientMark.service.ProcessGetList(**data_exp)
	return(data)

def convert_fecha_hora(data):
	date_fullE = str(data).split(" ")
	fecha_fullE = date_fullE[0].split("-")
	fecha_formatE = fecha_fullE[2]+"/"+fecha_fullE[1]+"/"+fecha_fullE[0]
	hora_puntoE = date_fullE[1].split(".")
	hora_guionE = hora_puntoE[0].split("-")
	return(str(fecha_formatE+" "+str(hora_guionE[0])))


#busqueda por expediente  ProcessGetList
'''
{
  "arg0": {
    "criteriaProcessByOfficedoc": {
      "topFileId": {
        "fileNbr": {
          "doubleValue": 22105981
        },
        "fileSeq": "PY",
        "fileSeries": {
          "doubleValue": 2022
        },
        "fileType": "M"
      }
    }
  },
  "arg1": {
    "doubleValue": ""
  }
}

'''

#En espera publicaciones por fecha ProcessGetList
'''
{
  "arg0": {
    "criteriaProcessByAction": {
      "captureUserId": {
        "userNbr": {
          "doubleValue": 89
        }
      }
    },
    "criteriaProcessByStatus": {
      "statusDateFrom": {
        "dateValue": "2023-01-20"
      },
      "statusDateTo": {
        "dateValue": "2023-01-24"
      }
    }
  },
  "arg1": {
    "doubleValue": ""
  }
}
'''