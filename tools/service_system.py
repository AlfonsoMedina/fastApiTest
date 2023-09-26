from ast import Try
from base64 import encode
import base64
import psycopg2








####################################################################################################################################

#Conexion con la tabla parametros
def config_parametro(id):
    params = []
    try:
        conn = psycopg2.connect(host = "192.168.50.216",user = "user_app_recepcion",password="bEL19ZBN1mQUxSRxYc2NV3EL9f",database="db_sfe_presencial")
        cursor = conn.cursor()
        cursor.execute("select * from parametros where id = "+id)
        row=cursor.fetchall()
        for i in row:
            params.append({"id":i[0],"origen":i[1],"descripcion":i[2],"valor1":i[3],"valor2":i[4],"valor3":i[5],"valor4":i[6],"valor5":i[7],"estado":i[8],"sistema_id":i[9]})
        return(params[0])          
    except Exception as e:
        print(e)
    finally:
        conn.close()

#print(config_parametro('49')['valor1'])




