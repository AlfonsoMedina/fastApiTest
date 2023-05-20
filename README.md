Instalar FastApi
- pip install "fastapi[all]"

Instalar Uvicorn
- pip install "uvicorn[standard]"


correr uvicorn
- uvicorn main:app --host 0.0.0.0 --port 3600

Generar el archivo con todos los paquetes
- pip freeze > requirements.txt
- pip3 freeze > requirements.txt

Instalar todos los paquetes
- pip install -r requirements.txt

Inicio de entorno Virtual
- source /bin/activate

Actualizar PIP
- pip install --upgrade pip

Crear entorno
- python3 -m venv nombre_entorno

Crear entorno Metodo Osvaldo 
- virtualenv -p python3 nombre_entorno 

Compilar ficheros a .pyc
- python3 -mpy_compile nombre_fichero.py





Ver pdf firmados por EDOC_ID desde la tabla DO_EDOC:

- http://192.168.50.185:8888/nuxeo/restAPI/default/edmsAPI/getEDocPdfById?eDocId=2317835


tablas por query
- DO_EDOC_TYP tipos de documentos

EDOC_IMAGE_LINKING_USER IN (4)
- DO_EDOC por EDOC_ID traigo el pdf



Lista de eventos por PROC_NBR
- ProcessReadEventList - METODO  = actionNbr
<arg0>
    <!--Optional:-->
    <processNbr>
       <!--Optional:-->
       <doubleValue>312021</doubleValue>
    </processNbr>
    <!--Optional:-->
    <processType>1</processType>
</arg0>



lista de accione por proce_nbr
ProcessReadAction - METODO  = actionType
<arg0>
   <!--Optional:-->
   <actionNbr>
      <!--Optional:-->
      <doubleValue>6</doubleValue>
   </actionNbr>
   <!--Optional:-->
   <processId>
      <!--Optional:-->
      <processNbr>
         <!--Optional:-->
         <doubleValue>312021</doubleValue>
      </processNbr>
      <!--Optional:-->
      <processType>1</processType>
   </processId>
</arg0>




- netstat -aon | findstr :443

- taskkill /pid 10720 /F



