from datetime import date, timedelta, datetime
from time import sleep
import qrcode
import base64




def fecha_mes_hora(fecha): # 2021-11-21 11:28:22.090
    x = str(fecha).split(" ")
    d = str(x[0]).split("-")
    h = str(x[1]).split("-")
    mes = ''
    if(str(d[1]) == '01'):
        mes = 'Enero'
    if(str(d[1]) == '02'):
        mes = 'Febrero'    
    if(str(d[1]) == '03'):
        mes = 'Marzo'
    if(str(d[1]) == '04'):
        mes = 'Abril'
    if(str(d[1]) == '05'):
        mes = 'Mayo'
    if(str(d[1]) == '06'):
        mes = 'Junio'
    if(str(d[1]) == '07'):
        mes = 'Julio'
    if(str(d[1]) == '08'):
        mes = 'Agosto'    
    if(str(d[1]) == '09'):
        mes = 'Septiebre'
    if(str(d[1]) == '10'):
        mes = 'Octubre'
    if(str(d[1]) == '11'):
        mes = 'Noviembre' 
    if(str(d[1]) == '12'):
        mes = 'Diciembre'

    if(str(d[1]) == '1'):
        mes = 'Enero'
    if(str(d[1]) == '2'):
        mes = 'Febrero'    
    if(str(d[1]) == '3'):
        mes = 'Marzo'
    if(str(d[1]) == '4'):
        mes = 'Abril'
    if(str(d[1]) == '5'):
        mes = 'Mayo'
    if(str(d[1]) == '6'):
        mes = 'Junio'
    if(str(d[1]) == '7'):
        mes = 'Julio'
    if(str(d[1]) == '8'):
        mes = 'Agosto'    
    if(str(d[1]) == '9'):
        mes = 'Septiebre'

    return(d[2] + ' de ' + mes +' de '+ d[0] + ' ' + h[0])

def fecha_mes(fecha): # 2021-11-21 11:28:22.090
    x = str(fecha).split(" ")
    d = str(x[0]).split("-")
    h = str(x[1]).split("-")
    mes = ''
    if(str(d[1]) == '01'):
        mes = 'Enero'
    if(str(d[1]) == '02'):
        mes = 'Febrero'    
    if(str(d[1]) == '03'):
        mes = 'Marzo'
    if(str(d[1]) == '04'):
        mes = 'Abril'
    if(str(d[1]) == '05'):
        mes = 'Mayo'
    if(str(d[1]) == '06'):
        mes = 'Junio'
    if(str(d[1]) == '07'):
        mes = 'Julio'
    if(str(d[1]) == '08'):
        mes = 'Agosto'    
    if(str(d[1]) == '09'):
        mes = 'Septiebre'
    if(str(d[1]) == '10'):
        mes = 'Octubre'
    if(str(d[1]) == '11'):
        mes = 'Noviembre' 
    if(str(d[1]) == '12'):
        mes = 'Diciembre'

    if(str(d[1]) == '1'):
        mes = 'Enero'
    if(str(d[1]) == '2'):
        mes = 'Febrero'    
    if(str(d[1]) == '3'):
        mes = 'Marzo'
    if(str(d[1]) == '4'):
        mes = 'Abril'
    if(str(d[1]) == '5'):
        mes = 'Mayo'
    if(str(d[1]) == '6'):
        mes = 'Junio'
    if(str(d[1]) == '7'):
        mes = 'Julio'
    if(str(d[1]) == '8'):
        mes = 'Agosto'    
    if(str(d[1]) == '9'):
        mes = 'Septiebre'

    return('Asunción, ' + d[2] + ' de ' + mes +' de '+ d[0])

def fecha_barra(fecha): # 2021-11-21 11:28:22.090
    x = str(fecha).split(" ")
    d = str(x[0]).split("-")
    h = str(x[1]).split("-")

    return(d[2] + '/' + d[1] +'/'+ d[0])

def hora(fecha): # 2021-11-21 11:28:22.090
    x = str(fecha).split(" ")
    d = str(x[0]).split("-")
    h = str(x[1]).split("-")

    return(h[0])

def signo_format(sign): # Cnvercion de signo
        if(sign == 'N'):
            return'Denominativa'
        if(sign == 'D'):
            return'Denominativa'
        if(sign == 'L'):
            return'Figurativa'        
        if(sign == 'F'):
            return'Figurativa'
        if(sign == 'B'):
            return'Mixta'
        if(sign == 'M'):
            return'Mixta'
        if(sign == 'T'):
            return'Tridimensional'
        if(sign == 'S'):
            return'Sonora'
        if(sign == 'O'):
            return'Olfativa' 

def Fecha_atras(fecha): # devuelve 10 dias atras a partir de la fecha establecida
    today_date = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    td = timedelta(0)
    fecha_atras = today_date + td
    return(fecha_atras.date())

def date_not_hour():

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Obtener el año, mes y día por separado
    año_actual = fecha_actual.year
    mes_actual = fecha_actual.month
    dia_actual = fecha_actual.day

    # Imprimir la fecha actual
    return(f"{año_actual}-{str(mes_actual).zfill(2)}-{str(dia_actual).zfill(2)}")

def qr_code(text): # convierte el texto en codigo QR y crea fichero .png
    img = qrcode.make(text)
    f = open("output.png", "wb")
    img.save(f)
    f.close()

    with open("output.png", "rb") as image2string: 
        converted_string = base64.b64encode(image2string.read()) 
    return(str(converted_string).replace("b'",'').replace("'","")) 

def pais(arg):
    paises = ['PY - Paraguay','AD - Andorra','AE - Emiratos Arabes Unidos','AF - Afganistan','AG - Antigua y Barbuda','AI - Anguila','AL - Albania','AM - Armenia','AN - Antillas Neerlandesas','AO - Angola','AQ - Antartida','AR - Argentina','AS - Samoa Americana','AT - Austria','AU - Australia','AW - Aruba','AZ - Azerbaiyan','BA - Bosnia y Herzegovina','BB - Barbados','BD - Bangladesh','BE - Belgica','BF - Burkina Faso','BG - Bulgaria','BH - Bahrein','BI - Burundi','BJ - Benin','BM - Bermudas','BN - Brunei','BO - Bolivia','BR - Brasil','BS - Bahamas','BT - Butan','BU - Burma','BV - Isla Bouvet','BW - Botsuana','BX - Benelux','BY - Belarus','BZ - Belice','CA - Canada','CC - Islas Cocos','CF - Rep. Centroafricana','CG - Republica del Congo','CH - Suiza','CI - Costa de Marfil','CK - Islas Cook','CL - Chile','CM - Camerun','CN - China','CO - Colombia','CR - Costa Rica','CS - Czechoslovakia','CU - Cuba','CV - Cabo Verde','CW - Curazao','CX - Isla de Navidad','CY - Chipre','CZ - Republica Checa','DD - Germany Dem.Rep','DE - Alemania','DJ - Yibuti','DK - Dinamarca','DM - Dominica','DO - Republica Dominicana','DT - unknown','DZ - Argelia','EC - Ecuador','EE - Estonia','EG - Egipto','EH - Sahara Occidental','EM - EUIPO (Union Europea)','EP - Oficina Europea Patentes (OEP)','ER - Eritrea','ES - España','ET - Etiopia','FI - Finlandia','FJ - Fiyi','FK - Islas Falkland (Malvinas)','FM - Micronesia','FO - Islas Feroe','FR - Francia','FX - France Metropol','GA - Gabon','GB - Reino Unido','GC - Grand Caymans','GD - Granada','GE - Georgia']
    for i in paises:
        str(i).split('-')
        key_ = str(i[0]+i[1])
        if key_ == arg:
            return(i)

def format_fecha_mes_hora():
    x = datetime.datetime.now()
    meses = ('','En','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic')
    f_h = str(x).split(" ")
    obj_dia = str(f_h[0]).split("-")
    format_dia = str(obj_dia[2])+' '+str(meses[int(obj_dia[1])])+' '+str(obj_dia[0])
    obj_hora = (f_h[1]).split(".")
    return(str(format_dia)+' a las '+str(obj_hora[0]))




#print(Fecha_atras('2022-05-24'))
#
#print(fecha_mes_hora('2021-11-21 11:28:22.090'))
#
#print(fecha_mes('2021-11-21 11:28:22.090'))
#
#print(fecha_barra('2021-11-21 11:28:22.090'))
#
#print(hora('2021-11-21 11:28:22.090'))
#
#print('data:image/png;base64,'+qr_code('https://sfe-tp.dinapi.gov.py/orden_publicacion/49943/'))
