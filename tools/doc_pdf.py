import base64
import json
import os
from subprocess import  Popen
from time import sleep

from flask import jsonify
import tools.base64Decode
from ipas.ipas_methods import consultar_expediente_ipas, fetch_all_offic_doc_OFFIDOC_PROC_NBR, fetch_all_offic_doc_PROC_NBR_OFFIDOC_TYP 



file_temp=''
out_folder = 'PUB_FILE'

#LIBRE_OFFICE = r"/usr//lib64//libreoffice//program//soffice"

#Complemento LibreOffice en Windows
LIBRE_OFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

def convert_to_pdf(input_docx, out_folder):
    p = Popen([LIBRE_OFFICE, '--headless', '--convert-to', 'pdf', '--outdir',out_folder, input_docx])
    #print([LIBRE_OFFICE, '--convert-to', 'pdf', input_docx])
    p.communicate()

#Orden de publicacion en PDF IPAS ORD_PUBL
def descargar_file(exp):
    try:
        #Descargar el Doc
        decoded = base64.b64decode(tools.base64Decode.decode_pdf(fetch_all_offic_doc_OFFIDOC_PROC_NBR(str(consultar_expediente_ipas(exp)))))
        #print(len(decoded))
        if len(decoded) > 10:
            with open('PUB_FILE/'+str(exp)+'pub.doc','wb') as f:
                f.write(decoded)

            sleep(0.3)

            file_temp= 'PUB_FILE/'+str(exp)+'pub.doc'

            convert_to_pdf(file_temp, out_folder)

            sleep(0.3)

            dir = 'PUB_FILE/'
            lista_ficheros = os.listdir(dir)
            for fichero in lista_ficheros:
                if fichero.endswith(".doc"):
                    os.remove('PUB_FILE/' + str(fichero))

            return('')
        else:
            pass
    except Exception as e:
        return('')


#sample_doc = '1501828pub.doc'
#out_folder = 'PUB_FILE'
#convert_to_pdf(sample_doc, out_folder)