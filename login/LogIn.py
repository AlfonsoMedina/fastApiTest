#from crypt import crypt
from ast import Try
import datetime
import hashlib
from flask import jsonify
import psycopg2
from tools.connect import db_host, db_user, db_password, db_database, hostME, userME, passwordME, databaseME, host_SFE_conn, user_SFE_conn, password_SFE_conn, database_SFE_conn,host_centura, user_centura, password_centura, database_centura


def authentication(user,password):
    try:
        conn = psycopg2.connect(host=hostME,user=userME,password=passwordME,database=databaseME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM public.usuarios_dinapi WHERE usuario = '"+user+"';")    
        row=cursor.fetchall()
        if row == []:
            return({"res":"no_existe_usuario"})
        for i in row:
            if i[3] == i[4]:
                return({"res":"cambia_pass"})
            if i[6] == 'Inactivo':
                return({"res":"Este usuario esta Inactivo"})   
            if i[3] != i[4]:
                if encrypt_win(password) == i[4]:
                    return({"res":{"id":i[0],"full_NAME":i[1]+" "+i[2],"login":i[3],"sys":i[12],"rol":i[14]}})
                else:
                    return({"res":"error_de_pass"})        
        conn.close()
    except Exception as e:
            return(e)

def new_password(user,new_pass, val_new_pass):
    if new_pass == val_new_pass:
        try:
            conn = psycopg2.connect(host=hostME,user=userME,password=passwordME,database=databaseME)
            cursor = conn.cursor()
            cursor.execute("UPDATE public.usuarios_dinapi SET contrasena='"+encrypt_win(new_pass)+"' WHERE usuario = '"+user+"';")
            cursor.rowcount
            conn.commit()
            conn.close()
            return({"res":"true"})
        except Exception as e:
            return('error de conexion')    
    else:    
        return({"res":"false"})

def last_session(arg):
    x = datetime.datetime.now()
    #print(str(x))
    try:
        conn = psycopg2.connect(host=hostME,user=userME,password=passwordME,database=databaseME)
        cursor = conn.cursor()
        cursor.execute("UPDATE public.usuarios_dinapi SET last_session='"+str(x)+"' WHERE usuario='"+str(arg)+"';")
        cursor.rowcount
        conn.commit()
        conn.close()
        return(str('true'))
    except Exception as e:
        return('error de conexion')  

def encrypt_win(password):
    passw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return(passw)

def change_pass(user, act_pass, new_pass, val_pass ):
    try:
        conn = psycopg2.connect(host=hostME,user=userME,password=passwordME,database=databaseME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM public.usuarios_dinapi WHERE usuario = '"+user+"';")    
        row=cursor.fetchall()
        if row == []:
            return(jsonify({"res":"no_existe_usuario"}))
        for i in row:
            if encrypt_win(act_pass) == i[4]: # si pass actual es igual que en base  
                if new_pass != '' or val_pass != '':   
                    if new_pass == val_pass:
                        conn_B = psycopg2.connect(
                            host=str(hostME).replace("('","").replace("',)",""),
                            user=str(userME).replace("('","").replace("',)",""),
                            password=str(passwordME).replace("('","").replace("',)",""),
                            database=str(databaseME).replace("('","").replace("',)","")
                                                )
                        cursor_b = conn_B.cursor()
                        cursor_b.execute("UPDATE public.usuarios_dinapi SET contrasena='"+encrypt_win(new_pass)+"' WHERE usuario = '"+user+"';")
                        cursor_b.rowcount
                        conn_B.commit()
                        conn_B.close()
                    else:
                        return({"res":"los campos deben coincidir"})
                else:
                    return({"res":"Complete ambos campos"})        
            else: # si no es igual que en base 
                return({"res":"contraseña incorrecta"})
        conn.close()
        return({"res":"Cambio exitoso!"})
    except Exception as e:
            return({"res":"error"})    


#def encrypt_linux(password):
#    passw = crypt.crypt(password,'salt')
#    return(passw)

#authentication('AMEDINA','2347079Ma')
#print(change_pass('AMEDINA','1234','456','456'))