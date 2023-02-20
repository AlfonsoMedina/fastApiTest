from urllib import request
from fastapi import FastAPI
from pydantic import BaseModel
from publicaciones.pub_2023 import convert_fecha_hora, orden_emitida, orden_emitida_exp
from redpi.Clasificados import consulta_Fop, consulta_caja, consulta_sfe, no_enviado_sfe
from wipo.ipas import Insert_Action, fetch_all_do_edoc_nuxeo, fetch_all_officdoc_nuxeo, get_agente, mark_getlist, mark_getlistReg #pip install "fastapi[all]"
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi


description = """
Version 2023 
## Métodos para proceso de clasificados REDPI SprintV2  
Engineer in charge ***W. Alfonso Medina***

las rutas reciben un objeto **JSON** como parametro y retornar un objeto **JSON**.
"""

app = FastAPI()

origins = ["*"]

#http://192.168.71.189:3000 //bloqueo por aplicacion

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"], #['*']
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Api REDPI",
        version="3.0.0",
        description=description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://sfe.dinapi.gov.py/assets/home/dinapilogo4-5eef9860ea6bb48707a76c1d97e2438b195bd72171233946a40177bb27cc7f11.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

#https://sfe.dinapi.gov.py/assets/home/dinapilogo4-5eef9860ea6bb48707a76c1d97e2438b195bd72171233946a40177bb27cc7f11.png	
#https://sfe.dinapi.gov.py/assets/logo_sprint-85d552f35942e4152f997bb4875b6283a05d34f7b9b7b6126e84414c924bb041.png

class por_fecha(BaseModel):
	fecha:str = ""
class por_expediente(BaseModel):
	expediente:str = ""

@app.post('/api/sfe', tags=["Pagos SFE"], summary="#", description="Pagos desde sfe por fecha")
def sfe_consulta(item: por_fecha):
	try:
		return(consulta_sfe(item.fecha))
	except Exception as e:
		return e
	else:
		pass
	finally:
		pass

@app.post('/api/caja', tags=["Pagos CAJA"], summary="#", description="Pagos desde caja DINAPI por fecha")
def caja_consulta(item: por_fecha):
	try:
		return(consulta_caja(item.fecha))
	except Exception as e:
		return 'Error en (/api/caja)'
	else:
		pass
	finally:
		pass

@app.post('/api/fop', tags=["form_orden_publicacion"], summary="#", description="Expediente sin inicio y fin ")
def fop_consulta(item:por_expediente):
	try:
		return(consulta_Fop(item.expediente))
	except Exception as e:
		return 'Error en (/api/fop)'
	else:
		pass
	finally:
		pass

app.openapi = custom_openapi