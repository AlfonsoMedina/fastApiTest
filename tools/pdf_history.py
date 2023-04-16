from datetime import datetime
import re
from fpdf import FPDF, HTMLMixin  #pip install fpdf2
import psycopg2
from tools.data_format import fecha_mes_hora
from os import getcwd
import unicodedata
from tools.connect import db_host, db_user, db_password, db_database, host_SFE_conn, user_SFE_conn, password_SFE_conn, database_SFE_conn,host_centura, user_centura, password_centura, database_centura


datos = ""
def traer_data(exp):
    try:
        conn = psycopg2.connect(
                                host = '192.168.50.215',
                                user = 'user_app_publicacion',
                                password = 'user_app_publicacion-202201!',
                                database = 'db_publicacion'
                    )
        cursor = conn.cursor()
        cursor.execute("select * from public.new_ordenes_publicaciones where estado = 2 and expediente = '"+exp+"'")    
        row=cursor.fetchall()
        for i in row:

            def firma():
                pdf.set_left_margin(5)
                pdf.cell(w=0, h=10, txt='', border=0,ln=1)
                
                pdf.cell(w=0, h=10, txt='De conformidad con la ley No. 1294/98. ', border='LTR',  ln=1,align='C')
                pdf.cell(w=0, h=10, txt='                                                 Publíquese la presente solicitud, por todo el término de ley.',border='LR', ln=1,align='L')
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(w=0, h=10, txt='                          '+str(i[11]), border='LR', ln=1,align='L')
                pdf.cell(w=0, h=4, txt='', border='LR',ln=1)
                #Imagen firma
                pdf.image(str(i[12]),x=140,y=(pdf.get_y() -7),w=35)
                pdf.cell(w=0, h=15, txt='', border='LR',ln=1)
                pdf.set_font('Arial', '', 8)
                pdf.set_font(style="I")
                pdf.cell(w=0, h=4, txt='Debe llevar la firma del funcionario autorizado y el sello oficial      ',border='LBR', ln=1,align='R')
                
                pdf.cell(w=0, h=5, txt='', border=0,ln=1)

                buzon = str(i[27]).split(".")
                
                pdf.set_font('Arial', '', 10)
                pdf.cell(w=0, h=9, txt='                                                                    Usuario:                      '+str(i[14]), border='LTR',  ln=1)
                pdf.cell(w=0, h=9, txt='                                                                    Enviada a Buzón el:   '+buzon[0], border='LR',  ln=1)
                pdf.image(str(i[13]),x=15,y=(pdf.get_y()-17),w=24,h=24 ,)
                pdf.cell(w=0, h=9, txt='                                                                    Fecha de impresión:   '+fecha_mes_hora(datetime.today()), border='LBR',  ln=1)
               
            pdf = FPDF(orientation= 'p', unit= 'mm', format= 'A4')
            pdf.add_page()

            
            #texto
            pdf.set_font('Arial', '', 15)


            #Imagen plantilla
            pdf.image('static/header.png',x=10,y=10,w=190,h=15)

            if(str(i[28]) == 'POP'):
                #Texto plantilla
                pdf.set_font('Arial', 'B', 16)
                pdf.text(x=25, y=46, txt='ORDEN DE'  )
                pdf.text(x=20, y=56, txt='PUBLICACIÓN' )
            else:
                #Texto plantilla
                pdf.set_font('Arial', 'B', 16)
                pdf.text(x=20, y=46, txt='2da ORDEN DE'  )
                pdf.text(x=20, y=56, txt='PUBLICACIÓN' )



            #Texto plantilla
            pdf.set_font('Arial', '', 9)
            pdf.text(x=90, y=46, txt='Expediente Nro.:      ' + str(i[1])  )
            pdf.text(x=90, y=56, txt='Fecha de Solicitud:      ' + str(i[2]) )

            #Marco  plantilla
            pdf.set_draw_color(215, 215, 215)
            pdf.cell(w=0, h=15, txt='', border=0,ln=1)
            pdf.cell(w=0, h=10, txt='', border=0,ln=1)
            pdf.cell(w=0, h=30, txt='', border=1,ln=1, align='c', fill=0)

            #Texto plantilla
            pdf.set_font('Arial', 'B', 13)
            pdf.text(x=75, y=75, txt='     D E N O M I N A C I Ó N'  )

            #Marco  plantilla
            pdf.set_font('Arial', '', 16)
            pdf.cell(w=0, h=5, txt='', border=0,ln=1 )


            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(w=0, h=20, txt= str(i[3]).replace("´","\'").replace("'","\'"), border=1, align='c',ln=1)
            pdf.cell(w=0, h=5, txt='', border=0,ln=1 )

            #Texto plantilla
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(w=0, h=4, txt='Nombre:      ' + unicodedata.normalize('NFKD', str(i[4])).encode('ascii', 'ignore').decode().strip(),ln=1)
            pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
            pdf.multi_cell(w=0, h=4, txt='Dirección:      ' + unicodedata.normalize('NFKD', str(i[5])).encode('ascii', 'ignore').decode().strip(),ln=1)
            pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
            pdf.multi_cell(w=0, h=4, txt='Agente de Propiedad Industrial:      '  + unicodedata.normalize('NFKD', str(i[6])).encode('ascii', 'ignore').decode().strip() ,ln=1)
            pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
            pdf.multi_cell(w=0, h=4, txt='Tipo de Solicitud:      ' + str(i[7])+'     Tipo de Signo:      '  + str(i[8])+'     Clase:      '  + str(i[9]) ,ln=1)


            #try:
            #    #Imagen logo
            #    pdf.image(str(i[10]),x=87,y=(pdf.get_y() + 6),w=40)
            #except Exception as e:
            #    print(e)

            try:
                #Imagen logo
                pdf.image(str(i[10]),x=10,y=(pdf.get_y() + 6),w=40)
            except Exception as e:
                print(e)
            #Detalle en la misma pagina     
            pdf.cell(w=0, h=5, txt='', border=0,ln=1)
            pdf.set_font('Arial', '', 10)
            pdf.set_left_margin(67)
            pdf.multi_cell(w=130,h=4, align='L', txt='Detalle:'+unicodedata.normalize('NFKD', str(i[18])).encode('ascii', 'ignore').decode().strip(), border=0 ,ln=1)

            if(len(str(i[18]).strip()) > 200):
                pass
            else:
                pdf.cell(w=0, h=25, txt='', border=0,ln=1)
                
            firma()
            
            #if(len(str(i[18])) > 10):
            #    #Pagina con detalle anexo
            #    pdf.add_page()
            #    pdf.set_font('Arial', 'B', 12)
            #    pdf.cell(w=0, h=8, txt='Descripción exp. Nro: '+ str(i[1]), border=1,ln=1 )
            #    pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
            #    pdf.set_font('Arial', '', 10)
            #    pdf.multi_cell(w=0,h=4, align='L', txt= unicodedata.normalize('NFKD', str(i[18])).encode('ascii', 'ignore').decode(), border=0)
            #
            #    #unicodedata.normalize('NFKD', str(i[18])).encode('ascii', 'ignore').decode()
            
            pdf.output(getcwd()+'/pdf/'+str(i[1])+'.pdf')


        conn.close()
    except Exception as e:
        return(e)
    


#traer_data('2259176')
