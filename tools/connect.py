from tools.service_system import config_parametro


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
hostCJ = '192.168.50.216'
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
#pagos SFE
host_SFE_conn = 'pgsql-sprint.dinapi.gov.py'
user_SFE_conn = 'user-sprint'
password_SFE_conn ='user-sprint--201901'
database_SFE_conn = 'db_sfe_production'

###################################################################
#centura
host_centura = '192.168.50.231'
user_centura = 'user-developer'
password_centura = 'user-developer--201901'
database_centura = 'centura'


###################################################################
'''
prod_server='192.168.50.188' 
prod_user='ADMIN' 
prod_password='ipas4PY$' 
prod_database='MARCAS_PY'
'''
###################################################################

prod_server='192.168.80.41' 
prod_user='ADMIN' 
prod_password='ipas4PY$' 
prod_database='MARCAS_PY'



