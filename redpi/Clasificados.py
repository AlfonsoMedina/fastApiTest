from ast import Try
from base64 import encode
import base64
from time import sleep
import time
from zeep import Client
from io import BytesIO
from flask import jsonify
import psycopg2
from datetime import date, timedelta
from wipo.ipas import Fech_All_Exp, Insert_Action_soporte, mark_getlist, mark_read
from tools.data_format import Fecha_atras, signo_format
from datetime import datetime
from tools.connect import db_host, db_user, db_password, db_database, hostCJ, userCJ, passwordCJ, databaseCJ, host_SFE_conn, user_SFE_conn, password_SFE_conn, database_SFE_conn,host_centura, user_centura, password_centura, database_centura

####################################################################################################################################

#Publicacion emitida form_orden_publicacion (sin inicio y fin)
def consulta_Fop(exp):
    orden = []
    try:
        conn = psycopg2.connect(
                                host = '192.168.50.215',
                                user='user_app_publicacion',
                                password='user_app_publicacion-202201!',
                                database='db_publicacion'
        )
        cursor = conn.cursor()
        cursor.execute("select tip_movimiento, to_char(fec_movimiento,'DD/MM/YYYY') as movimiento, tip_solicitud, to_char(fecha_pago,'DD/MM/YYYY') as pago, to_char(fecha_inicio,'DD/MM/YYYY') as fecha_inicio, to_char(fecha_fin,'DD/MM/YYYY') as fecha_fin \n"
                    + "FROM public.form_orden_publicacion \n"
                    + "WHERE num_acta = '"+exp+"' ORDER BY num_acta DESC LIMIT 1")
        row=cursor.fetchall()
        for i in row:
            if(i[4]==None and i[5] == None):
                orden.append({'tipo_movimiento':i[0],'movimiento':i[1],'tipo_solicitud':i[2],'fecha_pago':i[3],'fecha_inicio':i[4],'fecha_fin':i[5]})               
        return(orden)
    except Exception as e:
        print(e)
    finally:
        conn.close()

#Publicacion emitida form_orden_publicacion (con inicio y fin)
def consulta_Fop_out(exp):
    orden_out = []
    try:
        conn = psycopg2.connect(
                                host = '192.168.50.215',
                                user='user_app_publicacion',
                                password='user_app_publicacion-202201!',
                                database='db_publicacion'
        )
        cursor = conn.cursor()
        cursor.execute("select tip_movimiento, to_char(fec_movimiento,'DD/MM/YYYY') as movimiento, tip_solicitud, to_char(fecha_pago,'DD/MM/YYYY') as pago, to_char(fecha_inicio,'DD/MM/YYYY') as fecha_inicio, to_char(fecha_fin,'DD/MM/YYYY') as fecha_fin \n"
                    + "FROM public.form_orden_publicacion \n"
                    + "WHERE num_acta = '"+exp+"' ORDER BY num_acta DESC LIMIT 1")
        row=cursor.fetchall()
        for i in row:
            if(i[4] != None): 
                orden_out.append({'tipo_movimiento':i[0],'movimiento':i[1],'tipo_solicitud':i[2],'fecha_pago':i[3],'fecha_inicio':i[4],'fecha_fin':i[5]})
            if(i[4] == None):
                orden_out.append({'tipo_movimiento':i[0],'movimiento':i[1],'tipo_solicitud':i[2],'fecha_pago':'','fecha_inicio':'','fecha_fin':''})                       
            return(orden_out)
    except Exception as e:
        print(e)
    finally:
        conn.close()

#Pagos SFE enviados
def consulta_sfe(fecha):
    #data_fecha = str(fecha).split("/")
    #fecha_uno = data_fecha[2]+"-"+data_fecha[1]+"-"+data_fecha[0]
    #print(fecha_uno)
    temp = []
    try:
        conn = psycopg2.connect(host = host_SFE_conn,user= user_SFE_conn,password = password_SFE_conn,database = database_SFE_conn)
        cursor = conn.cursor()
        cursor.execute("select pagado_at,  authorization_number , to_char(bancard_transactions.updated_at,'DD/MM/YYYY') as fecha_pago ,status, respuestas \n"
        +" from bancard_transactions left join public.tramites on public.tramites.id = bancard_transactions.payable_id \n" 
        +" where bancard_transactions.status = 1 \n" 
        +" and public.tramites.estado = 7 \n" 
        +" and  public.tramites.formulario_id = 29 \n" 
        + "and enviado_at >= '"+fecha+" 00:59:00.0' and enviado_at <= '"+fecha+" 14:59:00.0'")
        row=cursor.fetchall()
        pagosSFE = []
        for i in row:
            pag_exp = ""
            for x in range(0,len(i[4])):
                if i[4][x]['campo'] == 'marcaredpi_expediente' and i[4][x]['descripcion'] == 'Buscar Solicitud N°':
                    pag_exp = str(str(i[4][x]['valor']))
                    Form_order = consulta_Fop_out(str(str(i[4][x]['valor'])))
            temp.append({'respuesta':i[3]})
            fpago = str(i[2]).split('/')
            format_fecha = fpago[2]+'-'+fpago[1]+'-'+fpago[0]
            try:
                pagosSFE.append({'fecha':i[2],'recibo':i[1],'expediente':pag_exp,'status':i[3],'ftabla':format_fecha,'tipo_movimiento':Form_order[0]['tipo_movimiento'],'movimiento':Form_order[0]['movimiento'],'tipo_solicitud':Form_order[0]['tipo_solicitud'],'fecha_pago':Form_order[0]['fecha_pago'],'fecha_inicio':Form_order[0]['fecha_inicio'],'fecha_fin':Form_order[0]['fecha_fin']})
            except Exception as ex:
                pagosSFE.append({'fecha':i[2],'recibo':i[1],'expediente':pag_exp,'status':i[3],'ftabla':format_fecha,'tipo_movimiento':"",'movimiento':"",'tipo_solicitud':"",'fecha_pago':"",'fecha_inicio':"",'fecha_fin':""})
            
        return(pagosSFE)

    except Exception as e:
        print(e)
    finally:
        conn.close()

#Pagos caja dinapi
def consulta_caja(fecha):
    try:
        pagosCJ = []
        #________________________________________________________
        conn = psycopg2.connect(host =  hostCJ,user =  userCJ,password =  passwordCJ,database =  databaseCJ)
        cursor = conn.cursor()
        #                                                RECIBO,                TASA,                EXPEDIENTE,                                        FECHA_RECIBO
        cursor.execute("select distinct r.num_recibo as RECIBO, dr.tasa_id as TASA, dr.expediente_nro as EXPEDIENTE, to_char(r.fec_recibo,'DD/MM/YYYY') as FECHA_RECIBO \n"
                            + "from public.recibo r left join public.recibo_tipo_tasa rtt on rtt.recibo_id = r.id \n"
                            + "left join public.detalles_recibo dr on dr.recibo_tipo_tasa_id = rtt.id  \n"
                            + "where dr.tasa_id = 80 \n"
                            + "and to_char(r.fec_recibo,'YYYY-MM-DD') like '"+fecha+"';")
        row = cursor.fetchall()
        #________________________________________________________    
        contador = 0
        for i in row:
            Form = consulta_Fop_out(str(i[2]))
            f_pago = str(i[3]).split('/')
            format_fech = f_pago[2]+'-'+f_pago[1]+'-'+f_pago[0] 
            try:
                pagosCJ.append({'fecha':i[3],'recibo':i[0],'expediente':i[2],'status':i[1],'ftabla':format_fech,'tipo_movimiento':Form[0]['tipo_movimiento'],'movimiento':Form[0]['movimiento'],'tipo_solicitud':Form[0]['tipo_solicitud'],'fecha_pago':Form[0]['fecha_pago'],'fecha_inicio':Form[0]['fecha_inicio'],'fecha_fin':Form[0]['fecha_fin']}) 
            except Exception as e:
                pagosCJ.append({'fecha':i[3],'recibo':i[0],'expediente':i[2],'status':i[1],'ftabla':format_fech,'tipo_movimiento':"",'movimiento':"",'tipo_solicitud':"",'fecha_pago':"",'fecha_inicio':"",'fecha_fin':""})     
        return(pagosCJ)    
    except Exception as e:
        print('Error de conexion DINAPI')
    finally:
        conn.close()

#pagos sfe no enviados
def no_enviado_sfe(fecha):
    temp = []
    try:
        conn = psycopg2.connect(
            host = host_SFE_conn,
            user= user_SFE_conn,
            password = password_SFE_conn,
            database = database_SFE_conn
        )
        cursor = conn.cursor()
        cursor.execute("select pagado_at,  authorization_number , to_char(bancard_transactions.updated_at,'DD/MM/YYYY') as fecha_pago ,status, respuestas, enviado_at, tramites.estado \n"
        +" from bancard_transactions left join public.tramites on public.tramites.id = bancard_transactions.payable_id \n" 
        +" where bancard_transactions.status = 1 \n" 
        +" and  public.tramites.formulario_id = 29 \n" 
        +" and public.tramites.enviado_at >= '"+str(Fecha_atras(fecha))+"'")# Para escanear fechas atras se cambia la condicion a >=
        row=cursor.fetchall()
        pagosSFE = []
        for i in row:
            temp.append({'respuesta':i[4]})
            fpago = str(i[2]).split('/')
            format_fecha = fpago[2]+'-'+fpago[1]+'-'+fpago[0]
            try:
                pagosSFE.append({'fecha':i[2],'recibo':i[1],'expediente':i[4][0]['valor'],'status':i[3],'ftabla':format_fecha,"enviado":i[5],"estado":i[6]})
            except Exception as ex:
                pass
        return(pagosSFE)

    except Exception as e:
        print(e)
    finally:
        conn.close()


# Toda la informacion de la vista por fecha
def full_package(fecha):
    return(*consulta_sfe(fecha),*consulta_caja(fecha))



"""

la fecha a procesar en testing 2022-12-01

"""

#Soporte por fecha
def consulta_Fop_fecha(facha):
    orden = []
    try:
        conn = psycopg2.connect(
                                host = '192.168.50.215',
                                user='user_app_publicacion',
                                password='user_app_publicacion-202201!',
                                database='db_publicacion'
        )
        cursor = conn.cursor()
        cursor.execute("""select tip_movimiento, 
                            to_char(fec_movimiento,'DD/MM/YYYY') as movimiento, 
                            tip_solicitud, 
                            to_char(fecha_pago,'DD/MM/YYYY') as pago, 
                            to_char(fecha_inicio,'DD/MM/YYYY') as fecha_inicio, 
                            to_char(fecha_fin,
                            'DD/MM/YYYY') as fecha_fin,
                            num_acta,
                            tip_signo,
                            nom_denominacion,
                            fec_movimiento 
                    FROM public.form_orden_publicacion WHERE fec_movimiento ='""" + str(facha)+"'")
        row=cursor.fetchall()
        for i in row:
            orden.append({
                        'tipo_movimiento':i[0],
                        'movimiento':i[1],
                        'tipo_solicitud':i[2],
                        'fecha_pago':i[3],
                        'fecha_inicio':i[4],
                        'fecha_fin':i[5],
                        'num_acta':i[6],
                        'tip_signo':signo_format(i[7]),
                        'nom_denominacion':i[8],
                        'origen':'Soporte'
                })           
        return(orden)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        
#Soporte por expediente
def consulta_Fop_expediente(exp):
    orden = []
    try:
        conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
        )
        cursor = conn.cursor()
        cursor.execute("""select tip_movimiento, 
                            to_char(fec_movimiento,
                            'DD/MM/YYYY') as movimiento, 
                            tip_solicitud, 
                            to_char(fecha_pago,'DD/MM/YYYY') as pago, 
                            to_char(fecha_inicio,'DD/MM/YYYY') as fecha_inicio, 
                            to_char(fecha_fin,
                            'DD/MM/YYYY') as fecha_fin,
                            num_acta,
                            tip_signo,
                            nom_denominacion  
                    FROM public.form_orden_publicacion WHERE num_acta ='""" + str(exp) +"' ORDER BY num_acta DESC LIMIT 1")
        row=cursor.fetchall()
        for i in row:
            orden.append({
                        'tipo_movimiento':i[0],
                        'movimiento':i[1],
                        'tipo_solicitud':i[2],
                        'fecha_pago':i[3],
                        'fecha_inicio':i[4],
                        'fecha_fin':i[5],
                        'num_acta':i[6],
                        'tip_signo':signo_format(i[7]),
                        'nom_denominacion':i[8],
                        'origen':'Soporte'
                })             
        return(orden)
    except Exception as e:
        print(e)
    finally:
        conn.close()


#Todo el proceso del la fecha en un click por backEnd 
def sfe_fileNbr(fecha):
    orderNbr = []
    try:
        conn = psycopg2.connect(host = host_SFE_conn,user= user_SFE_conn,password = password_SFE_conn,database = database_SFE_conn)
        cursor = conn.cursor()
        cursor.execute("""select pagado_at,  authorization_number , to_char(bancard_transactions.updated_at,'DD/MM/YYYY') as fecha_pago ,status, respuestas
        from bancard_transactions left join public.tramites on public.tramites.id = bancard_transactions.payable_id  
        where bancard_transactions.status = 1  
        and public.tramites.estado = 7  
        and  public.tramites.formulario_id = 29  
        and enviado_at >= '{} 01:59:00.0' and enviado_at <= '{} 14:59:00.0'""".format(fecha,fecha))
        row=cursor.fetchall()
        pagosSFE = []
        for i in row:
            for x in range(0,len(i[4])):
                if i[4][x]['campo'] == 'marcaredpi_expediente' and i[4][x]['descripcion'] == 'Buscar Solicitud N°':
                    orderNbr.append(int(str(i[4][x]['valor'])))
        return(orderNbr)
    except Exception as e:
        print(e)
    finally:
        conn.close()

def caja_fileNbr(fecha):
    orderNbr = []
    try:
        pagosCJ = []
        #________________________________________________________
        conn = psycopg2.connect(host =  hostCJ,user =  userCJ,password =  passwordCJ,database =  databaseCJ)
        cursor = conn.cursor()
        cursor.execute("""select distinct r.num_recibo as RECIBO, dr.tasa_id as TASA, dr.expediente_nro as EXPEDIENTE, to_char(r.fec_recibo,'DD/MM/YYYY') as FECHA_RECIBO 
                            from public.recibo r left join public.recibo_tipo_tasa rtt on rtt.recibo_id = r.id 
                            left join public.detalles_recibo dr on dr.recibo_tipo_tasa_id = rtt.id 
                            where dr.tasa_id = 80
                            and to_char(r.fec_recibo,'YYYY-MM-DD') like '{}';""".format(fecha,fecha))
        row = cursor.fetchall()  
        for i in row:
            orderNbr.append(int(str(i[2])))
        return(orderNbr)    
    except Exception as e:
        print('Error de conexion DINAPI')
    finally:
        conn.close()

#->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
def fileNbr_List(fecha):# Objeto iterador
    return(*sfe_fileNbr(fecha),*caja_fileNbr(fecha))

def update_inicio_fin(exp):# UpDate form segun iterador  
        try: 
            today = date.today()#Día actual
            today_date = date.today()
            td = timedelta(3)
            registro = today_date + td
            td_mañana = timedelta(1) # Fecha mañana inicio 
            fecha_mañana = today + td_mañana
            Form_order = consulta_Fop_out(exp)
            connif = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
            cursor = connif.cursor()

            if Form_order[0]['fecha_inicio'] == "":
                if(Form_order[0]['tipo_solicitud'] == 'REG'):
                    cursor.execute("update public.form_orden_publicacion set fecha_inicio='"+str(fecha_mañana)+"',fecha_fin='"+str(registro)+"',fecha_pago='"+str(today)+"' where num_acta = '"+str(exp)+"'")
                else:
                    cursor.execute("update public.form_orden_publicacion set fecha_inicio='"+str(fecha_mañana)+"',fecha_fin='"+str(fecha_mañana)+"',fecha_pago='"+str(today)+"' where num_acta = '"+str(exp)+"'")    
            else:
                pass
            cursor.rowcount
            connif.commit()
            connif.close()
            return('ok') 
        except Exception as e:
            pass
        finally:
            connif.close()

def update_inicio_fin_soporte(exp,pago):# UpDate form segun iterador  
        try: 
            today = date.today()#Día actual
            today_date = date.today()
            td = timedelta(3)
            registro = today_date + td
            td_mañana = timedelta(1) # Fecha mañana inicio 
            fecha_mañana = today + td_mañana
            Form_order = consulta_Fop_out(exp)
            connif = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
            cursor = connif.cursor()

            if Form_order[0]['fecha_inicio'] == "":
                if(Form_order[0]['tipo_solicitud'] == 'REG'):
                    cursor.execute("update public.form_orden_publicacion set fecha_inicio='"+str(fecha_mañana)+"',fecha_fin='"+str(registro)+"',fecha_pago='"+str(pago)+"' where num_acta = '"+str(exp)+"'")
                else:
                    cursor.execute("update public.form_orden_publicacion set fecha_inicio='"+str(fecha_mañana)+"',fecha_fin='"+str(fecha_mañana)+"',fecha_pago='"+str(pago)+"' where num_acta = '"+str(exp)+"'")    
            else:
                pass
            cursor.rowcount
            connif.commit()
            connif.close()
            return('ok') 
        except Exception as e:
            pass
        finally:
            connif.close()

def insert_clasificado(exp,userp):# Inserta la info del clasificado segun iterador
        try:
            todaypub = date.today()#Día actual
            today_date = date.today()
            td = timedelta(3)

            td_mañana = timedelta(1) # Fecha mañana inicio 
            fecha_mañana = todaypub + td_mañana
            
            registrof = today_date + td # fecha fin registro

            get_list = mark_getlist(exp)
            params = get_list[0]['fileIdAsString'].split('|')
            data = mark_read(params[3],params[0],params[2],params[1])
            respuesta = {
                            'fileNbr':data['file']['fileId']['fileNbr']['doubleValue'],
                            'fileSeq':data['file']['fileId']['fileSeq'],
                            'fileSeries':data['file']['fileId']['fileSeries']['doubleValue'],
                            'applicationSubtype':data['file']['filingData']['applicationSubtype'] ,
                            'applicationType':data['file']['filingData']['applicationType'] ,
                            'filingDate':data['file']['filingData']['filingDate']['dateValue'],
                            'signData':data['signData']['signType'],
                            'niceClassNbr':data['protectionData']['niceClassList'][0]['niceClassNbr']['doubleValue'],
                            'markName':str(data['signData']['markName']).replace("'","\'"),
                            'ownerPerson':data['file']['ownershipData']['ownerList'][0]['person']['personName'],
                            'owneraddress':data['file']['ownershipData']['ownerList'][0]['person']['addressStreet'],
                            'representativeList':data['file']['representationData']['representativeList'][0]['person']['personName'],
                            'agentCode':data['file']['representationData']['representativeList'][0]['person']['agentCode']['doubleValue'],
                            'processNbr':data.file.processId.processNbr.doubleValue,
						    'processType':data.file.processId.processType
                        }
            try:
                logo_mark = {'image':base64.b64encode(data['signData']['logo']['logoData']).decode("UTF-8")}
            except Exception as e:
                logo_mark = ""     
            try:		
                recibo = {'paymentList':{ 'receiptNbr':data['file']['filingData']['paymentList'][0]['receiptNbr'],'receiptType':data['file']['filingData']['paymentList'][0]['receiptType'] },}
            except Exception as err:										
                recibo = '0'
            try:
                registro = {'registrationNbr':data['file']['registrationData']['registrationId']['registrationNbr']['doubleValue'],'expirationDate':data['file']['registrationData']['expirationDate']['dateValue'],'registrationDate':data['file']['registrationData']['registrationDate']['dateValue']}
            except Exception as errrr:
                registro = '0'
            ########################################################## Insert detalle clasificado ####################################################################################
            try:
                exp_date = respuesta['filingDate']
                fecha_exp = str(exp_date).split(' ')
                hora_exp = fecha_exp[1].split('-')
                if(respuesta['signData'] == 'N'):
                    tipo_signo = 'Denominativa'
                if(respuesta['signData'] == 'D'):
                    tipo_signo = 'Denominativa'
                if(respuesta['signData'] == 'L'):
                    tipo_signo = 'Figurativa'        
                if(respuesta['signData'] == 'F'):
                    tipo_signo = 'Figurativa'
                if(respuesta['signData'] == 'B'):
                    tipo_signo = 'Mixta'
                if(respuesta['signData'] == 'M'):
                    tipo_signo = 'Mixta'
                if(respuesta['signData'] == 'T'):
                    tipo_signo = 'Tridimensional'
                if(respuesta['signData'] == 'S'):
                    tipo_signo = 'Sonora'
                if(respuesta['signData'] == 'O'):
                    tipo_signo = 'Olfativa' 

                clase = str(respuesta['niceClassNbr']).split('.')
                marca = respuesta['markName']
                nombre = respuesta['ownerPerson']
                direccion = respuesta['owneraddress']
                pais = respuesta['fileSeq']
                agente_nombre = respuesta['representativeList']
                logo_m_mark = logo_mark['image']
                expediente = str(respuesta['fileNbr']).split('.')
                nagente = str(respuesta['agentCode']).split('.')
                agente = nagente[0]

                if(respuesta['applicationType'] == 'REG'):
                    fin_pub = registrof
                if(respuesta['applicationType'] == 'REN'):
                    fin_pub = fecha_mañana
                expub = int(expediente[0])
                conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO public.detalle_clasificado (
                    num_orden, 
                    fecha_solicitud,
                    hora_solicitud, 
                    tipo_solicitud, 
                    tipo_signo, 
                    tipo_marca, 
                    clase, 
                    denominacion, 
                    solicitante, 
                    direccion, 
                    pais, 
                    agente, 
                    descripcion, 
                    logo, 
                    expediente, 
                    nom_agente, 
                    user_login, 
                    edicion, 
                    estado, 
                    inicio, 
                    fin, 
                    fecha_pago, 
                    fec_reg, 
                    process_user)
                    VALUES('0','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','DESCRIPCION ','{}',{},'','','','1','{}','{}','','','{}');""".format(fecha_exp[0],hora_exp[0], str(respuesta['applicationType']), str(tipo_signo),str(tipo_signo),str(clase[0]), str(marca), str(nombre), str(direccion).replace("'","\'"), str(pais), str(agente)+" -  "+str(agente_nombre), str(logo_m_mark),str(expediente[0]), str(fecha_mañana), str(fin_pub),userp))    
                cursor.rowcount
                conn.commit()
                conn.close()
                update_inicio_fin(exp)               
                return('indexado...')
            except Exception as e:
                print(e)
            finally:
                conn.close()
            ########################################################## fin Insert detalle clasificado #################################################################################
        except Exception as e:
            return 'Mark Read not found'
        else:
            pass
        finally:
            pass

def insertar_edicion(fecha,edicion):# inserta la edicion despues de iterar todo el paque
    lista_exp = []
    lista_id = []
    edicion_id = 0
    try: 
        td = timedelta(2)
        td_2 = timedelta(-2)
        td_3 = timedelta(-1)
        td_4 = timedelta(1)
        una_fecha = str(fecha)
        fecha_dt = datetime.strptime(una_fecha, '%Y-%m-%d') 
        dia_tras = str(fecha_dt+td).replace("00","").replace(":","")
        dia_tras_2 = str(fecha_dt+td_2).replace("00","").replace(":","")
        dia_tras_3 = str(fecha_dt+td_3).replace("00","").replace(":","")
        dia_tras_4 = str(fecha_dt+td_4).replace("00","").replace(":","")
        connDC = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
        cursorDC = connDC.cursor()
        cursorDC.execute("select id,expediente from detalle_clasificado where inicio = '"+str(fecha)+"' and fin = '"+str(fecha)+"'\n" 
                        + " union   \n"
                        + "select id,expediente from detalle_clasificado where inicio = '"+str(fecha)+"' and fin = '"+str(dia_tras).strip()+"'\n"
                        + " union   \n"
                        + "select id,expediente from detalle_clasificado where inicio = '"+str(dia_tras_2).strip()+"' and fin = '"+str(fecha)+"'\n"  
                        + " union   \n"  
                        + "select id,expediente from detalle_clasificado where inicio = '"+str(dia_tras_3).strip()+"' and fin = '"+str(dia_tras_4).strip()+"'")   # fin pasando mañana   
        row=cursorDC.fetchall()
        for i in row:
            lista_id.append(str(i[0]))
            lista_exp.append(str(i[1]))
        connDC.close()
        td = timedelta(1)
    except Exception as e:
        print(e)    
    ####################################################################################################################################  

    try: #insertar edicion en publicaciones_publicaciones
        sincoma = str(lista_exp).replace("'","")
        connPP = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
        cursorPP = connPP.cursor()
        cursorPP.execute("INSERT INTO public.publicaciones_publicaciones( fecha_publicacion, tipo_pi, tipo_publicacion, edicion, nexpedientes, estado, url_revistas) \n"
                        +"values('1977-09-01', 'MARCAS', 'CLASIFICADOS', '"+str(edicion)+"', '"+sincoma+"', 'true', NULL);") #"+str(fecha)+"
        cursorPP.rowcount
        connPP.commit()
        connPP.close() 
    except Exception as err:
        print(err)       
    ####################################################################################################################################
    try: #traer id de edicion en publicaciones_publicaciones
        connP_P = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
        cursorP_P = connP_P.cursor()
        cursorP_P.execute("select id from public.publicaciones_publicaciones where edicion = '"+str(edicion)+"'")
        row=cursorP_P.fetchall()
        for i in row:
            edicion_id = int(i[0])
        #print(i[0])
        connP_P.close()   
    except Exception as err:
        print(err)   
    ####################################################################################################################################
    try:#insertar id de clasificados con id edicion en publicacion_detalle_clasificado
        for item in lista_id:
            clas_id = int(item)
            pp_id = edicion_id
            url = "INSERT INTO public.publicacion_detalle_clasificado (detalle_publicacion_id,  publicacion_id) values ("+str(clas_id)+","+str(pp_id)+")"
            conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
            cursor = conn.cursor()
            cursor.execute(url)
            cursor.rowcount
            conn.commit()
            conn.close()    
    except Exception as err:
        print(err)
    return('listo!!')

def insert_only_new_pub(fecha):
	try:
		connH = psycopg2.connect(host=db_host,user=db_user,password=db_password,database=db_database)
		cursor = connH.cursor()
		cursor.execute("SELECT fecha_publicacion,nexpedientes FROM public.publicaciones_publicaciones where fecha_publicacion = '"+str(fecha)+"'")    
		row=cursor.fetchall()
		for i in row:
			exp_ipas = str(i[1]).replace("[","").replace("]","").split(',')
			for x in range(len(exp_ipas)):
				print(Insert_Action_soporte(exp_ipas[x],str(date.today()),'47','Publicacion REDPI','573'))
		connH.close()
	except Exception as e:
		pass

#->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
def processToDate(fecha):

    print(len(fileNbr_List(fecha)))

    for i in fileNbr_List(fecha):
        try:
            if update_inicio_fin(str(i)) == 'ok':
                insert_clasificado(str(i),'47')
        except Exception as e:
            pass    
    
    time.sleep(1) 

    masUno = timedelta(1)                 
    insertar_edicion(date.today()+masUno,'77')        
    
    time.sleep(1) 
                   
    insert_only_new_pub('1977-09-01')
    
def insertar_edicion_finde(fecha,edicion):
    lista_exp = []
    lista_id = []
    edicion_id = 0
    try:
        today_date = date.today()
        td = timedelta(1) 
        #dia_mas_uno = today_date+td   
        connDC = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursorDC = connDC.cursor()
        cursorDC.execute("select id,expediente  from public.detalle_clasificado where inicio = '"+str(fecha)+"' union  \n"
                        +"select id,expediente from public.detalle_clasificado where fin = '"+str(fecha)+"' union  \n"
                        +"select  id,expediente from public.detalle_clasificado where fin = '"+str(today_date+td)+"' ")    
        row=cursorDC.fetchall()
        for i in row:
            lista_id.append(str(i[0]))
            lista_exp.append(str(i[1]))
        #print(lista_exp)
        #print(lista_id)
        connDC.close()
        td = timedelta(1)
    except Exception as e:
        print(e)    
    ####################################################################################################################################  

    try: #insertar edicion en publicaciones_publicaciones
        sincoma = str(lista_exp).replace("'","")
        connPP = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
            )
        cursorPP = connPP.cursor()
        cursorPP.execute("INSERT INTO public.publicaciones_publicaciones( fecha_publicacion, tipo_pi, tipo_publicacion, edicion, nexpedientes, estado, url_revistas) \n"
                        +"values('"+str(fecha)+"', 'MARCAS', 'CLASIFICADOS', '"+str(edicion)+"', '"+sincoma+"', 'true', NULL);")
        cursorPP.rowcount
        connPP.commit()
        connPP.close() 
    except Exception as err:
        print(err)       
    ####################################################################################################################################
    try: #traer id de edicion en publicaciones_publicaciones
        connP_P = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
            )
        cursorP_P = connP_P.cursor()
        cursorP_P.execute("select id from publicaciones_publicaciones where edicion = '"+str(edicion)+"'")
        row=cursorP_P.fetchall()
        for i in row:
            edicion_id = int(i[0])
        #print(i[0])
        connP_P.close()   
    except Exception as err:
        print(err)   
    ####################################################################################################################################
    try:#insertar id de clasificados con id edicion en publicacion_detalle_clasificado
        for item in lista_id:
            clas_id = int(item)
            pp_id = edicion_id
            url = "INSERT INTO public.publicacion_detalle_clasificado (detalle_publicacion_id,	publicacion_id) values ("+str(clas_id)+","+str(pp_id)+")"
            conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                )
            cursor = conn.cursor()
            cursor.execute(url)
            cursor.rowcount
            conn.commit()
            conn.close()    
    except Exception as err:
        print(err)
    return('listo!!') 

#clasificados de edicion de hoy
def previa_edicion(fecha):
    lista_exp = []
    try: 
        td = timedelta(2)
        td_2 = timedelta(-2)
        td_3 = timedelta(-1)
        td_4 = timedelta(1)
        una_fecha = str(fecha)
        fecha_dt = datetime.strptime(una_fecha, '%Y-%m-%d') 
        dia_tras = str(fecha_dt+td).replace("00","").replace(":","")
        dia_tras_2 = str(fecha_dt+td_2).replace("00","").replace(":","")
        dia_tras_3 = str(fecha_dt+td_3).replace("00","").replace(":","")
        dia_tras_4 = str(fecha_dt+td_4).replace("00","").replace(":","")
        conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
        cursor = conn.cursor()
        cursor.execute("select * from detalle_clasificado where inicio = '"+str(fecha)+"' and fin = '"+str(fecha)+"'\n" 
                        + " union   \n"
                        + "select * from detalle_clasificado where inicio = '"+str(fecha)+"' and fin = '"+str(dia_tras).strip()+"'\n"
                        + " union   \n"
                        + "select * from detalle_clasificado where inicio = '"+str(dia_tras_2).strip()+"' and fin = '"+str(fecha)+"'\n"  
                        + " union   \n"  
                        + "select * from detalle_clasificado where inicio = '"+str(dia_tras_3).strip()+"' and fin = '"+str(dia_tras_4).strip()+"'")     
        row=cursor.fetchall()
        for i in row:
            lista_exp.append({"num_orden":i[0],"fecha_solicitud":i[2],"hora_solicitud":i[3],"tipo_solicitud":i[4],"tipo_signo":i[5],"tipo_marca":i[6],"clase":i[7],"denominacion":i[8],"solicitante":i[9],"direccion":i[10],"pais":i[11],"agente":i[12],"descripcion":i[13],"logo":i[14],"expediente":i[15],"nom_agente":i[16],"user_login":i[17],"edicion":i[18],"estado":i[19],"inicio":i[20],"fin":i[21],"fecha_pago":i[22],"fec_reg":i[23],})
        #print(len(lista_exp))
        conn.close()
        return(lista_exp)
    except Exception as e:
        print(e)

#Contador de edicion    
def edicion_cont():
    try: 
        edition = 0   
        conn = psycopg2.connect(
                                 host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursor = conn.cursor()
        cursor.execute("select edicion  from public.publicaciones_publicaciones pp where  pp.tipo_publicacion = 'CLASIFICADOS' and pp.tipo_pi = 'MARCAS' ORDER BY id DESC LIMIT 1")    
        row=cursor.fetchall()
        for i in row:
            edition = i[0]
        conn.close()   
    except Exception as e:
        print(e)
    return(str(int(edition)+1))

#Link para verificacion
def edicion_cont_link():
    try: 
        id_link = 0   
        conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursor = conn.cursor()
        cursor.execute("select id from publicaciones_publicaciones where tipo_publicacion = 'CLASIFICADOS' ORDER BY id DESC LIMIT 1")    
        row=cursor.fetchall()
        for i in row:
            id_link = i[0]
        conn.close()
        
    except Exception as e:
        print(e)
    return('https://redpi.dinapi.gov.py/visualizarPdf/'+str(id_link))    

#USUARIOS ADMIN
def user_admin_redpi():
    lista_user = []
    try:    
        conn = psycopg2.connect(
                        host='pgsql-sprint.dinapi.gov.py',
                        user='user-sprint',
                        password='user-sprint--201901',
                        database='kuriju_produccion'
                    )
        cursor = conn.cursor()
        cursor.execute("select valor1,valor2,valor3,valor4,valor5 from kuriju_produccion.octopus.parametros where id = 28")    
        row=cursor.fetchall()
        for i in row:
            return({'valor1':i[0],'valor2':i[1],'valor3':i[2],'valor4':i[3],'valor5':i[4],})
        #print(lista_exp)
        conn.close()
    except Exception as e:
        print(e)

def migrar_servicios(fecha):
    fecha_mas = str(fecha).split("-")
    dia_mas_uno = int(fecha_mas[2]) + 1
    lista_exp = []
    today_date = date.today()
    td = timedelta(1)
    dia_mas_uno = today_date+td 
    try:    
        conn = psycopg2.connect(
		            host =	host_centura,
		            user =	user_centura,
		            password =	password_centura,
		            database =	database_centura
                    )
        cursor = conn.cursor()
        cursor.execute("select * from form_orden_publicacion  where fecha_inicio = '"+str(today_date)+"' union  \n"
                        +"select * from form_orden_publicacion where fecha_fin = '"+str(today_date)+"' union  \n"
                        +"select * from form_orden_publicacion where fecha_fin = '"+str(dia_mas_uno)+"' ")    
        row=cursor.fetchall()
        for i in row:
            lista_exp.append(int(i[0]))
        conn.close()

    except Exception as e:
        print(e) 
    
    #print(fecha)
    #print(lista_exp) 

    try:
        connPP = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
            )
        cursorPP = connPP.cursor()
        cursorPP.execute("INSERT INTO publicaciones_publicaciones (fecha_publicacion, tipo_pi, tipo_publicacion, edicion, nexpedientes, estado, url_revistas) VALUES('"+fecha+"','MARCAS','CLASIFICADOS','0', '"+str(lista_exp)+"', 'true', NULL);")
        cursorPP.rowcount
        connPP.commit()
        connPP.close()
    except Exception as er:
        print(er)
    return('Migrada la fecha ' + fecha)

#Datos de publicacion 
def insert_dia_proceso(fecha,sfe,caja,reg,ren,total,process):
    try:
            url = "INSERT INTO dia_proceso (fecha_proceso, sfe, caja, reg, ren, total, process) values ('"+fecha+"',"+str(sfe)+","+str(caja)+","+str(reg)+","+str(ren)+","+str(total)+",'"+process+"');"
            conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
            cursor = conn.cursor()
            cursor.execute(url)
            cursor.rowcount
            conn.commit()
            conn.close()    
    except Exception as err:
        print(err)

def select_dia_proceso():
    procesado = []
    try:
        conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
        cursor = conn.cursor()
        cursor.execute("select * from dia_proceso where id = 1")
        row=cursor.fetchall()
        for i in row:
            procesado.append({"fecha":i[0],"sfe":i[1],"caja":i[2],"reg":i[3],"ren":i[4],"total":i[5],"process":i[6]})           
        return(procesado)
    except Exception as e:
        print(e)
    finally:
        conn.close()
     
def update_dia_proceso(fecha,sfe,caja,reg,ren,total,process):
    try:
            url = "update dia_proceso set fecha_proceso = '"+fecha+"', sfe = "+sfe+", caja = "+caja+", reg = "+reg+", ren = "+ren+", total = "+total+", process = '"+process+"' where id = 1"
            conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
            cursor = conn.cursor()
            cursor.execute(url)
            cursor.rowcount
            conn.commit()
            conn.close()    
    except Exception as err:
        print(err)

def serv_img(exp):
    conn = psycopg2.connect(host = db_host,user = db_user,password = db_password,database = db_database)
    cursor = conn.cursor()
    cursor.execute("select * from public.new_ordenes_publicaciones where expediente = '"+exp+"'")    
    row=cursor.fetchall()
    for i in row:
        return(i[10])
    conn.close()

def consulta_sfe_prueba(fecha):
    data_fecha = str(fecha).split("/")
    fecha_uno = data_fecha[2]+"-"+data_fecha[1]+"-"+data_fecha[0]
    temp = []
    try:
        conn = psycopg2.connect(
            host = host_SFE_conn,
            user= user_SFE_conn,
            password = password_SFE_conn,
            database = database_SFE_conn
        )
        cursor = conn.cursor()
        cursor.execute("select pagado_at,  authorization_number , to_char(bancard_transactions.updated_at,'DD/MM/YYYY') as fecha_pago ,status, respuestas \n"
        +" from bancard_transactions left join public.tramites on public.tramites.id = bancard_transactions.payable_id \n" 
        +" where bancard_transactions.status = 1 \n" 
        +" and public.tramites.estado = 7 \n" 
        +" and  public.tramites.formulario_id = 29 \n" 
        + "and enviado_at >= '"+fecha_uno+" 01:59:00.0' and enviado_at <= '"+fecha_uno+" 14:59:00.0'")
        row=cursor.fetchall()
        pagosSFE = []
        for i in row:

            pag_exp = ""
            if i[4][0]['campo'] == 'marcaredpi_expediente' and i[4][0]['descripcion'] == 'Buscar Solicitud N°':
                pag_exp = str(i[4][0]['valor']) 

            temp.append({'respuesta':i[3]})
            fpago = str(i[2]).split('/')
            format_fecha = fpago[2]+'-'+fpago[1]+'-'+fpago[0]
            try:
                pagosSFE.append({'fecha':i[2],'recibo':i[1],'expediente':pag_exp,'status':i[3],'ftabla':format_fecha,'tipo_movimiento':consulta_Fop_out(str(pag_exp))[0]['tipo_movimiento'],'movimiento':consulta_Fop_out(str(pag_exp))[0]['movimiento'],'tipo_solicitud':consulta_Fop_out(str(pag_exp))[0]['tipo_solicitud'],'fecha_pago':consulta_Fop_out(str(pag_exp))[0]['fecha_pago'],'fecha_inicio':consulta_Fop_out(str(pag_exp))[0]['fecha_inicio'],'fecha_fin':consulta_Fop_out(str(pag_exp))[0]['fecha_fin']})
            except Exception as ex:
                pagosSFE.append({'fecha':i[2],'recibo':i[1],'expediente':pag_exp,'status':i[3],'ftabla':format_fecha,'tipo_movimiento':"",'movimiento':"",'tipo_solicitud':"",'fecha_pago':"",'fecha_inicio':"",'fecha_fin':""})
            
        return(jsonify(pagosSFE))

    except Exception as e:
        print(e)
    finally:
        conn.close()

def insert_form_orden_publicacion(exp):
    try:
        item = Fech_All_Exp(exp)
        position = int(len(item))-1
        todaypub = datetime.now()
        event_date = str(todaypub).split(' ')
        des_mov=""


        if(item[position].sqlColumnList[13].sqlColumnValue == '549'):
            des_mov = "Emisión Orden Publicación"
        if(item[position].sqlColumnList[13].sqlColumnValue == '550'):
            des_mov = "Informe de renovación"
        if(item[position].sqlColumnList[13].sqlColumnValue == '560'):
            des_mov = "Segunda orden de publicacion"

        if(item[position].sqlColumnList[13].sqlColumnValue == '549'):
            tip_sol = "REG"
        if(item[position].sqlColumnList[13].sqlColumnValue == '550'):
            tip_sol = "REN"
        if(item[position].sqlColumnList[13].sqlColumnValue == '560'):
            tip_sol = "SOP"

    #insert registro en form_o_p
    
        connG = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursorG = connG.cursor()
        cursorG.execute("INSERT INTO public.form_orden_publicacion (num_acta, tip_movimiento, tip_signo, fec_movimiento, tip_solicitud, cod_usuario, estado, tipo, num_agente, des_movimiento, nom_denominacion, nom_agente, fecha_pago, fecha_inicio, fecha_fin, pdf, fecha_reg, proceso_id)VALUES("+str(item[position].sqlColumnList[0].sqlColumnValue)+", '"+str(item[position].sqlColumnList[13].sqlColumnValue)+"', '"+str(item[position].sqlColumnList[4].sqlColumnValue)+"','"+str(item[position].sqlColumnList[12].sqlColumnValue)+"', '"+str(tip_sol)+"', '"+str(item[position].sqlColumnList[17].sqlColumnValue)+"', 'A', 'FOP', "+str(item[position].sqlColumnList[9].sqlColumnValue)+", '"+str(des_mov)+"', '"+str(item[position].sqlColumnList[6].sqlColumnValue).replace("'","\'")+"', '"+str(item[position].sqlColumnList[10].sqlColumnValue)+"', NULL,  NULL, NULL, NULL, '"+str(todaypub)+"', NULL);")    
        cursorG.rowcount
        connG.commit()
        connG.close()
    except Exception as e:
        print(e)

def existexp(exp):
    try:    
        connA = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursorA = connA.cursor()
        cursorA.execute("SELECT num_acta FROM public.form_orden_publicacion WHERE num_acta = " + str(exp))    
        row=cursorA.fetchall()
        for i in row: # capturar datos de registro 
            return(len(i))
        connA.close()
    except Exception as e:
        print(e)

def checking_payment_suport(exp):
    try:
        #________________________________________________________
        conn = psycopg2.connect(host =  hostCJ,user =  userCJ,password =  passwordCJ,database =  databaseCJ)
        cursor = conn.cursor()
        #                                                RECIBO,                TASA,                EXPEDIENTE,                                        FECHA_RECIBO
        cursor.execute(f"""select distinct r.num_recibo as RECIBO, dr.tasa_id as TASA, dr.expediente_nro as EXPEDIENTE, to_char(r.fec_recibo,'DD/MM/YYYY') as FECHA_RECIBO
                            from public.recibo r left join public.recibo_tipo_tasa rtt on rtt.recibo_id = r.id 
                            left join public.detalles_recibo dr on dr.recibo_tipo_tasa_id = rtt.id 
                            where dr.tasa_id = 80
                            --and to_char(r.fec_recibo,'DD/MM/YYYY') like '01/12/2022%'; --28/11/2022 primera fecha
                            and dr.expediente_nro = {exp}""")
        row = cursor.fetchall()
        #________________________________________________________  
        if row != []:  
            return(True)
        else:
            return(False)   
    except Exception as e:
        print('Error de conexion DINAPI')
    finally:
        conn.close() 

#print(consulta_sfe_prueba('10/01/2023'))

#insertar_edicion_finde('2022-12-02','0')

#crea la fecha espesificada (no procesa solo compila la revista)
#insertar_edicion('2023-01-02','0')

#print(select_dia_proceso())
#print(edicion_cont())
#migrar_servicios('2022-09-04')
# enero 2019 - enero 2020 - enero 2021 - enero 2022
# febrero 2019 - febrero 2020 - febrero 2022
# marzo 2019 - marzo 2020 - marzo 2021 - marzo 2022
# abril 2019 - abril 2020 - abril 2021 - abril 2022
# mayo 2019 - mayo 2020 - mayo 2021 mayo 2022
# junio 2019 - junio 2020 - junio 2021 
# julio 2021 - julio 2020 - julio 2019
# agosto 2019 - agosto 2020 - agosto 2021
# setiembre 2019 - setiembre 2020 - setiembre 2021
# octubre 2019 - octubre 2020 - octubre 2021
# noviembre 2019 - noviembre 2020 noviembre 2021
# diciembre 2018 - diciembre 2019 - diciembre 2020 - diciembre 2021  

"""
    Funcion para soporte  
    1) capturar casos con (pago y movimiento en form_orden_publicacion)
    2) Mantener todas las propiedades del registro, insertar en detalle_clasificado con fecha inicio de proxima publicacion
    3) no se podra publicar para atras, solo agregar en publicacion mas proxima    
"""

####################################################################################################################################

#data_clas = [2300011,2283743,22111110,22111025,22111024]
#for i in data_clas:
#    print(insert_clasificado(str(i),'AMEDINA'))


#data_REG = [2300011,2283743,22111110,22111025,22111024]
#for i in data_REG:
#    update_inicio_fin(str(i),'REG','2022-11-25')

#insertar_edicion('2022-03-24')

#previa_edicion('2022-03-24')

#insertar_edicion('2022-09-5','100')

#edicion_cont()

'''
        host: pgsql-sprint.dinapi.gov.py
        Puerto: 5432
        DB: kuriju_produccion
        Usuario: user-sprint
        Password: user-sprint--201901

select     tr.pagado_at, bt.authorization_number, to_char(bt.updated_at,'dd/mm/yyyy') as FECHA_PAGO, to_char(tr.enviado_at,'dd/mm/yyyy') as FECHA_envio,
bt.status as ESTADO_PAGOS, tr.respuestas, tr.estado as ESTADOS_TRAMITES, TR.enviado_at from  bancard_transactions bt
left join tramites tr on tr.id = bt.payable_id 
where bt.status = 1 and  tr.estado = 7  and  tr.formulario_id = 29 and to_char(tr.enviado_at,'dd/mm/yyyy') = '24/05/2022';

'''
