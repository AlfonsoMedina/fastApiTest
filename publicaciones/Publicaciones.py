from tools.connect import db_host, db_user, db_password, db_database, host_SFE_conn, user_SFE_conn, password_SFE_conn, database_SFE_conn,host_centura, user_centura, password_centura, database_centura
import base64
from datetime import date, timedelta
import datetime
import time
from flask import jsonify
import psycopg2
from ipas.ipas_methods import Fech_All_Exp, Insert_Action, Insert_note, Process_Read_Action, fetch_all, mark_getlist, mark_getlistFecha, mark_read, Fech_All_Exp_titulares
from tools.base64Decode import decode_img
from tools.data_format import fecha_barra, fecha_mes, fecha_mes_hora, qr_code, signo_format
import unicodedata

#--------------------------------------------------------------- funciones de proeba Orden de publicacion -------------------------------------------------------------
def Consulta_fecha_orden(exp):
    movimiento = {"action_name": "","evento": "","fecha_solicitud": "","nom_user": "","user_Id": ""}
    try:
        expediente = mark_getlist(exp)[0]
        data = mark_read(expediente.fileId.fileNbr.doubleValue,expediente.fileId.fileSeq,expediente.fileId.fileSeries.doubleValue,expediente.fileId.fileType)
    except Exception as e:
        print(e)

    try:
        try:
            for i in range(1,10):
                try:
                    mov = Process_Read_Action(i,str(int(data.file.processId.processNbr.doubleValue)),str(int(data.file.processId.processType))).actionType.actionTypeId.actionType
                    if(mov == '550' or mov == '549' or mov == '560'):
                        movimiento = {
                "fecha_solicitud":fecha_mes(Process_Read_Action(i,str(int(data.file.processId.processNbr.doubleValue)),str(int(data.file.processId.processType))).actionDate.dateValue),
                "evento":Process_Read_Action(i,str(int(data.file.processId.processNbr.doubleValue)),str(int(data.file.processId.processType))).actionType.actionTypeId.actionType,
                "action_name":Process_Read_Action(i,str(int(data.file.processId.processNbr.doubleValue)),str(int(data.file.processId.processType))).actionType.actionName,
                "nom_user":Process_Read_Action(i,str(int(data.file.processId.processNbr.doubleValue)),str(int(data.file.processId.processType))).captureUser.userName,
                "user_Id":str(int(Process_Read_Action(i,str(int(data.file.processId.processNbr.doubleValue)),str(int(data.file.processId.processType))).captureUser.userId.userNbr.doubleValue))
            }
                        break
                    else:
                        pass
                except Exception as e:
                        movimiento = {"action_name": "","evento": "no","fecha_solicitud": "","nom_user": "","user_Id": ""}
                        break
        except Exception as e:
            movimiento = {"action_name": "","evento": "no","fecha_solicitud": "","nom_user": "","user_Id": ""}

        respuesta = {
                    "fileNbr":str(int(data.file.fileId.fileNbr.doubleValue)),
                    "fileSeq":data.file.fileId.fileSeq,
                    "fileType":data.file.fileId.fileType,
                    "applicationSubtype":data.file.filingData.applicationSubtype,
                    "applicationType":data.file.filingData.applicationType,
                    "captureUserId":str(int(data.file.filingData.captureUserId.doubleValue)),
                    "filingDate":data.file.filingData.filingDate.dateValue,
                    "lawCode":str(int(data.file.filingData.lawCode.doubleValue)),
                    "novelty1Date":data.file.filingData.novelty1Date.dateValue,
                    "receptionDate":data.file.filingData.receptionDate.dateValue,
                    "docLog":data.file.filingData.receptionDocument.documentId.docLog,
                    "docNbr":str(int(data.file.filingData.receptionDocument.documentId.docNbr.doubleValue)),
                    "docOrigin":data.file.filingData.receptionDocument.documentId.docOrigin,
                    "docSeries":data.file.filingData.receptionDocument.documentId.docSeries.doubleValue, 
                    "processNbr":str(int(data.file.processId.processNbr.doubleValue)),
                    "processType":data.file.processId.processType,
                    "solicitud":fecha_mes_hora(data.file.filingData.receptionDate.dateValue),
                    "denominacion":data.signData.markName,
                    "signo":signo_format(data.signData.signType),
                    "clase":str(int(data.protectionData.niceClassList[0].niceClassNbr.doubleValue)),
                    "logo":base64.b64encode(data.signData.logo.logoData).decode("UTF-8"),
                    "descripcion_distintivo":data.protectionData.niceClassList[0].niceClassDescription,
                    "movimiento":fecha_barra(data.file.filingData.receptionDate.dateValue),
                    "reception":data.file.filingData.receptionDate.dateValue,
                }
        
        return({"data":respuesta,"movimiento":movimiento})     
    except Exception as e:
        print(e)

#consulta por fecha en IPAS para 
def Consulta_expediente_orden_fecha(fecha):
    respuesta = []
    try:
        for i in mark_getlistFecha(fecha+'T08:00:00',fecha+'T13:00:00'):
            expediente = mark_getlist(str(int(i.fileId.fileNbr.doubleValue)))[0]
            data = mark_read(expediente.fileId.fileNbr.doubleValue,expediente.fileId.fileSeq,expediente.fileId.fileSeries.doubleValue,expediente.fileId.fileType)
            if(Consulta_fecha_orden(str(int(data.file.fileId.fileNbr.doubleValue)))['movimiento']['evento'] != 'no'):          
                respuesta.append({
                            "expediente":Consulta_fecha_orden(str(int(data.file.fileId.fileNbr.doubleValue)))['data']['fileNbr'],
                            "fecha":Consulta_fecha_orden(str(int(data.file.fileId.fileNbr.doubleValue)))['data']['movimiento'],
                            "tipo":Consulta_fecha_orden(str(int(data.file.fileId.fileNbr.doubleValue)))['data']['applicationType'],
                            "signo":Consulta_fecha_orden(str(int(data.file.fileId.fileNbr.doubleValue)))['data']['signo'],
                            "clase":str(int(Consulta_fecha_orden(str(int(data.file.fileId.fileNbr.doubleValue)))['data']['clase'])),
                            "denominacion":Consulta_fecha_orden(str(int(data.file.fileId.fileNbr.doubleValue)))['data']['denominacion'],
                            "evento":Consulta_fecha_orden(str(int(data.file.fileId.fileNbr.doubleValue)))['movimiento']['evento'],
                            "userId":Consulta_fecha_orden(str(int(data.file.fileId.fileNbr.doubleValue)))['movimiento']['user_Id']
                })
        #print(respuesta)
        return(jsonify(respuesta))
    except Exception as e:
        print(e)

#CONSULTAR EXPEDIENTE IPAS replicar las url de consulta en publicaciones para reemplasar las consultas en el frontend 
def Consulta_expediente_orden(exp,user):
    t_nombre = []
    t_direccion = []
    t_pais = []
    for i in range(0,5):
        try:
            t_nombre.append(Fech_All_Exp_titulares(exp)[i].sqlColumnList[0].sqlColumnValue)
            t_direccion.append(Fech_All_Exp_titulares(exp)[i].sqlColumnList[1].sqlColumnValue)
            t_pais.append(Fech_All_Exp_titulares(exp)[i].sqlColumnList[3].sqlColumnValue)
        except Exception as e:
            pass
    try:
        item = Fech_All_Exp(exp)
        position = int(len(item))-1
        pack_data = {
            "ppn": str(item[position].sqlColumnList[10].sqlColumnValue),
            "user_login":str(item[position].sqlColumnList[17].sqlColumnValue),
            "solicitud":   str(fecha_mes_hora(str(item[position].sqlColumnList[2].sqlColumnValue))),
            "fecha_solicitud": str(fecha_mes(str(item[position].sqlColumnList[12].sqlColumnValue))),
            "fecha_invert": str(fecha_barra(str(item[position].sqlColumnList[12].sqlColumnValue))),
            "firma":   "",
            "estado":  str(getEstado(exp)), # consulta a new_ordenes_publicaciones
            "firmaD":  "data:image/png;base64,"+firma_user(str(item[position].sqlColumnList[17].sqlColumnValue)),
            "estado_pub":  int(getEstado_pub(exp)),     # consulta a new_ordenes_publicaciones
            "text_Pub":    getText_Pub(exp), # consulta a new_ordenes_publicaciones
            "file_NBR":    int(item[position].sqlColumnList[0].sqlColumnValue),
            "action_DATE": str(item[position].sqlColumnList[12].sqlColumnValue),
            "mark_NAME":   str(item[position].sqlColumnList[6].sqlColumnValue).replace("'", "\'"),
            "addr_STREET": str(t_direccion).replace("[","").replace("]","").replace("'",""),
            "agent_CODE":  str(item[position].sqlColumnList[9].sqlColumnValue),
            "person_NAME": str(t_nombre).replace("[","").replace("]","").replace("'",""), #.replace(","," ")
            "sign_WCODE":  signo_format(str(item[position].sqlColumnList[4].sqlColumnValue)),
            "nice_CLASS_TXT":  str(item[position].sqlColumnList[5].sqlColumnValue).replace("'","\'"),
            "logo_DATA": decode_img(str(item[position].sqlColumnList[11].sqlColumnValue)).replace("\n", ""),
            "filing_DATE": str(item[position].sqlColumnList[2].sqlColumnValue),
            "nice_CLASS_DESCRIPTION":  str(item[position].sqlColumnList[15].sqlColumnValue).replace("'", "\'"),
            "user_NAME":   str(item[position].sqlColumnList[16].sqlColumnValue),
            "action_TYPE_NAME": str(item[position].sqlColumnList[14].sqlColumnValue),
            "action_TYP":  str(item[position].sqlColumnList[13].sqlColumnValue),
            "appl_TYPE_NAME":  str(item[position].sqlColumnList[3].sqlColumnValue),
            "proc_NBR": str(item[position].sqlColumnList[1].sqlColumnValue)
        }
        return(jsonify([pack_data]))
    except Exception as err:
        return()

    
def Consulta_fecha_prim_orden(fecha,user):
    try:
        data = fetch_all(fecha, fecha)
        pack_data=[]
        t_nombre = []
        t_direccion = []
        t_pais = []
        for i in data:           
            if str(i.sqlColumnList[17].sqlColumnValue) == user: 
                for it in range(0,5):
                    try:
                                t_nombre.append(Fech_All_Exp_titulares(str(i.sqlColumnList[0].sqlColumnValue))[it].sqlColumnList[0].sqlColumnValue)
                                t_direccion.append(Fech_All_Exp_titulares(str(i.sqlColumnList[0].sqlColumnValue))[it].sqlColumnList[1].sqlColumnValue)
                                t_pais.append(Fech_All_Exp_titulares(str(i.sqlColumnList[0].sqlColumnValue))[it].sqlColumnList[3].sqlColumnValue)
                    except Exception as e:
                        pass                 
                pack_data.append({
                        "ppn": str(i.sqlColumnList[10].sqlColumnValue),
                        "user_login":str(i.sqlColumnList[17].sqlColumnValue),
                        "solicitud":   str(fecha_mes_hora(str(i.sqlColumnList[2].sqlColumnValue))),
                        "fecha_solicitud": str(fecha_mes(str(i.sqlColumnList[12].sqlColumnValue))),
                        "fecha_invert":    str(fecha_barra(str(i.sqlColumnList[12].sqlColumnValue))),
                        "firma":   "",
                        "estado":  str(getEstado(str(i.sqlColumnList[0].sqlColumnValue))),
                        "firmaD":  "data:image/png;base64,"+firma_user(str(i.sqlColumnList[17].sqlColumnValue)),
                        "estado_pub":  int(getEstado_pub(str(i.sqlColumnList[0].sqlColumnValue))),
                        "text_Pub":    getText_Pub(str(i.sqlColumnList[0].sqlColumnValue)),
                        "file_NBR":    int(i.sqlColumnList[0].sqlColumnValue),
                        "action_DATE": str(i.sqlColumnList[12].sqlColumnValue),
                        "mark_NAME":   str(i.sqlColumnList[6].sqlColumnValue).replace("'", "\'"),
                        "addr_STREET": str(t_direccion).replace("[","").replace("]","").replace("'", ""),
                        "agent_CODE":  str(i.sqlColumnList[9].sqlColumnValue),
                        "person_NAME": str(t_nombre).replace("[","").replace("]","").replace("'", ""),
                        "sign_WCODE":  signo_format(str(i.sqlColumnList[4].sqlColumnValue)),
                        "nice_CLASS_TXT":  str(i.sqlColumnList[5].sqlColumnValue),
                        "logo_DATA":   decode_img(str(i.sqlColumnList[11].sqlColumnValue)).replace("\n", ""),
                        "filing_DATE": str(i.sqlColumnList[2].sqlColumnValue),
                        "nice_CLASS_DESCRIPTION":  str(i.sqlColumnList[15].sqlColumnValue).replace("'", "\'"),
                        "user_NAME":   str(i.sqlColumnList[16].sqlColumnValue),
                        "action_TYPE_NAME": str(i.sqlColumnList[14].sqlColumnValue),
                        "action_TYP":  str(i.sqlColumnList[13].sqlColumnValue),
                        "appl_TYPE_NAME":  str(i.sqlColumnList[3].sqlColumnValue),
                        "proc_NBR": str(i.sqlColumnList[1].sqlColumnValue)
                    })
            #print(str(i.sqlColumnList[12].sqlColumnValue))
            t_nombre = []
            t_direccion = []
        return(jsonify(pack_data))
    except Exception as err:
        print(err)

#Insert por expediente para generar orden estado uno
def Generar_orden(exp):
    titulares = []
    item = Fech_All_Exp(exp)
    for i in range(0,5):
        try:
            #print(Fech_All_Exp_titulares(exp)[i].sqlColumnList[0].sqlColumnValue)
            titulares.append(Fech_All_Exp_titulares(exp)[i].sqlColumnList[0].sqlColumnValue)
        except Exception as e:
            pass
    position = int(len(item))-1
    todaypub = date.today()
    QR_b64 = ""
    tipo_orden = ""
    denominacion = ""
    if(item[position].sqlColumnList[13].sqlColumnValue =='550' or item[position].sqlColumnList[13].sqlColumnValue =='549'):
        tipo_orden = 'POP'
    if(item[position].sqlColumnList[13].sqlColumnValue =='560'):
        tipo_orden = 'SOP'

    if(str(item[position].sqlColumnList[6].sqlColumnValue) == 'None'):
        denominacion = " "
    if(str(item[position].sqlColumnList[6].sqlColumnValue) != 'None'):
        denominacion = str(item[position].sqlColumnList[6].sqlColumnValue)    
    try:   
        conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                   )
        cursor = conn.cursor()                         #  .replace("'","\'") 19-12-2022                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         #Nombre
        url = "INSERT INTO public.new_ordenes_publicaciones(expediente, solicitud, denominacion, nombre, direccion, agente, tipo, signo,clase, logo, fecha_solicitud, firma, codigo_qr, usuario, descripcion_distintivo, cod_agente, fecha_impresion, desc_servicio, estado,movimiento, url, fecha_generado, action_date, user_login, user_id, evento, envio_buzon, orden) VALUES ('"+item[position].sqlColumnList[0].sqlColumnValue+"','"+str(fecha_mes_hora(str(item[position].sqlColumnList[2].sqlColumnValue)))+"','"+str(denominacion).replace("'","`")+"','"+str(titulares).replace("[","").replace("]","").replace("'","").replace(","," ")+"','"+str(item[position].sqlColumnList[8].sqlColumnValue).replace("'","`")+"','"+str(item[position].sqlColumnList[9].sqlColumnValue)+" - "+str(item[position].sqlColumnList[10].sqlColumnValue)+"','"+str(item[position].sqlColumnList[3].sqlColumnValue)+"','"+signo_format(str(item[position].sqlColumnList[4].sqlColumnValue))+"','"+str(item[position].sqlColumnList[5].sqlColumnValue)+"','data:image/png;base64,"+decode_img(str(item[position].sqlColumnList[11].sqlColumnValue))+"','"+fecha_mes(str(item[position].sqlColumnList[12].sqlColumnValue))+"','data:image/png;base64,"+firma_user(str(item[position].sqlColumnList[17].sqlColumnValue))+"','QR','"+str(item[position].sqlColumnList[16].sqlColumnValue)+"','',"+str(item[position].sqlColumnList[9].sqlColumnValue)+",'','"+str(item[position].sqlColumnList[15].sqlColumnValue).replace("'","\'")+"',1,'"+str(fecha_barra(str(item[position].sqlColumnList[2].sqlColumnValue)))+"','','"+str(todaypub)+"','"+str(item[position].sqlColumnList[12].sqlColumnValue)+"','"+str(item[position].sqlColumnList[17].sqlColumnValue)+"','"+str(item[position].sqlColumnList[18].sqlColumnValue)+"','"+str(item[position].sqlColumnList[13].sqlColumnValue)+"','','"+tipo_orden+"')"   
        cursor.execute(url)
        cursor.rowcount
        conn.commit()
        conn.close()
    except Exception as e:
        print(e) 
    
    try:   
        conn_id = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursor = conn_id.cursor()
        cursor.execute("select id FROM public.new_ordenes_publicaciones where expediente = '"+exp+"' and estado = 1")    
        row=cursor.fetchall()
        for i in row:
           QR_b64 = str(i).replace("(","").replace(",)","")
        conn_id.close()
    except Exception as e:
        print(e) 
    
    try:   
        conn_qr = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                   )
        cursor = conn_qr.cursor()
        url = "UPDATE public.new_ordenes_publicaciones SET codigo_qr='data:image/png;base64,"+qr_code('https://sfe-tp.dinapi.gov.py/orden_publicacion/'+QR_b64)+"',url='"+QR_b64+"' where expediente='"+exp+"' and estado = 1"   
        cursor.execute(url)
        cursor.rowcount
        conn_qr.commit()
        conn_qr.close()
    except Exception as e:
        print(e)
        
    return('Orden de publicacion generada')

#Consulta por fecha para enviar
def getGenerados(fecha,user):
    pub_state = 0  
    try: 
        data = []   
        conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursor = conn.cursor()
        cursor.execute("select * from public.new_ordenes_publicaciones where fecha_generado like '"+fecha+"%' and user_login = '"+user+"' and estado = 1")    
        row=cursor.fetchall()
        for i in row:

            actual=''
            get_estado = int(i[19])+int(Estado_notify(str(i[1])))
            if(get_estado == 2):
                actual = 'Enviado'
            if(get_estado == 3):
                actual = 'Enviado'    
            if(get_estado == 1):
                actual = 'A enviar'

            fecha_event = str(i[23]).split('-')
            fech_convert = fecha_event[2][:2]+'/'+fecha_event[1]+'/'+fecha_event[0]

            fecha_generate = str(i[22]).split('-')
            fech_convert_generate = fecha_generate[2][:2]+'/'+fecha_generate[1]+'/'+fecha_generate[0]

            data.append({"id":i[0],
                    "expediente":i[1],
                    "solicitud":i[2],
                    "denominacion":i[3],
                    "nombre":i[4],
                    "direccion":i[5],
                    "agente":i[6],
                    "tipo":i[7],
                    "signo":i[8],
                    "clase":i[9],
                    "logo":i[10].replace("\n",""),
                    "fecha_solicitud":i[11],
                    "firma":i[12],
                    "codigo_qr":i[13],
                    "usuario":i[14],
                    "descripcion_distintivo":i[15],
                    "cod_agente":i[16],
                    "fecha_impresion":i[17],
                    "desc_servicio":i[18],
                    "estado":i[19],
                    "movimiento":i[20],
                    "url":i[21],
                    "fecha_generado":fech_convert_generate,
                    "action_date":fech_convert,
                    "user_login":i[24],
                    "user_id":i[25],
                    "evento":i[26],
                    "envio_buzon":i[27],
                    "orden":i[28],
                    "pub":Estado_notify(str(i[1])),
                    "estado_Actual":actual
                    }) 
        conn.close()
        return(data)
    except Exception as e:
        print(e)   

#Consulta por fecha para enviar
def getGeneradoshistorico(fecha,user):
    pub_state = 0  
    try: 
        data = []   
        conn = psycopg2.connect(

                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM public.new_ordenes_publicaciones where fecha_generado LIKE  '"+fecha+"%' and user_login = '"+user+"'")
            
        row=cursor.fetchall()
        for i in row:

            actual=''
            get_estado = int(i[19])+int(Estado_notify(str(i[1])))
            if(get_estado == 2):
                actual = 'Enviado'
            if(get_estado == 3):
                actual = 'Enviado'    
            if(get_estado == 1):
                actual = 'A enviar'

            fecha_event = str(i[23]).split('-')
            fech_convert = fecha_event[2][:2]+'/'+fecha_event[1]+'/'+fecha_event[0]
            data.append({"id":i[0],
                    "expediente":i[1],
                    "solicitud":i[2],
                    "denominacion":i[3],
                    "nombre":i[4],
                    "direccion":i[5],
                    "agente":i[6],
                    "tipo":i[7],
                    "signo":i[8],
                    "clase":i[9],
                    "logo":i[10].replace("\n",""),
                    "fecha_solicitud":i[11],
                    "firma":i[12],
                    "codigo_qr":i[13],
                    "usuario":i[14],
                    "descripcion_distintivo":i[15],
                    "cod_agente":i[16],
                    "fecha_impresion":i[17],
                    "desc_servicio":i[18],
                    "estado":i[19],
                    "movimiento":i[20],
                    "url":i[21],
                    "fecha_generado":i[22],
                    "action_date":fech_convert,
                    "user_login":i[24],
                    "user_id":i[25],
                    "evento":i[26],
                    "envio_buzon":i[27],
                    "orden":i[28],
                    "pub":Estado_notify(str(i[1])),
                    "estado_Actual":actual
                    }) 
        conn.close()
        
        return(data)
    except Exception as e:
        print(e) 

def descarga(base):
    print(base)

#Consulta por expediente para enviar
def getGenerado(exp):
    pub_state = 0
    try:
        connX = psycopg2.connect(
                        host = '192.168.50.215',
                        user= 'user_dev',
                        password = 'lP1zZIq7DIhP1wY1bLTxbTEu56JsSi',
                        database='db_sfe_production'
                        )
        cursor = connX.cursor()
        cursor.execute("select estado from notificaciones where expediente = "+ exp + " ORDER BY id desc limit 1")    
        row=cursor.fetchall()
        for i in row:
            pub_state = i[0]
        if(pub_state == None):
            pub_state = 0
        else:
            pub_state    
        connX.close()
    except Exception as e:
            print('Error al insertar en notificaciones')
    try:
        data = []   
        conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursor = conn.cursor()
        cursor.execute("select * from public.new_ordenes_publicaciones where estado = 1 and expediente = '"+exp+"'")    
        row=cursor.fetchall()
        for i in row:
           
            actual=''
            get_estado = int(i[19])+int(Estado_notify(str(i[1])))
            if(get_estado == 2):
                actual = 'Enviado'
            if(get_estado == 3):
                actual = 'Enviado'    
            if(get_estado == 1):
                actual = 'A enviar'

            fecha_event = str(i[23]).split('-')
            fech_convert = fecha_event[2][:2]+'/'+fecha_event[1]+'/'+fecha_event[0]


            fecha_generate = str(i[22]).split('-')
            fech_convert_generate = fecha_generate[2][:2]+'/'+fecha_generate[1]+'/'+fecha_generate[0]

            data.append({"id":i[0],
                    "expediente":i[1],
                    "solicitud":i[2],
                    "denominacion":i[3],
                    "nombre":i[4],
                    "direccion":i[5],
                    "agente":i[6],
                    "tipo":i[7],
                    "signo":i[8],
                    "clase":i[9],
                    "logo":str(i[10]).replace("\n",""),
                    "fecha_solicitud":i[11],
                    "firma":i[12],
                    "codigo_qr":i[13],
                    "usuario":i[14],
                    "descripcion_distintivo":i[15],
                    "cod_agente":i[16],
                    "fecha_impresion":i[17],
                    "desc_servicio":i[18],
                    "estado":i[19],
                    "movimiento":i[20],
                    "url":i[21],
                    "fecha_generado":fech_convert_generate,
                    "action_date":fech_convert,
                    "user_login":i[24],
                    "user_id":i[25],
                    "evento":i[26],
                    "envio_buzon":i[27],
                    "orden":i[28],
                    "pub":pub_state,
                    "estado_Actual":actual
                    }) 
        conn.close()
        return(data)
    except Exception as e:
        print(e)   

#Consulta por expediente para enviar
def getGeneradoHistorico(exp):
    pub_state = 0
    try:
        connX = psycopg2.connect(
                        host = '192.168.50.215',
                        user= 'user_dev',
                        password = 'lP1zZIq7DIhP1wY1bLTxbTEu56JsSi',
                        database='db_sfe_production'
                        )
        cursor = connX.cursor()
        cursor.execute("select estado from notificaciones where expediente = "+ exp + " ORDER BY id desc limit 1")    
        row=cursor.fetchall()
        for i in row:
            pub_state = i[0]
        if(pub_state == None):
            pub_state = 0
        else:
            pub_state    
        connX.close()
    except Exception as e:
            print('Error al insertar en notificaciones')
    try:
        data = []   
        conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursor = conn.cursor()
        cursor.execute("select * from public.new_ordenes_publicaciones where expediente = '"+exp+"'")    
        row=cursor.fetchall()
        for i in row:

            actual=''
            get_estado = int(i[19])+int(Estado_notify(str(i[1])))
            if(get_estado == 2):
                actual = 'Enviado'
            if(get_estado == 3):
                actual = 'Enviado'    
            if(get_estado == 1):
                actual = 'A enviar'

            fecha_event = str(i[23]).split('-')
            fech_convert = fecha_event[2][:2]+'/'+fecha_event[1]+'/'+fecha_event[0]
            data.append({"id":i[0],
                    "expediente":i[1],
                    "solicitud":i[2],
                    "denominacion":i[3],
                    "nombre":i[4],
                    "direccion":i[5],
                    "agente":i[6],
                    "tipo":i[7],
                    "signo":i[8],
                    "clase":i[9],
                    "logo":str(i[10]).replace("\n",""),
                    "fecha_solicitud":i[11],
                    "firma":i[12],
                    "codigo_qr":i[13],
                    "usuario":i[14],
                    "descripcion_distintivo":i[15],
                    "cod_agente":i[16],
                    "fecha_impresion":i[17],
                    "desc_servicio":i[18],
                    "estado":i[19],
                    "movimiento":i[20],
                    "url":i[21],
                    "fecha_generado":i[22],
                    "action_date":fech_convert,
                    "user_login":i[24],
                    "user_id":i[25],
                    "evento":i[26],
                    "envio_buzon":i[27],
                    "orden":i[28],
                    "pub":pub_state,
                    "estado_Actual":actual
                    }) 
        conn.close()
        return(data)
    except Exception as e:
        print(e)   

#Envio flujo normal del expediente
def Enviar_buzon(exp,user):
    item = Fech_All_Exp(exp)
    position = int(len(item))-1
    todaypub = datetime.datetime.now()
    event_date = str(todaypub).split(' ')
    des_mov=""
    id_url = ""
    estado_exp = ""

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


    try:                        
        pub = Insert_Action(str(exp),str(event_date[0]),str(item[position].sqlColumnList[18].sqlColumnValue),'SprintV2 OP','554').statusCode
                            
        if(pub == 'PUB'):
            try:   
                conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                            )
                cursor = conn.cursor()
                cursor.execute("select id,estado from public.new_ordenes_publicaciones where expediente = '"+exp+"'")    
                row=cursor.fetchall()
                for i in row:
                    id_url = i[0]
                    estado_exp = i[1]
                conn.close()
            except Exception as e:
                print(e) 

            #insert registro en form_o_p
            try:
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
                print('Error al insertar en form_orden_publicacion')

            ##insert registro en notificaciones
            try:
                connX = psycopg2.connect(
                            host = '192.168.50.215',
                            user= 'user_dev',
                            password = 'lP1zZIq7DIhP1wY1bLTxbTEu56JsSi',
                            database='db_sfe_production'
                                )
                cursor = connX.cursor()
                cursor.execute("INSERT INTO notificaciones(created_at, updated_at, expediente, agente, denominacion, clase, estado, notas, tiponotificacion, tipotramite, adjuntos, recibido_at, enviado_at, firmado_at, datos_pdf, signo, tramite, cabecera_id, usuario_id, adjuntos2)VALUES('"+str(todaypub)+"', '"+str(todaypub)+"', "+item[position].sqlColumnList[0].sqlColumnValue+", "+item[position].sqlColumnList[9].sqlColumnValue+", '"+str(item[position].sqlColumnList[6].sqlColumnValue).replace("'","\'")+"', '"+str(item[position].sqlColumnList[5].sqlColumnValue)+"', 2, NULL, 1, 1, 'https://sfe-tp.dinapi.gov.py/orden_publicacion/"+str(id_url)+"/', NULL, '"+str(todaypub)+"', NULL, '{}', '"+str(signo_format(item[position].sqlColumnList[4].sqlColumnValue))+"', '"+tip_sol+"', NULL, NULL, NULL);")    
                cursor.rowcount
                connX.commit()
                connX.close()
            except Exception as e:
                print('Error al insertar en notificaciones')

            #CAMBIA ESTADO
            Estado_enviado(exp,todaypub)
        return(str(pub))
    except Exception as err:
        return(str(Insert_Action(str(exp),str(event_date[0]),str(item[position].sqlColumnList[18].sqlColumnValue),'SprintV2 OP','554')))

def Re_enviar_buzon(exp,user):
    item = Fech_All_Exp(exp)
    position = int(len(item))-1
    todaypub = datetime.datetime.now()
    event_date = str(todaypub).split(' ')
    try:                        
        pub = Insert_note(str(exp),str(event_date[0]),str(item[position].sqlColumnList[18].sqlColumnValue),'Orden de publicacion reenviada SprintV2','1007') 
        if(int(getEstado_pub(exp)) == 1):
            Estado_enviado(exp, str(todaypub) )
            pass                  
        return(str(pub))
    except Exception as err:
        return(str(Insert_note(str(exp),str(event_date[0]),str(item[position].sqlColumnList[18].sqlColumnValue),'Orden de publicacion reenviada SprintV2','1007')))

def Re_generar(exp):
    try:
        Estado_historico(exp)
        time.sleep(2)
        Generar_orden(exp)
    except Exception as err:
        pass
#-----------------------------------------------------------------------------------------------------
def Estado_notify(exp):
    try:
        pub_state = 0
        connX = psycopg2.connect(
                        host = '192.168.50.215',
                        user= 'user_dev',
                        password = 'lP1zZIq7DIhP1wY1bLTxbTEu56JsSi',
                        database='db_sfe_production'
                        )
        cursor = connX.cursor()
        cursor.execute("select estado from notificaciones where expediente = "+ exp + " ORDER BY id desc limit 1")    
        row=cursor.fetchall()
        for i in row:
            pub_state = i[0]
        if(pub_state == None):
            return(0)
        else:
            return(pub_state)    
        connX.close()
    except Exception as e:
          return(e)  

def Estado_enviado(exp, fecha ):
    try: 
        conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursor = conn.cursor()
        cursor.execute("UPDATE public.new_ordenes_publicaciones SET estado=2, envio_buzon = '" + fecha_mes_hora(str(fecha)) + "'  where expediente='"+str(exp)+"' and estado = 1")    
        cursor.rowcount
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)   
    return()

def Estado_historico(exp):
    try: 
        conn = psycopg2.connect(
                                 host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursor = conn.cursor()
        cursor.execute("UPDATE public.new_ordenes_publicaciones SET estado=0  where expediente='"+str(exp)+"'")    
        cursor.rowcount
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)   
    return()

####################################################################################################################################################################
#Firma de usuario formas
def firma_user(user):#usuario de tipo ('RBEJARANO')
    try: 
        firm = 0   
        conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursor = conn.cursor()
        cursor.execute("SELECT firma_base64,usuario FROM public.new_firmas WHERE usuario ='"+user+"'")    
        row=cursor.fetchall()
        for i in row:
            firm = i[0]
        conn.close()
    except Exception as e:
        print(e)   
    return(firm)

def getEstado_pub(exp):
    try:
        estado = 0   
        conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
        cursor = conn.cursor()
        cursor.execute("select estado  FROM public.new_ordenes_publicaciones WHERE expediente='" + exp + "' ")    
        row=cursor.fetchall()
        for i in row:
            estado = i[0]
        conn.close()
        if estado == None:
            return(0)
        else:
            return(estado)
    except Exception as e:
        return(e)

def getEstado(exp):
    try:
        if(getEstado_pub(exp) == 1):
            return("Generado")
        if(getEstado_pub(exp) == 2):
            return("Enviado")
        if(getEstado_pub(exp) == 0):
            return("Pendiente") 
    except Exception as e:
        print(e)

def getText_Pub(exp):
    try:
        if getEstado_pub(exp) == None:
            return('no Generado')
        if getEstado_pub(exp) == 1:
            return('a Enviar')
        if getEstado_pub(exp) == 2:
            return('en Buzon')
    except Exception as e:
        return("")

def migrar_cucaracha():
    try:    
        connA = psycopg2.connect(
                        host='pgsql-sprint.dinapi.gov.py',
                        user='user-sprint',
                        password='BdnwaqdJPcVKR2kAcg3qP0C5HFrM1N',
                        database='kuriju_produccion'
                    )
        cursorA = connA.cursor()
        cursorA.execute("select * from me_publicaciones.new_ordenes_publicaciones nop where id >= 1 AND id <= 58443; --order by id desc")    
        row=cursorA.fetchall()
        data = []
        for i in row: # capturar datos de registro 
            data.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24],i[25],i[26],i[27],i[28]])
        connA.close()
    except Exception as e:
        print(e)

    try:
        for x in data:
            #print(x[1])
            connB = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                    )
            cursorB = connB.cursor()
            cursorB.execute("INSERT INTO public.new_ordenes_publicaciones(expediente, solicitud, denominacion, nombre, direccion, agente, tipo, signo, clase, logo, fecha_solicitud, firma, codigo_qr, usuario, descripcion_distintivo, cod_agente, fecha_impresion, desc_servicio, estado, movimiento, url, fecha_generado, action_date, user_login, user_id, evento, envio_buzon, orden)VALUES('"+str(x[1])+"','"+str(x[2])+"', '"+str(x[3])+"', '"+str(x[4]).replace("'","\'")+"', '"+str(x[5]).replace("'","\'")+"','"+str(x[6]).replace("'","\'")+"','"+str(x[7])+"','"+str(x[8])+"','"+str(x[9])+"', '"+str(x[10])+"', '"+str(x[11])+"', '"+str(x[12])+"', '"+str(x[13])+"', '"+str(x[14])+"', '"+str(x[15]).replace("'","\'")+"', "+str(x[16])+", '"+str(x[17])+"', '"+unicodedata.normalize('NFKD', str(x[18])).encode('ascii', 'ignore').decode().strip()+"', "+str(x[19])+", '"+str(x[20])+"', '"+str(x[21])+"', '"+str(x[22])+"', '"+str(x[23])+"', '"+str(x[24])+"', "+str(x[25])+", '"+str(x[26])+"', '"+str(x[27])+"', '"+str(x[28])+"');")    
            cursorB.rowcount
            connB.commit()
            connB.close()
        return(x[1])
    except Exception as e:
        print(e)


def insert_form_orden_publicacion(exp):
    try:
        item = Fech_All_Exp(exp)
        position = int(len(item))-1
        todaypub = datetime.datetime.now()
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

def insert_notificaciones(exp):
    try:
        item = Fech_All_Exp(exp)
        position = int(len(item))-1
        todaypub = datetime.datetime.now()
        event_date = str(todaypub).split(' ')
        des_mov=""
        id_url = ""
        estado_exp = ""

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

        connX = psycopg2.connect(
                        host = '192.168.50.215',
                        user= 'user_dev',
                        password = 'lP1zZIq7DIhP1wY1bLTxbTEu56JsSi',
                        database='db_sfe_production'
                        )
        cursor = connX.cursor()
        cursor.execute("INSERT INTO notificaciones(created_at, updated_at, expediente, agente, denominacion, clase, estado, notas, tiponotificacion, tipotramite, adjuntos, recibido_at, enviado_at, firmado_at, datos_pdf, signo, tramite, cabecera_id, usuario_id, adjuntos2)VALUES('"+str(todaypub)+"', '"+str(todaypub)+"', "+item[position].sqlColumnList[0].sqlColumnValue+", "+item[position].sqlColumnList[9].sqlColumnValue+", '"+str(item[position].sqlColumnList[6].sqlColumnValue).replace("'","\'")+"', '"+str(item[position].sqlColumnList[5].sqlColumnValue)+"', 2, NULL, 1, 1, 'https://sfe-tp.dinapi.gov.py/orden_publicacion/""/', NULL, '"+str(todaypub)+"', NULL, '{}', '"+str(signo_format(item[position].sqlColumnList[4].sqlColumnValue))+"', '"+tip_sol+"', NULL, NULL, NULL);")    
        cursor.rowcount
        connX.commit()
        connX.close()
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
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#print(insert_notificaciones('2104138'))

#print(insert_form_orden_publicacion(2104138))


#print(Generar_orden('2053034','4'))

#Enviar_buzon('2002251','4')

#print(migrar_cucaracha())

#print(getEstado('2208744'))

#print(getGenerado('2002251'))

#print(getEstado_pub('2002251'))

#print('Estado en notificaciones: ' + str(Estado_notify('2225625')))

#print('Estado generado como texto: ' + str(getEstado('2225625')))

#print('Estado en new_orden_publicaciones: ' + str(getEstado_pub('2225625')))

#Prueba de flujo OP con estos valores 2107417/298




