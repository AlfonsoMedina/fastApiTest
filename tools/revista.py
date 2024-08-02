from datetime import timedelta
from datetime import datetime
import unicodedata
from fpdf import FPDF
import psycopg2
from tools.data_format import fecha_mes,fecha_barra, pais
from tools.connect import db_host, db_user, db_password, db_database, host_SFE_conn, user_SFE_conn, password_SFE_conn, database_SFE_conn;

def crear_pub(fecha):
    lista_exp = []
    total = 0
    reg = 0
    ren = 0
    fecha_pub = ''
    td_nom = timedelta(1)
    una_fecha_nom = str(fecha)
    fecha_dt_nom = datetime.strptime(una_fecha_nom, '%Y-%m-%d') 
    dia_mas_nom = str(fecha_dt_nom+td_nom).replace("00","").replace(":","")


    def pub_hoy(fecha):
        try: 
            td = timedelta(2)
            td_2 = timedelta(-2)
            td_3 = timedelta(-1)
            td_4 = timedelta(1)
            td_5 = timedelta(3)
            una_fecha = str(fecha)
            fecha_dt = datetime.strptime(una_fecha, '%Y-%m-%d') 
            dia_tras = str(fecha_dt+td).replace("00","").replace(":","")
            dia_tras_2 = str(fecha_dt+td_2).replace("00","").replace(":","")
            dia_tras_3 = str(fecha_dt+td_3).replace("00","").replace(":","")
            dia_tras_4 = str(fecha_dt+td_4).replace("00","").replace(":","")
            dia_tras_5 = str(fecha_dt+td_5).replace("00","").replace(":","")
            #print(str(fecha)+' Fecha que recibe')
            #print(str(dia_tras).strip() +' Fecha mas 2')
            #print(str(dia_tras_2).strip()+' Fecha menos 2')
            #print(str(dia_tras_3).strip()+' Fecha medos 1')
            #print(str(dia_tras_4).strip()+' Fecha mas 1')
            #print(str(dia_tras_5).strip()+' Fecha mas 3')
            conn = psycopg2.connect(
                                host = db_host,
                                user = db_user,
                                password = db_password,
                                database = db_database
                        )
            cursor = conn.cursor()
            cursor.execute("select * from detalle_clasificado where inicio = '"+str(dia_tras_4).strip()+"' and fin = '"+str(dia_tras_4).strip()+"'\n" 
                            + " union   \n"
                            + "select * from detalle_clasificado where inicio = '"+str(dia_tras_4).strip()+"' and fin = '"+str(dia_tras_5).strip()+"'\n"
                            + " union   \n"
                            + "select * from detalle_clasificado where inicio = '"+str(dia_tras_3).strip()+"' and fin = '"+str(dia_tras_4).strip()+"'\n"  
                            + " union   \n"  
                            + "select * from detalle_clasificado where inicio = '"+str(fecha)+"' and fin = '"+str(dia_tras).strip()+"'")     
            row=cursor.fetchall()
            for i in row:
                lista_exp.append([str(i[0]),str(i[2]),str(i[3]),str(i[4]),str(i[5]),str(i[6]),str(i[7]),str(i[8]),str(i[9]),str(i[10]),str(i[11]),str(i[12]),str(i[13]),str(i[14]),str(i[15]),str(i[16]),str(i[17]),str(i[18]),str(i[19]),str(i[20]),str(i[21]),str(i[22]),str(i[23])])
            conn.close()
            
        except Exception as e:
            print(e)

    pub_hoy(fecha)

    print(len(lista_exp)-1)
    for a in range(0, len(lista_exp)):
        fecha_pub = str(lista_exp[a][0])
        if lista_exp[a][3] == 'REG':      
            reg = reg + 1
        if lista_exp[a][3] == 'REN':      
            ren = ren + 1

    file_name = f'{dia_mas_nom} 11:28:22.090'        
    #print(fecha_mes(file_name))

    def revista_data():
            try:
                class PDF(FPDF):
                    def header(self):
                        #fondo
                        #self.image("static/redpi2.png", 0, 0, 210)
                        # Rendering logo:
                        #self.image("static/redpi_clasificados.png", 10, 8, 33)
                        # Setting font: helvetica bold 15
                        self.set_font("helvetica", "B", 15)
                        # Moving cursor to the right:
                        self.cell(5)
                        # Printing title:
                        #self.cell(30, 10, "Title", border=1, align="C")
                        self.cell(1, 0, f'Clasificados - {fecha_barra(dia_mas_nom)}', align="L"  )
                        # Performing a line break:
                        self.ln(20)
                        
                    def footer(self):
                        # Position cursor at 1.5 cm from bottom:
                        self.set_y(-15)
                        # Setting font: helvetica italic 8
                        self.set_font("helvetica", "I", 8)
                        # Printing page number:
                        self.cell(330, 10, f"Page {self.page_no()}/{{nb}}", align="C")
                pdf = PDF()

                pdf.add_page()
                pdf.image("static/redpi2.png", 0, 0, 210)

                pdf.add_page()
                pdf.image("static/redpi2detall.png", 0, 0, 210)

                pdf.add_page()
                pdf.image("static/page2.png", 0, 0, 210)
                pdf.set_font("Arial", size=16)
                pdf.set_xy(15,120)
                pdf.cell(0,10, fecha_mes(file_name), new_x="LMARGIN", new_y="NEXT")
                pdf.set_x(15)
                pdf.cell(0,10, f'Clasificados:  {len(lista_exp)}', new_x="LMARGIN", new_y="NEXT")
                pdf.set_x(15)
                pdf.cell(0,10, f'Registro de Marcas:  {reg}', new_x="LMARGIN", new_y="NEXT")
                pdf.set_x(15)
                pdf.cell(0,10, f'Renovación de Marcas:  {ren}', new_x="LMARGIN", new_y="NEXT")            
                pdf.add_page()
                pdf.set_font("Arial", size=10)
                #print(lista_exp)
                cont = 0
                pdf.image("static/g1004.png", 0, 0, 210)
                for i in range(0, len(lista_exp)):
                    tipo_text = ''
                    pais_text = ''
                    sol_fech = str(lista_exp[i][1]).split('-')
                    hor_sol = str(lista_exp[i][2]).split('.')
                    if str(lista_exp[i][3]) == 'REG':
                        tipo_text = 'Registro de Marcas'
                    if str(lista_exp[i][3]) == 'REN':
                        tipo_text = 'Renovación de Marcas'
                    if str(lista_exp[i][10]) == 'PY':
                        pais_text = 'PY - PARAGUAY'
                    
                    fecha_pub = str(lista_exp[i][20])
                    #print(fecha_pub)
                    cont = cont + 1
                    try:
                        pdf.cell(0, 5, f"Número de Orden:................. {unicodedata.normalize('NFKD', str(lista_exp[i][0])).encode('ascii', 'ignore').decode()}", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pdf.cell(0, 5, f"Número de Orden:................. ", new_x="LMARGIN", new_y="NEXT")
                    try:
                        pdf.cell(0, 5, f"(210) Expediente:.................. {unicodedata.normalize('NFKD', str(lista_exp[i][14])).encode('ascii', 'ignore').decode()}", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pdf.cell(0, 5, f"(210) Expediente:.................. ", new_x="LMARGIN", new_y="NEXT")
                    try:    
                        pdf.cell(0, 5, f"Tipo Solicitud:........................ {unicodedata.normalize('NFKD', str(tipo_text)).encode('ascii', 'ignore').decode()}", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pdf.cell(0, 5, f"Tipo Solicitud:........................ ", new_x="LMARGIN", new_y="NEXT")
                    try:    
                        pdf.cell(0, 5, f"(220) Fecha de Solicitud:....... {unicodedata.normalize('NFKD', str(str(sol_fech[2])+'/'+str(sol_fech[1])+'/'+str(sol_fech[0]))).encode('ascii', 'ignore').decode()}", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pdf.cell(0, 5, f"(220) Fecha de Solicitud:....... ", new_x="LMARGIN", new_y="NEXT")
                    try:    
                        pdf.cell(0, 5, f"Hora de Solicitud:.................. {unicodedata.normalize('NFKD', str(hor_sol[0])).encode('ascii', 'ignore').decode()}", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pdf.cell(0, 5, f"Hora de Solicitud:.................. ", new_x="LMARGIN", new_y="NEXT")
                    try:
                        pdf.image(("data:image/png;base64,"+str(lista_exp[i][13])), 110, pdf.get_y()-24, w=18)
                    except Exception as e:
                        pass

                    try:
                        pdf.cell(0, 5, f"Tipo Signo:........................... {unicodedata.normalize('NFKD', str(lista_exp[i][4])).encode('ascii', 'ignore').decode()}", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pdf.cell(0, 5, f"Tipo Signo:........................... ", new_x="LMARGIN", new_y="NEXT")
                    try:    
                        pdf.cell(0, 5, f"(511) Clase:........................... {unicodedata.normalize('NFKD', str(lista_exp[i][6])).encode('ascii', 'ignore').decode()}", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pdf.cell(0, 5, f"(511) Clase:........................... ", new_x="LMARGIN", new_y="NEXT")
                    try:    
                        pdf.cell(0, 5, f"(540) Denominación:............. {unicodedata.normalize('NFKD', str(lista_exp[i][7])).encode('ascii', 'ignore').decode().replace('None','')}", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pdf.cell(0, 5, f"(540) Denominación:............. ", new_x="LMARGIN", new_y="NEXT")
                    try:    
                        pdf.cell(0, 5, f"(731) Solicitante/s:................. {unicodedata.normalize('NFKD', str(lista_exp[i][8])).encode('ascii', 'ignore').decode()}", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pdf.cell(0, 5, f"(731) Solicitante/s:................. ", new_x="LMARGIN", new_y="NEXT")
                    try:    
                        pdf.multi_cell(w=0,h=4, align='L', txt= f"Dirección:............................... {unicodedata.normalize('NFKD', str(lista_exp[i][9])).encode('ascii', 'ignore').decode()}",new_x="LMARGIN", new_y="NEXT" )
                    except Exception as e:
                        pdf.multi_cell(w=0,h=4, align='L', txt= f"Dirección:............................... ",new_x="LMARGIN", new_y="NEXT" )
                    try:    
                        pdf.cell(0, 5, f"País:....................................... {unicodedata.normalize('NFKD', pais(str(lista_exp[i][10]))).encode('ascii', 'ignore').decode()}", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pdf.cell(0, 5, f"País:....................................... ", new_x="LMARGIN", new_y="NEXT")
                    try:    
                        pdf.cell(0, 5, f"Agente:.................................. {unicodedata.normalize('NFKD', str(lista_exp[i][11])).encode('ascii', 'ignore').decode()}", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pdf.cell(0, 5, f"Agente:.................................. ", new_x="LMARGIN", new_y="NEXT")
                    try:    
                        pdf.cell(0, 4, "_______________________________________________________________________________", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pass
                    try:    
                        pdf.cell(0, 3, "", new_x="LMARGIN", new_y="NEXT")
                    except Exception as e:
                        pass
                    if cont < len(lista_exp):
                        if(cont == 3):
                            pdf.add_page()
                            pdf.image("static/g1004.png", 0, 0, 210)
                            cont = 0
                        else:
                            pass
                pdf.add_page()
                pdf.image("static/g1046.png", 0, 0, 210)

                pdf.output(f"static/clasificados_{dia_mas_nom.strip()}.pdf") 

            except Exception as e:
                print(e)

    revista_data()    
    return(dia_mas_nom.strip())

