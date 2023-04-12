from tools.service_system import config_parametro

########################MEA########################################
MEA_TIEMPO_ACTUALIZACION = config_parametro('62')['valor2']
MEA_DB_ORIGEN_host = config_parametro('58')['valor2']
MEA_SFE_FORMULARIOS_ID_tipo = config_parametro('60')['valor3']
MEA_SFE_FORMULARIOS_ID_estado = config_parametro('60')['valor4']
MEA_SFE_FORMULARIOS_ID_Origin = config_parametro('60')['valor5']
MEA_PERIODO_RECEPCION_userId = config_parametro('63')['valor5']
MEA_PERIODO_RECEPCION_horaIn = config_parametro('63')['valor3']
MEA_PERIODO_RECEPCION_horaOut = config_parametro('63')['valor4']
MEA_ADJUNTOS_DESTINO_location = config_parametro('61')['valor3']

###################################################################

#Base de datos PUBLICACIONES posgresSql v14 
#db_host = '192.168.50.216'
#db_user='user_app_publicacion'
#db_password='user_app_publicacion-202201!'
#db_database='db_publicacion'

###################################################################

#Base de datos PUBLICACIONES posgresSql v14 
db_host = '192.168.50.215'
db_user='user_app_publicacion'
db_password='user_app_publicacion-202201!'
db_database='db_publicacion'

###################################################################

#Base de datos PUBLICACIONES posgresSql v9
#db_host = 'pgsql-sprint.dinapi.gov.py'
#db_user = 'user-sprint'
#db_password ='user-sprint--201901'
#db_database = 'publicaciones'

###################################################################

#Base de datos MESA DE ENTRADA posgresSql v14
hostME = '192.168.50.215'
userME='user_app_recepcion'
passwordME='user_app_recepcion-202201!'
databaseME='db_sfe_presencial'

###################################################################

#Base de datos MESA DE ENTRADA posgresSql v14
#hostME = '192.168.50.216'
#userME='user_app_recepcion'
#passwordME='user_app_recepcion-202201!'
#databaseME='db_sfe_presencial'

###################################################################

#tablas viejas de Mesa de entrada posgresSql v9
#hostME='pgsql-sprint.dinapi.gov.py'
#userME='user-sprint'
#passwordME='user-sprint--201901'
#databaseME='mesa_entrada'

###################################################################

#Base de datos CAJA posgresSql v14 
hostCJ = '192.168.50.215'
userCJ='user_app_caja'
passwordCJ='user_app_caja-202201!'
databaseCJ='db_caja_dinapi'

###################################################################

#ipas Beta
#                                192.168.80.42
ipas_sprint = config_parametro('49')['valor2']

#                                     192.168.50.182
ipas_produccion_A = config_parametro('50')['valor1']

#                                     192.168.50.183
ipas_produccion_B = config_parametro('51')['valor1']

#                                     192.168.50.184
ipas_produccion_C = config_parametro('52')['valor1']

ipas_produccion_patent = config_parametro('53')['valor1']
ipas_produccion_disenio = config_parametro('54')['valor1']

###################################################################
'''
#pagos SFE
host_SFE_conn = 'pgsql-sprint.dinapi.gov.py'
user_SFE_conn = 'user-sprint'
password_SFE_conn ='user-sprint--201901'
database_SFE_conn = 'db_sfe_production'
'''
###################################################################
host_SFE_conn = '192.168.50.219'
user_SFE_conn = 'user-developer'
password_SFE_conn ='user-developer--201901'
database_SFE_conn = 'db_sfe_production'

#centura
host_centura = '192.168.50.231'
user_centura = 'user-developer'
password_centura = 'user-developer--201901'
database_centura = 'centura'

###################################################################
#Pendiente por ID
PENDING = """
select 
id,
fecha,
formulario_id,
estado,
created_at,
updated_at,
respuestas,
costo,
usuario_id,
deleted_at,
codigo,
firmado_at,
pagado_at,
expediente_id,
pdf_url,
to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,
to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,
nom_funcionario,
pdf,
expediente_afectado,
notificacion_id,
expedientes_autor,
autorizado_por_id,
locked_at,
locked_by_id,
tipo_documento_id 
from tramites where id = {}
"""
###################################################################
#Pendientes por fecha
EARRINGS = """
select id,
fecha,
formulario_id,
estado,
created_at,
updated_at,
respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
from tramites where id = {}
"""

"""
http://192.168.50.194:8050/Stat/stat?type=loggedUser

"""















































###################################################################
'''
prod_server='192.168.50.188' 
prod_user='ADMIN' 
prod_password='ipas4PY$' 
prod_database='MARCAS_PY'
'''
###################################################################

'''
prod_server='192.168.80.41' 
prod_user='ADMIN' 
prod_password='ipas4PY$' 
prod_database='MARCAS_PY
'''

###################################################################

prod_server='192.168.50.195' 
prod_user='ADMIN' 
prod_password='ipas4PY$' 
prod_database='MARCAS_PY'



