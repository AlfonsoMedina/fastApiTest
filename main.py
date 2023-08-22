
from urllib import request
from fastapi import FastAPI
from pydantic import BaseModel
from login.LogIn import authentication, new_password
from publicaciones.pub_2023 import convert_fecha_hora, orden_emitida, orden_emitida_exp
from redpi.Clasificados import checking_payment_suport, consulta_Fop, consulta_Fop_expediente, consulta_Fop_fecha, consulta_caja, consulta_sfe, edicion_cont, existexp, full_package, getClasificados, insert_clasificado, insert_dia_proceso, insert_form_orden_publicacion, insertar_edicion, no_enviado_sfe, previa_edicion, processToDate, select_dia_proceso, update_dia_proceso, update_inicio_fin, update_inicio_fin_soporte, user_admin_redpi
from tools.data_format import format_fecha_mes_hora
from wipo.ipas import Insert_Action, Insert_Action_soporte, fetch_all_do_edoc_nuxeo, fetch_all_officdoc_nuxeo, fetch_all_user_mark, get_agente, mark_getlist, mark_getlistReg #pip install "fastapi[all]"
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from tools.revista import crear_pub
#from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


description = """
Version 2023 
## Métodos para proceso de clasificados REDPI SprintV2  
Engineer in charge ***W. Alfonso Medina***

las rutas reciben un objeto **JSON** como parametro y retornar un objeto **JSON**.
"""

app = FastAPI()

#app.mount("/static", StaticFiles(directory="static"), name="static")

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
class process_day(BaseModel):
	fecha:str = "" 
	sfe:str = ""
	caja:str = ""
	reg:str = ""
	ren:str = ""
	total:str = ""
	process:str = ""
class pub_day(BaseModel):
	fecha:str = "" 
	edicion:str = ""
class user_mark(BaseModel):
	login:str = "" 
class user_exp(BaseModel):
	exp:str = ""
	user:str = "" 
class sop_in(BaseModel):
	exp:str = ""
	pago:str = "" 
class user_pwr(BaseModel):
	user:str = ""
	pwr:str = ""
class user_pwr_new(BaseModel):
	user:str = ""
	npass:str = ""
	vnpass:str = ""
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

@app.post('/api/packageToDay', tags=["Lista de pagos de caja y de SFE con su relacion en form_orden_publicacion"], summary="#", description="Conjunto de datos para llenar vista ")
def packageToDay(fecha):
	return(full_package(fecha))

@app.post('/api/processToDate', tags=["Procesar fecha"], summary="#", description="consulta pagos, inserta clasificados, actualiza form, inserta en ipas")
def process_To_Date(fecha):
	processToDate(fecha)
	return('end')

@app.post('/api/diaproceso_nuevo', tags=["Proceso nuevo"], summary="#", description="")
def select_back_process():
	return(select_dia_proceso())

@app.post('/api/diaproceso_nuevo_insert', tags=["dia proceso nuevo insert"], summary="#", description="")
def insertar_nuevo_proceso(item:process_day):
	try:
		insert_dia_proceso(item.fecha,item.sfe,item.caja,item.reg,item.ren,item.total,item.process) 
		return('ok')
	except Exception as e:
		pass

#Actualiza el ultimo dia de proceso para la vista 
@app.post('/api/updatediaproceso_nuevo', tags=["update dia proceso nuevo"], summary="#", description="")
def update_nuevo_proceso(item:process_day):
	try:
		update_dia_proceso(item.fecha,item.sfe,item.caja,item.reg,item.ren,item.total,item.process) 
		return('ok')
	except Exception as e:
		pass	

@app.post('/api/edicionnumber', tags=[""], summary="#", description="")
def numberedition():
	return(edicion_cont())

@app.post('/api/admin_soporte', tags=[""], summary="#", description="")
def user_admin():	
	return(user_admin_redpi())

@app.post('/api/user_mark', tags=[""], summary="#", description="")
def fetchallusermark(item:user_mark):
	try:	
		return({
		"USER_ID":str(fetch_all_user_mark(item.login)[0].sqlColumnList[0].sqlColumnValue),
		"LOGIN":str(fetch_all_user_mark(item.login)[0].sqlColumnList[1].sqlColumnValue)
		}
		)
	except Exception as e:
		return({"error":"undefine"})

@app.post('/api/publicar', tags=["update dia proceso nuevo"], summary="#", description="")
def publicarhoy(item:pub_day):
	return(insertar_edicion(item.fecha,item.edicion))

@app.post('/api/admin_soporte', tags=[""], summary="#", description="")
def user_admin():	
	return(user_admin_redpi())

@app.post('/api/ultima_sesion_view', tags=["Fecha y hora"], summary="#", description="")
def ultima_sesion():
	return(format_fecha_mes_hora())

@app.post('/api/pubhoy', tags=["Clasificados por fecha"], summary="#", description="Devuelve una lista de clasificados segun la fecha indicada")
def pubtoday(item:por_fecha):
	return previa_edicion(item.fecha)

@app.post('/api/casificado_pdf', tags=["Crear PDF"], summary="#", description="Crea la revista de clasificados como un archivo PDF")
def pub_pdf_revista(fecha):
	return(crear_pub(fecha))

@app.get("/api/pdf_redpi", tags=["Consultar PDF"], summary="#", description="Consulta una revista segun su fecha de publicacion")
def get_pdf_redpi(fileName):
	return FileResponse(f'static/clasificados_{fileName}.pdf')

@app.post('/api/soporteExp', tags=["Consulta expediente"], summary="#", description="")
def soporte_exp(item:por_expediente):
	return(consulta_Fop_expediente(item.expediente))

@app.post('/api/soporteFecha', tags=["Consulta por fecha"], summary="#", description="")
def soporte_fecha(item:por_fecha):
	return(consulta_Fop_fecha(item.fecha))

@app.post('/api/indetalleclasificado', tags=["Inserta clasificado por soporte"], summary="#", description="")
def insert_clas(item:user_exp):
	return(insert_clasificado(item.exp,item.user))	

@app.post('/api/iniciofin', tags=["UpDate form para soporte"], summary="#", description="")
def update_fop_inicio(item:sop_in):
	return update_inicio_fin_soporte(item.exp,item.pago)

class insert_ipas(BaseModel):
	exp:str = ""
	pago:str = ""
	userid:str = ""
	nota:str = ""
	evento:str = ""
@app.post('/api/insert_ipas', tags=["Isert IPAS para soporte"], summary="#", description="")
def insert_redpi(item:insert_ipas):	
	Insert_Action(item.exp,item.pago,'4',item.nota,item.evento)
	return('573 ok')

@app.post('/api/cargar_nuevo_form_op', tags=["Isert en form_orden_publicacion"], summary="#", description="")
def nuevo_en_form(item:por_expediente):
	if str(existexp(item.expediente)) == 'None':
		print(insert_form_orden_publicacion(item.expediente))
		return('true')
	else:	
		return('false')

@app.post('/api/admin_soporte', tags=["User soporte"], summary="#", description="")
def user_admin():
	return(user_admin_redpi())

@app.post('/api/autentication', tags=["Auth"], summary="#", description="")
def auth(item:user_pwr):
	return(authentication(item.user,item.pwr))

@app.post('/api/change_autentication', tags=["change_autentication"], summary="#", description="")
def change_auth(item:user_pwr_new):
	return(new_password(item.user,item.npass,item.vnpass))

@app.post('/api/checking_payment_suport', tags=["Suport payment checking"], summary="#", description="Chekar pago para soporte REDPI")
def checkingpaymentsuport(exp):
	return(checking_payment_suport(exp))

class in_ipas_method(BaseModel):
	exp:str = ""
	pago:str = ""
	userid:str = ""
	nota:str = ""
	evento:str = ""
@app.post('/api/insert_ipas_soporte', tags=["Insert Action IPAS"], summary="#", description="Insertar evento en ipas usando el metodo InsertAction ")
def insert_action_sop(item:in_ipas_method):
	return(Insert_Action_soporte(item.exp,item.pago,item.userid,item.nota,item.evento))

@app.get('/api/post_view', tags=["Post"], summary="#", description="Vista de clasificados")
def insert_action_sop(date_post):
	data = getClasificados()
	edit_Nbr = data.edicion(date_post)
	list_post = data.listado(edit_Nbr)
	data_list = data.detalles(list_post)	
	return(data_list)





















app.openapi = custom_openapi