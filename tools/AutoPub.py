import time
from time import sleep
import psycopg2
from redpi.Clasificados import edicion_cont, insertar_edicion, previa_edicion
from tools.connect import host, user, password, database, host_SFE_conn, user_SFE_conn, password_SFE_conn, database_SFE_conn,host_centura, user_centura, password_centura, database_centura



def timer(step):
    print('Proceso de publicacion automatica...............')
    H = str(time.strftime("%H:%M:%S"))
    i = 0
    while i < step:
        for i in range(step):
            H = str(time.strftime("%H:%M:%S"))
            if(H == '19:30:01'):
##############################################################################################################                
                check_date()
##############################################################################################################
            sleep(1)
            if(i == 10):
                i=0

def check_date():
    try:
        msg = ''
        dia = str(time.strftime("%Y-%m-%d"))
        dbfecha = '0000-00-00'
        conn = psycopg2.connect(
            host=str(host).replace("('","").replace("',)",""),
            user=str(user).replace("('","").replace("',)",""),
            password=str(password).replace("('","").replace("',)",""),
            database=str(database).replace("('","").replace("',)","")
        )
        cursor = conn.cursor()
        cursor.execute("select fecha_publicacion  from publicaciones_publicaciones where fecha_publicacion  = '"+dia+"'")
        row=cursor.fetchall()
        for i in row:
            if(str(i[0])==str(dia)):
                dbfecha = str(i[0])    
        if(str(dia) == dbfecha):
            print('publicado por el usuario')
            msg = 'publicado por el usuario: '+ str(dia)
        else:
######################################################################################################
                                    #zona de ejecucion
            try:
                # 1) definir la edicion (consultar edicion para incrementar)
                num_edicion = int(edicion_cont())+1

                sleep(2) # Pausa

                # 2) actualizar lista de clasificados segun fecha
                previa_edicion(dia)

                sleep(2) # Pausa

                # 3) Publicar  (ver como formato de la fecha)
                insertar_edicion(dia,str(num_edicion))

            except Exception as e:
                pass
            # print(num_edicion)
            print('publicado por el sistema')
            print('Publicacion de ' + dia + ' edicion N° ' + str(num_edicion) )
            msg = 'publicado por el sistema: '+ str(dia)

######################################################################################################            
                       
        return(msg)
    except Exception as e:
        print(e)
    finally:
        conn.close()

timer(60) # Inicio


'''
##############################################################################################################
Hora por 24H
    time.strftime("%H:%M:%S") #Formato de 24 horas

Hora por 12H
    time.strftime("%I:%M:%S") #Formato de 12 horas


Fecha formato: dd/mm/yyyy
    print (time.strftime("%d/%m/%y"))
    

Las siguientes directivas se pueden utilizar en el formato de cadena:

%a - Nombre del día de la semana
%A - Nombre del día completo
%b - Nombre abreviado del mes
%B - Nombre completo del mes
%c - Fecha y hora actual
%d - Día del mes
%H - Hora (formato 24 horas)
%I - Hora (formato 12 horas)
%j - Día del año
%m - Mes en número
%M- Minutos
%p - Equivalente de AM o PM
%S - Segundos
%U - Semana del año (domingo como primer día de la semana)
%w - Día de la semana
%W - Semana del año (lunes como primer día de la semana)
%x - Fecha actual
%X - Hora actual
%y - Número de año (14)
%Y - Numero de año entero (2014)
%Z - Zona horaria


'''