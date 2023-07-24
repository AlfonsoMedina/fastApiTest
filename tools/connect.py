from tools.service_system import config_parametro

########################MEA########################################
MEA_TIEMPO_ACTUALIZACION = config_parametro('62')['valor2']
MEA_SFE_FORMULARIOS_ID_tipo = config_parametro('60')['valor3']
MEA_SFE_FORMULARIOS_ID_estado = config_parametro('60')['valor4']
MEA_SFE_FORMULARIOS_ID_Origin = config_parametro('64')['valor2']
MEA_PERIODO_RECEPCION_userId = config_parametro('63')['valor5']
MEA_PERIODO_RECEPCION_horaIn = config_parametro('63')['valor3']
MEA_PERIODO_RECEPCION_horaOut = config_parametro('63')['valor4']
MEA_ADJUNTOS_DESTINO_location = config_parametro('61')['valor3']
MEA_ADJUNTOS_DESTINO_REG_REN = config_parametro('61')['valor4']
MEA_IPAS_DESTINO = config_parametro('59')['valor2']
WORKING_DAY_AND_TIME = config_parametro('63')['valor3']
MEA_ACUSE_FORMULARIO = config_parametro('76')['valor2']
MEA_DB_ORIGEN_host = config_parametro('58')['valor2']
MEA_DB_ORIGEN_user = config_parametro('58')['valor3']
MEA_DB_ORIGEN_password = config_parametro('58')['valor4']
MEA_DB_ORIGEN_database = config_parametro('58')['valor5']
MEA_OFICINA_ORIGEN_user = config_parametro('64')['valor5']
MEA_OFICINA_ORIGEN_FULL_VIEW = config_parametro('64')['valor4']
MEA_OFICINA_ORIGEN_cap = config_parametro('64')['valor3']


###################################################################

#Base de datos PUBLICACIONES posgresSql v14 
#db_host = '192.168.50.215'
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
#hostME = '192.168.50.215'
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
ipas_sprint = config_parametro('49')['valor1']

#                                     192.168.50.182
ipas_produccion_A = config_parametro('50')['valor1']

#                                     192.168.50.183
ipas_produccion_B = config_parametro('51')['valor1']

#                                     192.168.50.184
ipas_produccion_C = config_parametro('52')['valor1']

ipas_produccion_patent = config_parametro('53')['valor1']
ipas_produccion_disenio = config_parametro('54')['valor1']

###################################################################

#pagos SFE
host_SFE_conn = 'pgsql-sprint.dinapi.gov.py'
user_SFE_conn = 'user-sprint'
password_SFE_conn ='user-sprint--201901'
database_SFE_conn = 'db_sfe_production'
'''
###################################################################
#host_SFE_conn = '192.168.50.219'
#user_SFE_conn = 'user-developer'
#password_SFE_conn ='user-developer--201901'
#database_SFE_conn = 'db_sfe_production'

host_SFE_conn = MEA_DB_ORIGEN_host
user_SFE_conn = MEA_DB_ORIGEN_user
password_SFE_conn = MEA_DB_ORIGEN_password
database_SFE_conn = MEA_DB_ORIGEN_database
'''

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
###################################################################
#Campo respuesta
TRAMITE_REG = """select t.id,t.fecha,t.formulario_id,f.nombre as nombre_formulario ,t.estado as estado_id,case when t.estado =7 then 'Enviado' when t.estado =8 then 'Recepcionado' end estado_desc,
						to_char(t.created_at,'yyyy-mm-dd hh24:mi:ss')created_at,to_char(t.updated_at,'yyyy-mm-dd hh24:mi:ss')updated_at,t.respuestas,t.costo,t.usuario_id, t.deleted_at,
						t.codigo,t.firmado_at,to_char(t.pagado_at,'yyyy-mm-dd hh24:mi:ss') as pagado_at,t.expediente_id,t.pdf_url,to_char(t.enviado_at,'yyyy-mm-dd hh24:mi:ss') as enviado_at,
						to_char(t.recepcionado_at,'yyyy-mm-dd hh24:mi:ss') as recepcionado_at,t.nom_funcionario,t.pdf,t.expediente_afectado,t.notificacion_id,t.expedientes_autor,t.autorizado_por_id,u.nombre as nombre_agente,pa.numero_agente,
						u.email as email_agente,pa.celular as telefonoAgente,pa.domicilio_agpi,t.nom_funcionario as funcionario_autorizado 
						from tramites t join formularios f on t.formulario_id  = f.id  
						join usuarios u on u.id = t.usuario_id  
						join perfiles_agentes pa on pa.usuario_id = u.id         
						where t.id = {};"""
###################################################################
#Consulta ultimo dia de proceso
LAST_DAY_PROCESS = """select  fec_proceso from dia_proceso order by fec_proceso desc limit 1"""

LAST_NUMBER = """select  num_acta_ultima from dia_proceso order by fec_proceso desc limit 1"""

CLOSE_PROCESS_DATE = """UPDATE public.dia_proceso SET ind_atencion_comp='S', ind_recepcion_comp='S' WHERE fec_proceso='{}';"""

OPEN_PROCESS_DATE = """INSERT INTO public.dia_proceso
(fec_proceso, num_acta_primera, num_acta_ultima, ind_atencion_comp, ind_recepcion_comp, fec_recepcion_comp, ind_captura_comp, fec_captura_comp, ind_digitaliz_comp, fec_digitaliz_comp, ind_clasific_comp, fec_clasific_comp)
VALUES('{}', {}, {}, 'N', 'N', NULL, 'N', NULL, 'N', NULL, 'N', NULL);"""

#reglas_notificacion
email_user_notas_status_name = """select email_user,notas,status_name from reglas_notificacion where status_cod = '{}'"""
usuario_reglas_notificacion = """select usuario FROM public.reglas_notificacion WHERE status_cod='{}'"""
create_all_group = """select usuario from reglas_notificacion"""

#reglas_me
exp_ri_reglas_me = """select exp_ri from reglas_me where tipo_escrito = '{}'"""
###################################################################
#MSG CORREO AGENTE

msg_body_mail = '''Su solicitud de REGISTRO/RENOVACIÓN ha ingresado satisfactoriamente a la Dirección Nacional de Propiedad Intelectual – DINAPI, bajo los siguientes datos:  (se adjunta archivo PDF de su solicitud).\n Seguimos Mejorando para brindarte un servicio de calidad. \n --- \n Saludos cordiales,\n DIRECCIÓN NACIONAL DE PROPIEDAD INTELECTUAL''' 

msg_body_ESC = '''Su solicitud de ESCRITO ha ingresado satisfactoriamente a la Dirección Nacional de Propiedad Intelectual – DINAPI, bajo los siguientes datos:  (se adjunta archivo PDF de su solicitud).\n Seguimos Mejorando para brindarte un servicio de calidad. \n --- \n Saludos cordiales,\n DIRECCIÓN NACIONAL DE PROPIEDAD INTELECTUAL''' 

"""
http://192.168.50.194:8050/Stat/stat?type=loggedUser

"""


            #JCENTURION
            #IMATTO
            #IPAS TEST - 50.155 (glassfish)
            # nombre de archivo en ves de E poner PY













































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

'''
prod_server='192.168.50.195' 
prod_user='ADMIN' 
prod_password='ipas4PY$' 
prod_database='MARCAS_PY
'''



