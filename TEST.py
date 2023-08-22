
import psycopg2
from tools.connect import db_host, db_user, db_password, db_database, hostCJ, userCJ, passwordCJ, databaseCJ, host_SFE_conn, user_SFE_conn, password_SFE_conn, database_SFE_conn,host_centura, user_centura, password_centura, database_centura


# Lista de clasificados por numero de edicion
# select detalle_publicacion_id from publicacion_detalle_clasificado where publicacion_id = 3056 

# Lista de clasificados con todos sus datos
# select * from detalle_clasificado where id in ()


class getClasificados():

    def edicion(self,fecha):
        try:
            conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
            cursor = conn.cursor()
            cursor.execute(f"select id from publicaciones_publicaciones where fecha_publicacion = '{fecha}' ")    
            row=cursor.fetchall()
            for i in row:
                return(i[0])
        except Exception as e:
            print(e)
        finally:
            conn.close()
    
    def listado(self,edit):
        try:
            list = []
            conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
            cursor = conn.cursor()
            cursor.execute(f"select detalle_publicacion_id from publicacion_detalle_clasificado where publicacion_id = {edit}")    
            row=cursor.fetchall()
            for i in row:
                list.append(i[0])
            return(str(list).replace("[","").replace("]",""))
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def detalles(self,list_id):
        try:
            list_details = []
            conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
            cursor = conn.cursor()
            cursor.execute(f"select * from detalle_clasificado where id in ({list_id})")    
            row=cursor.fetchall()
            for i in row:
                list_details.append(i)
            return(list_details)
        except Exception as e:
            print(e)
        finally:
            conn.close()


data = getClasificados()

edit_Nbr = data.edicion('2023-08-14')

list_post = data.listado(edit_Nbr)

data_list = data.detalles(list_post)